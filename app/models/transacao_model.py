from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)

    # Descrição da movimentação financeira
    descricao = Column(String(150), nullable=False)

    # Valor da transação. Numeric é melhor para dinheiro do que Float
    valor = Column(Numeric(10, 2), nullable=False)

    # Tipo: receita ou despesa
    tipo = Column(String(20), nullable=False)

    # Data em que a transação aconteceu
    data = Column(Date, nullable=False)

    # Exemplo: Pix, Cartão, Dinheiro, Boleto
    metodo_pagamento = Column(String(50), nullable=True)

    # Campo opcional para observações
    observacao = Column(String(255), nullable=True)

    # Liga a transação ao usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Liga a transação a uma categoria
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="transacoes")
    categoria = relationship("Categoria", back_populates="transacoes")