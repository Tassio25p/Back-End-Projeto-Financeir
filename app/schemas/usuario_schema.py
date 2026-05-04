from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

# Schema base com campos comuns do usuário
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None


# Schema usado para criar usuário
# A senha precisa ter entre 6 e 72 caracteres por causa do bcrypt
class UsuarioCreate(UsuarioBase):
    senha: str = Field(
        min_length=6,
        max_length=72,
        description="Senha do usuário. Deve ter no minimo 6 caracteres!" )
    renda_mensal: Decimal = 0
    saldo_inicial: Decimal = 0

# Schema usado para atualizar dados do perfil
# Todos os campos são opcionais porque o usuário pode alterar só um deles
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    foto_url: Optional[str] = None
    renda_mensal: Optional[Decimal] = None
    saldo_inicial: Optional[Decimal] = None
    configuracao_inicial_concluida: Optional[bool] = None
# Schema usado para devolver usuário para o frontend
# Não retornamos senha_hash por segurança
class UsuarioResponse(UsuarioBase):
    id: int
    foto_url: Optional[str] = None
    renda_mensal: Decimal
    saldo_inicial: Decimal
    configuracao_inicial_concluida: bool
    provedor_auth: str
    email_verificado: bool
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True