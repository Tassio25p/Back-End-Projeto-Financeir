from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()


class Settings:
    """
    Classe central de configurações do projeto.

    Todas as variáveis sensíveis ficam no .env
    e são lidas por esta classe.
    """

    # Banco de dados
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Segurança / JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_temporaria_de_desenvolvimento")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Frontend / CORS
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    FRONTEND_PROD_URL = os.getenv("FRONTEND_PROD_URL", "")

    # Brevo SMTP
    BREVO_SMTP_SERVER = os.getenv("BREVO_SMTP_SERVER")
    BREVO_SMTP_PORT = int(os.getenv("BREVO_SMTP_PORT", 587))
    BREVO_SMTP_LOGIN = os.getenv("BREVO_SMTP_LOGIN")
    BREVO_SMTP_KEY = os.getenv("BREVO_SMTP_KEY")

    # Remetente dos e-mails
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Projeto Financeiro")


settings = Settings()