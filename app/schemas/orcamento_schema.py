from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


# Campos principais do orçamento mensal
class OrcamentoBase(BaseModel):
    mes: int
    ano: int
    valor_limite: Decimal
    categoria_id: int


# Schema para criar orçamento
class OrcamentoCreate(OrcamentoBase):
    pass


# Schema para atualizar orçamento
class OrcamentoUpdate(BaseModel):
    mes: Optional[int] = None
    ano: Optional[int] = None
    valor_limite: Optional[Decimal] = None
    categoria_id: Optional[int] = None


# Schema de resposta
class OrcamentoResponse(OrcamentoBase):
    id: int
    usuario_id: int
    criado_em: datetime

    class Config:
        from_attributes = True