from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ClienteCreate(BaseModel):
    nome: str
    documento: str = Field(min_length=11, max_length=20)
    email: Optional[str] = None
    telefone: Optional[str] = None


class ClienteOut(BaseModel):
    id: str
    nome: str
    documento: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TerrenoCreate(BaseModel):
    matricula: str
    lote: str
    quadra: Optional[str] = None
    area_m2: float
    preco_base: float


class TerrenoOut(BaseModel):
    id: str
    matricula: str
    lote: str
    quadra: Optional[str] = None
    area_m2: float
    preco_base: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContratoCreate(BaseModel):
    cliente_id: str
    terreno_id: str
    numero: str
    valor_total: float
    entrada: float = 0
    num_parcelas: int


class ContratoOut(BaseModel):
    id: str
    cliente_id: str
    terreno_id: str
    numero: str
    valor_total: float
    entrada: float
    num_parcelas: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PagamentoCreate(BaseModel):
    contrato_id: str
    parcela: int
    vencimento: datetime
    valor_original: float


class PagamentoOut(BaseModel):
    id: str
    contrato_id: str
    parcela: int
    vencimento: datetime
    valor_original: float
    valor_pago: Optional[float] = None
    forma: Optional[str] = None
    status: str
    pago_em: Optional[datetime] = None
    juros: float
    multa: float
    desconto: float

    model_config = {"from_attributes": True}


class RegistrarPagamento(BaseModel):
    valor_pago: float
    forma: str
    pago_em: Optional[datetime] = None

