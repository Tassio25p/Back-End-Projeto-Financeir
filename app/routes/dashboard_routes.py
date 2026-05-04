from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.usuario_model import Usuario
from app.schemas.dashboard_schema import DashboardResumoResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/resumo", response_model=DashboardResumoResponse)
def obter_resumo_dashboard(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_current_active_user)
):
    """
    Retorna o resumo financeiro do usuário logado.

    Inclui:
    - saldo atual
    - total de receitas
    - total de despesas
    - quantidade de transações
    - últimas transações
    - gastos por categoria
    """
    return DashboardService.resumo(db, usuario_logado)