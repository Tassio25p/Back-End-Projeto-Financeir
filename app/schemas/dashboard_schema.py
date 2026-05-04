from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class DashboardTransacaoResponse(BaseModel):
    """
    Representa uma transação exibida no dashboard.
    """
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    data: date
    metodo_pagamento: Optional[str] = None
    observacao: Optional[str] = None
    categoria_id: int
    categoria_nome: Optional[str] = None
    categoria_cor: Optional[str] = None
    categoria_icone: Optional[str] = None

    class Config:
        from_attributes = True


class DashboardCategoriaResumo(BaseModel):
    """
    Representa o total gasto por categoria.
    """

    categoria: str
    cor: Optional[str] = None
    icone: Optional[str] = None
    total: Decimal


class DashboardOrcamentoResumo(BaseModel):
    """
    Representa o acompanhamento de um orçamento.

    Compara:
    - valor limite
    - gasto atual
    - valor restante
    - percentual utilizado
    """

    orcamento_id: int
    categoria_id: int
    categoria: str
    cor: Optional[str] = None
    icone: Optional[str] = None
    mes: int
    ano: int
    valor_limite: Decimal
    gasto_atual: Decimal
    valor_restante: Decimal
    percentual_utilizado: Decimal
    status: str


class DashboardResumoResponse(BaseModel):
    """
    Resposta principal do dashboard.
    """

    saldo: Decimal
    total_receitas: Decimal
    total_despesas: Decimal
    quantidade_transacoes: int
    ultimas_transacoes: List[DashboardTransacaoResponse]
    gastos_por_categoria: List[DashboardCategoriaResumo]
    orcamentos: List[DashboardOrcamentoResumo]