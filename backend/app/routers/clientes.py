from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.ClienteOut])
def list_clientes(db: Session = Depends(get_db), q: str | None = Query(default=None)):
    query = db.query(models.Cliente)
    if q:
        like = f"%{q}%"
        query = query.filter(models.Cliente.nome.ilike(like))
    return query.order_by(models.Cliente.created_at.desc()).all()


@router.post("/", response_model=schemas.ClienteOut, status_code=201)
def create_cliente(payload: schemas.ClienteCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Cliente).filter(models.Cliente.documento == payload.documento).first()
    if exists:
        raise HTTPException(status_code=409, detail="Documento já cadastrado")
    cliente = models.Cliente(**payload.dict())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def get_cliente(cliente_id: str, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

