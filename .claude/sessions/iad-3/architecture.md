# Arquitetura: IAD-3 - Monorepo Setup com Turborepo

> **Issue:** IAD-3
> **Tipo:** Infrastructure Architecture
> **Data:** 20 de Novembro de 2025

---

## Nota Importante

**Esta issue é sobre BUILD INFRASTRUCTURE, não aplicação.**

Os princípios de Clean Architecture (Domain → Application → Infrastructure) **não se aplicam aqui**, pois estamos configurando **build tooling** (Turborepo, PNPM, package structure), não código de negócio.

Clean Architecture será implementada **dentro** de `packages/backend/` nas issues:
- **IAD-6**: Domain Layer (entities, value objects)
- **IAD-7**: Application Layer (use cases, DTOs)
- **IAD-8**: Infrastructure Layer (MongoDB, Redis, S3)

---

## Visão Arquitetural

### Tipo de Arquitetura

**Monorepo com Turborepo** - Build system architecture para gerenciar múltiplos packages com dependências e builds coordenados.

### Decisão Formal

Conforme **ADR-001: Monorepo com Turborepo**:
- **Escolha**: Monorepo com Turborepo (Option C)
- **Alternativas rejeitadas**: Multi-repo (A), Monorepo sem tooling (B), Monorepo com Nx (D)
- **Justificativa**: Compartilhamento de código, atomic commits, cache inteligente, integração Vercel

---

## Estrutura de Packages

### Package Dependency Graph

```
┌──────────────────────────────────────────┐
│              Root (/)                    │
│  - Orchestrator                          │
│  - Scripts: dev, build, test, lint       │
└──────────────┬───────────────────────────┘
               │
       ┌───────┴────────┬──────────┬─────────┐
       │                │          │         │
  ┌────▼─────┐   ┌──────▼───┐  ┌──▼──────┐ ┌▼────────────┐
  │ frontend │   │ backend  │  │ shared  │ │ agno-agents │
  │  (Nuxt)  │   │(FastAPI) │  │  (Zod)  │ │  (Python)   │
  └────┬─────┘   └────┬─────┘  └─────────┘ └─────────────┘
       │              │
       │              │
       ▼              ▼
    shared      agno-agents
```

**Dependency Rules:**
- ✅ `frontend` → `shared` (importa types)
- ✅ `backend` → `agno-agents` (importa agents)
- ❌ `backend` → `shared` (duplicação intencional, sem import)
- ❌ Circular dependencies (quebram build)
- ❌ `frontend` → `backend` (violaria separação)

### Package Responsibilities

| Package | Linguagem | Framework | Responsabilidade | Dependências |
|---------|-----------|-----------|------------------|--------------|
| `frontend` | TypeScript | Nuxt 3 | UI, client-side logic | `shared` |
| `backend` | Python | FastAPI | API, business logic | `agno-agents` |
| `shared` | TypeScript | Zod | Schemas, types | None |
| `agno-agents` | Python | Agno | AI agents | None (leaf) |

---

## Turborepo Pipeline

### Pipeline Tasks

Definidos em `turbo.json`:

```json
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".nuxt/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    }
  }
}
```

**Task Explanations:**

1. **`dev`**: Development servers
   - `cache: false` (live reload não deve cachear)
   - `persistent: true` (processo long-running)
   - Executado via `concurrently` no root

2. **`build`**: Production builds
   - `dependsOn: ["^build"]` (build dependencies primeiro)
   - `outputs`: Arquivos gerados (para cache)
   - Turborepo cacheia automaticamente

3. **`test`**: Test suites
   - `dependsOn: ["build"]` (testa código compilado)
   - `outputs`: Coverage reports

4. **`lint`**: Linting/formatting
   - Sem outputs (validação apenas)
   - Rápido, sem dependências

### Task Execution Order

Quando rodar `pnpm build`:

```
1. turbo build
2. ├─ shared (build primeiro, é dependency)
3. ├─ agno-agents (build primeiro, é dependency)
4. ├─ frontend (build após shared)
5. └─ backend (build após agno-agents)
```

Turborepo executa **shared** e **agno-agents** em paralelo (não dependem um do outro), depois **frontend** e **backend** em paralelo.

---

## PNPM Workspaces

### Workspace Configuration

**pnpm-workspace.yaml:**
```yaml
packages:
  - 'packages/*'
```

**Root package.json:**
```json
{
  "name": "context-first",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "concurrently \"pnpm dev:frontend\" \"pnpm dev:backend\"",
    "dev:frontend": "pnpm --filter frontend dev",
    "dev:backend": "cd packages/backend && source venv/bin/activate && uvicorn src.main:app --reload",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint"
  }
}
```

### Workspace Features

1. **Hoisting**: Dependencies compartilhadas hoisted para root `node_modules/`
2. **Linking**: Packages locais linkados automaticamente (ex: `frontend` acessa `shared`)
3. **Filtering**: `pnpm --filter <package>` executa comandos em package específico
4. **Isolation**: Cada package tem seu próprio `package.json` e dependencies

---

## Package Structures

### 1. packages/frontend/ (Nuxt 3)

