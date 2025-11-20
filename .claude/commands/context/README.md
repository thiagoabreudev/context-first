# Commands de Gerenciamento de Contexto

**5 commands** para integrar na metodologia CONTEXT-FIRST™

---

## 📦 Conteúdo

| Command | Arquivo | Quando Usar |
|---------|---------|-------------|
| `/context status` | `status.md` | A cada 10-15 interações |
| `/context budget` | `budget.md` | Início de feature |
| `/context compact` | `compact.md` | Contexto >= 40% |
| `/context clean` | `clean.md` | Periodicamente |
| `/context checkpoint` | `checkpoint.md` | Contexto >= 50% |

---

## 🚀 Como Instalar

### Opção 1: Manual

```bash
# Copiar para projeto
cp *.md /caminho/do/projeto/.claude/commands/context/

# Estrutura final:
.claude/
└── commands/
    └── context/
        ├── status.md
        ├── budget.md
        ├── compact.md
        ├── clean.md
        └── checkpoint.md
```

### Opção 2: Automatizada

```bash
# Criar script de instalação
cat > install-context-commands.sh << 'EOF'
#!/bin/bash
mkdir -p .claude/commands/context
cp context-commands-final/*.md .claude/commands/context/
echo "✅ Context commands installed!"
EOF

chmod +x install-context-commands.sh
./install-context-commands.sh
```

---

## 📖 Guia Rápido

### 1. Começar Feature

```bash
/engineer start feat-login
/context budget feat-login
# Budget: 40,000 tokens (20%)
```

### 2. Monitorar

```bash
# A cada 10-15 interações
/context status
# Current: 18,567 / 40,000 tokens (46.4%) ✅
```

### 3. Compactar (40%)

```bash
/context compact
# SAVED: 14,000 tokens (35%)
```

### 4. Limpar (Opcional)

```bash
/context clean
# Remove arquivos desnecessários
```

### 5. Checkpoint (50%)

```bash
/context checkpoint
# Salva estado completo
# Pronto para chavear feature!
```

---

## 🎯 Workflow Completo

```
┌─────────────────────────────────────────────────────┐
│ 1. START FEATURE                                    │
│    /engineer start feat-login                       │
│    /context budget feat-login                       │
│    Budget: 40k tokens (20%)                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. DEVELOP                                          │
│    /context-first test-first "login endpoint"      │
│    /engineer work                                   │
│    ... (10-15 interações)                           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. MONITOR                                          │
│    /context status                                  │
│    Current: 32k / 40k (80% of budget) ⚠️            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. COMPACT (se >= 40%)                              │
│    /context compact                                 │
│    SAVED: 14k tokens                                │
│    New: 18k / 40k (45%) ✅                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. CLEAN (opcional)                                 │
│    /context clean                                   │
│    Removed 6 files                                  │
│    SAVED: 8k tokens                                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 6. CHECKPOINT (se >= 50%)                           │
│    /context checkpoint                              │
│    Saved to .claude/sessions/feat-login/            │
│    Context: 49% → 6%                                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 7. NEW FEATURE                                      │
│    /engineer start feat-logout                      │
│    /context budget feat-logout                      │
│    Budget: 40k tokens (20%)                         │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Thresholds

| Contexto | Status | Ação |
|----------|--------|------|
| 0-40% | ✅ HEALTHY | Continue normalmente |
| 40-60% | ⚠️ WARNING | `/context compact` |
| 60-80% | 🔴 CRITICAL | `/context checkpoint` |
| 80-100% | 💥 DANGER | Fechar sessão obrigatório |

---

## 💡 Conceitos

### Context Budget™

Orçamento de tokens alocado para cada feature.

**Benefícios**:
- ✅ Previne explosão de contexto
- ✅ Força modularização
- ✅ Reduz custos (40-60%)
- ✅ Melhora performance

**Budgets Recomendados**:
```
CRUD simples:    20k tokens (10%)
Feature média:   40k tokens (20%)
Feature com IA:  60k tokens (30%)
Refactoring:     30k tokens (15%)

