from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse
)
from app.services.categoria_service import CategoriaService


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.post("/", response_model=CategoriaResponse)
def criar_categoria(
    dados: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova categoria para o usuário logado.

    Exemplo:
    - Alimentação / despesa
    - Salário / receita
    """
    return CategoriaService.criar(db, dados, usuario_logado)


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Lista todas as categorias do usuário logado.
    """
    return CategoriaService.listar(db, usuario_logado)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Busca uma categoria específica pelo ID.

    Só retorna se a categoria pertencer ao usuário logado.
    """
    return CategoriaService.buscar_por_id(db, categoria_id, usuario_logado)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(
    categoria_id: int,
    dados: CategoriaUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma categoria existente.
    """
    return CategoriaService.atualizar(
        db,
        categoria_id,
        dados,
        usuario_logado
    )


@router.delete("/{categoria_id}")
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Exclui uma categoria existente.
    """
    return CategoriaService.excluir(db, categoria_id, usuario_logado)