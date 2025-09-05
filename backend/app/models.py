from sqlalchemy import Column, String, DateTime, Numeric, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base


def default_uuid() -> str:
    return str(uuid.uuid4())


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, default=default_uuid)
    nome = Column(String, nullable=False)
    documento = Column(String(20), unique=True, nullable=False)
    email = Column(String)
    telefone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    contratos = relationship("Contrato", back_populates="cliente")


class Terreno(Base):
    __tablename__ = "terrenos"

    id = Column(String, primary_key=True, default=default_uuid)
    matricula = Column(String(50), unique=True, nullable=False)
    lote = Column(String(20), nullable=False)
    quadra = Column(String(20))
    area_m2 = Column(Numeric(12, 2), nullable=False)
    preco_base = Column(Numeric(14, 2), nullable=False)
    status = Column(String(20), nullable=False, default="disponivel")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    contratos = relationship("Contrato", back_populates="terreno")


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(String, primary_key=True, default=default_uuid)
    cliente_id = Column(String, ForeignKey("clientes.id"), nullable=False)
    terreno_id = Column(String, ForeignKey("terrenos.id"), nullable=False)
    numero = Column(String(50), unique=True, nullable=False)
    valor_total = Column(Numeric(14, 2), nullable=False)
    entrada = Column(Numeric(14, 2), nullable=False, default=0)
    num_parcelas = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="ativo")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="contratos")
    terreno = relationship("Terreno", back_populates="contratos")
    pagamentos = relationship("Pagamento", back_populates="contrato", cascade="all, delete-orphan")


class Pagamento(Base):
    __tablename__ = "pagamentos"
    __table_args__ = (UniqueConstraint("contrato_id", "parcela", name="uix_contrato_parcela"),)

    id = Column(String, primary_key=True, default=default_uuid)
    contrato_id = Column(String, ForeignKey("contratos.id"), nullable=False)
    parcela = Column(Integer, nullable=False)
    vencimento = Column(DateTime, nullable=False)
    valor_original = Column(Numeric(14, 2), nullable=False)
    valor_pago = Column(Numeric(14, 2))
    forma = Column(String(20))
    status = Column(String(20), nullable=False, default="previsto")
    pago_em = Column(DateTime)
    juros = Column(Numeric(14, 2), nullable=False, default=0)
    multa = Column(Numeric(14, 2), nullable=False, default=0)
    desconto = Column(Numeric(14, 2), nullable=False, default=0)

    contrato = relationship("Contrato", back_populates="pagamentos")