```
frontend/
├── package.json        # Dependencies: nuxt, vue, typescript, shared
├── nuxt.config.ts      # Nuxt config (minimal)
├── tsconfig.json       # Extends tsconfig.base.json
├── app.vue             # Root component (minimal)
└── [estrutura Nuxt]    # (será criada em IAD-9)
```

**package.json:**
```json
{
  "name": "frontend",
  "type": "module",
  "scripts": {
    "dev": "nuxt dev",
    "build": "nuxt build",
    "lint": "eslint ."
  },
  "dependencies": {
    "nuxt": "^3.x",
    "vue": "^3.x",
    "shared": "workspace:*"
  },
  "devDependencies": {
    "@nuxtjs/tailwindcss": "^6.x",
    "typescript": "^5.x"
  }
}
```

**Dependency Explanation:**
- `"shared": "workspace:*"`: PNPM resolve para `packages/shared/` local

### 2. packages/backend/ (FastAPI)

```
backend/
├── src/
│   ├── main.py         # FastAPI entry (minimal)
│   ├── domain/         # (empty, criado em IAD-6)
│   ├── application/    # (empty, criado em IAD-7)
│   ├── infrastructure/ # (empty, criado em IAD-8)
│   └── interfaces/     # (empty, criado em IAD-8)
├── requirements.txt    # Python dependencies
├── pyproject.toml      # (opcional, para black/ruff config)
├── venv/               # Python virtual environment
└── .gitignore          # venv/, __pycache__
```

**requirements.txt:**
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.0
# agno-agents será instalado via pip install -e ../agno-agents
```

**Dependency Management:**
- Python dependencies em `requirements.txt` (não gerenciado por PNPM)
- `agno-agents` instalado como editable package: `pip install -e ../agno-agents`

### 3. packages/shared/ (Zod Schemas)

```
shared/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts        # Re-exports
│   └── schemas/
│       ├── demand.ts   # (empty structure)
│       ├── project.ts  # (empty structure)
│       └── metaspec.ts # (empty structure)
└── dist/               # Compiled output (gitignored)
```

**package.json:**
```json
{
  "name": "shared",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "lint": "eslint src/"
  },
  "dependencies": {
    "zod": "^3.x"
  },
  "devDependencies": {
    "typescript": "^5.x"
  }
}
```

**Build Output:**
- TypeScript compila `src/` → `dist/`
- `frontend` importa de `shared` (já compilado)

### 4. packages/agno-agents/ (Python Package)

```
agno-agents/
├── setup.py            # Python package setup
├── agno_agents/
│   ├── __init__.py     # Package exports
│   ├── spec_writer/    # (empty structure)
│   ├── architect/      # (empty structure)
│   ├── coder/          # (empty structure)
│   └── reviewer/       # (empty structure)
└── requirements.txt    # agno, anthropic
```

**setup.py:**
```python
from setuptools import setup, find_packages

setup(
    name="agno-agents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "agno>=0.x",
        "anthropic>=0.x",
    ],
)
```

**Usage in Backend:**
```python
# packages/backend/src/infrastructure/ai/agents.py
from agno_agents.spec_writer import SpecWriterAgent

agent = SpecWriterAgent()
```

---

## Development Workflow

### Local Development

**Setup (uma vez):**
```bash
# 1. Clone repo
git clone <repo> && cd context-first

# 2. Install Node dependencies
pnpm install

# 3. Setup Python backend
cd packages/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Setup agno-agents (editable)
pip install -e ../agno-agents
```

**Daily Development:**
```bash
# Root do monorepo
pnpm dev  # Roda frontend + backend simultaneamente
```

**Detalhes do `pnpm dev`:**
```bash
# Internamente executa (via concurrently):
# Terminal 1: pnpm --filter frontend dev
# Terminal 2: cd packages/backend && uvicorn src.main:app --reload
```

**URLs de Desenvolvimento:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### Build Workflow

```bash
# Build todos packages
pnpm build

# Turborepo executa:
# 1. shared: tsc (TS → JS)
# 2. agno-agents: (nenhum build, Python)
# 3. frontend: nuxt build (após shared built)
# 4. backend: (nenhum build específico, Python runtime)
```

### Testing Workflow

```bash
# Rodar testes (quando implementados em issues futuras)
pnpm test

# Por package:
pnpm --filter frontend test
pnpm --filter backend test
```

### Linting Workflow

```bash
# Lint todos packages
pnpm lint

# Por linguagem:
pnpm --filter frontend lint  # ESLint (TS/Vue)
cd packages/backend && ruff check .  # Ruff (Python)
```

---

## Configuration Files

### 1. turbo.json (Root)

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true
    },
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".nuxt/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    }
  }
}
```

### 2. pnpm-workspace.yaml (Root)

```yaml
packages:
  - 'packages/*'
```

### 3. tsconfig.base.json (Root)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  }
}
```

Packages estendem: `"extends": "../../tsconfig.base.json"`

### 4. .eslintrc.js (Root)

```js
module.exports = {
  root: true,
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  env: {
    node: true,
    es2022: true
  }
}
```

### 5. .prettierrc (Root)

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2
}
```

