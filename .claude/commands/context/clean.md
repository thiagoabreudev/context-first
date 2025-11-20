---
name: context-clean
description: Remover informações desnecessárias do contexto
tools: None
---

# Context Clean

Remove arquivos, referências e informações desnecessárias do contexto atual, mantendo apenas o essencial.

## Quando Usar

- ✅ Muitos arquivos carregados que não são mais relevantes
- ✅ Specs antigas de features já concluídas
- ✅ Testes que já estão passando
- ✅ Documentação de referência que já foi consultada
- ✅ Contexto atingiu **40%+** e você quer prevenir crescimento

## Comportamento

1. **Analisar** todos os arquivos em contexto
2. **Identificar** arquivos não utilizados recentemente
3. **Categorizar** por relevância
4. **Sugerir** remoções
5. **Remover** após confirmação

## Output

```
🧹 CONTEXT CLEANING

Current files in context: 18 files (34,567 tokens)

Candidates for removal:

HIGH PRIORITY (not used in last 10 messages):
  ❌ metaspecs/business/authentication/register.md (1,234 tokens)
  ❌ src/auth/register.ts (2,345 tokens)
  ❌ src/auth/register.test.ts (1,890 tokens)
  ❌ docs/API_REFERENCE.md (3,456 tokens)
  
  Subtotal: 8,925 tokens (25.8%)

MEDIUM PRIORITY (not used in last 5 messages):
  ⚠️  src/utils/validation.ts (567 tokens)
  ⚠️  src/utils/validation.test.ts (789 tokens)
  
  Subtotal: 1,356 tokens (3.9%)

LOW PRIORITY (used recently):
  ✅ src/auth/login.ts (2,345 tokens)
  ✅ src/auth/login.test.ts (1,890 tokens)
  ✅ metaspecs/business/authentication/login.md (1,456 tokens)
  
  Subtotal: 5,691 tokens (16.5%)

Recommendation:
  Remove HIGH PRIORITY files to save 8,925 tokens (25.8%)

Proceed? (yes/no)
```

## Categorias de Limpeza

### 1. **Specs de Features Concluídas**
```
✅ Feature implementada
✅ Testes passando
✅ Spec não será mais modificada
→ REMOVER do contexto
```

### 2. **Testes que Já Passam**
```
✅ Testes implementados
✅ Todos passando
✅ Não precisa modificar
→ REMOVER do contexto (manter apenas spec)
```

### 3. **Documentação de Referência**
```
✅ Já consultada
✅ Informação já absorvida
✅ Não será consultada novamente
→ REMOVER do contexto
```

### 4. **Arquivos de Outras Features**
```
✅ Feature diferente da atual
✅ Não há dependência
✅ Não será modificada
→ REMOVER do contexto
```

## Implementação

### Algoritmo de Relevância

```typescript
function calculateRelevance(file: string): number {
  let score = 0;
  
  // Usado recentemente?
  const lastUsed = getLastUsedMessage(file);
  if (lastUsed <= 3) score += 50;
  else if (lastUsed <= 5) score += 30;
  else if (lastUsed <= 10) score += 10;
  
  // Tipo de arquivo
  if (file.includes('metaspecs/')) score += 20;
  if (file.includes('.test.')) score -= 10;
  if (file.includes('docs/')) score -= 15;
  
  // Feature atual?
  const currentFeature = getCurrentFeature();
  if (file.includes(currentFeature)) score += 30;
  
  // Modificado recentemente?
  if (wasModifiedInSession(file)) score += 40;
  
  return score;
}

// score >= 70: Keep (LOW PRIORITY)
// score 40-69: Maybe remove (MEDIUM PRIORITY)
// score < 40: Remove (HIGH PRIORITY)
```

## Output Após Limpeza

```
✅ CONTEXT CLEANED

Removed 6 files:
  - metaspecs/business/authentication/register.md
  - src/auth/register.ts
  - src/auth/register.test.ts
  - docs/API_REFERENCE.md
  - src/utils/validation.ts
  - src/utils/validation.test.ts

BEFORE: 34,567 tokens (17.3%)
AFTER:  24,286 tokens (12.1%)
SAVED:  10,281 tokens (5.2%)

Remaining files: 12
  ✅ All relevant to current feature (feat-login)

Continue working with cleaned context!
```

## Dica Pro

Combine com `/context compact`:

```bash
# 1. Limpar arquivos desnecessários
/context clean

# 2. Compactar conversa
/context compact

# Resultado: Contexto otimizado!
```
