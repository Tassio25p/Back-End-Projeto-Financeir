from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario
from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    """
    Service responsável pelos cálculos do Dashboard.

    Aqui ficam as regras e cálculos do resumo financeiro.
    As consultas ao banco ficam no DashboardRepository.
    """

    @staticmethod
    def resumo(db: Session, usuario_logado: Usuario):
        """
        Retorna o resumo financeiro do usuário logado.

        Calcula:
        - saldo
        - receitas
        - despesas
        - quantidade de transações
        - últimas transações
        - gastos por categoria
        - acompanhamento de orçamentos
        """

        transacoes = DashboardRepository.listar_transacoes_do_usuario(
            db,
            usuario_logado.id
        )

        total_receitas = Decimal("0.00")
        total_despesas = Decimal("0.00")

        for transacao in transacoes:
            if transacao.tipo == "receita":
                total_receitas += transacao.valor

            if transacao.tipo == "despesa":
                total_despesas += transacao.valor

        saldo_inicial = usuario_logado.saldo_inicial or Decimal("0.00")

        saldo = saldo_inicial + total_receitas - total_despesas

        # Pegamos apenas as 5 transações mais recentes
        # Pegamos apenas as 5 transações mais recentes com os dados da categoria
        ultimas_transacoes = DashboardRepository.listar_ultimas_transacoes_com_categoria(
        db,
        usuario_logado.id,
        limite=5
        )

        despesas_com_categoria = DashboardRepository.listar_despesas_com_categoria(
            db,
            usuario_logado.id
        )

        categorias_resumo = {}

        for item in despesas_com_categoria:
            nome = item.categoria

            if nome not in categorias_resumo:
                categorias_resumo[nome] = {
                    "categoria": nome,
                    "cor": item.cor,
                    "icone": item.icone,
                    "total": Decimal("0.00")
                }

            categorias_resumo[nome]["total"] += item.valor

        orcamentos_do_usuario = DashboardRepository.listar_orcamentos_com_categoria(
            db,
            usuario_logado.id
        )

        resumo_orcamentos = []

        for orcamento in orcamentos_do_usuario:
            gasto_atual = Decimal("0.00")

            # Somamos apenas despesas da mesma categoria, mês e ano do orçamento
            for transacao in transacoes:
                if (
                    transacao.tipo == "despesa"
                    and transacao.categoria_id == orcamento.categoria_id
                    and transacao.data.month == orcamento.mes
                    and transacao.data.year == orcamento.ano
                ):
                    gasto_atual += transacao.valor

            valor_restante = orcamento.valor_limite - gasto_atual

            if orcamento.valor_limite > 0:
                percentual_utilizado = (gasto_atual / orcamento.valor_limite) * 100
            else:
                percentual_utilizado = Decimal("0.00")

            status = "dentro_do_limite"

            if gasto_atual > orcamento.valor_limite:
                status = "ultrapassado"

            resumo_orcamentos.append({
                "orcamento_id": orcamento.orcamento_id,
                "categoria_id": orcamento.categoria_id,
                "categoria": orcamento.categoria,
                "cor": orcamento.cor,
                "icone": orcamento.icone,
                "mes": orcamento.mes,
                "ano": orcamento.ano,
                "valor_limite": orcamento.valor_limite,
                "gasto_atual": gasto_atual,
                "valor_restante": valor_restante,
                "percentual_utilizado": percentual_utilizado,
                "status": status
            })

        return {
            "saldo": saldo,
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "quantidade_transacoes": len(transacoes),
            "ultimas_transacoes": ultimas_transacoes,
            "gastos_por_categoria": list(categorias_resumo.values()),
            "orcamentos": resumo_orcamentos
        }