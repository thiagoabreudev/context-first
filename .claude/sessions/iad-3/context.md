# Contexto: IAD-3 - Setup de Monorepo com Turborepo

> **Issue:** IAD-3
> **Título:** Configurar estrutura de monorepo com Turborepo + PNPM workspaces
> **Tipo:** Infrastructure Setup
> **Prioridade:** P0 (Bloqueador)
> **Status:** In Progress
> **Engenheiro:** Claude
> **Data de Início:** 20 de Novembro de 2025

---

## Por Que Esta Tarefa Existe?

### Problema de Negócio

O projeto context-first está iniciando do zero e precisa de uma base sólida de infraestrutura de código antes que qualquer funcionalidade possa ser desenvolvida. Atualmente:

- **Não existe estrutura de código**: Apenas arquivos .claude/ e specs/
- **Impossível desenvolver features**: Sem packages organizados, build system, ou dev environment
- **Bloqueio total**: Todas as outras 17 issues (IAD-4 a IAD-20) dependem desta estrutura

### Valor de Negócio

**Redução de 40% em context switching** entre repositórios, possibilitando:
- **Time-to-market 30% mais rápido** (atomic commits em vez de PRs coordenados entre repos)
- **Onboarding < 30 minutos** (vs 4+ horas com multi-repo)
- **Zero incidentes de dessincronia de schemas** (compartilhamento automático)

**Métricas de Sucesso (definidas em ADR-001):**
- Build time de CI < 5 minutos (com cache)
- Onboarding de novo dev < 30 minutos
- Zero incidentes de dessincronia de schemas (6 meses)

### Persona Alvo

**Developer** (interno): Tech lead e desenvolvedores do time context-first que precisarão trabalhar no código diariamente.

### Fase do Produto

**MVP - Fase 0 (Foundational Infrastructure)**: Esta é a primeira tarefa técnica do projeto, sem a qual nenhuma outra pode começar.

---

## O Que Precisa Ser Construído?

### Resultado Final Esperado

Um monorepo funcional com:

```
context-first/
├── packages/
│   ├── frontend/           # Nuxt 3 app (pronto para IAD-9)
│   ├── backend/            # FastAPI app (pronto para IAD-6)
│   ├── shared/             # Schemas Zod/TS (pronto para IAD-11)
│   └── agno-agents/        # Python package (pronto para IAD-12)
├── turbo.json              # Turborepo pipeline config
├── package.json            # Root com workspaces e scripts
├── pnpm-workspace.yaml     # PNPM workspaces config
└── [configs]               # ESLint, Prettier, tsconfig
```

### Componentes Principais

1. **Root Configuration**
   - `package.json`: Monorepo root, workspaces definition, shared scripts
   - `pnpm-workspace.yaml`: PNPM workspaces configuration
   - `turbo.json`: Build pipeline (tasks: dev, build, test, lint)
   - `.gitignore`: Ignorar node_modules, dist, venv, etc.

