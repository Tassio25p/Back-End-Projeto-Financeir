from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioResponse
from app.schemas.usuario_schema import UsuarioResponse, UsuarioUpdate
from app.repositories.usuario_repository import UsuarioRepository
from app.database import get_db
from sqlalchemy.orm import Session

# O nome precisa ser router, porque no main.py importamos router
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/me", response_model=UsuarioResponse)
def buscar_meu_perfil(
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Retorna os dados do usuário autenticado.

    Essa rota exige:
    - token JWT válido
    - usuário ativo
    """
    return usuario_logado

@router.delete("/me", response_model=UsuarioResponse)  
def desativar_conta(
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Desativa a conta do usuário autenticado.

    Essa rota exige:
    - token JWT válido
    - usuário ativo

    A desativação é feita definindo o campo "ativo" como False.
    O usuário não é deletado do banco de dados, apenas fica inativo.
    """
    usuario_logado.ativo = False
    return usuario_logado

@router.put("/me", response_model=UsuarioResponse)
def atualizar_meu_perfil(
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Atualiza os dados do usuário autenticado.

    Pode atualizar:
    - nome
    - telefone
    - foto_url
    - renda_mensal
    """
    dados_atualizados = dados.model_dump(exclude_unset=True)

    return UsuarioRepository.atualizar(
        db,
        usuario_logado,
        dados_atualizados
    )