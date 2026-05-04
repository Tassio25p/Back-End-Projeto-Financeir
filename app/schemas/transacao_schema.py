from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


# Campos comuns da transação
class TransacaoBase(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str  # receita ou despesa
    data: date
    metodo_pagamento: Optional[str] = None
    observacao: Optional[str] = None
    categoria_id: int


# Schema para criar transação
class TransacaoCreate(TransacaoBase):
    pass


# Schema para atualizar transação
class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    tipo: Optional[str] = None
    data: Optional[date] = None
    metodo_pagamento: Optional[str] = None
    observacao: Optional[str] = None
    categoria_id: Optional[int] = None


# Schema para devolver transação ao frontend
class TransacaoResponse(TransacaoBase):
    id: int
    usuario_id: int
    criado_em: datetime

    class Config:
        from_attributes = True