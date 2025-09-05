from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.PagamentoOut])
def list_pagamentos(db: Session = Depends(get_db)):
    return db.query(models.Pagamento).order_by(models.Pagamento.vencimento.asc()).all()


@router.post("/", response_model=schemas.PagamentoOut, status_code=201)
def criar_pagamento(payload: schemas.PagamentoCreate, db: Session = Depends(get_db)):
    contrato = db.query(models.Contrato).get(payload.contrato_id)
    if not contrato:
        raise HTTPException(status_code=400, detail="Contrato inválido")
    existente = (
        db.query(models.Pagamento)
        .filter(models.Pagamento.contrato_id == payload.contrato_id, models.Pagamento.parcela == payload.parcela)
        .first()
    )
    if existente:
        raise HTTPException(status_code=409, detail="Parcela já cadastrada")
    pagamento = models.Pagamento(
        contrato_id=payload.contrato_id,
        parcela=payload.parcela,
        vencimento=payload.vencimento,
        valor_original=payload.valor_original,
        status="previsto",
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento


@router.post("/{pagamento_id}/registrar", response_model=schemas.PagamentoOut)
def registrar_pagamento(pagamento_id: str, payload: schemas.RegistrarPagamento, db: Session = Depends(get_db)):
    pg = db.query(models.Pagamento).get(pagamento_id)
    if not pg:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    if pg.status == "pago":
        return pg
    pg.valor_pago = payload.valor_pago
    pg.forma = payload.forma
    pg.pago_em = payload.pago_em or datetime.utcnow()
    pg.status = "pago"
    db.commit()
    db.refresh(pg)
    return pg


@router.post("/jobs/atualizar-status")
def atualizar_status_atraso(db: Session = Depends(get_db)):
    hoje = date.today()
    pendentes = (
        db.query(models.Pagamento)
        .filter(models.Pagamento.status == "previsto")
        .all()
    )
    atualizados = 0
    for pg in pendentes:
        if pg.vencimento.date() < hoje:
            pg.status = "atrasado"
            atualizados += 1
    db.commit()
    return {"atualizados": atualizados}

