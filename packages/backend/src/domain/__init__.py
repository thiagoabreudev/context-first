"""
Domain Layer

Business logic, entities, value objects seguindo DDD e Clean Architecture.

Este layer contém:
- Entities: Objetos com identidade (Project, Demand, Metaspec, Checkpoint)
- Value Objects: Objetos imutáveis (ContextBudget, DemandStatus)
- Exceptions: Exceções de negócio
- Domain Services: Lógica de domínio que não pertence a uma entity específica

Princípios:
- Sem dependências externas (framework-agnostic)
- Regras de negócio como métodos
- Type hints completo
- Imutabilidade onde aplicável (Value Objects)
"""

# Entities
from .entities import (
    Project,
    Demand,
    Metaspec,
    MetaspecType,
    Checkpoint,
)

# Value Objects
from .value_objects import (
    ContextBudget,
    DemandStatus,
)

# Exceptions
from .exceptions import (
    DomainException,
    ContextBudgetExceededError,
    InvalidStatusTransitionError,
    DemandAlreadyCompletedError,
    InvalidMetaspecError,
    InvalidCheckpointError,
)

__all__ = [
    # Entities
    "Project",
    "Demand",
    "Metaspec",
    "MetaspecType",
    "Checkpoint",
    # Value Objects
    "ContextBudget",
    "DemandStatus",
    # Exceptions
    "DomainException",
    "ContextBudgetExceededError",
    "InvalidStatusTransitionError",
    "DemandAlreadyCompletedError",
    "InvalidMetaspecError",
    "InvalidCheckpointError",
]
