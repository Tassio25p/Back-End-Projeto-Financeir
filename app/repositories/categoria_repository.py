from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria


class CategoriaRepository:
    """
    Repository de categorias.

    Essa camada é responsável apenas por acessar o banco de dados.
    Não colocamos regras de negócio aqui.
    """

    @staticmethod
    def criar(db: Session, categoria: Categoria):
        """
        Salva uma nova categoria no banco.
        """
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        return categoria

    @staticmethod
    def listar_por_usuario(db: Session, usuario_id: int):
        """
        Lista todas as categorias de um usuário específico.

        Isso garante que um usuário não veja categorias de outro.
        """
        return (
            db.query(Categoria)
            .filter(Categoria.usuario_id == usuario_id)
            .order_by(Categoria.nome.asc())
            .all()
        )

    @staticmethod
    def buscar_por_id_e_usuario(db: Session, categoria_id: int, usuario_id: int):
        """
        Busca uma categoria pelo ID, mas garantindo que ela pertence ao usuário logado.
        """
        return (
            db.query(Categoria)
            .filter(
                Categoria.id == categoria_id,
                Categoria.usuario_id == usuario_id
            )
            .first()
        )

    @staticmethod
    def atualizar(db: Session, categoria: Categoria, dados: dict):
        """
        Atualiza os campos de uma categoria.
        """
        for campo, valor in dados.items():
            setattr(categoria, campo, valor)

        db.commit()
        db.refresh(categoria)

        return categoria

    @staticmethod
    def excluir(db: Session, categoria: Categoria):
        """
        Exclui uma categoria do banco.
        """
        db.delete(categoria)
        db.commit()

        return None