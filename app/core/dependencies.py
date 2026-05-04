from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import verificar_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario_model import Usuario


# HTTPBearer faz o Swagger pedir apenas o token Bearer.
# Exemplo de header gerado:
# Authorization: Bearer eyJhbGciOi...
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Retorna o usuário autenticado a partir do token JWT.
    """

    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Aqui pegamos só o token, sem a palavra Bearer
    token = credentials.credentials

    payload = verificar_token(token)

    if payload is None:
        raise erro_credenciais

    usuario_id = payload.get("sub")

    if usuario_id is None:
        raise erro_credenciais

    try:
        usuario_id = int(usuario_id)
    except ValueError:
        raise erro_credenciais

    usuario = UsuarioRepository.buscar_por_id(db, usuario_id)

    if usuario is None:
        raise erro_credenciais

    return usuario


def get_current_active_user(
    usuario: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Retorna apenas usuários ativos.
    """

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo."
        )

    return usuario


def require_verified_email(
    usuario: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """
    Exige que o usuário esteja ativo e com e-mail verificado.
    """

    if not usuario.email_verificado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="E-mail ainda não verificado."
        )

    return usuario