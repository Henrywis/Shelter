from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from ..db import get_db
from ..models.intake import IntakeRequest
from ..models.shelter import Shelter
from ..models.user import User
from ..schemas import (
    IntakeRequestCreate,
    IntakeRequestOut,
    IntakeStatusUpdate,       # strict (pending|fulfilled|cancelled)
    IntakeStatusUpdateLoose,  # for future use
)
from ..auth import require_role, get_current_user
from ..utils.notifications import send_email_intake

router = APIRouter(prefix="/intake", tags=["intake"])

# Public: submit intake request
@router.post("/", response_model=IntakeRequestOut, status_code=201)
def create_intake(
    payload: IntakeRequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    shelter = db.get(Shelter, payload.shelter_id)
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    req = IntakeRequest(
        shelter_id=payload.shelter_id,
        name=payload.name,
        reason=payload.reason,
        eta=payload.eta,
        status="pending",
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # Fire-and-forget notification (email; falls back to stub if disabled)
    background_tasks.add_task(send_email_intake, shelter.name, req, None)

    return req

# Role-aware list with filters
# - Admin: can view all; optional ?shelter_id=
# - Shelter role: only their own shelter
# - Optional status filter (?status=pending|fulfilled|cancelled)
@router.get("/", response_model=List[IntakeRequestOut])
def list_intakes_flexible(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(
        None, description="Filter by status: pending|fulfilled|cancelled"
    ),
    shelter_id: Optional[int] = Query(
        None, description="Admin-only: filter by a specific shelter_id"
    ),
):
    q = select(IntakeRequest)

    if status:
        s = status.lower().strip()
        if s not in {"pending", "fulfilled", "cancelled"}:
            raise HTTPException(status_code=422, detail="Invalid status")
        q = q.where(IntakeRequest.status == s)

    if current_user.role == "admin":
        if shelter_id:
            q = q.where(IntakeRequest.shelter_id == shelter_id)
    elif current_user.role == "shelter":
        if not current_user.shelter_id:
            raise HTTPException(
                status_code=403,
                detail="Shelter role is not associated with a shelter",
            )
        q = q.where(IntakeRequest.shelter_id == current_user.shelter_id)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    q = q.order_by(IntakeRequest.created_at.desc())
    return list(db.execute(q).scalars().all())

# Admin/shelter: list requests
@router.get(
    "/{shelter_id}",
    response_model=List[IntakeRequestOut],
    dependencies=[Depends(require_role("admin", "shelter"))],
)
def list_intakes(
    shelter_id: int,
    db: Session = Depends(get_db),
):
    stmt = (
        select(IntakeRequest)
        .where(IntakeRequest.shelter_id == shelter_id)
        .order_by(IntakeRequest.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


# Update intake status (admin or owning shelter)
@router.patch("/{intake_id}/status", response_model=IntakeRequestOut)
def update_intake_status(
    intake_id: int,
    payload: IntakeStatusUpdate,  # IntakeStatusUpdateLoose for case-insensitive
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = db.get(IntakeRequest, intake_id)
    if not req:
        raise HTTPException(status_code=404, detail="Intake not found")

    # Admin can update any intake; Shelter role can update only if it belongs to their shelter
    if current_user.role == "admin":
        pass
    elif current_user.role == "shelter":
        if not current_user.shelter_id or current_user.shelter_id != req.shelter_id:
            raise HTTPException(status_code=403, detail="Forbidden")
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    req.status = payload.status  # already validated by schema
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
