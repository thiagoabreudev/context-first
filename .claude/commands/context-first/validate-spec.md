---
name: context-first-validate-spec
description: Validar código contra metaspecs (regras de negócio)
tools: Read, Glob, Grep, Bash
---

# Validate Spec Command

## Uso
```bash
# Validar arquivo específico
/context-first validate-spec src/workflows/candle_buy.py

# Validar todos os arquivos modificados
/context-first validate-spec
```

<file_path>
#$ARGUMENTS
</file_path>

---

## Passo 0: Carregar Variáveis de Ambiente

Antes de executar, carregar a variável `METASPECS_DIR` do arquivo `.ia.env`:

```bash
# Carregar .ia.env
if [ -f .ia.env ]; then
    export $(grep -v '^#' .ia.env | xargs)
    echo "✅ METASPECS_DIR carregado: $METASPECS_DIR"
else
    echo "❌ Arquivo .ia.env não encontrado. Crie baseado em .ia.env.example"
    exit 1
fi
```

**Importante**: Todos os caminhos de metaspecs devem usar `$METASPECS_DIR` como prefixo.

---

## Comportamento

### Passo 1: Identificar Arquivos a Validar

**Se <file_path> estiver vazio**:
- Executar `git diff --name-only` para listar arquivos modificados
- Validar todos os arquivos modificados

**Se <file_path> estiver preenchido**:
- Validar apenas <file_path>

---

### Passo 2: Identificar Metaspecs Relevantes

Baseado no caminho do arquivo, identificar metaspecs aplicáveis usando `$METASPECS_DIR`:

**Exemplos**:
- `src/workflows/candle_buy.py` → `$METASPECS_DIR/business/strategies/candle-buy.md`
- `src/api/auth.py` → `$METASPECS_DIR/business/authentication/`
- `src/domain/calculations.py` → `$METASPECS_DIR/technical/architecture/clean-architecture-principles.md`

**Usar keywords**:
- `candle_buy` → candle-buy.md
- `auth`, `login` → authentication/
- `balance` → strategy-balance-isolation.md
- `domain/` → clean-architecture-principles.md

---

### Passo 3: Ler Metaspecs Identificadas

Ler TODAS as metaspecs identificadas como relevantes de `$METASPECS_DIR`.

---

### Passo 4: Ler Código do Arquivo

Ler conteúdo completo do arquivo a validar.

---

### Passo 5: Validar Contra Regras

Para cada metaspec lida, validar:

#### Must Do (O que DEVE fazer)

Verificar se código implementa TODAS as regras obrigatórias.

**Exemplo** (candle-buy.md):
- ✅ DEVE validar `candle_strategy_enabled = true`
- ✅ DEVE buscar sinal BUY pendente
- ✅ DEVE calcular budget Candle
- ✅ DEVE validar quantidade >= mínimo
- ✅ DEVE colocar ordem MAKER
- ✅ DEVE marcar sinal como executed
- ✅ DEVE salvar strategy_source
- ✅ DEVE instrumentar observabilidade

**Validação**:
- Buscar no código cada regra
- Marcar como ✅ (implementado) ou ❌ (não implementado)

---

#### Must Not Do (O que NÃO DEVE fazer)

Verificar se código NÃO viola anti-patterns.

**Exemplo** (candle-buy.md):
- ❌ NÃO DEVE cancelar ordens de outras estratégias
- ❌ NÃO DEVE usar budget de Traditional
- ❌ NÃO DEVE executar sinal já executed

**Validação**:
- Buscar no código violações
- Marcar como ✅ (não viola) ou ❌ (VIOLA!)

---

#### Edge Cases (Casos extremos)

Verificar se código trata casos extremos.

**Exemplo** (candle-buy.md):
- ⚠️ Timeout de operação
- ⚠️ Database unavailable
- ⚠️ Sinal mudou de BUY para SELL

**Validação**:
- Buscar tratamento de erros
- Marcar como ✅ (tratado) ou ⚠️ (não tratado)

---

### Passo 6: Calcular Spec Compliance Score

**Pontuação**:
- Total de regras = Must Do + Must Not Do + Edge Cases
- Regras implementadas/validadas = contagem de ✅
- **Compliance Score** = (regras validadas / total) × 100%

**Classificação**:
- **>= 90%**: Excelente ✅
- **80-89%**: Bom ✅
- **70-79%**: Aceitável ⚠️
- **< 70%**: Crítico ❌

---

### Passo 7: Gerar Relatório

