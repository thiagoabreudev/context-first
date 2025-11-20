"""
Checkpoint Entity

Representa um snapshot do estado de conversa para context management.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..exceptions import InvalidCheckpointError


@dataclass
class Checkpoint:
    """
    Checkpoint que armazena estado de conversa.

    Storage-agnostic - não sabe sobre S3 ou compressão (Infrastructure concern).

    Attributes:
        id: Identificador único
        demand_id: ID da demand à qual pertence
        context_snapshot: Snapshot do contexto em JSON
        tokens_used: Tokens consumidos até este checkpoint
        created_at: Data/hora de criação
        expires_at: Data/hora de expiração (TTL)
    """

    id: str
    demand_id: str
    context_snapshot: str  # JSON serializado
    tokens_used: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Valida invariantes após inicialização."""
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.demand_id:
            raise ValueError("demand_id cannot be empty")

        # Validações simples
        self._validate()

    def _validate(self) -> None:
        """
        Valida checkpoint.

        Validações simples para MVP.
        """
        if not self.validate_not_empty():
            raise InvalidCheckpointError("Checkpoint context_snapshot cannot be empty")

        if not self.validate_tokens_positive():
            raise InvalidCheckpointError("Checkpoint tokens_used must be positive")

    def validate_not_empty(self) -> bool:
        """
        Valida que snapshot não está vazio.

        Returns:
            True se context_snapshot não é vazio
        """
        return bool(self.context_snapshot and self.context_snapshot.strip())

    def validate_tokens_positive(self) -> bool:
        """
        Valida que tokens_used é positivo.

        Returns:
            True se tokens_used > 0
        """
        return self.tokens_used > 0

    def is_expired(self) -> bool:
        """
        Verifica se checkpoint expirou.

        Returns:
            True se expires_at está no passado
        """
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
