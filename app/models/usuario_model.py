from sqlalchemy import Column, Integer, String, Boolean, DateTime , Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Usuario(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "usuarios"

    # Chave primária da tabela
    id = Column(Integer, primary_key=True, index=True)

    # Dados básicos do usuário
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=True)

    # Dados opcionais do perfil
    foto_url = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    # Renda mensal planejada do usuário
    saldo_inicial = Column(Numeric(10, 2), nullable=False, default=0)
    renda_mensal = Column(Numeric(10, 2), nullable=False, default=0)
    configuracao_inicial_concluida = Column(Boolean, nullable=False, default=False)
    # Campos para login normal ou login com Google
    provedor_auth = Column(String(30), nullable=False, default="local")
    google_id = Column(String(255), unique=True, nullable=True)

    # Controle da conta
    email_verificado = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)

    # Datas de criação e atualização
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos com outras tabelas
    categorias = relationship("Categoria", back_populates="usuario", cascade="all, delete")
    transacoes = relationship("Transacao", back_populates="usuario", cascade="all, delete")
    metas = relationship("MetaFinanceira", back_populates="usuario", cascade="all, delete")
    orcamentos = relationship("Orcamento", back_populates="usuario", cascade="all, delete")