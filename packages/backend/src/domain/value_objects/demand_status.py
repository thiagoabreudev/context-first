"""
DemandStatus Value Object

Representa os possíveis estados de uma Demand no workflow SPARC+DD.
"""

from enum import Enum
from typing import Optional


class DemandStatus(str, Enum):
    """
    Status de uma Demand seguindo workflow SPARC+DD.

    Workflow linear:
    DRAFT → SPEC_APPROVED → ARCHITECTURE_DONE → CODE_COMPLETE → PR_MERGED
    """

    DRAFT = "draft"
    SPEC_APPROVED = "spec_approved"
    ARCHITECTURE_DONE = "architecture_done"
    CODE_COMPLETE = "code_complete"
    PR_MERGED = "pr_merged"

    def next_status(self) -> Optional['DemandStatus']:
        """
        Retorna o próximo status na sequência linear.

        Returns:
            Próximo status ou None se já estiver no final (PR_MERGED)
        """
        transitions = {
            DemandStatus.DRAFT: DemandStatus.SPEC_APPROVED,
            DemandStatus.SPEC_APPROVED: DemandStatus.ARCHITECTURE_DONE,
            DemandStatus.ARCHITECTURE_DONE: DemandStatus.CODE_COMPLETE,
            DemandStatus.CODE_COMPLETE: DemandStatus.PR_MERGED,
            DemandStatus.PR_MERGED: None,  # Status final
        }
        return transitions.get(self)

    def can_transition_to(self, target: 'DemandStatus') -> bool:
        """
        Valida se transição para status específico é permitida.

        Args:
            target: Status de destino

        Returns:
            True se transição é válida (próximo na sequência)
        """
        return target == self.next_status()

    def is_final(self) -> bool:
        """
        Verifica se é o status final do workflow.

        Returns:
            True se for PR_MERGED
        """
        return self == DemandStatus.PR_MERGED
