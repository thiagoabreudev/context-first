---
name: context-checkpoint
description: Salvar estado completo e preparar para chaveamento de contexto
tools: None
---

# Context Checkpoint

Salva o estado completo da feature atual em `.claude/sessions/<feature>/`, permitindo chavear para outra feature ou retomar depois.

## Quando Usar

- ✅ Contexto atingiu **50-60%**
- ✅ Feature atual está em bom ponto de parada
- ✅ Precisa chavear para outra feature urgente
- ✅ Fim do dia de trabalho
- ✅ Antes de passar feature para outro dev

## Comportamento

1. **Compactar** contexto (se necessário)
2. **Salvar** estado completo em `.claude/sessions/<feature>/`
3. **Criar** snapshot de arquivos relevantes
4. **Gerar** resumo executivo
5. **Preparar** para chaveamento

## Output

```
💾 CONTEXT CHECKPOINT

Feature: feat-login
Checkpoint ID: feat-login-20251114-1045

Saving state...
  ✅ Conversation compacted → NOTES.md
  ✅ Files snapshot → files.json
  ✅ Metaspecs → metaspecs/
  ✅ Test results → test-results.json
  ✅ Executive summary → CHECKPOINT.md

Checkpoint saved to:
  .claude/sessions/feat-login/checkpoint-20251114-1045/

Context status:
  BEFORE: 98,456 tokens (49.2%)
  AFTER:  12,345 tokens (6.2%)
  SAVED:  86,111 tokens (43.0%)

✅ Checkpoint created successfully!

Next steps:
  1. Start new feature: /engineer start <new-feature>
  2. Resume later: /engineer resume feat-login
  3. Share with team: Share .claude/sessions/feat-login/
```

## Estrutura do Checkpoint

```
.claude/sessions/feat-login/
├── checkpoint-20251114-1045/
│   ├── CHECKPOINT.md          # Resumo executivo
│   ├── NOTES.md               # Conversa compactada
│   ├── files.json             # Lista de arquivos em contexto
│   ├── test-results.json      # Resultados dos testes
│   ├── context-state.json     # Estado do contexto
│   └── metaspecs/             # Cópia das metaspecs
│       └── business/
│           └── authentication/
│               └── login.md
└── latest -> checkpoint-20251114-1045/  # Symlink
```

## CHECKPOINT.md (Exemplo)

```markdown
# Checkpoint: feat-login

**Created**: 2025-11-14 10:45
**Checkpoint ID**: feat-login-20251114-1045
**Status**: 🟢 Ready for handoff

## Executive Summary

Login endpoint implementado e testado. Autenticação JWT funcionando com refresh token. Todos os testes passando (12/12).

## Progress

- [x] Metaspec criada e validada
- [x] Endpoint `/auth/login` implementado
- [x] Validação com Zod (frontend + backend)
- [x] JWT com refresh token
- [x] 12 testes unitários passando
- [x] Integração com Prisma
- [ ] Rate limiting (próximo passo)
- [ ] Deploy em staging

## Key Decisions

1. **JWT Strategy**: Access token (15min) + Refresh token (7 dias)
2. **Storage**: httpOnly cookies para segurança
3. **Validation**: Zod schema compartilhado
4. **Testing**: Vitest com mocks de Date.now()

## Files Modified

- `src/auth/login.ts` (234 lines)
- `src/auth/login.test.ts` (189 lines)
- `specs/business/authentication/login.md` (67 lines)
- `src/middleware/auth.ts` (45 lines)

## Test Results

```
✅ 12/12 tests passing
⏱️  Duration: 1.2s
📊 Coverage: 98.5%
```

## Next Steps

1. Implementar rate limiting (5 tentativas/min)
2. Adicionar logging de tentativas falhas
3. Testar em staging environment
4. Documentar API no Swagger

## Context State

- Tokens used: 98,456 (49.2%)
- Files in context: 18
- Conversation length: 47 messages
- Budget: 40,000 tokens (exceeded by 58,456)

## How to Resume

```bash
# Restaurar contexto completo
/engineer resume feat-login

# Ou manualmente
cd .claude/sessions/feat-login/latest/
cat CHECKPOINT.md
cat NOTES.md
```

## Team Handoff

Este checkpoint está pronto para handoff. Próximo dev pode:
1. Ler CHECKPOINT.md (5 min)
2. Ler NOTES.md (10 min)
3. Rodar testes (1 min)
4. Continuar do item "Next Steps"

Tempo estimado para contexto completo: **15-20 min**
```

## Implementação

### 1. Criar Estrutura

```bash
mkdir -p .claude/sessions/<feature>/checkpoint-<timestamp>/
```

### 2. Salvar Arquivos

```bash
# Compactar conversa
/context compact

# Copiar NOTES.md
cp NOTES.md .claude/sessions/<feature>/checkpoint-<timestamp>/

# Salvar lista de arquivos
echo '["src/auth/login.ts", "src/auth/login.test.ts", ...]' > files.json

# Copiar metaspecs
cp -r metaspecs/ .claude/sessions/<feature>/checkpoint-<timestamp>/
```

### 3. Gerar Resumo

Analise conversa e gere CHECKPOINT.md com:
- Executive summary (2-3 frases)
- Progress checklist
- Key decisions
- Files modified
- Test results
- Next steps
- Context state

### 4. Criar Symlink

```bash
ln -sf checkpoint-<timestamp> .claude/sessions/<feature>/latest
```

## Restaurar Checkpoint

```bash
# Command: /engineer resume <feature>

# Comportamento:
1. Ler .claude/sessions/<feature>/latest/CHECKPOINT.md
2. Carregar arquivos de files.json
3. Mostrar resumo executivo
4. Perguntar: "Continue from where we left off?"
```

## Dica Pro

**Checkpoint Periódico**:
```bash
# A cada feature concluída
/context checkpoint

# Ou a cada 50% de contexto
/context status  # 52% → Time to checkpoint!
/context checkpoint
```

**Colaboração**:
```bash
# Dev A
/context checkpoint
git add .claude/sessions/feat-login/
git commit -m "checkpoint: login endpoint done"
git push

# Dev B
git pull
/engineer resume feat-login
# Contexto completo restaurado! 🎉
```
