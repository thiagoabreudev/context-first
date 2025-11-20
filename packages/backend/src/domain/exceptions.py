"""
Domain Layer Exceptions

Exceções de negócio que representam violações de regras de domínio.
"""


class DomainException(Exception):
    """Base exception para todas exceções de domínio."""

    pass


# Context Budget Exceptions
class ContextBudgetExceededError(DomainException):
    """Lançada quando orçamento de contexto é excedido."""

    pass


# Demand Status Exceptions
class InvalidStatusTransitionError(DomainException):
    """Lançada quando transição de status é inválida."""

    pass


class DemandAlreadyCompletedError(DomainException):
    """Lançada quando tentativa de modificar demand já finalizada."""

    pass


# Metaspec Exceptions
class InvalidMetaspecError(DomainException):
    """Lançada quando metaspec não atende requisitos mínimos."""

    pass


# Checkpoint Exceptions
class InvalidCheckpointError(DomainException):
    """Lançada quando checkpoint não atende requisitos mínimos."""

    pass
