from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class CodigoRecuperacaoSenha(Base):
    __tablename__ = "codigos_recuperacao_senha"

    id = Column(Integer, primary_key=True, index=True)

    # E-mail que solicitou a recuperação de senha
    email = Column(String(150), nullable=False, index=True)

    # Código PIN salvo em formato de hash, nunca puro
    codigo_hash = Column(String(255), nullable=False)

    # Data e hora em que o código expira
    expira_em = Column(DateTime(timezone=True), nullable=False)

    # Indica se o código já foi utilizado
    usado = Column(Boolean, default=False)

    # Conta quantas tentativas o usuário fez
    tentativas = Column(Integer, default=0)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())