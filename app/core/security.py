from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings


# Contexto de criptografia de senha
# bcrypt é usado para gerar e verificar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    """
    Recebe uma senha normal e retorna a senha criptografada.

    Nunca salvamos senha pura no banco.
    """
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Compara a senha digitada com o hash salvo no banco.

    Retorna True se a senha estiver correta.
    """
    return pwd_context.verify(senha, senha_hash)


def criar_token_acesso(dados: dict) -> str:
    """
    Cria um token JWT com os dados do usuário.

    Normalmente colocamos:
    - sub: id do usuário
    - email: e-mail do usuário
    """

    dados_para_token = dados.copy()

    expira_em = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_para_token.update({"exp": expira_em})

    token = jwt.encode(
        dados_para_token,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def verificar_token(token: str):
    """
    Verifica se o token JWT é válido.

    Se for válido, retorna o payload.
    Se for inválido, retorna None.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None