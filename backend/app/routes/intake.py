from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Response
from io import StringIO
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
import csv

from ..db import get_db
from ..models.intake import IntakeRequest
from ..models.shelter import Shelter
from ..models.user import User
from ..schemas import (
    IntakeRequestCreate,
    IntakeRequestOut,
    IntakeStatusUpdate,       # strict (pending|fulfilled|cancelled)
    IntakeStatusUpdateLoose,  # for future use
    Paginated,
)
from ..auth import require_role, get_current_user
from ..utils.notifications import send_email_intake, send_intake_sms, send_intake_status_sms
from ..settings import settings

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

    # Fire-and-forget SMS notification (local/dev)
    if settings.TWILIO_ENABLED and settings.TEST_SMS_TO:
        background_tasks.add_task(
            send_intake_sms,
            shelter.name,
            req,
            settings.TEST_SMS_TO,  # destination for now (Marker 9: use shelter phone)
        )

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

    from_dt: Optional[datetime] = Query(None, description="Filter created_at >= this ISO datetime"),
    to_dt: Optional[datetime] = Query(None, description="Filter created_at <= this ISO datetime"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    q = select(IntakeRequest)

    if status:
        s = status.lower().strip()
        if s not in {"pending", "fulfilled", "cancelled"}:
            raise HTTPException(status_code=422, detail="Invalid status")
        q = q.where(IntakeRequest.status == s)

    # date range filters
    if from_dt:
        q = q.where(IntakeRequest.created_at >= from_dt)
    if to_dt:
        q = q.where(IntakeRequest.created_at <= to_dt)

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
    # pagination (calculate total first)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    offset = (page - 1) * page_size
    q = q.limit(page_size).offset(offset)
    return list(db.execute(q).scalars().all())


@router.get("/search", response_model=Paginated[IntakeRequestOut])
def search_intakes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None),
    shelter_id: Optional[int] = Query(None),
    from_dt: Optional[datetime] = Query(None),
    to_dt: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    q = select(IntakeRequest)

    if status:
        s = status.lower().strip()
        if s not in {"pending", "fulfilled", "cancelled"}:
            raise HTTPException(status_code=422, detail="Invalid status")
        q = q.where(IntakeRequest.status == s)

    if from_dt:
        q = q.where(IntakeRequest.created_at >= from_dt)
    if to_dt:
        q = q.where(IntakeRequest.created_at <= to_dt)

    if current_user.role == "admin":
        if shelter_id:
            q = q.where(IntakeRequest.shelter_id == shelter_id)
    elif current_user.role == "shelter":
        if not current_user.shelter_id:
            raise HTTPException(status_code=403, detail="Shelter role is not associated with a shelter")
        q = q.where(IntakeRequest.shelter_id == current_user.shelter_id)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    q = q.order_by(IntakeRequest.created_at.desc())

    total = db.scalar(select(func.count()).select_from(q.subquery()))
    offset = (page - 1) * page_size
    q = q.limit(page_size).offset(offset)

    items = list(db.execute(q).scalars().all())
    return {"items": items, "total": total or 0, "page": page, "page_size": page_size}


@router.get("/export.csv")
def export_intakes_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None),
    shelter_id: Optional[int] = Query(None),
    from_dt: Optional[datetime] = Query(None),
    to_dt: Optional[datetime] = Query(None),
):
    q = select(IntakeRequest)

    if status:
        s = status.lower().strip()
        if s not in {"pending", "fulfilled", "cancelled"}:
            raise HTTPException(status_code=422, detail="Invalid status")
        q = q.where(IntakeRequest.status == s)

    if from_dt:
        q = q.where(IntakeRequest.created_at >= from_dt)
    if to_dt:
        q = q.where(IntakeRequest.created_at <= to_dt)

    if current_user.role == "admin":
        if shelter_id:
            q = q.where(IntakeRequest.shelter_id == shelter_id)
    elif current_user.role == "shelter":
        if not current_user.shelter_id:
            raise HTTPException(status_code=403, detail="Shelter role is not associated with a shelter")
        q = q.where(IntakeRequest.shelter_id == current_user.shelter_id)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    q = q.order_by(IntakeRequest.created_at.desc())
    rows = list(db.execute(q).scalars().all())

    # Build CSV
    sio = StringIO()
    writer = csv.writer(sio)
    writer.writerow(["id", "shelter_id", "name", "reason", "eta", "status", "created_at"])
    for r in rows:
        writer.writerow([
            r.id,
            r.shelter_id,
            r.name or "",
            r.reason or "",
            r.eta.isoformat() if r.eta else "",
            r.status,
            r.created_at.isoformat() if r.created_at else "",
        ])

    data = sio.getvalue().encode("utf-8")
    headers = {
        "Content-Disposition": 'attachment; filename="intakes.csv"',
        "Content-Type": "text/csv; charset=utf-8",
    }
    return Response(content=data, headers=headers, media_type="text/csv")


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
    payload: IntakeStatusUpdate,  # or IntakeStatusUpdateLoose for case-insensitive
    background_tasks: BackgroundTasks,            # <--- added
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    req = db.get(IntakeRequest, intake_id)
    if not req:
        raise HTTPException(status_code=404, detail="Intake not found")

    # Admin can update any intake; Shelter role only if it belongs to their shelter
    # if current_user.role == "admin":
    #     pass
    # elif current_user.role == "shelter":
    #     if not current_user.shelter_id or current_user.shelter_id != req.shelter_id:
    #         raise HTTPException(status_code=403, detail="Forbidden")
    # else:
    #     raise HTTPException(status_code=403, detail="Forbidden")

    # Only do work if status actually changes
    if req.status != payload.status:
        req.status = payload.status  # validated by schema
        db.add(req)
        db.commit()
        db.refresh(req)

        # Fetch shelter so the SMS can include name/address
        shelter = db.get(Shelter, req.shelter_id)
        if shelter:
            # Fire-and-forget SMS to requester (for now uses TEST_SMS_TO)
            background_tasks.add_task(send_intake_status_sms, shelter, req)

    return req

