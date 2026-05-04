from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transacao_model import Transacao
from app.models.usuario_model import Usuario
from app.repositories.transacao_repository import TransacaoRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.transacao_schema import TransacaoCreate, TransacaoUpdate


class TransacaoService:
    """
    Service de transações.

    Esta camada valida regras de negócio antes de criar,
    editar, listar ou excluir transações.
    """

    TIPOS_VALIDOS = ["receita", "despesa"]

    @staticmethod
    def validar_tipo(tipo: str):
        """
        Garante que o tipo seja receita ou despesa.
        """
        if tipo not in TransacaoService.TIPOS_VALIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo inválido. Use 'receita' ou 'despesa'."
            )

    @staticmethod
    def validar_valor(valor):
        """
        Garante que o valor seja maior que zero.
        """
        if valor <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor da transação deve ser maior que zero."
            )

    @staticmethod
    def validar_categoria(db: Session, categoria_id: int, usuario_logado: Usuario):
        """
        Garante que a categoria existe e pertence ao usuário logado.
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
    def criar(db: Session, dados: TransacaoCreate, usuario_logado: Usuario):
        """
        Cria uma nova transação para o usuário logado.
        """

        TransacaoService.validar_tipo(dados.tipo)
        TransacaoService.validar_valor(dados.valor)
        TransacaoService.validar_categoria(db, dados.categoria_id, usuario_logado)

        nova_transacao = Transacao(
            descricao=dados.descricao,
            valor=dados.valor,
            tipo=dados.tipo,
            data=dados.data,
            metodo_pagamento=dados.metodo_pagamento,
            observacao=dados.observacao,
            usuario_id=usuario_logado.id,
            categoria_id=dados.categoria_id
        )

        return TransacaoRepository.criar(db, nova_transacao)

    @staticmethod
    def listar(db: Session, usuario_logado: Usuario):
        """
        Lista apenas as transações do usuário logado.
        """
        return TransacaoRepository.listar_por_usuario(db, usuario_logado.id)

    @staticmethod
    def buscar_por_id(db: Session, transacao_id: int, usuario_logado: Usuario):
        """
        Busca uma transação específica do usuário logado.
        """
        transacao = TransacaoRepository.buscar_por_id_e_usuario(
            db,
            transacao_id,
            usuario_logado.id
        )

        if not transacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada."
            )

        return transacao

    @staticmethod
    def atualizar(
        db: Session,
        transacao_id: int,
        dados: TransacaoUpdate,
        usuario_logado: Usuario
    ):
        """
        Atualiza uma transação do usuário logado.
        """
        transacao = TransacaoService.buscar_por_id(
            db,
            transacao_id,
            usuario_logado
        )

        dados_atualizados = dados.model_dump(exclude_unset=True)

        if "tipo" in dados_atualizados:
            TransacaoService.validar_tipo(dados_atualizados["tipo"])

        if "valor" in dados_atualizados:
            TransacaoService.validar_valor(dados_atualizados["valor"])

        if "categoria_id" in dados_atualizados:
            TransacaoService.validar_categoria(
                db,
                dados_atualizados["categoria_id"],
                usuario_logado
            )

        return TransacaoRepository.atualizar(
            db,
            transacao,
            dados_atualizados
        )

    @staticmethod
    def excluir(db: Session, transacao_id: int, usuario_logado: Usuario):
        """
        Exclui uma transação do usuário logado.
        """
        transacao = TransacaoService.buscar_por_id(
            db,
            transacao_id,
            usuario_logado
        )

        TransacaoRepository.excluir(db, transacao)

        return {
            "mensagem": "Transação excluída com sucesso."
        }