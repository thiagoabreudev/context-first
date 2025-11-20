---
name: context-budget
description: Definir orçamento de tokens para uma feature
tools: None
---

# Context Budget

Define um orçamento máximo de tokens para a feature atual, garantindo que o contexto não exploda.

## Argumentos

```
/context budget <feature-name> [percentage]
```

- `feature-name`: Nome da feature (ex: `feat-login`)
- `percentage`: Percentual do contexto total (padrão: 20%)

## Comportamento

1. **Calcular budget** em tokens absolutos
2. **Registrar** em `.claude/sessions/<feature>/budget.json`
3. **Monitorar** automaticamente durante desenvolvimento
4. **Alertar** quando budget for atingido

## Output

```
💰 CONTEXT BUDGET DEFINED

Feature: feat-login
Budget: 40,000 tokens (20% of total)
Current: 8,234 tokens (20.6% of budget)
Remaining: 31,766 tokens

Status: ✅ HEALTHY

Alerts:
  ⚠️  At 32,000 tokens (80%): Warning
  🔴 At 36,000 tokens (90%): Critical
  💥 At 40,000 tokens (100%): Budget exceeded!

Recommendations:
  - Keep feature scope focused
  - Use /context status to monitor
  - Run /context compact if needed
  - Consider splitting into sub-features if budget exceeded
```

## Budgets Recomendados

| Tipo de Feature | Budget | Percentual |
|------------------|--------|------------|
| CRUD simples | 20k tokens | 10% |
| Feature média | 40k tokens | 20% |
| Feature com IA | 60k tokens | 30% |
| Refactoring | 30k tokens | 15% |

**Regra de Ouro**: NUNCA exceder 30% do contexto total em uma única feature!

## Implementação

Crie arquivo `.claude/sessions/<feature>/budget.json`:

```json
{
  "feature": "feat-login",
  "budget_tokens": 40000,
  "budget_percentage": 20,
  "created_at": "2025-11-14T10:30:00Z",
  "alerts": {
    "warning": 32000,
    "critical": 36000,
    "exceeded": 40000
  }
}
```

A cada interação, verifique:
1. Tokens atuais da feature
2. Compare com budget
3. Mostre alerta se necessário
