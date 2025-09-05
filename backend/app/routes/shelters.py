from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List

from ..db import get_db
from ..models.shelter import Shelter
from ..schemas import ShelterCreate, ShelterUpdate, ShelterOut
from ..auth import require_role

router = APIRouter(prefix="/shelters", tags=["shelters"])

# Create (admin or shelter role)
@router.post("/", response_model=ShelterOut, status_code=201,
             dependencies=[Depends(require_role("admin", "shelter"))])
def create_shelter(payload: ShelterCreate, db: Session = Depends(get_db)):
    s = Shelter(**payload.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

# List (public)
@router.get("/", response_model=List[ShelterOut])
def list_shelters(db: Session = Depends(get_db)):
    stmt = select(Shelter).order_by(Shelter.id.desc())
    return list(db.execute(stmt).scalars().all())

# Get by id (public)
@router.get("/{shelter_id}", response_model=ShelterOut)
def get_shelter(shelter_id: int, db: Session = Depends(get_db)):
    s = db.get(Shelter, shelter_id)
    if not s:
        raise HTTPException(404, "Shelter not found")
    return s

# Update (admin or shelter role)
@router.patch("/{shelter_id}", response_model=ShelterOut,
              dependencies=[Depends(require_role("admin", "shelter"))])
def update_shelter(shelter_id: int, payload: ShelterUpdate, db: Session = Depends(get_db)):
    s = db.get(Shelter, shelter_id)
    if not s:
        raise HTTPException(404, "Shelter not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

# Delete (admin only)
@router.delete("/{shelter_id}", status_code=204,
               dependencies=[Depends(require_role("admin"))])
def delete_shelter(shelter_id: int, db: Session = Depends(get_db)):
    s = db.get(Shelter, shelter_id)
    if not s:
        raise HTTPException(404, "Shelter not found")
    db.delete(s)
    db.commit()
    return
