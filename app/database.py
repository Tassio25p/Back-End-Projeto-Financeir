from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

#Cria a conexão principal com o banco PostgreSQL.   
engine = create_engine(settings.DATABASE_URL)
#Cria sessões de banco.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Base que será usada pelos models.
Base = declarative_base()

#Essa função será usada nas rotas para acessar o banco.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()