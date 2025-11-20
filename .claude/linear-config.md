# Configuração do Linear - IA do Jeito Certo

Este documento contém as informações de configuração do Linear para o projeto **iadojeitocerto.com.br**.

## Informações do Projeto

- **Nome do Team**: iadojeitocerto
- **Team ID**: `2b1273da-f961-407a-b0f5-4047378ecb4d`
- **Team Key**: IADJ (issues terão formato IADJ-1, IADJ-2, etc.)
- **Criado em**: 2025-11-17

## MCP do Linear

O MCP do Linear está **configurado e ativo**. Não é necessário usar API keys ou credenciais no `.env`. Use as ferramentas MCP diretamente:

- `mcp__linear-server__create_issue`
- `mcp__linear-server__update_issue`
- `mcp__linear-server__get_issue`
- `mcp__linear-server__list_issues`
- `mcp__linear-server__create_comment`
- E outras (veja seção "MCP Tools Disponíveis" abaixo)

## MCP Tools Disponíveis

### Issues

#### Listar Issues
```
mcp__linear-server__list_issues
```
Parâmetros úteis:
- `project`: "IA do Jeito Certo" ou ID `82c382fe-1bf3-45c9-9352-b17c1cd3a8a8`
- `assignee`: "me" para suas issues
- `state`: Filtrar por status
- `orderBy`: "createdAt" ou "updatedAt"

#### Criar Issue
```
mcp__linear-server__create_issue
```
Parâmetros obrigatórios:
- `title`: Título da issue
- `team`: `2b1273da-f961-407a-b0f5-4047378ecb4d` (iadojeitocerto)

Parâmetros recomendados:
- `description`: Descrição completa em Markdown
- `project`: "IA do Jeito Certo" ou ID do projeto
- `priority`: 0 (None), 1 (Urgent), 2 (High), 3 (Normal), 4 (Low)
- `labels`: Array de labels (pode usar nomes diretamente)

#### Ler Issue
```
mcp__linear-server__get_issue
```
Parâmetro:
- `id`: ID da issue

#### Atualizar Issue
```
mcp__linear-server__update_issue
```
Parâmetros:
- `id`: ID da issue (obrigatório)
- `title`: Novo título
- `description`: Nova descrição
- `state`: Novo estado
- `priority`: Nova prioridade
- `labels`: Novos labels

### Comentários

#### Listar Comentários
```
mcp__linear-server__list_comments
```
Parâmetro:
- `issueId`: ID da issue

#### Criar Comentário
```
mcp__linear-server__create_comment
```
Parâmetros:
- `issueId`: ID da issue
- `body`: Conteúdo do comentário em Markdown

### Labels

#### Listar Labels
```
mcp__linear-server__list_issue_labels
```
Parâmetros opcionais:
- `team`: ID do time para filtrar
- `name`: Filtrar por nome

#### Criar Label
```
mcp__linear-server__create_issue_label
```
Parâmetros:
- `name`: Nome do label
- `color`: Código hex da cor
- `teamId`: ID do time (opcional, se não especificado cria workspace label)

## Workflow Recomendado

### Fase de Especificação (Product)

1. **Coletar Ideia** (`/collect`):
   - Criar issue no Linear com título e descrição básica
   - Team: `2b1273da-f961-407a-b0f5-4047378ecb4d` (iadojeitocerto)
   - Labels recomendados: `["feature", "needs-refinement"]`

2. **Refinar Requisito** (`/refine`):
   - Ler issue do Linear com `get_issue`
   - Atualizar descrição com detalhamento completo
   - Atualizar labels: `["feature", "refined"]`

3. **Criar PRD** (`/spec`):
   - Ler issue refinada
   - Atualizar com PRD completo (template estruturado)
   - Atualizar labels: `["feature", "spec-ready"]`
   - Mover para status: "Ready for Development" (ou equivalente)

### Fase de Desenvolvimento (Engineer)