### 6. .gitignore (Root)

```
# Dependencies
node_modules/
pnpm-lock.yaml

# Build outputs
dist/
.nuxt/
build/

# Python
venv/
__pycache__/
*.pyc
.pytest_cache/

# Env
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## Decisões de Design

### 1. Schema Duplication (TS + Python)

**Decisão**: Duplicar schemas em vez de codegen (por enquanto)

**Trade-offs:**
- ❌ **Contra**: Duplicação de código, risco de dessincronia
- ✅ **Pró**: Simplicidade, zero tooling extra, MVP mais rápido

**Timing**: Codegen automático (zod-to-pydantic) será adicionado em **Phase 2** (post-MVP)

**Implementação Atual:**
```typescript
// packages/shared/src/schemas/demand.ts
export const DemandSchema = z.object({
  id: z.string(),
  title: z.string(),
  // ...
})
```

```python
# packages/backend/src/domain/entities/demand.py
from pydantic import BaseModel

class Demand(BaseModel):
    id: str
    title: str
    # ...
```

### 2. Agno-agents como Library (não Microservice)

**Decisão**: Python package importável pelo backend

**Trade-offs:**
- ❌ **Contra**: Acoplamento, deploy único
- ✅ **Pró**: Simplicidade, zero latência de rede, debugging fácil

**Implementação:**
```python
# Backend importa agents diretamente
from agno_agents.spec_writer import SpecWriterAgent

agent = SpecWriterAgent()
result = await agent.run(prompt)
```

**Futuro (se necessário)**: Se agentes precisarem escalar independentemente, extrair para microservice em **V2.0**.

### 3. Concurrently para Dev Scripts

**Decisão**: Usar `concurrently` para rodar front + back simultaneamente

**Trade-offs:**
- ❌ **Contra**: Menos features que Turborepo daemon ou Docker Compose
- ✅ **Pró**: Simples, funciona, zero learning curve

**Implementação:**
```json
{
  "scripts": {
    "dev": "concurrently \"pnpm dev:frontend\" \"pnpm dev:backend\""
  }
}
```

**Alternativas Consideradas:**
- Turborepo `--parallel`: Não suporta Python bem
- Docker Compose: Overhead de Docker, setup complexo para MVP

### 4. Cache Remoto Vercel: Phase 2

**Decisão**: Não configurar cache remoto no MVP

**Justificativa:**
- Cache local Turborepo funciona out-of-the-box
- Cache remoto só vale a pena com CI/CD configurado (IAD-19, IAD-20)
- MVP: Desenvolvimento local apenas (1-2 devs)

**Timing**: Configurar em **Phase 2** junto com CI/CD

---

## Validação Arquitetural

### ✅ Alinhamento com ADR-001

| Critério ADR-001 | Status | Notas |
|------------------|--------|-------|
| Monorepo com Turborepo | ✅ | Implementado conforme decisão |
| PNPM workspaces | ✅ | Configurado em `pnpm-workspace.yaml` |
| Estrutura de 4 packages | ✅ | frontend, backend, shared, agno-agents |
| Cache inteligente | ✅ | Turborepo local cache habilitado |
| Scripts unificados | ✅ | `pnpm dev`, `pnpm build`, etc. |

### ✅ Dependency Graph Válido

```
shared (leaf) ←─── frontend
agno-agents (leaf) ←─── backend
```

- Sem dependências circulares ✅
- Frontend não acessa backend ✅
- Packages leaf sem dependencies ✅

### ✅ MVP Philosophy: Start Simple

| Princípio | Implementação |
|-----------|---------------|
| Simplicidade | Concurrently, schemas duplicados |
| Funcionalidade | `pnpm dev` roda tudo, hot reload |
| Extensibilidade | Estrutura preparada para Fase 2 (codegen, cache remoto) |

---

## Próximos Passos (Outras Issues)

Esta issue cria a **fundação**. Features serão implementadas nas próximas issues:

1. **IAD-6**: Domain Layer (backend) - Entities, Value Objects
2. **IAD-7**: Application Layer (backend) - Use Cases, DTOs
3. **IAD-8**: Infrastructure Layer (backend) - MongoDB, Redis, S3
4. **IAD-9**: Frontend Base Setup - Nuxt pages, components, stores
5. **IAD-11**: Shared Schemas - Zod schemas reais (Demand, Project, Metaspec)
6. **IAD-12**: Agno Agents - Spec Writer, Architect, Coder, Reviewer

---

## Glossário

- **Monorepo**: Repositório único contendo múltiplos packages relacionados
- **Workspace**: Package individual dentro do monorepo (managed by PNPM)
- **Turborepo**: Build orchestrator que otimiza execução de tasks em monorepo
- **PNPM**: Package manager que suporta workspaces nativamente
- **Pipeline**: Configuração de tasks e dependências em Turborepo
- **Hoisting**: Mover dependencies compartilhadas para root `node_modules/`
- **Editable Install**: `pip install -e` instala package em modo dev (changes refletem imediatamente)

---

**Documento criado por:** Claude (Engineer Agent)
**Revisado por:** _(pending human review)_
**Última atualização:** 20 de Novembro de 2025
