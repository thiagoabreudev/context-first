# Integrações - context-first

Esta pasta documenta todas as integrações externas via MCP (Model Context Protocol) e outras APIs.

---

## Integrações Ativas

### ✅ Linear (MCP)

**Status:** Conectado e Ativo
**Provider:** Linear MCP Server
**Documentação:** [linear.md](linear.md)

**Ferramentas:**
- `mcp__linear-server__search_teams` - Buscar teams
- `mcp__linear-server__create_issue` - Criar issue
- `mcp__linear-server__search_issues` - Buscar issues
- `mcp__linear-server__get_issue` - Detalhes de issue
- `mcp__linear-server__update_issue` - Atualizar issue

**Uso Típico:**
- Coletar ideias via `/collect` → cria issue no Linear
- Refinar issues via `/spec` → atualiza issue com PRD
- Listar backlog → busca issues pendentes

---

## Integrações Planejadas

### 🔄 GitHub (Planejado - Q1 2026)

**Status:** Não implementado
**Objetivo:** Criar PRs automaticamente via `/pr`

**Ferramentas Necessárias:**
- Criar branch
- Commit changes
- Criar PR com template

### 🔄 Anthropic Claude (API Direta)

**Status:** Planejado via Agno
**Objetivo:** Orquestrar agentes (Spec Writer, Architect, Coder, Reviewer)

**Ferramentas:**
- Agno framework (wrapper sobre Anthropic SDK)
- Multi-model strategy (Haiku/Sonnet/Opus)

### 🔄 Clerk (Auth)

**Status:** Planejado - MVP
**Objetivo:** Autenticação de usuários

**Integração:**
- Frontend: Clerk Vue SDK
- Backend: Verificação de tokens

---

## Como Adicionar Nova Integração

1. Criar arquivo `[integration-name].md` nesta pasta
2. Documentar:
   - Status (ativo/planejado)
   - Ferramentas disponíveis
   - Exemplos de uso
   - Workflows integrados
   - Troubleshooting
3. Atualizar este README
4. Adicionar referência em `/products/warm-up.md`

---

## Convenções

**Naming:**
- MCP tools: `mcp__[provider]__[action]`
- API wrappers: `api__[service]__[action]`

**Documentação:**
- Sempre incluir exemplos completos
- Documentar retornos esperados
- Listar troubleshooting comum

---

**Gerado com Metodologia CONTEXT-FIRST™**
