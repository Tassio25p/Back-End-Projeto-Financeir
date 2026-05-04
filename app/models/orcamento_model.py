from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Orcamento(Base):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, index=True)

    # Mês e ano do orçamento
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)

    # Limite de gasto definido para a categoria
    valor_limite = Column(Numeric(10, 2), nullable=False)

    # Liga o orçamento ao usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Liga o orçamento a uma categoria
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="orcamentos")
    categoria = relationship("Categoria", back_populates="orcamentos")