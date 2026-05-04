from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
    ForgotPasswordRequest,
    VerifyPinRequest,
    ResetPasswordRequest
)
from app.services.auth_service import AuthService
from app.services.password_recovery_service import PasswordRecoveryService


# APIRouter serve para organizar rotas por módulo
# Aqui todas as rotas terão o prefixo /auth
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/register", response_model=UsuarioResponse)
def registrar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Rota para cadastrar um novo usuário.

    Recebe:
    - nome
    - email
    - telefone opcional
    - senha

    Retorna:
    - dados do usuário criado, sem retornar senha_hash
    """
    return AuthService.registrar(db, dados)


@router.post("/login", response_model=TokenResponse)
def login_usuario(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Rota para login do usuário.

    Recebe:
    - email
    - senha

    Retorna:
    - access_token JWT
    - token_type
    """
    return AuthService.login(db, dados)


@router.post("/forgot-password")
def solicitar_recuperacao_senha(
    dados: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Solicita recuperação de senha.

    Recebe:
    - email

    A API gera um PIN e envia para o e-mail,
    caso ele esteja cadastrado.
    """
    return PasswordRecoveryService.solicitar_recuperacao(db, dados)


@router.post("/verify-pin")
def verificar_pin_recuperacao(
    dados: VerifyPinRequest,
    db: Session = Depends(get_db)
):
    """
    Verifica se o PIN informado está correto.

    Recebe:
    - email
    - pin
    """
    return PasswordRecoveryService.verificar_pin(db, dados)


@router.post("/reset-password")
def redefinir_senha(
    dados: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Redefine a senha usando o PIN recebido por e-mail.

    Recebe:
    - email
    - pin
    - nova_senha
    """
    return PasswordRecoveryService.redefinir_senha(db, dados)