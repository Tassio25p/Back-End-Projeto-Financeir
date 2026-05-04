from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class MetaFinanceira(Base):
    __tablename__ = "metas_financeiras"

    id = Column(Integer, primary_key=True, index=True)

    # Nome da meta, exemplo: Comprar notebook
    titulo = Column(String(150), nullable=False)

    # Valor final que o usuário quer alcançar
    valor_alvo = Column(Numeric(10, 2), nullable=False)

    # Valor que o usuário já guardou
    valor_atual = Column(Numeric(10, 2), nullable=False, default=0)

    # Data limite opcional para concluir a meta
    data_limite = Column(Date, nullable=True)

    # Status: ativa, concluida ou cancelada
    status = Column(String(30), nullable=False, default="ativa")

    # Liga a meta ao usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento
    usuario = relationship("Usuario", back_populates="metas")