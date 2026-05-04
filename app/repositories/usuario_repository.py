from sqlalchemy.orm import Session

from app.models.usuario_model import Usuario


class UsuarioRepository:
    """
    Camada responsável por acessar a tabela de usuários no banco.

    Aqui não colocamos regra de negócio.
    Apenas consultas, criação e atualização no banco.
    """

    @staticmethod
    def buscar_por_email(db: Session, email: str):
        """
        Busca um usuário pelo e-mail.

        Usado no cadastro para verificar se já existe conta
        e no login para encontrar o usuário.
        """
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def buscar_por_id(db: Session, usuario_id: int):
        """
        Busca um usuário pelo ID.

        Será usado  para identificar o usuário logado pelo token.
        """
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    @staticmethod
    def criar(db: Session, usuario: Usuario):
        """
        Salva um novo usuário no banco.
        """
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario
    
    @staticmethod
    def atualizar(db: Session, usuario: Usuario, dados: dict):
        """
        Atualiza os campos de um usuário.
        """
        for campo, valor in dados.items():
            setattr(usuario, campo, valor)

        db.commit()
        db.refresh(usuario)
       
        return usuario
    
@staticmethod
def atualizar(db: Session, usuario: Usuario, dados: dict):
    """
    Atualiza os dados do usuário no banco.
    """
    for campo, valor in dados.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario