from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from ..db import get_db
from ..models.intake import IntakeRequest
from ..schemas import IntakeRequestCreate, IntakeRequestOut
from ..models.shelter import Shelter
from ..auth import require_role
from ..utils.notifications import send_email_stub

router = APIRouter(prefix="/intake", tags=["intake"])

# Public: submit request
@router.post("/", response_model=IntakeRequestOut, status_code=201)
def create_intake(payload: IntakeRequestCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    shelter = db.get(Shelter, payload.shelter_id)
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    req = IntakeRequest(
        shelter_id=payload.shelter_id,
        name=payload.name,
        reason=payload.reason,
        eta=payload.eta
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # Fire-and-forget notification
    background_tasks.add_task(send_email_stub, shelter.name, req)

    return req

# Admin/shelter: list requests
@router.get("/{shelter_id}", response_model=List[IntakeRequestOut], dependencies=[Depends(require_role("admin", "shelter"))])
def list_intakes(shelter_id: int, db: Session = Depends(get_db)):
    stmt = select(IntakeRequest).where(IntakeRequest.shelter_id == shelter_id).order_by(IntakeRequest.created_at.desc())
    return list(db.execute(stmt).scalars().all())