```
📋 Spec Validation - <file_path>

Metaspecs Aplicáveis:
  - $METASPECS_DIR/business/strategies/candle-buy.md
  - $METASPECS_DIR/technical/architecture/clean-architecture-principles.md

Validation Results:

  ✅ MUST DO (8/10 implemented) - 80%
    ✅ Validar candle_strategy_enabled
    ✅ Buscar sinal BUY pendente
    ✅ Calcular budget Candle
    ✅ Validar quantidade >= mínimo
    ✅ Colocar ordem MAKER
    ✅ Marcar sinal como executed
    ✅ Salvar strategy_source
    ✅ Instrumentar observabilidade
    ❌ Cancelar ordens antigas quando preço muda (NOT IMPLEMENTED)
    ❌ Ignorar sinal quando quantidade < mínimo (NOT IMPLEMENTED)
  
  ✅ MUST NOT DO (3/3 validated) - 100%
    ✅ NÃO cancela ordens de outras estratégias
    ✅ NÃO usa budget de Traditional
    ✅ NÃO executa sinal já executed
  
  ⚠️ EDGE CASES (2/3 handled) - 67%
    ✅ Timeout de operação (try/except com timeout)
    ✅ Database unavailable (retry logic)
    ❌ Sinal mudou de BUY para SELL (NOT HANDLED)

Overall Spec Compliance: 13/16 (81%) ✅

Recommendations:
  1. Implementar cancelamento de ordens quando preço muda
  2. Implementar ignore de sinal quando quantidade < mínimo
  3. Tratar mudança de sinal BUY → SELL

Decision:
  ✅ Compliance >= 80%: APPROVED
  ⚠️ Compliance 70-79%: REVIEW RECOMMENDED
  ❌ Compliance < 70%: BLOCKED - fix violations
```

---

### Passo 8: Decisão

**Se Compliance >= 80%**:
```
✅ APPROVED

Spec compliance is good. Code follows business rules.

Minor improvements suggested:
  - Implement missing edge case handling
  - Add validation for quantity < minimum
```

**Se Compliance 70-79%**:
```
⚠️ REVIEW RECOMMENDED

Spec compliance is acceptable but could be improved.

Missing implementations:
  1. Cancel old orders when price changes
  2. Ignore signal when quantity < minimum
  3. Handle signal change BUY → SELL

Consider implementing before merge.
```

**Se Compliance < 70%**:
```
❌ BLOCKED - Spec violations

Code does NOT follow business rules. Critical violations found:

MUST DO not implemented (5):
  1. Validate candle_strategy_enabled
  2. Check for pending BUY signal
  3. Calculate Candle budget
  4. Validate quantity >= minimum
  5. Mark signal as executed

Actions required:
  1. Implement missing MUST DO rules
  2. Run /context-first validate-spec again
  3. Only proceed after compliance >= 70%
```

---

## Exemplo de Uso

### Exemplo 1: Validar Arquivo Específico

```bash
/context-first validate-spec src/workflows/candle_buy.py
```

**Output**:
```
📋 Spec Validation - src/workflows/candle_buy.py

Metaspecs:
  - $METASPECS_DIR/business/strategies/candle-buy.md

Results:
  ✅ MUST DO (10/10) - 100%
  ✅ MUST NOT DO (3/3) - 100%
  ✅ EDGE CASES (3/3) - 100%

Compliance: 16/16 (100%) ✅

✅ PERFECT COMPLIANCE

Code fully implements all business rules!
```

---

### Exemplo 2: Validar Todos os Arquivos Modificados

```bash
/context-first validate-spec
```

**Output**:
```
📋 Spec Validation - Multiple Files

Files validated (3):
  - src/workflows/candle_buy.py
  - src/workflows/candle_sales.py
  - src/domain/calculations.py

Overall Compliance: 85% ✅

Results by File:

  src/workflows/candle_buy.py: 100% ✅
  src/workflows/candle_sales.py: 75% ⚠️
  src/domain/calculations.py: 80% ✅

Issues Found:

  src/workflows/candle_sales.py:
    ❌ MUST DO not implemented (2):
      - Validate urgent_sales_enabled
      - Check for pending SELL signal
    
    ⚠️ EDGE CASE not handled (1):
      - Insufficient balance for sale

Recommendations:
  1. Fix candle_sales.py to implement missing rules
  2. Add edge case handling for insufficient balance
  3. Re-validate after fixes

✅ APPROVED (with recommendations)
```

---

## Relacionado

- [/context-first test-first](./test-first.md) - Criar testes baseados em specs
- [/metaspecs validate](../metaspecs/validate.md) - Validar metaspecs lidas
- [@metaspec-gate-keeper](../../agents/metaspec-gate-keeper.md) - Agente de validação
