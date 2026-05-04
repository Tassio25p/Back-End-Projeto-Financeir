from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.meta_model import MetaFinanceira
from app.models.usuario_model import Usuario
from app.repositories.meta_repository import MetaRepository
from app.schemas.meta_schema import MetaCreate, MetaUpdate


class MetaService:
    """
    Service de metas financeiras.

    Essa camada contém as regras de negócio antes de criar,
    editar, listar ou excluir metas.
    """

    STATUS_VALIDOS = ["ativa", "concluida", "cancelada"]

    @staticmethod
    def validar_status(status_meta: str):
        """
        Valida se o status da meta é permitido.

        Status aceitos:
        - ativa
        - concluida
        - cancelada
        """
        if status_meta not in MetaService.STATUS_VALIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status inválido. Use 'ativa', 'concluida' ou 'cancelada'."
            )

    @staticmethod
    def validar_valores(valor_alvo, valor_atual):
        """
        Valida os valores da meta.

        Regras:
        - valor_alvo precisa ser maior que zero
        - valor_atual não pode ser negativo
        - valor_atual não pode ser maior que valor_alvo
        """
        if valor_alvo <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor alvo deve ser maior que zero."
            )

        if valor_atual < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor atual não pode ser negativo."
            )

        if valor_atual > valor_alvo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor atual não pode ser maior que o valor alvo."
            )

    @staticmethod
    def criar(db: Session, dados: MetaCreate, usuario_logado: Usuario):
        """
        Cria uma nova meta financeira para o usuário logado.
        """

        MetaService.validar_status(dados.status)
        MetaService.validar_valores(dados.valor_alvo, dados.valor_atual)

        nova_meta = MetaFinanceira(
            titulo=dados.titulo,
            valor_alvo=dados.valor_alvo,
            valor_atual=dados.valor_atual,
            data_limite=dados.data_limite,
            status=dados.status,
            usuario_id=usuario_logado.id
        )

        return MetaRepository.criar(db, nova_meta)

    @staticmethod
    def listar(db: Session, usuario_logado: Usuario):
        """
        Lista apenas as metas do usuário logado.
        """
        return MetaRepository.listar_por_usuario(db, usuario_logado.id)

    @staticmethod
    def buscar_por_id(db: Session, meta_id: int, usuario_logado: Usuario):
        """
        Busca uma meta específica do usuário logado.
        """
        meta = MetaRepository.buscar_por_id_e_usuario(
            db,
            meta_id,
            usuario_logado.id
        )

        if not meta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meta financeira não encontrada."
            )

        return meta

    @staticmethod
    def atualizar(
        db: Session,
        meta_id: int,
        dados: MetaUpdate,
        usuario_logado: Usuario
    ):
        """
        Atualiza uma meta financeira do usuário logado.
        """

        meta = MetaService.buscar_por_id(db, meta_id, usuario_logado)

        dados_atualizados = dados.model_dump(exclude_unset=True)

        if "status" in dados_atualizados:
            MetaService.validar_status(dados_atualizados["status"])

        valor_alvo = dados_atualizados.get("valor_alvo", meta.valor_alvo)
        valor_atual = dados_atualizados.get("valor_atual", meta.valor_atual)

        MetaService.validar_valores(valor_alvo, valor_atual)

        return MetaRepository.atualizar(db, meta, dados_atualizados)

    @staticmethod
    def excluir(db: Session, meta_id: int, usuario_logado: Usuario):
        """
        Exclui uma meta financeira do usuário logado.
        """
        meta = MetaService.buscar_por_id(db, meta_id, usuario_logado)

        MetaRepository.excluir(db, meta)

        return {
            "mensagem": "Meta financeira excluída com sucesso."
        }