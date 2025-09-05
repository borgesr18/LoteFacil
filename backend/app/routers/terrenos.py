from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.TerrenoOut])
def list_terrenos(db: Session = Depends(get_db)):
    return db.query(models.Terreno).order_by(models.Terreno.created_at.desc()).all()


@router.post("/", response_model=schemas.TerrenoOut, status_code=201)
def create_terreno(payload: schemas.TerrenoCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Terreno).filter(models.Terreno.matricula == payload.matricula).first()
    if exists:
        raise HTTPException(status_code=409, detail="Matrícula já cadastrada")
    terreno = models.Terreno(**payload.dict())
    db.add(terreno)
    db.commit()
    db.refresh(terreno)
    return terreno

