from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.orcamento_schema import (
    OrcamentoCreate,
    OrcamentoUpdate,
    OrcamentoResponse
)
from app.services.orcamento_service import OrcamentoService


router = APIRouter(
    prefix="/orcamentos",
    tags=["Orçamentos"]
)


@router.post("/", response_model=OrcamentoResponse)
def criar_orcamento(
    dados: OrcamentoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo orçamento para o usuário logado.

    Exemplo:
    - categoria Alimentação
    - mês 5
    - ano 2026
    - limite R$ 600
    """
    return OrcamentoService.criar(db, dados, usuario_logado)


@router.get("/", response_model=List[OrcamentoResponse])
def listar_orcamentos(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Lista todos os orçamentos do usuário logado.
    """
    return OrcamentoService.listar(db, usuario_logado)


@router.get("/{orcamento_id}", response_model=OrcamentoResponse)
def buscar_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Busca um orçamento específico pelo ID.

    Só retorna se o orçamento pertencer ao usuário logado.
    """
    return OrcamentoService.buscar_por_id(db, orcamento_id, usuario_logado)


@router.put("/{orcamento_id}", response_model=OrcamentoResponse)
def atualizar_orcamento(
    orcamento_id: int,
    dados: OrcamentoUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza um orçamento existente.
    """
    return OrcamentoService.atualizar(
        db,
        orcamento_id,
        dados,
        usuario_logado
    )


@router.delete("/{orcamento_id}")
def excluir_orcamento(
    orcamento_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Exclui um orçamento existente.
    """
    return OrcamentoService.excluir(db, orcamento_id, usuario_logado)