from sqlalchemy.orm import Session

from app.models.orcamento_model import Orcamento


class OrcamentoRepository:
    """
    Repository de orçamentos.

    Essa camada acessa diretamente o banco de dados.
    Aqui não colocamos regras de negócio, apenas consultas e operações no banco.
    """

    @staticmethod
    def criar(db: Session, orcamento: Orcamento):
        """
        Salva um novo orçamento no banco.
        """
        db.add(orcamento)
        db.commit()
        db.refresh(orcamento)

        return orcamento

    @staticmethod
    def listar_por_usuario(db: Session, usuario_id: int):
        """
        Lista todos os orçamentos de um usuário específico.
        """
        return (
            db.query(Orcamento)
            .filter(Orcamento.usuario_id == usuario_id)
            .order_by(Orcamento.ano.desc(), Orcamento.mes.desc())
            .all()
        )

    @staticmethod
    def buscar_por_id_e_usuario(db: Session, orcamento_id: int, usuario_id: int):
        """
        Busca um orçamento pelo ID, garantindo que ele pertence ao usuário logado.
        """
        return (
            db.query(Orcamento)
            .filter(
                Orcamento.id == orcamento_id,
                Orcamento.usuario_id == usuario_id
            )
            .first()
        )

    @staticmethod
    def buscar_por_categoria_mes_ano(
        db: Session,
        usuario_id: int,
        categoria_id: int,
        mes: int,
        ano: int
    ):
        """
        Busca se já existe um orçamento para a mesma categoria, mês e ano.

        Isso evita duplicidade, exemplo:
        dois orçamentos para Alimentação em maio/2026.
        """
        return (
            db.query(Orcamento)
            .filter(
                Orcamento.usuario_id == usuario_id,
                Orcamento.categoria_id == categoria_id,
                Orcamento.mes == mes,
                Orcamento.ano == ano
            )
            .first()
        )

    @staticmethod
    def atualizar(db: Session, orcamento: Orcamento, dados: dict):
        """
        Atualiza os campos de um orçamento.
        """
        for campo, valor in dados.items():
            setattr(orcamento, campo, valor)

        db.commit()
        db.refresh(orcamento)

        return orcamento

    @staticmethod
    def excluir(db: Session, orcamento: Orcamento):
        """
        Exclui um orçamento do banco.
        """
        db.delete(orcamento)
        db.commit()

        return None