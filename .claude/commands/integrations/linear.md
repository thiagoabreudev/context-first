---
name: integrations-linear
description: Guia de integração com Linear via MCP
tools: mcp__linear-server__*
---

# Integração Linear via MCP - context-first

Este guia documenta como usar a integração Linear via MCP (Model Context Protocol) para gerenciar issues do projeto context-first.

---

## Status da Integração

✅ **MCP Linear Conectado e Ativo**

**Provider:** Linear MCP Server
**Team:** context-first
**Workspace:** _(configurar)_

---

## Ferramentas Disponíveis

### 1. Buscar Teams

**Tool:** `mcp__linear-server__search_teams`

```javascript
// Buscar team context-first
{
  query: "context-first"
}
```

**Retorna:**
- `team_id`: ID do team (usar em create_issue)
- `name`: Nome do team
- `key`: Prefixo das issues (ex: CF)

---

### 2. Criar Issue

**Tool:** `mcp__linear-server__create_issue`

```javascript
{
  title: "Título claro da issue (max 10 palavras)",
  description: "Descrição markdown completa com contexto",
  team_id: "<team_id>",
  priority: 2,  // 0=None, 1=Urgent, 2=High, 3=Medium, 4=Low
  labels: ["feature"],  // Opcional: ["feature", "bug", "improvement", "docs"]
  assignee_id: "<user_id>"  // Opcional
}
```

**Retorna:**
- `issue_id`: ID da issue criada
- `url`: URL da issue no Linear
- `identifier`: Identificador (ex: CF-123)

**Exemplo Completo:**
```javascript
{
  title: "Implementar Spec Writer Agent",
  description: `
# Spec Writer Agent

## Descrição
Implementar agente de IA especializado em gerar metaspecs seguindo metodologia SPARC+DD.

## Contexto
- Persona: Tech Lead, Developer
- Fase: MVP (Q4 2025)
- Stack: Agno + Claude Sonnet

## Requisitos Funcionais
- Gerar metaspec a partir de demand description
- Validar contra business rules (Jidoka)
- Streaming de output via WebSocket
- Context budget tracking

## Critérios de Aceitação
- [ ] Metaspec gerada em < 30s (P95)
- [ ] Validation accuracy > 85%
- [ ] Context budget respeitado
- [ ] Testes unitários (80% coverage)
  `,
  team_id: "abc123",
  priority: 2,  // High (MVP)
  labels: ["feature", "ai", "mvp"]
}
```

---

### 3. Buscar Issues

**Tool:** `mcp__linear-server__search_issues`

```javascript
{
  query: "spec writer",  // Busca por palavras-chave
  team_id: "<team_id>",  // Opcional: filtrar por team
  limit: 10  // Opcional: max resultados
}
```

**Retorna:** Lista de issues matching

**Casos de Uso:**
- Verificar se feature já foi criada
- Buscar issues relacionadas
- Listar backlog

---

### 4. Obter Issue

**Tool:** `mcp__linear-server__get_issue`

```javascript
{
  issue_id: "<issue_id>"
}
```

**Retorna:** Detalhes completos da issue (título, descrição, status, assignee, etc.)

---

### 5. Atualizar Issue

**Tool:** `mcp__linear-server__update_issue`

```javascript
{
  issue_id: "<issue_id>",
  title: "Novo título",  // Opcional
  description: "Nova descrição",  // Opcional
  state_id: "<state_id>",  // Opcional: Todo, In Progress, Done, etc.
  priority: 3,  // Opcional
  assignee_id: "<user_id>"  // Opcional
}
```

---

## Mapeamento de Prioridades

**Do Projeto → Linear:**

| Projeto | Emoji | Linear Priority | Valor |
|---------|-------|-----------------|-------|
| **Crítica (MVP)** | 🔴 | Urgent | `1` |
| **Alta (Fase 2)** | 🟡 | High | `2` |
| **Média (Fase 3)** | 🟢 | Medium | `3` |
| **Baixa (Backlog)** | ⚪ | Low | `4` |
| **Sem prioridade** | - | None | `0` |

