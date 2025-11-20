"""
Metaspec Entity

Representa uma metaspecification (spec de negócio, técnica ou arquitetura).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from ..exceptions import InvalidMetaspecError


class MetaspecType(str, Enum):
    """
    Tipos de metaspecification.

    BUSINESS: Requisitos de negócio (Product Manager perspective)
    TECHNICAL: Especificação técnica (Tech Lead perspective)
    ARCHITECTURE: Design de arquitetura (Architect perspective)
    """

    BUSINESS = "business"
    TECHNICAL = "technical"
    ARCHITECTURE = "architecture"


@dataclass
class Metaspec:
    """
    Metaspecification que define requisitos e constraints de uma demand.

    Attributes:
        id: Identificador único
        demand_id: ID da demand à qual pertence
        type: Tipo de metaspec (business, technical, architecture)
        content: Conteúdo em Markdown
        version: Versão da metaspec (incremental)
        created_at: Data/hora de criação
        updated_at: Data/hora de última atualização
    """

    id: str
    demand_id: str
    type: MetaspecType
    content: str
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Valida invariantes após inicialização."""
        if not self.id:
            raise ValueError("id cannot be empty")
        if not self.demand_id:
            raise ValueError("demand_id cannot be empty")
        if self.version < 1:
            raise ValueError("version must be >= 1")

        # Validações simples de conteúdo
        self._validate_content()

    def _validate_content(self) -> None:
        """
        Valida conteúdo básico da metaspec.

        Regras simples para MVP:
        - Não pode ser vazio
        - Deve ter formato Markdown básico (headers)
        """
        if not self.validate_not_empty():
            raise InvalidMetaspecError("Metaspec content cannot be empty")

        if not self.validate_markdown_format():
            raise InvalidMetaspecError(
                "Metaspec content must be valid Markdown (requires headers)"
            )

    def validate_not_empty(self) -> bool:
        """
        Valida que conteúdo não está vazio.

        Returns:
            True se conteúdo não é vazio
        """
        return bool(self.content and self.content.strip())

    def validate_markdown_format(self) -> bool:
        """
        Valida formato básico de Markdown.

        Validação simples: verifica presença de headers (# ou ##).
        Validação complexa (schemas, templates) é feita por Agno Agents (IAD-12).

        Returns:
            True se tem pelo menos um header Markdown
        """
        if not self.content:
            return False
        return '#' in self.content

    def increment_version(self) -> None:
        """
        Incrementa versão da metaspec.

        Usado quando metaspec é atualizada.
        """
        self.version += 1
        self.updated_at = datetime.utcnow()
