from sqlalchemy.orm import Session

from app.models.transacao_model import Transacao
from app.models.categoria_model import Categoria
from app.models.orcamento_model import Orcamento


class DashboardRepository:
    """
    Repository do Dashboard.

    Essa camada é responsável por buscar no banco os dados
    necessários para montar o resumo financeiro.
    """

    @staticmethod
    def listar_transacoes_do_usuario(db: Session, usuario_id: int):
        """
        Busca todas as transações do usuário logado.

        Usamos essas transações para calcular:
        - total de receitas
        - total de despesas
        - saldo
        - últimas transações
        """
        return (
            db.query(Transacao)
            .filter(Transacao.usuario_id == usuario_id)
            .order_by(Transacao.data.desc())
            .all()
        )

    @staticmethod
    def listar_despesas_com_categoria(db: Session, usuario_id: int):
        """
        Busca apenas despesas do usuário junto com os dados da categoria.

        Usamos isso para montar o resumo de gastos por categoria.
        """
        return (
            db.query(
                Categoria.nome.label("categoria"),
                Categoria.cor.label("cor"),
                Categoria.icone.label("icone"),
                Transacao.valor.label("valor"),
            )
            .join(Categoria, Categoria.id == Transacao.categoria_id)
            .filter(
                Transacao.usuario_id == usuario_id,
                Transacao.tipo == "despesa"
            )
            .all()
        )

    @staticmethod
    def listar_orcamentos_com_categoria(db: Session, usuario_id: int):
        """
        Busca os orçamentos do usuário junto com os dados da categoria.

        Usamos isso para comparar:
        - limite definido
        - gasto real da categoria
        """
        return (
            db.query(
                Orcamento.id.label("orcamento_id"),
                Orcamento.mes.label("mes"),
                Orcamento.ano.label("ano"),
                Orcamento.valor_limite.label("valor_limite"),
                Categoria.id.label("categoria_id"),
                Categoria.nome.label("categoria"),
                Categoria.cor.label("cor"),
                Categoria.icone.label("icone"),
            )
            .join(Categoria, Categoria.id == Orcamento.categoria_id)
            .filter(Orcamento.usuario_id == usuario_id)
            .order_by(Orcamento.ano.desc(), Orcamento.mes.desc())
            .all()
        )
    
    @staticmethod
    def listar_ultimas_transacoes_com_categoria(db: Session, usuario_id: int, limite: int = 5):
        """
        Busca as últimas transações do usuário com os dados da categoria.

        Usamos no Dashboard para mostrar:
        - descrição
        - valor
        - tipo
        - data
        - nome da categoria
        """
        return (
            db.query(
                Transacao.id.label("id"),
                Transacao.descricao.label("descricao"),
                Transacao.valor.label("valor"),
                Transacao.tipo.label("tipo"),
                Transacao.data.label("data"),
                Transacao.metodo_pagamento.label("metodo_pagamento"),
                Transacao.observacao.label("observacao"),
                Transacao.categoria_id.label("categoria_id"),
                Categoria.nome.label("categoria_nome"),
                Categoria.cor.label("categoria_cor"),
                Categoria.icone.label("categoria_icone"),
            )
            .join(Categoria, Categoria.id == Transacao.categoria_id)
            .filter(Transacao.usuario_id == usuario_id)
            .order_by(Transacao.data.desc(), Transacao.id.desc())
            .limit(limite)
            .all()
        )