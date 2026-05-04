from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria
from app.models.usuario_model import Usuario
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaService:
    """
    Service de categorias.

    Essa camada contém as regras de negócio antes de salvar, editar,
    listar ou excluir uma categoria.
    """

    TIPOS_VALIDOS = ["receita", "despesa"]

    #@staticmethod  para utilizar em metodos estáticos, ou seja, sem a necessidade de criar uma instância da classe para usar o método. como se fosse funções 
    # Isso é útil para organizar o código e deixar claro que esses métodos não dependem do estado da classe.
    
    @staticmethod

    def validar_tipo(tipo: str):
        """
        Valida se o tipo da categoria é permitido.

        Tipos aceitos:
        - receita
        - despesa
        """
        if tipo not in CategoriaService.TIPOS_VALIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo inválido. Use 'receita' ou 'despesa'."
            )

    @staticmethod
    def criar(db: Session, dados: CategoriaCreate, usuario_logado: Usuario):
        """
        Cria uma categoria para o usuário logado.
        """

        CategoriaService.validar_tipo(dados.tipo)

        nova_categoria = Categoria(
            nome=dados.nome,
            tipo=dados.tipo,
            cor=dados.cor,
            icone=dados.icone,
            usuario_id=usuario_logado.id
        )

        return CategoriaRepository.criar(db, nova_categoria)

    @staticmethod
    def listar(db: Session, usuario_logado: Usuario):
        """
        Lista apenas as categorias do usuário logado.
        """
        return CategoriaRepository.listar_por_usuario(db, usuario_logado.id)

    @staticmethod
    def buscar_por_id(db: Session, categoria_id: int, usuario_logado: Usuario):
        """
        Busca uma categoria específica do usuário logado.
        """

        categoria = CategoriaRepository.buscar_por_id_e_usuario(
            db,
            categoria_id,
            usuario_logado.id
        )

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada."
            )

        return categoria

    @staticmethod
    def atualizar(
        db: Session,
        categoria_id: int,
        dados: CategoriaUpdate,
        usuario_logado: Usuario
    ):
        """
        Atualiza uma categoria do usuário logado.
        """

        categoria = CategoriaService.buscar_por_id(
            db,
            categoria_id,
            usuario_logado
        )

        dados_atualizados = dados.model_dump(exclude_unset=True)

        if "tipo" in dados_atualizados:
            CategoriaService.validar_tipo(dados_atualizados["tipo"])

        return CategoriaRepository.atualizar(
            db,
            categoria,
            dados_atualizados
        )

    @staticmethod
    def excluir(db: Session, categoria_id: int, usuario_logado: Usuario):
        """
        Exclui uma categoria do usuário logado.
        """

        categoria = CategoriaService.buscar_por_id(
            db,
            categoria_id,
            usuario_logado
        )

        CategoriaRepository.excluir(db, categoria)

        return {
            "mensagem": "Categoria excluída com sucesso."
        }