1. **Iniciar Desenvolvimento** (`/start`):
   - Ler issue com PRD usando `get_issue`
   - Criar branch de feature
   - Atualizar status para "In Progress"
   - Adicionar comentário com link da branch

2. **Durante Desenvolvimento** (`/work`):
   - Adicionar comentários com progresso usando `create_comment`

3. **Code Review** (`/review`, `/pre-pr`):
   - Atualizar labels: `["in-review"]`

4. **Pull Request** (`/pr`):
   - Adicionar comentário com link do PR
   - Atualizar labels: `["pr-open"]`

5. **Deploy** (`/deploy`):
   - Atualizar status para "Done"
   - Atualizar labels: `["deployed"]`
   - Adicionar comentário com link de produção

## Labels Recomendados

Crie estes labels no workspace ou time usando `create_issue_label`:

### Por Fase
- `needs-refinement` - Precisa ser refinado
- `refined` - Requisito refinado
- `spec-ready` - PRD completo
- `in-review` - Em revisão de código
- `pr-open` - Pull request aberto
- `deployed` - Em produção

### Por Tipo
- `feature` - Nova funcionalidade
- `enhancement` - Melhoria de feature existente
- `bug` - Correção de bug
- `tech-debt` - Débito técnico
- `docs` - Documentação

### Por Prioridade
- `mvp` - Fase MVP
- `phase-2` - Fase 2
- `phase-3` - Fase 3

### Por Área
- `frontend` - Frontend (Vue/Nuxt)
- `backend` - Backend/API
- `design` - Design/UX
- `seo` - SEO
- `performance` - Performance
- `accessibility` - Acessibilidade

## Exemplo Completo: Criando Issue com Labels

```markdown
# Exemplo: Criar nova feature

1. Criar issue base com `mcp__linear-server__create_issue`:
   - title: "Adicionar formulário de contato"
   - team: "2b1273da-f961-407a-b0f5-4047378ecb4d"
   - description: "Descrição inicial..."
   - labels: ["feature", "needs-refinement", "mvp"]

2. Após refinamento, atualizar com `mcp__linear-server__update_issue`:
   - description: "Descrição refinada com detalhes..."
   - labels: ["feature", "refined", "mvp"]

3. Após criar PRD:
   - description: "PRD completo..."
   - labels: ["feature", "spec-ready", "mvp"]
   - state: "Ready for Development"

4. Iniciar desenvolvimento:
   - state: "In Progress"
   - Adicionar comentário com branch usando `mcp__linear-server__create_comment`

5. Finalizar:
   - state: "Done"
   - labels: ["feature", "deployed", "mvp"]
   - Adicionar comentário com link de produção
```

## Integração com SPARC+DD

O Linear serve como **fonte de verdade** para rastreamento de features:

- **S (Specification)**: Issues com labels de refinamento (`needs-refinement`, `refined`, `spec-ready`)
- **P (PseudoCode)**: Comentários na issue com pseudocódigo
- **A (Architecture)**: Comentários ou anexos com decisões arquiteturais
- **R (Refinement)**: Plano de execução em `.claude/sessions/` + comentários no Linear
- **C (Completion)**: Progresso via comentários, commits linkados
- **D (Deployment)**: Status "Done" + label `deployed`
- **D (Documentation)**: Docs atualizados e linkados na issue

## Troubleshooting

### Erro: "Team not found"
- Use o Team ID: `2b1273da-f961-407a-b0f5-4047378ecb4d`
- Ou use o nome: "iadojeitocerto"

### Labels não aparecem
- Crie labels primeiro com `mcp__linear-server__create_issue_label`
- Ou use labels existentes do workspace

## Referências

- [Linear MCP Documentation](https://github.com/modelcontextprotocol/servers/tree/main/src/linear)
- [Linear API Docs](https://developers.linear.app/docs)
- [Team no Linear](https://linear.app/iadojeitocerto)

---

**Última Atualização**: 2025-11-17
**Projeto**: iadojeitocerto.com.br
