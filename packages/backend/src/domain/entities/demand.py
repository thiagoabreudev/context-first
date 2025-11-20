"""
Demand Entity

Representa uma demanda de desenvolvimento no workflow SPARC+DD.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..value_objects.demand_status import DemandStatus
from ..value_objects.context_budget import ContextBudget
from ..exceptions import (
    InvalidStatusTransitionError,
    DemandAlreadyCompletedError,
)


@dataclass
class Demand:
    """
    Demanda de desenvolvimento seguindo workflow SPARC+DD.

    Attributes:
        id: Identificador único
        project_id: ID do projeto ao qual pertence
        title: Título da demand
        description: Descrição detalhada
        status: Status atual no workflow
        context_budget: Orçamento de contexto específico da demand
        created_at: Data/hora de criação
        updated_at: Data/hora de última atualização
    """

    id: str
    project_id: str
    title: str
    description: str
    status: DemandStatus = DemandStatus.DRAFT
    context_budget: Optional[ContextBudget] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Valida invariantes após inicialização."""
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.project_id:
            raise ValueError("project_id cannot be empty")
        if not self.title or not self.title.strip():
            raise ValueError("title cannot be empty")

    def can_transition_to(self, new_status: DemandStatus) -> bool:
        """
        Valida se transição para novo status é permitida.

        Args:
            new_status: Status de destino

        Returns:
            True se transição é válida
        """
        return self.status.can_transition_to(new_status)

    def transition_to(self, new_status: DemandStatus) -> None:
        """
        Transiciona demand para novo status.

        Regra de negócio: Transições devem seguir sequência linear do workflow.

        Args:
            new_status: Status de destino

        Raises:
            InvalidStatusTransitionError: Se transição é inválida
            DemandAlreadyCompletedError: Se demand já está finalizada
        """
        if self.status.is_final():
            raise DemandAlreadyCompletedError(
                f"Cannot transition demand '{self.title}' - already completed (PR_MERGED)"
            )

        if not self.can_transition_to(new_status):
            raise InvalidStatusTransitionError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )

        self.status = new_status
        self.updated_at = datetime.utcnow()

    def advance_to_next_status(self) -> None:
        """
        Avança demand para o próximo status na sequência.

        Convenience method para avançar sem especificar status destino.

        Raises:
            DemandAlreadyCompletedError: Se demand já está no status final
        """
        if self.status.is_final():
            raise DemandAlreadyCompletedError(
                f"Cannot advance demand '{self.title}' - already completed (PR_MERGED)"
            )

        next_status = self.status.next_status()
        if next_status is None:
            raise DemandAlreadyCompletedError(
                f"Demand '{self.title}' has no next status"
            )

        self.status = next_status
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        """
        Verifica se demand foi completada (PR merged).

        Returns:
            True se status é PR_MERGED
        """
        return self.status.is_final()
