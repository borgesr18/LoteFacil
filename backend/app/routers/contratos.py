from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.ContratoOut])
def list_contratos(db: Session = Depends(get_db)):
    return db.query(models.Contrato).order_by(models.Contrato.created_at.desc()).all()


@router.post("/", response_model=schemas.ContratoOut, status_code=201)
def create_contrato(payload: schemas.ContratoCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).get(payload.cliente_id)
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente inválido")

    terreno = db.query(models.Terreno).get(payload.terreno_id)
    if not terreno:
        raise HTTPException(status_code=400, detail="Terreno inválido")
    if terreno.status != "disponivel":
        raise HTTPException(status_code=409, detail="Terreno não disponível")

    exists = db.query(models.Contrato).filter(models.Contrato.numero == payload.numero).first()
    if exists:
        raise HTTPException(status_code=409, detail="Número de contrato já existente")

    contrato = models.Contrato(
        cliente_id=payload.cliente_id,
        terreno_id=payload.terreno_id,
        numero=payload.numero,
        valor_total=payload.valor_total,
        entrada=payload.entrada,
        num_parcelas=payload.num_parcelas,
        status="ativo",
    )
    terreno.status = "vendido"
    db.add(contrato)
    db.commit()
    db.refresh(contrato)
    return contrato

