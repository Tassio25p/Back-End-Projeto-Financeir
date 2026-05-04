from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.auth_routes import router as auth_router
from app.routes.usuario_routes import router as usuario_router
from app.routes.categoria_routes import router as categoria_router
from app.routes.transacao_routes import router as transacao_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.meta_routes import router as meta_router
from app.routes.orcamento_routes import router as orcamento_router


app = FastAPI(
    title="Projeto Financeiro API",
    description="API para controle financeiro pessoal com autenticação, transações, categorias, metas e orçamentos.",
    version="1.0.0"
)


# Lista de origens permitidas.
# São os endereços de onde o frontend pode chamar a API.
origins = [
    settings.FRONTEND_URL,
]

# Adiciona a URL de produção apenas se ela existir no .env
if settings.FRONTEND_PROD_URL:
    origins.append(settings.FRONTEND_PROD_URL)


# Middleware de CORS.
# Ele permite que o React acesse a API pelo navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas da aplicação
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(transacao_router)
app.include_router(dashboard_router)
app.include_router(meta_router)
app.include_router(orcamento_router)


@app.get("/", tags=["Status"])
def home():
    """
    Rota inicial da API.

    Serve para verificar se o backend está funcionando.
    """
    return {
        "status": "online",
        "mensagem": "API do Projeto Financeiro funcionando!"
    }