---

## Labels Recomendados

**Por Tipo:**
- `feature` - Nova funcionalidade
- `bug` - Correção de bug
- `improvement` - Melhoria de feature existente
- `docs` - Documentação
- `tech-debt` - Dívida técnica
- `refactor` - Refactoring

**Por Área:**
- `frontend` - Frontend (Nuxt 3)
- `backend` - Backend (FastAPI)
- `ai` - AI/Agentes (Agno)
- `infra` - Infraestrutura
- `database` - MongoDB
- `api` - API REST/WebSocket

**Por Fase:**
- `mvp` - MVP (Q4 2025)
- `v1.1` - V1.1 (Q1 2026)
- `v2.0` - V2.0 (Q2-Q3 2026)

---

## Workflows Integrados

### Workflow 1: Coletar Nova Ideia

```bash
# Usuário
/collect Implementar dashboard de context budget

# Sistema (via comando /collect)
1. Faz perguntas de esclarecimento
2. Cria rascunho de issue
3. Obtém aprovação do usuário
4. Busca team_id via mcp__linear-server__search_teams
5. Cria issue via mcp__linear-server__create_issue
6. Retorna: "Issue criada: CF-123 (https://linear.app/...)"
```

### Workflow 2: Refinar Issue Existente

```bash
# Usuário
/spec CF-123

# Sistema
1. Busca issue via mcp__linear-server__get_issue
2. Lê descrição atual
3. Valida contra specs (business + technical)
4. Gera PRD completo
5. Atualiza issue via mcp__linear-server__update_issue
6. Adiciona PRD à descrição
```

### Workflow 3: Listar Backlog

```bash
# Usuário quer ver todas features pendentes

# Sistema
1. Busca issues via mcp__linear-server__search_issues
   query: "", team_id: "<context-first>", state: "Todo"
2. Agrupa por prioridade
3. Apresenta lista formatada
```

---

## Boas Práticas

### Títulos de Issues

✅ **BOM:**
- "Implementar Spec Writer Agent"
- "Corrigir validation loop no Jidoka"
- "Melhorar performance do dashboard"

❌ **RUIM:**
- "Fazer agente" (vago)
- "Bug no sistema" (não específico)
- "Implementar tudo da arquitetura" (escopo grande demais)

### Descrições de Issues

**Template Recomendado:**

```markdown
# [Título]

## Descrição
[2-3 parágrafos explicando o problema/feature]

## Contexto
- Persona: [CTO / Tech Lead / Developer]
- Fase: [MVP / V1.1 / V2.0]
- Stack: [Nuxt 3 / FastAPI / Agno / etc]

## Requisitos Funcionais
- [ ] Requisito 1
- [ ] Requisito 2

## Requisitos Não-Funcionais
- Performance: [target]
- Escalabilidade: [target]

## Critérios de Aceitação
- [ ] Critério 1
- [ ] Critério 2
- [ ] Testes (80% coverage)

## Links Relevantes
- Spec: `/specs/business/FEATURE_CATALOG.md#feature-x`
- ADR: `/specs/technical/adr/XXX.md`
```

---

## Troubleshooting

### Erro: Team não encontrado

```bash
# Buscar todos teams disponíveis
mcp__linear-server__search_teams
query: ""

# Verificar nome exato do team
```

### Erro: Priority inválida

```bash
# Valores válidos: 0, 1, 2, 3, 4
# Não usar strings ("high") ou outros números
```

### Issue criada mas não aparece

```bash
# Verificar se foi criada:
mcp__linear-server__search_issues
query: "<título da issue>"

# Verificar se está no team correto:
# Acessar Linear web interface
```

---

## Referências

- [Linear API Docs](https://developers.linear.app/docs)
- [MCP Linear Server](https://github.com/modelcontextprotocol/servers/tree/main/src/linear)
- [Linear Webhook Guide](https://developers.linear.app/docs/graphql/webhooks) (futuro)

---

**Gerado com Metodologia CONTEXT-FIRST™**
