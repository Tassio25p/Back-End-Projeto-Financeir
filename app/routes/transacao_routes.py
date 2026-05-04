from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.transacao_schema import (
    TransacaoCreate,
    TransacaoUpdate,
    TransacaoResponse
)
from app.services.transacao_service import TransacaoService


router = APIRouter(
    prefix="/transacoes",
    tags=["Transações"]
)


@router.post("/", response_model=TransacaoResponse)
def criar_transacao(
    dados: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova transação para o usuário logado.

    A transação precisa estar vinculada a uma categoria do próprio usuário.
    """
    return TransacaoService.criar(db, dados, usuario_logado)


@router.get("/", response_model=List[TransacaoResponse])
def listar_transacoes(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Lista todas as transações do usuário logado.
    """
    return TransacaoService.listar(db, usuario_logado)


@router.get("/{transacao_id}", response_model=TransacaoResponse)
def buscar_transacao(
    transacao_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Busca uma transação específica pelo ID.

    Só retorna se a transação pertencer ao usuário logado.
    """
    return TransacaoService.buscar_por_id(db, transacao_id, usuario_logado)


@router.put("/{transacao_id}", response_model=TransacaoResponse)
def atualizar_transacao(
    transacao_id: int,
    dados: TransacaoUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma transação existente.
    """
    return TransacaoService.atualizar(
        db,
        transacao_id,
        dados,
        usuario_logado
    )


@router.delete("/{transacao_id}")
def excluir_transacao(
    transacao_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Exclui uma transação existente.
    """
    return TransacaoService.excluir(db, transacao_id, usuario_logado)