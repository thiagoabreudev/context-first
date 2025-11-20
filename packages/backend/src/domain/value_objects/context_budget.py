"""
ContextBudget Value Object

Representa o orçamento de contexto (tokens) de um Project ou Demand.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextBudget:
    """
    Orçamento de contexto para gerenciar uso de tokens.

    Imutável - operações retornam nova instância.

    Attributes:
        max_tokens: Máximo de tokens alocados
        used_tokens: Tokens já consumidos
    """

    max_tokens: int
    used_tokens: int

    def __post_init__(self) -> None:
        """Valida invariantes após inicialização."""
        if self.max_tokens < 0:
            raise ValueError("max_tokens must be >= 0")
        if self.used_tokens < 0:
            raise ValueError("used_tokens must be >= 0")

    @property
    def remaining_tokens(self) -> int:
        """
        Tokens restantes disponíveis.

        Returns:
            Quantidade de tokens ainda disponíveis (nunca negativo)
        """
        return max(0, self.max_tokens - self.used_tokens)

    @property
    def percentage_used(self) -> float:
        """
        Percentual de tokens já utilizados.

        Returns:
            Valor entre 0.0 (0%) e 1.0 (100%)
        """
        if self.max_tokens == 0:
            return 0.0
        return min(1.0, self.used_tokens / self.max_tokens)

    def is_critical(self) -> bool:
        """
        Verifica se budget está em nível crítico (< 10% restante).

        Returns:
            True se menos de 10% do budget disponível
        """
        return self.percentage_used > 0.9

    def is_warning(self) -> bool:
        """
        Verifica se budget está em nível de aviso (< 30% restante).

        Returns:
            True se menos de 30% do budget disponível
        """
        return self.percentage_used > 0.7

    def is_healthy(self) -> bool:
        """
        Verifica se budget está saudável (> 30% restante).

        Returns:
            True se mais de 30% do budget disponível
        """
        return self.percentage_used <= 0.7

    def can_consume(self, tokens: int) -> bool:
        """
        Valida se é possível consumir quantidade específica de tokens.

        Args:
            tokens: Quantidade de tokens a consumir

        Returns:
            True se há tokens suficientes disponíveis
        """
        if tokens < 0:
            raise ValueError("tokens must be >= 0")
        return self.remaining_tokens >= tokens

    def consume(self, tokens: int) -> 'ContextBudget':
        """
        Consome tokens e retorna novo ContextBudget.

        Imutável - retorna nova instância.

        Args:
            tokens: Quantidade de tokens a consumir

        Returns:
            Novo ContextBudget com tokens consumidos

        Raises:
            ValueError: Se não há tokens suficientes
        """
        if tokens < 0:
            raise ValueError("tokens must be >= 0")

        if not self.can_consume(tokens):
            raise ValueError(
                f"Cannot consume {tokens} tokens. "
                f"Only {self.remaining_tokens} remaining."
            )

        return ContextBudget(
            max_tokens=self.max_tokens,
            used_tokens=self.used_tokens + tokens,
        )
