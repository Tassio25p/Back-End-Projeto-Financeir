from sqlalchemy.orm import Session

from app.models.transacao_model import Transacao


class TransacaoRepository:
    """
    Repository de transações.

    Esta camada conversa diretamente com o banco de dados.
    Não colocamos regras de negócio aqui.
    """

    @staticmethod
    def criar(db: Session, transacao: Transacao):
        """
        Salva uma nova transação no banco.
        """
        db.add(transacao)
        db.commit()
        db.refresh(transacao)

        return transacao

    @staticmethod
    def listar_por_usuario(db: Session, usuario_id: int):
        """
        Lista todas as transações de um usuário específico.
        """
        return (
            db.query(Transacao)
            .filter(Transacao.usuario_id == usuario_id)
            .order_by(Transacao.data.desc())
            .all()
        )

    @staticmethod
    def buscar_por_id_e_usuario(db: Session, transacao_id: int, usuario_id: int):
        """
        Busca uma transação específica, garantindo que ela pertence ao usuário logado.
        """
        return (
            db.query(Transacao)
            .filter(
                Transacao.id == transacao_id,
                Transacao.usuario_id == usuario_id
            )
            .first()
        )

    @staticmethod
    def atualizar(db: Session, transacao: Transacao, dados: dict):
        """
        Atualiza os campos de uma transação.
        """
        for campo, valor in dados.items():
            setattr(transacao, campo, valor)

        db.commit()
        db.refresh(transacao)

        return transacao

    @staticmethod
    def excluir(db: Session, transacao: Transacao):
        """
        Exclui uma transação do banco.
        """
        db.delete(transacao)
        db.commit()

        return None