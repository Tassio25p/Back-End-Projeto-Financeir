from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.meta_schema import (
    MetaCreate,
    MetaUpdate,
    MetaResponse
)
from app.services.meta_service import MetaService


router = APIRouter(
    prefix="/metas",
    tags=["Metas Financeiras"]
)


@router.post("/", response_model=MetaResponse)
def criar_meta(
    dados: MetaCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova meta financeira para o usuário logado.

    Exemplo:
    - Comprar notebook
    - Reserva de emergência
    - Viagem
    """
    return MetaService.criar(db, dados, usuario_logado)


@router.get("/", response_model=List[MetaResponse])
def listar_metas(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Lista todas as metas financeiras do usuário logado.
    """
    return MetaService.listar(db, usuario_logado)


@router.get("/{meta_id}", response_model=MetaResponse)
def buscar_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Busca uma meta financeira específica pelo ID.

    Só retorna se a meta pertencer ao usuário logado.
    """
    return MetaService.buscar_por_id(db, meta_id, usuario_logado)


@router.put("/{meta_id}", response_model=MetaResponse)
def atualizar_meta(
    meta_id: int,
    dados: MetaUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma meta financeira existente.
    """
    return MetaService.atualizar(db, meta_id, dados, usuario_logado)


@router.delete("/{meta_id}")
def excluir_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Exclui uma meta financeira existente.
    """
    return MetaService.excluir(db, meta_id, usuario_logado)