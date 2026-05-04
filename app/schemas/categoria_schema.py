from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Campos comuns de uma categoria
class CategoriaBase(BaseModel):
    nome: str
    tipo: str  # receita ou despesa
    cor: Optional[str] = None
    icone: Optional[str] = None


# Schema para criar categoria
class CategoriaCreate(CategoriaBase):
    pass


# Schema para editar categoria
# Campos opcionais para permitir edição parcial
class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    cor: Optional[str] = None
    icone: Optional[str] = None


# Schema de resposta para o frontend
class CategoriaResponse(CategoriaBase):
    id: int
    usuario_id: int
    criado_em: datetime

    class Config:
        from_attributes = True