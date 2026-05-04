from sqlalchemy.orm import Session

from app.models.meta_model import MetaFinanceira


class MetaRepository:
    """
    Repository de metas financeiras.

    Essa camada conversa diretamente com o banco de dados.
    Não colocamos regra de negócio aqui.
    """

    @staticmethod
    def criar(db: Session, meta: MetaFinanceira):
        """
        Salva uma nova meta financeira no banco.
        """
        db.add(meta)
        db.commit()
        db.refresh(meta)

        return meta

    @staticmethod
    def listar_por_usuario(db: Session, usuario_id: int):
        """
        Lista todas as metas financeiras de um usuário.
        """
        return (
            db.query(MetaFinanceira)
            .filter(MetaFinanceira.usuario_id == usuario_id)
            .order_by(MetaFinanceira.criado_em.desc())
            .all()
        )

    @staticmethod
    def buscar_por_id_e_usuario(db: Session, meta_id: int, usuario_id: int):
        """
        Busca uma meta pelo ID, garantindo que ela pertence ao usuário logado.
        """
        return (
            db.query(MetaFinanceira)
            .filter(
                MetaFinanceira.id == meta_id,
                MetaFinanceira.usuario_id == usuario_id
            )
            .first()
        )

    @staticmethod
    def atualizar(db: Session, meta: MetaFinanceira, dados: dict):
        """
        Atualiza os campos de uma meta financeira.
        """
        for campo, valor in dados.items():
            setattr(meta, campo, valor)

        db.commit()
        db.refresh(meta)

        return meta

    @staticmethod
    def excluir(db: Session, meta: MetaFinanceira):
        """
        Exclui uma meta financeira do banco.
        """
        db.delete(meta)
        db.commit()

        return None