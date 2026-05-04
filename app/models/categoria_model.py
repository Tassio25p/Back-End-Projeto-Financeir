from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)

    # Nome da categoria, exemplo: Alimentação, Salário, Transporte
    nome = Column(String(100), nullable=False)

    # Tipo da categoria: receita ou despesa
    tipo = Column(String(20), nullable=False)

    # Campos visuais usados no frontend
    cor = Column(String(50), nullable=True)
    icone = Column(String(50), nullable=True)

    # Chave estrangeira ligando a categoria ao usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="categorias")
    transacoes = relationship("Transacao", back_populates="categoria")
    orcamentos = relationship("Orcamento", back_populates="categoria")