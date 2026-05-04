from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.orcamento_model import Orcamento
from app.models.usuario_model import Usuario
from app.repositories.orcamento_repository import OrcamentoRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.orcamento_schema import OrcamentoCreate, OrcamentoUpdate


class OrcamentoService:
    """
    Service de orçamentos.

    Essa camada contém as regras de negócio antes de criar,
    editar, listar ou excluir orçamentos.
    """

    @staticmethod
    def validar_mes(mes: int):
        """
        Valida se o mês está entre 1 e 12.
        """
        if mes < 1 or mes > 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O mês deve estar entre 1 e 12."
            )

    @staticmethod
    def validar_ano(ano: int):
        """
        Valida se o ano é aceitável para o sistema.

        Aqui usamos uma regra simples para evitar anos muito fora da realidade.
        """
        if ano < 2000 or ano > 2100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O ano deve estar entre 2000 e 2100."
            )

    @staticmethod
    def validar_valor_limite(valor_limite):
        """
        Valida se o limite do orçamento é maior que zero.
        """
        if valor_limite <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor limite deve ser maior que zero."
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
    def validar_duplicidade(
        db: Session,
        usuario_logado: Usuario,
        categoria_id: int,
        mes: int,
        ano: int,
        orcamento_id_atual: int | None = None
    ):
        """
        Evita criar dois orçamentos para a mesma categoria, mês e ano.

        O parâmetro orcamento_id_atual é usado na atualização,
        para permitir atualizar o próprio orçamento sem acusar duplicidade.
        """
        orcamento_existente = OrcamentoRepository.buscar_por_categoria_mes_ano(
            db,
            usuario_logado.id,
            categoria_id,
            mes,
            ano
        )

        if orcamento_existente and orcamento_existente.id != orcamento_id_atual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um orçamento para essa categoria neste mês e ano."
            )

    @staticmethod
    def criar(db: Session, dados: OrcamentoCreate, usuario_logado: Usuario):
        """
        Cria um novo orçamento para o usuário logado.
        """

        OrcamentoService.validar_mes(dados.mes)
        OrcamentoService.validar_ano(dados.ano)
        OrcamentoService.validar_valor_limite(dados.valor_limite)
        OrcamentoService.validar_categoria(db, dados.categoria_id, usuario_logado)

        OrcamentoService.validar_duplicidade(
            db,
            usuario_logado,
            dados.categoria_id,
            dados.mes,
            dados.ano
        )

        novo_orcamento = Orcamento(
            mes=dados.mes,
            ano=dados.ano,
            valor_limite=dados.valor_limite,
            usuario_id=usuario_logado.id,
            categoria_id=dados.categoria_id
        )

        return OrcamentoRepository.criar(db, novo_orcamento)

    @staticmethod
    def listar(db: Session, usuario_logado: Usuario):
        """
        Lista apenas os orçamentos do usuário logado.
        """
        return OrcamentoRepository.listar_por_usuario(db, usuario_logado.id)

    @staticmethod
    def buscar_por_id(db: Session, orcamento_id: int, usuario_logado: Usuario):
        """
        Busca um orçamento específico do usuário logado.
        """
        orcamento = OrcamentoRepository.buscar_por_id_e_usuario(
            db,
            orcamento_id,
            usuario_logado.id
        )

        if not orcamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado."
            )

        return orcamento

    @staticmethod
    def atualizar(
        db: Session,
        orcamento_id: int,
        dados: OrcamentoUpdate,
        usuario_logado: Usuario
    ):
        """
        Atualiza um orçamento do usuário logado.
        """

        orcamento = OrcamentoService.buscar_por_id(
            db,
            orcamento_id,
            usuario_logado
        )

        dados_atualizados = dados.model_dump(exclude_unset=True)

        mes = dados_atualizados.get("mes", orcamento.mes)
        ano = dados_atualizados.get("ano", orcamento.ano)
        categoria_id = dados_atualizados.get("categoria_id", orcamento.categoria_id)
        valor_limite = dados_atualizados.get("valor_limite", orcamento.valor_limite)

        OrcamentoService.validar_mes(mes)
        OrcamentoService.validar_ano(ano)
        OrcamentoService.validar_valor_limite(valor_limite)
        OrcamentoService.validar_categoria(db, categoria_id, usuario_logado)

        OrcamentoService.validar_duplicidade(
            db,
            usuario_logado,
            categoria_id,
            mes,
            ano,
            orcamento_id_atual=orcamento.id
        )

        return OrcamentoRepository.atualizar(
            db,
            orcamento,
            dados_atualizados
        )

    @staticmethod
    def excluir(db: Session, orcamento_id: int, usuario_logado: Usuario):
        """
        Exclui um orçamento do usuário logado.
        """
        orcamento = OrcamentoService.buscar_por_id(
            db,
            orcamento_id,
            usuario_logado
        )

        OrcamentoRepository.excluir(db, orcamento)

        return {
            "mensagem": "Orçamento excluído com sucesso."
        }