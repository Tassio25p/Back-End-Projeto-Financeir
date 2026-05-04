from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate
from app.schemas.auth_schema import LoginRequest
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso


class AuthService:
    """
    Camada de serviço da autenticação.

    Aqui ficam as regras:
    - verificar se e-mail já existe
    - gerar hash da senha
    - validar login
    - criar token JWT
    """

    @staticmethod
    def registrar(db: Session, dados: UsuarioCreate):
        """
        Registra um novo usuário no sistema.
        """

        usuario_existente = UsuarioRepository.buscar_por_email(db, dados.email)

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado."
            )

        senha_hash = gerar_hash_senha(dados.senha)

        novo_usuario = Usuario(
    nome=dados.nome,
    email=dados.email,
    telefone=dados.telefone,
    senha_hash=senha_hash,
    provedor_auth="local",
    email_verificado=False,
    ativo=True,
    configuracao_inicial_concluida=False
)


        return UsuarioRepository.criar(db, novo_usuario)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate
from app.schemas.auth_schema import LoginRequest
from app.core.security import gerar_hash_senha, verificar_senha, criar_token_acesso


class AuthService:
    """
    Camada de serviço da autenticação.

    Aqui ficam as regras:
    - verificar se e-mail já existe
    - gerar hash da senha
    - validar login
    - criar token JWT
    """

    @staticmethod
    def registrar(db: Session, dados: UsuarioCreate):
        """
        Registra um novo usuário no sistema.
        """

        usuario_existente = UsuarioRepository.buscar_por_email(db, dados.email)

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado."
            )

        senha_hash = gerar_hash_senha(dados.senha)

        novo_usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            senha_hash=senha_hash,
            provedor_auth="local",
            email_verificado=False,
            ativo=True
        )

        return UsuarioRepository.criar(db, novo_usuario)

    @staticmethod
    def login(db: Session, dados: LoginRequest):
        """
        Realiza login com e-mail e senha.
        """

        usuario = UsuarioRepository.buscar_por_email(db, dados.email)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        if not usuario.senha_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Essa conta não possui senha local."
            )

        senha_correta = verificar_senha(dados.senha, usuario.senha_hash)

        if not senha_correta:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo."
            )

        token = criar_token_acesso({
            "sub": str(usuario.id),
            "email": usuario.email
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    @staticmethod
    def login(db: Session, dados: LoginRequest):
        """
        Realiza login com e-mail e senha.
        """

        usuario = UsuarioRepository.buscar_por_email(db, dados.email)

        if not usuario:
            raise HTTPException( #para retornar erro 
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        if not usuario.senha_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Essa conta não possui senha local."
            )

        senha_correta = verificar_senha(dados.senha, usuario.senha_hash)

        if not senha_correta:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos."
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo."
            )

        token = criar_token_acesso({
            "sub": str(usuario.id),
            "email": usuario.email
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }