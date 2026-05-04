from datetime import datetime, timedelta, timezone
import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.codigo_recuperacao_model import CodigoRecuperacaoSenha
from app.repositories.codigo_recuperacao_repository import CodigoRecuperacaoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.core.security import gerar_hash_senha, verificar_senha
from app.core.email import EmailService
from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    VerifyPinRequest,
    ResetPasswordRequest
)


class PasswordRecoveryService:
    """
    Service responsável pela recuperação de senha com PIN por e-mail.

    Fluxo:
    1. Usuário solicita recuperação
    2. Sistema gera PIN
    3. Sistema salva hash do PIN no banco
    4. Sistema envia PIN por e-mail via Brevo
    5. Usuário valida PIN
    6. Usuário redefine a senha
    """

    PIN_EXPIRATION_MINUTES = 10
    MAX_TENTATIVAS = 5

    @staticmethod
    def gerar_pin() -> str:
        """
        Gera um PIN numérico de 6 dígitos.

        Exemplo: 482913
        """
        return str(random.randint(100000, 999999))

    @staticmethod
    def solicitar_recuperacao(db: Session, dados: ForgotPasswordRequest):
        """
        Inicia a recuperação de senha.

        Por segurança, retornamos a mesma mensagem mesmo que o e-mail não exista.
        Isso evita revelar se um e-mail está cadastrado ou não.
        """

        usuario = UsuarioRepository.buscar_por_email(db, dados.email)

        mensagem_padrao = {
            "mensagem": "Se o e-mail estiver cadastrado, enviaremos um PIN de recuperação."
        }

        if not usuario:
            return mensagem_padrao

        if not usuario.ativo:
            return mensagem_padrao

        pin = PasswordRecoveryService.gerar_pin()
        pin_hash = gerar_hash_senha(pin)

        expira_em = datetime.now(timezone.utc) + timedelta(
            minutes=PasswordRecoveryService.PIN_EXPIRATION_MINUTES
        )

        # Invalida códigos anteriores para esse e-mail
        CodigoRecuperacaoRepository.invalidar_codigos_anteriores(
            db,
            dados.email
        )

        novo_codigo = CodigoRecuperacaoSenha(
            email=dados.email,
            codigo_hash=pin_hash,
            expira_em=expira_em,
            usado=False,
            tentativas=0
        )

        CodigoRecuperacaoRepository.criar(db, novo_codigo)

        EmailService.enviar_pin_recuperacao(dados.email, pin)

        return mensagem_padrao

    @staticmethod
    def verificar_pin(db: Session, dados: VerifyPinRequest):
        """
        Verifica se o PIN informado está correto.

        Essa rota serve para o frontend validar o PIN antes de mostrar
        o formulário de nova senha.
        """

        codigo = CodigoRecuperacaoRepository.buscar_codigo_ativo_por_email(
            db,
            dados.email
        )

        if not codigo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN inválido ou expirado."
            )

        agora = datetime.now(timezone.utc)

        if codigo.expira_em < agora:
            CodigoRecuperacaoRepository.marcar_como_usado(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN expirado."
            )

        if codigo.tentativas >= PasswordRecoveryService.MAX_TENTATIVAS:
            CodigoRecuperacaoRepository.marcar_como_usado(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número máximo de tentativas excedido."
            )

        pin_correto = verificar_senha(dados.pin, codigo.codigo_hash)

        if not pin_correto:
            CodigoRecuperacaoRepository.incrementar_tentativas(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN inválido."
            )

        return {
            "mensagem": "PIN validado com sucesso."
        }

    @staticmethod
    def redefinir_senha(db: Session, dados: ResetPasswordRequest):
        """
        Redefine a senha do usuário usando o PIN enviado por e-mail.
        """

        usuario = UsuarioRepository.buscar_por_email(db, dados.email)

        if not usuario or not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível redefinir a senha."
            )

        codigo = CodigoRecuperacaoRepository.buscar_codigo_ativo_por_email(
            db,
            dados.email
        )

        if not codigo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN inválido ou expirado."
            )

        agora = datetime.now(timezone.utc)

        if codigo.expira_em < agora:
            CodigoRecuperacaoRepository.marcar_como_usado(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN expirado."
            )

        if codigo.tentativas >= PasswordRecoveryService.MAX_TENTATIVAS:
            CodigoRecuperacaoRepository.marcar_como_usado(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número máximo de tentativas excedido."
            )

        pin_correto = verificar_senha(dados.pin, codigo.codigo_hash)

        if not pin_correto:
            CodigoRecuperacaoRepository.incrementar_tentativas(db, codigo)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PIN inválido."
            )

        usuario.senha_hash = gerar_hash_senha(dados.nova_senha)

        db.commit()
        db.refresh(usuario)

        CodigoRecuperacaoRepository.marcar_como_usado(db, codigo)

        return {
            "mensagem": "Senha redefinida com sucesso."
        }