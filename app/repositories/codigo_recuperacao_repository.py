from sqlalchemy.orm import Session

from app.models.codigo_recuperacao_model import CodigoRecuperacaoSenha


class CodigoRecuperacaoRepository:
    """
    Repository dos códigos de recuperação de senha.

    Essa camada acessa diretamente o banco de dados.
    Ela não envia e-mail e não valida regras de negócio.
    """

    @staticmethod
    def criar(db: Session, codigo: CodigoRecuperacaoSenha):
        """
        Salva um novo código de recuperação no banco.
        """
        db.add(codigo)
        db.commit()
        db.refresh(codigo)

        return codigo

    @staticmethod
    def buscar_codigo_ativo_por_email(db: Session, email: str):
        """
        Busca o código mais recente ainda não usado para o e-mail informado.

        Esse código será usado para validar o PIN digitado pelo usuário.
        """
        return (
            db.query(CodigoRecuperacaoSenha)
            .filter(
                CodigoRecuperacaoSenha.email == email,
                CodigoRecuperacaoSenha.usado == False
            )
            .order_by(CodigoRecuperacaoSenha.criado_em.desc())
            .first()
        )

    @staticmethod
    def marcar_como_usado(db: Session, codigo: CodigoRecuperacaoSenha):
        """
        Marca um código como usado.

        Depois disso, ele não poderá ser reutilizado.
        """
        codigo.usado = True
        db.commit()
        db.refresh(codigo)

        return codigo

    @staticmethod
    def incrementar_tentativas(db: Session, codigo: CodigoRecuperacaoSenha):
        """
        Aumenta o número de tentativas de uso do PIN.

        Usamos isso para bloquear abuso de tentativas.
        """
        codigo.tentativas += 1
        db.commit()
        db.refresh(codigo)

        return codigo

    @staticmethod
    def invalidar_codigos_anteriores(db: Session, email: str):
        """
        Marca como usados todos os códigos antigos desse e-mail.

        Assim, quando o usuário pedir um novo PIN,
        apenas o último código fica válido.
        """
        codigos = (
            db.query(CodigoRecuperacaoSenha)
            .filter(
                CodigoRecuperacaoSenha.email == email,
                CodigoRecuperacaoSenha.usado == False
            )
            .all()
        )

        for codigo in codigos:
            codigo.usado = True

        db.commit()