from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from ..db import get_db
from ..models.shelter import Shelter
from ..models.capacity import CapacityLog
from ..schemas import CapacityUpdate, CapacityLogOut
from ..auth import get_current_user, require_role
from ..models.user import User

router = APIRouter(prefix="/capacity", tags=["capacity"])

# Latest capacity logs for a shelter (public)
@router.get("/{shelter_id}", response_model=List[CapacityLogOut])
def list_capacity_logs(shelter_id: int, db: Session = Depends(get_db)):
    # Return last ~20 entries, newest first
    stmt = select(CapacityLog).where(CapacityLog.shelter_id == shelter_id)\
        .order_by(CapacityLog.updated_at.desc()).limit(20)
    return list(db.execute(stmt).scalars().all())

# Update capacity (admin or shelter)
@router.post("/{shelter_id}", response_model=CapacityLogOut,
             dependencies=[Depends(require_role("admin", "shelter"))])
def update_capacity(shelter_id: int, payload: CapacityUpdate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    shelter = db.get(Shelter, shelter_id)
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    # validation: available <= total
    if payload.beds_available > payload.beds_total:
        raise HTTPException(status_code=400, detail="beds_available cannot exceed beds_total")

    log = CapacityLog(
        shelter_id=shelter_id,
        beds_total=payload.beds_total,
        beds_available=payload.beds_available,
        updated_by=user.id
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
