from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


# Campos principais de uma meta financeira
class MetaBase(BaseModel):
    titulo: str
    valor_alvo: Decimal
    valor_atual: Decimal = 0
    data_limite: Optional[date] = None
    status: str = "ativa"


# Schema usado para criar uma meta
class MetaCreate(MetaBase):
    pass


# Schema usado para atualizar uma meta
class MetaUpdate(BaseModel):
    titulo: Optional[str] = None
    valor_alvo: Optional[Decimal] = None
    valor_atual: Optional[Decimal] = None
    data_limite: Optional[date] = None
    status: Optional[str] = None


# Schema usado para devolver a meta para o frontend
class MetaResponse(MetaBase):
    id: int
    usuario_id: int
    criado_em: datetime

    class Config:
        from_attributes = True