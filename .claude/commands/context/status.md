---
name: context-status
description: Monitorar uso atual da janela de contexto
tools: None
---

# Context Status

Exibe informações detalhadas sobre o uso atual da janela de contexto.

## Comportamento

1. **Estimar tokens** de cada componente do contexto
2. **Calcular percentual** de uso
3. **Mostrar breakdown** detalhado
4. **Dar recomendações** baseadas em thresholds

## Output

```
📊 CONTEXT STATUS

Current Usage: 45,234 / 200,000 tokens (22.6%)
Status: ✅ HEALTHY

Breakdown:
  System Prompt:        2,145 tokens (1.1%)
  Conversation:        18,567 tokens (9.3%)
  Files in Context:    22,890 tokens (11.4%)
  Specs (business/technical): 1,632 tokens (0.8%)
  Available:          154,766 tokens (77.4%)

Files Loaded (12):
  - CLAUDE.md (1,234 tokens)
  - specs/business/authentication/login.md (456 tokens)
  - src/auth/login.ts (2,345 tokens)
  - src/auth/login.test.ts (1,890 tokens)
  - ... (8 more)

Recommendations:
  ✅ Context usage is healthy
  ✅ No action needed yet
  
  When context reaches 40%:
    → Run /context compact
  
  When context reaches 50%:
    → Run /context checkpoint
    → Consider finishing current feature
```

## Thresholds

- **0-40%**: ✅ HEALTHY (verde) - Continue normalmente
- **40-60%**: ⚠️ WARNING (amarelo) - Compactar recomendado
- **60-80%**: 🔴 CRITICAL (vermelho) - Ação necessária
- **80-100%**: 💥 DANGER (vermelho piscante) - Fechar sessão

## Implementação

Estime tokens usando esta fórmula aproximada:
- 1 token ≈ 4 caracteres
- 1 token ≈ 0.75 palavras

Para cada arquivo em contexto:
1. Conte caracteres
2. Divida por 4
3. Some todos os arquivos
4. Adicione conversa atual
5. Calcule percentual