2. **Package: frontend/**
   - Nuxt 3 app scaffold (minimal, sem features ainda)
   - `package.json` com dependencies: nuxt, vue, typescript, tailwindcss
   - Depende de: `shared` package

3. **Package: backend/**
   - FastAPI structure scaffold (empty domain/application/infrastructure layers)
   - Python venv + `requirements.txt`
   - Depende de: `agno-agents` package

4. **Package: shared/**
   - Schemas em Zod/TypeScript (schemas vazios, estrutura apenas)
   - Exporta types para frontend

5. **Package: agno-agents/**
   - Python package structure (empty agents, imports apenas)
   - `setup.py` ou `pyproject.toml`
   - Importável pelo backend

6. **Development Tooling**
   - ESLint config (shared)
   - Prettier config (shared)
   - TypeScript config base (tsconfig.base.json)
   - Dev scripts usando `concurrently`

### Nível de Atomic Design

**N/A** - Esta é tarefa de **build infrastructure**, não de componentes UI.

### Integrações

**Nenhuma integração externa nesta fase**. Apenas setup de build tooling local.

---

## Como Será Implementado?

### Stack Tecnológica Aprovada

Conforme **ADR-001: Monorepo com Turborepo**, usando:
- **Turborepo**: Build orchestration e caching
- **PNPM**: Package manager (workspaces)
- **TypeScript**: Frontend + shared
- **Python 3.11+**: Backend + agno-agents
- **Nuxt 3**: Frontend framework
- **FastAPI**: Backend framework

### Padrões Arquiteturais

**Monorepo Best Practices:**
- Workspaces isolados com dependências explícitas
- Scripts root que orquestram packages (`pnpm dev`, `pnpm build`)
- Turborepo pipeline para otimização de builds
- Dependency graph claro:
  ```
  frontend → shared
  backend → agno-agents
  (circular dependencies proibidas)
  ```

**Simplicity First (MVP Philosophy):**
- Schema sharing: Duplicated (TS + Python) - sem codegen ainda
- Dev scripts: `concurrently` - sem complexidade extra
- Tooling mínimo: Apenas ESLint/Prettier - sem Husky/Lint-staged ainda

### Dependências

**NPM Packages (Root + Frontend):**
- `turbo`: ^2.x (latest)
- `concurrently`: ^9.x
- `nuxt`: ^3.x
- `vue`: ^3.x
- `typescript`: ^5.x
- `@nuxtjs/tailwindcss`: ^6.x
- `zod`: ^3.x (shared)
- `eslint`: ^9.x
- `prettier`: ^3.x

**Python Packages (Backend + Agno):**
- `fastapi`: ^0.115.x
- `uvicorn[standard]`: ^0.32.x
- `pydantic`: ^2.x
- `agno`: Latest (from pip)
- `pytest`: ^8.x
- `black`: ^24.x
- `ruff`: ^0.8.x

### Testing

**N/A para esta issue** - Build configuration não tem testes unitários. Validação será:
- ✅ `pnpm install` roda sem erros
- ✅ `pnpm dev` sobe frontend + backend
- ✅ `pnpm build` compila com sucesso
- ✅ `pnpm lint` valida código

---

## Validação Contra Metaspecs

### ✅ visao-produto.md
Alinha com visão de "usar mesma metodologia para construir a plataforma" - setup estruturado e documentado.

### ✅ perfil-cliente.md
Tooling interno para desenvolvedores do time (target persona: Developer).

### ✅ features-valores.md
Feature foundational que habilita todas as outras. Sem monorepo, nenhuma feature pode ser implementada.

### ✅ stack-tecnologica.md
Usa exatamente a stack aprovada: Turborepo, PNPM, Nuxt 3, FastAPI, Python, TypeScript.

### ⚠️ arquitetura.md
**Não aplicável nesta issue** - Clean Architecture (domain/application/infrastructure) será implementada nas issues de aplicação (IAD-6, IAD-7, IAD-8). Esta issue é apenas build tooling.

### ✅ problemas-conhecidos.md
Nenhum conflito detectado. Problemas conhecidos são sobre aplicação (WebSocket, MongoDB, etc), não sobre build tooling.

---

## Decisões Arquiteturais Documentadas

Todas as decisões desta issue já foram formalizadas em:
- **ADR-001**: Monorepo com Turborepo (vs multi-repo, vs Nx)

**Decisões específicas tomadas no refinamento:**

1. **Schema Sharing Strategy**: Duplicated (Option D)
   - **Trade-off**: Duplicação vs simplicidade
   - **Decisão**: Duplicar schemas (Zod em TS, Pydantic em Python) por enquanto
   - **Timing**: Codegen automático será adicionado em Phase 2 (post-MVP)

2. **Agno-agents Package**: Python library (Option B)
   - **Trade-off**: Separar como serviço vs biblioteca
   - **Decisão**: Python package importável pelo backend
   - **Justificativa**: Simplicidade, zero overhead de rede, deploy único

3. **Dev Scripts**: Concurrently (Option A)
   - **Trade-off**: Concurrently vs Turborepo daemon vs Docker Compose
   - **Decisão**: `concurrently` para rodar front + back em paralelo
   - **Justificativa**: Simples, funciona, zero complexidade extra

4. **Cache Remoto Vercel**: Phase 2
   - **Timing**: Não essencial para MVP, adicionar quando CI/CD estiver pronto

5. **Package Dependencies**:
   - ✅ frontend → shared (compartilhar types)
   - ✅ backend → agno-agents (importar agents)
   - ❌ backend → shared (duplicação intencional)
   - ❌ frontend → backend (violaria isolamento)
   - ❌ circular dependencies (quebra build)

6. **Additional Tooling**: Minimal
   - ✅ ESLint + Prettier: Sim (código limpo desde início)
   - ❌ Husky + Lint-staged: Phase 2 (não essencial para MVP)

---

## Checklist de Implementação

Conforme especificado no refinamento IAD-3:

### Phase 1: Root Setup
- [ ] 1. Criar `package.json` root com workspaces
- [ ] 2. Criar `pnpm-workspace.yaml`
- [ ] 3. Criar `turbo.json` com pipelines (dev, build, test, lint)
- [ ] 4. Criar `.gitignore` (node_modules, dist, venv, .env)

### Phase 2: Package Scaffolding
- [ ] 5. Scaffold `packages/frontend/` (Nuxt 3 minimal)
- [ ] 6. Scaffold `packages/backend/` (FastAPI structure)
- [ ] 7. Scaffold `packages/shared/` (Zod schemas structure)
- [ ] 8. Scaffold `packages/agno-agents/` (Python package)

### Phase 3: Development Environment
- [ ] 9. Configurar scripts de desenvolvimento (`pnpm dev` com concurrently)
- [ ] 10. Configurar ESLint + Prettier (shared configs)
- [ ] 11. Criar README.md root com instruções de setup

### Phase 4: Validation
- [ ] 12. Rodar `pnpm install` e verificar workspaces
- [ ] 13. Rodar `pnpm dev` e verificar hot reload
- [ ] 14. Rodar `pnpm build` e verificar output
- [ ] 15. Rodar `pnpm lint` e verificar sem erros

---

## Critérios de Aceitação

Conforme definido no refinamento:

1. ✅ **Estrutura completa criada**: 4 packages + root configs existem
2. ✅ **PNPM workspaces funcionando**: `pnpm install` detecta todos packages
3. ✅ **Turborepo configurado**: `turbo.json` com tasks (dev, build, test, lint)
4. ✅ **Frontend scaffold**: Nuxt 3 app mínima rodando em http://localhost:3000
5. ✅ **Backend scaffold**: FastAPI app mínima rodando em http://localhost:8000
6. ✅ **Shared package**: Estrutura de schemas criada, exportando types
7. ✅ **Agno-agents package**: Python package importável pelo backend
8. ✅ **Dev scripts**: `pnpm dev` roda front + back simultaneamente
9. ✅ **Build funcional**: `pnpm build` compila frontend + backend sem erros
10. ✅ **Linting configurado**: `pnpm lint` valida TypeScript/Python
11. ✅ **Documentação**: README.md root com setup instructions

---

## Riscos e Mitigações

### Risco 1: PNPM Workspaces Não Detectam Packages
**Probabilidade**: Baixa
**Impacto**: Alto (bloqueador)
**Mitigação**: Seguir exatamente a estrutura documentada no ADR-001. Validar com `pnpm list --depth=0` após setup.

### Risco 2: Turborepo Cache Não Funciona Localmente
**Probabilidade**: Média
**Impacto**: Baixo (apenas performance, não bloqueador)
**Mitigação**: Turborepo local cache funciona out-of-the-box. Cache remoto (Vercel) fica para Phase 2.

### Risco 3: Python venv Conflita com Node Modules
**Probabilidade**: Baixa
**Impacto**: Médio
**Mitigação**: `.gitignore` correto + documentação clara sobre setup (Python venv dentro de `packages/backend/`, Node modules gerenciados por PNPM).

---

## Questões Pendentes (do Refinamento)

**Todas as questões foram respondidas no refinamento anterior.** Nenhuma pendência restante.

---

## Referências

- **ADR-001**: [Monorepo com Turborepo](../../context-first-metaspecs/specs/technical/adr/001-monorepo-structure.md)
- **CODEBASE_GUIDE.md**: [Estrutura de código esperada](../../context-first-metaspecs/specs/technical/CODEBASE_GUIDE.md)
- **Issue Linear**: IAD-3

---

**Documento criado por:** Claude (Engineer Agent)
**Revisado por:** _(pending human review)_
**Última atualização:** 20 de Novembro de 2025
