---
name: context-compact
description: Compactar contexto resumindo conversa em NOTES.md
tools: None
---

# Context Compact

Resume a conversa atual em um arquivo `NOTES.md`, liberando espaço no contexto sem perder informações importantes.

## Quando Usar

- ✅ Contexto atingiu **40-60%**
- ✅ Conversa ficou muito longa
- ✅ Muitas idas e voltas sobre o mesmo tópico
- ✅ Antes de começar uma nova sub-feature

## Comportamento

1. **Analisar** toda a conversa atual
2. **Extrair** decisões, problemas resolvidos, e próximos passos
3. **Resumir** em formato estruturado
4. **Salvar** em `NOTES.md` (ou `.claude/sessions/<feature>/NOTES.md`)
5. **Limpar** histórico de conversa (mantendo apenas últimas 3-5 mensagens)

## Output

```
🗜️  CONTEXT COMPACTION

BEFORE:
  Total tokens: 68,450 (34.2%)
  Conversation: 42,300 tokens
  Files: 26,150 tokens

AFTER:
  Total tokens: 31,200 (15.6%)
  Conversation: 5,050 tokens (compacted!)
  Files: 26,150 tokens

SAVED: 37,250 tokens (18.6%)

Summary saved to: NOTES.md

✅ Context compacted successfully!
   Continue working normally.
```

## Formato do NOTES.md

```markdown
# Session Notes - feat-login

**Last Updated**: 2025-11-14 10:45

## Decisões Tomadas

1. **Autenticação**: JWT com refresh token
   - Access token: 15min
   - Refresh token: 7 dias
   - Armazenamento: httpOnly cookies

2. **Validação**: Zod no frontend + backend
   - Email: formato válido
   - Senha: min 8 chars, 1 upper, 1 number

## Problemas Resolvidos

1. **CORS Error**: Configurado `credentials: 'include'`
2. **Token Expiration**: Implementado auto-refresh
3. **Test Flakiness**: Mockado Date.now() nos testes

## Arquivos Modificados

- `src/auth/login.ts` - Endpoint implementado
- `src/auth/login.test.ts` - 12 testes passando
- `metaspecs/business/authentication/login.md` - Spec atualizada

## Próximos Passos

- [ ] Implementar logout endpoint
- [ ] Adicionar rate limiting (5 tentativas/min)
- [ ] Testar em staging

## Contexto Técnico

- Stack: Node.js + Express + Prisma
- DB: PostgreSQL
- Auth: JWT (jsonwebtoken)
- Tests: Vitest
```

## Implementação

1. **Ler** toda a conversa atual
2. **Identificar** padrões:
   - "Vamos fazer X" → Decisão
   - "Erro: Y" + "Resolvido com Z" → Problema resolvido
   - "Próximo: W" → Próximo passo
3. **Estruturar** em seções
4. **Salvar** em NOTES.md
5. **Referenciar** NOTES.md automaticamente no contexto

## Dica Pro

Após compactar, adicione no início da próxima mensagem:

```
📝 Context compacted! Summary in NOTES.md

Continue from where we left off:
- Last completed: Login endpoint tests passing
- Next: Implement logout endpoint
```
