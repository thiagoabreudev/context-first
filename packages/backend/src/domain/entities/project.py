"""
Project Entity

Representa um projeto que contém múltiplas demands.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..value_objects.context_budget import ContextBudget
from ..exceptions import ContextBudgetExceededError


@dataclass
class Project:
    """
    Projeto que agrupa demands relacionadas.

    Attributes:
        id: Identificador único
        name: Nome do projeto
        description: Descrição detalhada
        owner_id: ID do usuário dono do projeto
        context_budget: Orçamento de contexto (tokens)
        created_at: Data/hora de criação
        updated_at: Data/hora de última atualização
    """

    id: str
    name: str
    description: str
    owner_id: str
    context_budget: ContextBudget
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Valida invariantes após inicialização."""
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("name cannot be empty")
        if not self.owner_id:
            raise ValueError("owner_id cannot be empty")

    def can_consume_tokens(self, tokens: int) -> bool:
        """
        Valida se projeto pode consumir quantidade específica de tokens.

        Args:
            tokens: Quantidade de tokens a validar

        Returns:
            True se há budget suficiente
        """
        return self.context_budget.can_consume(tokens)

    def consume_tokens(self, tokens: int) -> None:
        """
        Consome tokens do budget do projeto.

        Regra de negócio: Projeto não pode exceder seu budget de contexto.

        Args:
            tokens: Quantidade de tokens a consumir

        Raises:
            ContextBudgetExceededError: Se não há budget suficiente
        """
        if not self.can_consume_tokens(tokens):
            raise ContextBudgetExceededError(
                f"Cannot consume {tokens} tokens from project '{self.name}'. "
                f"Only {self.context_budget.remaining_tokens} remaining."
            )

        self.context_budget = self.context_budget.consume(tokens)
        self.updated_at = datetime.utcnow()

    def is_budget_critical(self) -> bool:
        """
        Verifica se budget do projeto está em nível crítico.

        Returns:
            True se < 10% do budget disponível
        """
        return self.context_budget.is_critical()

    def is_budget_warning(self) -> bool:
        """
        Verifica se budget do projeto está em nível de aviso.

        Returns:
            True se < 30% do budget disponível
        """
        return self.context_budget.is_warning()
