import smtplib
from email.message import EmailMessage

from app.config import settings


class EmailService:
    """
    Serviço responsável pelo envio de e-mails.

    Neste projeto usamos Brevo SMTP para enviar:
    - PIN de recuperação de senha
    """

    @staticmethod
    def enviar_email(destinatario: str, assunto: str, conteudo: str):
        """
        Envia um e-mail simples em formato texto.

        Parâmetros:
        - destinatario: e-mail que receberá a mensagem
        - assunto: título do e-mail
        - conteudo: corpo da mensagem
        """

        mensagem = EmailMessage()
        mensagem["Subject"] = assunto
        mensagem["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
        mensagem["To"] = destinatario
        mensagem.set_content(conteudo)

        try:
            with smtplib.SMTP(
                settings.BREVO_SMTP_SERVER,
                settings.BREVO_SMTP_PORT
            ) as servidor:
                # Inicia conexão segura TLS
                servidor.starttls()

                # Faz login no SMTP da Brevo
                servidor.login(
                    settings.BREVO_SMTP_LOGIN,
                    settings.BREVO_SMTP_KEY
                )

                # Envia a mensagem
                servidor.send_message(mensagem)

        except Exception as erro:
            raise Exception(f"Erro ao enviar e-mail: {str(erro)}")

    @staticmethod
    def enviar_pin_recuperacao(destinatario: str, pin: str):
        """
        Envia o PIN de recuperação de senha para o usuário.
        """

        assunto = "Código de recuperação de senha"

        conteudo = f"""
Olá!

Você solicitou a recuperação de senha no Projeto Financeiro.

Seu código PIN é:

{pin}

Este código expira em 10 minutos.

Se você não solicitou essa recuperação, ignore este e-mail.

Atenciosamente,
Projeto Financeiro
"""

        EmailService.enviar_email(destinatario, assunto, conteudo)