Regra: NUNCA exceder 30% em uma feature!
```

### Context Compaction

Resume conversa em `NOTES.md`, liberando espaço sem perder informações.

**Quando**:
- ✅ Contexto >= 40%
- ✅ Conversa muito longa
- ✅ Muitas idas e voltas

**Resultado**:
```
BEFORE: 68,450 tokens (34.2%)
AFTER:  31,200 tokens (15.6%)
SAVED:  37,250 tokens (18.6%)
```

### Context Checkpoint

Salva estado completo para chavear ou retomar depois.

**Quando**:
- ✅ Contexto >= 50%
- ✅ Bom ponto de parada
- ✅ Chavear para outra feature
- ✅ Fim do dia

**Estrutura**:
```
.claude/sessions/feat-login/
└── checkpoint-20251114-1045/
    ├── CHECKPOINT.md      # Resumo executivo
    ├── NOTES.md           # Conversa compactada
    ├── files.json         # Arquivos em contexto
    └── metaspecs/         # Cópia das specs
```

---

## 🎓 Ensinar no Workshop

### Dia 1 (Introdução)

**Manhã**: Conceitos
```
- O que é Context Window
- Por que 50% é o limite
- Demo: /context status
```

**Tarde**: Primeira prática
```
Feature 2: /context budget
Feature 3: /context compact (se atingir 40%)
```

### Dia 2 (Avançado)

**Manhã**: Commands avançados
```
Feature 5: /context clean
Feature 6: /context checkpoint
```

**Tarde**: Projeto real
```
Participantes aplicam TODOS os 5 commands
no projeto deles
```

---

## ✅ Checklist de Implementação

### Para Claude Code

- [ ] Copiar 5 commands para `.claude/commands/context/`
- [ ] Testar cada command individualmente
- [ ] Documentar no `CLAUDE.md` do projeto
- [ ] Adicionar thresholds no `.claude/settings.json`

### Para Workshop

- [ ] Adicionar módulo "Context Management" no roteiro
- [ ] Criar exercícios práticos para cada command
- [ ] Preparar demos ao vivo
- [ ] Criar checklist para participantes

### Para Metodologia

- [ ] Atualizar documentação CONTEXT-FIRST™
- [ ] Adicionar Context Budget™ como conceito
- [ ] Incluir workflow de gerenciamento
- [ ] Atualizar whitepaper com diferencial

---

## 🔧 Customização

### Ajustar Thresholds

Edite cada command para ajustar percentuais:

```markdown
# Em status.md
- 0-40%: ✅ HEALTHY
- 40-60%: ⚠️ WARNING
- 60-80%: 🔴 CRITICAL
- 80-100%: 💥 DANGER

# Ajuste conforme necessidade:
- 0-30%: ✅ HEALTHY
- 30-50%: ⚠️ WARNING
- 50-70%: 🔴 CRITICAL
- 70-100%: 💥 DANGER
```

### Ajustar Budgets

```markdown
# Em budget.md
CRUD simples:    20k tokens (10%)
Feature média:   40k tokens (20%)
Feature com IA:  60k tokens (30%)

# Ajuste conforme projeto:
CRUD simples:    30k tokens (15%)
Feature média:   50k tokens (25%)
Feature com IA:  70k tokens (35%)
```

---

## 📚 Referências

- **Context Window**: 200,000 tokens (Claude 3.5 Sonnet)
- **Threshold Recomendado**: 50% (100,000 tokens)
- **Budget Padrão**: 20% por feature (40,000 tokens)
- **Compaction Trigger**: 40% de uso
- **Checkpoint Trigger**: 50% de uso

---

## 🆘 Troubleshooting

### "Context ainda está crescendo"

```bash
# 1. Verificar status
/context status

# 2. Limpar arquivos
/context clean

# 3. Compactar conversa
/context compact

# 4. Se ainda alto, checkpoint
/context checkpoint
```

### "Budget sempre excedido"

```bash
# Feature muito grande!
# Solução: Split em sub-features

# Antes:
feat-authentication (80k tokens) ❌

# Depois:
feat-login (30k tokens) ✅
feat-logout (20k tokens) ✅
feat-refresh-token (25k tokens) ✅
```

### "Checkpoint não restaura corretamente"

```bash
# Verificar estrutura
ls -la .claude/sessions/<feature>/latest/

# Deve ter:
- CHECKPOINT.md
- NOTES.md
- files.json
- metaspecs/

# Se faltando, recriar checkpoint
/context checkpoint
```

---

## 📞 Suporte

Para dúvidas sobre os commands:
1. Ler documentação de cada command
2. Testar em projeto de exemplo
3. Ajustar thresholds conforme necessidade

---

**Versão**: 1.0.0  
**Data**: 2025-11-14  
**Autor**: IA do Jeito Certo  
**Licença**: Uso interno para workshop CONTEXT-FIRST™
