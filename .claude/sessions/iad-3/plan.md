# IAD-3: Setup de Monorepo com Turborepo

**Importante**: Atualize este arquivo conforme progride na implementação.

---

## FASE 1: Root Configuration (Build System) [Em Progresso ⏰]

### Descrição
Configurar arquivos root do monorepo que definem workspaces, pipeline de build e tooling compartilhado.

### Tarefas

#### 1.1 - Criar package.json root [Não Iniciada ⏳]
- Definir workspaces PNPM: `packages/*`
- Scripts: dev, build, test, lint
- Dependencies: turbo, concurrently
- DevDependencies: eslint, prettier, typescript

**Arquivos**:
- `package.json`

**Conteúdo Crítico**:
```json
{
  "name": "context-first",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "dev": "concurrently \"pnpm dev:frontend\" \"pnpm dev:backend\"",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint"
  }
}
```

**Validação**:
- [ ] `package.json` é valid JSON
- [ ] Workspaces aponta para `packages/*`

#### 1.2 - Criar pnpm-workspace.yaml [Não Iniciada ⏳]
- Configurar packages: `packages/*`
- PNPM version: Latest stable (>= 8.x)

**Arquivos**:
- `pnpm-workspace.yaml`

**Conteúdo**:
```yaml
packages:
  - 'packages/*'
```

**Validação**:
- [ ] YAML válido
- [ ] Pattern `packages/*` correto

#### 1.3 - Criar turbo.json [Não Iniciada ⏳]
- Pipeline: dev, build, test, lint
- Cache configuration
- Outputs definidos

**Arquivos**:
- `turbo.json`

**Conteúdo Crítico**:
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

**Validação**:
- [ ] JSON válido
- [ ] Schema URL correto
- [ ] Pipeline tasks definidas

#### 1.4 - Criar .gitignore root [Não Iniciada ⏳]
- Ignorar: node_modules, dist, venv, .env, __pycache__
- Cobrir Node.js e Python artifacts

**Arquivos**:
- `.gitignore`

**Validação**:
- [ ] Cobre Node.js (node_modules, dist, .nuxt)
- [ ] Cobre Python (venv, __pycache__, *.pyc)
- [ ] Cobre env files (.env, .env.local)

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 2: Shared Configuration (Tooling) [Não Iniciada ⏳]

### Descrição
Criar configurações compartilhadas de linting, formatting e TypeScript que serão estendidas pelos packages.

### Tarefas

#### 2.1 - Criar tsconfig.base.json [Não Iniciada ⏳]
- Target: ES2022
- Module: ESNext
- Strict mode: true
- Base para todos os packages TS

**Arquivos**:
- `tsconfig.base.json`

**Conteúdo**:
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

**Validação**:
- [ ] JSON válido
- [ ] Strict mode habilitado

#### 2.2 - Criar .eslintrc.js root [Não Iniciada ⏳]
- Config base: eslint:recommended
- TypeScript support: @typescript-eslint
- Env: node, es2022

**Arquivos**:
- `.eslintrc.js`

**Validação**:
- [ ] Config válida
- [ ] TypeScript plugin incluído

#### 2.3 - Criar .prettierrc [Não Iniciada ⏳]
- Semi: false
- Single quotes: true
- Trailing comma: es5
- Print width: 80

**Arquivos**:
- `.prettierrc`

**Validação**:
- [ ] JSON válido
- [ ] Regras definidas

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 3: Package Shared (Zod Schemas) [Não Iniciada ⏳]

### Descrição
Criar package TypeScript com schemas Zod. Este é um **leaf package** (sem dependências internas).

### Tarefas

#### 3.1 - Scaffold packages/shared/ [Não Iniciada ⏳]
- Estrutura de diretórios: src/, dist/
- package.json com name: "shared"
- tsconfig.json extends base
- Entry point: src/index.ts

**Arquivos**:
- `packages/shared/package.json`
- `packages/shared/tsconfig.json`
- `packages/shared/src/index.ts`
- `packages/shared/src/schemas/`

**package.json**:
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
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "typescript": "^5.6.3"
  }
}
```

**Validação**:
- [ ] package.json válido
- [ ] tsconfig extends ../../tsconfig.base.json
- [ ] src/index.ts existe

#### 3.2 - Criar estrutura de schemas (vazia) [Não Iniciada ⏳]
- demand.ts (export empty schema)
- project.ts (export empty schema)
- metaspec.ts (export empty schema)
- index.ts re-exports tudo

**Arquivos**:
- `packages/shared/src/schemas/demand.ts`
- `packages/shared/src/schemas/project.ts`
- `packages/shared/src/schemas/metaspec.ts`

**Conteúdo de Exemplo (demand.ts)**:
```typescript
import { z } from 'zod'

// TODO: Implementar schema completo em IAD-11
export const DemandSchema = z.object({
  id: z.string(),
  title: z.string(),
})

export type Demand = z.infer<typeof DemandSchema>
```

**Validação**:
- [ ] Schemas exportam tipos
- [ ] index.ts re-exporta tudo
- [ ] `pnpm --filter shared build` compila

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 4: Package Agno-Agents (Python) [Não Iniciada ⏳]

### Descrição
Criar package Python com estrutura de agents. Este é um **leaf package** (sem dependências internas).

### Tarefas

#### 4.1 - Scaffold packages/agno-agents/ [Não Iniciada ⏳]
- Python package structure
- setup.py ou pyproject.toml
- requirements.txt
- agno_agents/__init__.py

**Arquivos**:
- `packages/agno-agents/setup.py`
- `packages/agno-agents/requirements.txt`
- `packages/agno-agents/agno_agents/__init__.py`
- `packages/agno-agents/.gitignore`

**setup.py**:
```python
from setuptools import setup, find_packages

setup(
    name="agno-agents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "agno>=0.0.1",
        "anthropic>=0.40.0",
    ],
)
```

**Validação**:
- [ ] setup.py válido
- [ ] requirements.txt lista dependencies
- [ ] agno_agents é importável

#### 4.2 - Criar estrutura de agents (vazia) [Não Iniciada ⏳]
- spec_writer/ (empty __init__.py)
- architect/ (empty __init__.py)
- coder/ (empty __init__.py)
- reviewer/ (empty __init__.py)

**Arquivos**:
- `packages/agno-agents/agno_agents/spec_writer/__init__.py`
- `packages/agno-agents/agno_agents/architect/__init__.py`
- `packages/agno-agents/agno_agents/coder/__init__.py`
- `packages/agno-agents/agno_agents/reviewer/__init__.py`

**Conteúdo Placeholder**:
```python
# TODO: Implementar agent em IAD-12

class SpecWriterAgent:
    """Spec Writer agent placeholder."""
    pass
```

**Validação**:
- [ ] Estrutura de diretórios criada
- [ ] Todos __init__.py existem
- [ ] Package é importável: `from agno_agents.spec_writer import SpecWriterAgent`

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 5: Package Backend (FastAPI) [Não Iniciada ⏳]

### Descrição
Criar structure FastAPI com Clean Architecture layers (vazias). Depende de **agno-agents**.

### Tarefas

#### 5.1 - Scaffold packages/backend/ [Não Iniciada ⏳]
- Python structure: src/
- requirements.txt
- main.py (FastAPI app mínima)
- venv/ setup instructions

**Arquivos**:
- `packages/backend/requirements.txt`
- `packages/backend/src/main.py`
- `packages/backend/pyproject.toml` (opcional, para black/ruff)
- `packages/backend/.gitignore`

**requirements.txt**:
```txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.2
# agno-agents instalado via: pip install -e ../agno-agents
```

**main.py**:
```python
from fastapi import FastAPI

app = FastAPI(title="Context-First API", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Validação**:
- [ ] FastAPI app roda: `uvicorn src.main:app --reload`
- [ ] http://localhost:8000/health retorna {"status": "ok"}
- [ ] http://localhost:8000/docs abre Swagger UI

#### 5.2 - Criar Clean Architecture layers (vazias) [Não Iniciada ⏳]
- src/domain/ (entities, value_objects)
- src/application/ (use_cases, dtos, interfaces)
- src/infrastructure/ (persistence, ai, external)
- src/interfaces/ (api, websockets)

**Arquivos**:
- `packages/backend/src/domain/__init__.py`
- `packages/backend/src/application/__init__.py`
- `packages/backend/src/infrastructure/__init__.py`
- `packages/backend/src/interfaces/__init__.py`

**Subdiretorios (vazios por enquanto)**:
```
src/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   └── services/
├── application/
│   ├── use_cases/
│   ├── dtos/
│   └── interfaces/
├── infrastructure/
│   ├── persistence/
│   ├── ai/
│   └── external/
└── interfaces/
    ├── api/
    └── websockets/
```

**Validação**:
- [ ] Estrutura de diretórios criada
- [ ] Todos __init__.py existem
- [ ] Imports funcionam: `from src.domain.entities import ...`

#### 5.3 - Configurar dependência agno-agents [Não Iniciada ⏳]
- Instalar agno-agents como editable: `pip install -e ../agno-agents`
- Validar import: `from agno_agents.spec_writer import SpecWriterAgent`

**Comandos**:
```bash
cd packages/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ../agno-agents
```

**Validação**:
- [ ] `pip list` mostra agno-agents
- [ ] Import funciona em Python shell

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 6: Package Frontend (Nuxt 3) [Não Iniciada ⏳]

### Descrição
Criar Nuxt 3 app minimal. Depende de **shared**.

### Tarefas

#### 6.1 - Scaffold packages/frontend/ [Não Iniciada ⏳]
- Nuxt 3 app via `npx nuxi init`
- package.json com dependency: shared
- tsconfig.json extends base
- nuxt.config.ts (minimal)

**Arquivos**:
- `packages/frontend/package.json`
- `packages/frontend/nuxt.config.ts`
- `packages/frontend/tsconfig.json`
- `packages/frontend/app.vue`

**package.json**:
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
    "nuxt": "^3.14.0",
    "vue": "^3.5.0",
    "shared": "workspace:*"
  },
  "devDependencies": {
    "@nuxtjs/tailwindcss": "^6.12.0",
    "typescript": "^5.6.3"
  }
}
```

**nuxt.config.ts**:
```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],
  devtools: { enabled: true },
  typescript: {
    strict: true
  }
})
```

**Validação**:
- [ ] `pnpm --filter frontend install` funciona
- [ ] `pnpm --filter frontend dev` sobe em localhost:3000
- [ ] Hot reload funciona

#### 6.2 - Criar estrutura Atomic Design (vazia) [Não Iniciada ⏳]
- components/atoms/
- components/molecules/
- components/organisms/
- components/templates/

**Arquivos**:
- `packages/frontend/components/atoms/.gitkeep`
- `packages/frontend/components/molecules/.gitkeep`
- `packages/frontend/components/organisms/.gitkeep`
- `packages/frontend/components/templates/.gitkeep`

**Validação**:
- [ ] Estrutura de diretórios criada
- [ ] .gitkeep preserva diretórios vazios

#### 6.3 - Criar app.vue minimal [Não Iniciada ⏳]
- Template: "Context-First Platform"
- Import de shared (teste de dependency)

**app.vue**:
```vue
<template>
  <div>
    <h1>Context-First Platform</h1>
    <p>Monorepo Setup Complete ✅</p>
  </div>
</template>

<script setup lang="ts">
// Teste de import do package shared
import type { Demand } from 'shared'

// TODO: Usar tipos em componentes reais (IAD-9)
</script>
```

**Validação**:
- [ ] App renderiza em localhost:3000
- [ ] Import de 'shared' não causa erro TypeScript

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 7: Development Scripts e README [Não Iniciada ⏳]

### Descrição
Configurar scripts de desenvolvimento e documentação completa de setup.

### Tarefas

#### 7.1 - Configurar scripts root [Não Iniciada ⏳]
- dev:frontend → `pnpm --filter frontend dev`
- dev:backend → `cd packages/backend && uvicorn ...`
- dev → `concurrently` roda ambos

**Atualização de package.json root**:
```json
{
  "scripts": {
    "dev": "concurrently \"pnpm dev:frontend\" \"pnpm dev:backend\" --names \"FRONT,BACK\" --prefix-colors \"blue,green\"",
    "dev:frontend": "pnpm --filter frontend dev",
    "dev:backend": "cd packages/backend && source venv/bin/activate && uvicorn src.main:app --reload --port 8000",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint"
  }
}
```

**Validação**:
- [ ] `pnpm dev` sobe frontend (3000) e backend (8000)
- [ ] Logs são coloridos e com prefixos
- [ ] Hot reload funciona em ambos

#### 7.2 - Criar README.md root [Não Iniciada ⏳]
- Overview do projeto
- Estrutura de monorepo
- Setup instructions (passo a passo)
- Scripts disponíveis
- Links para documentação

**Arquivos**:
- `README.md`

**Seções Obrigatórias**:
1. Sobre o Projeto
2. Estrutura do Monorepo
3. Pré-requisitos (Node, Python, PNPM)
4. Setup Inicial
5. Desenvolvimento
6. Build e Deploy
7. Testes
8. Documentação

**Validação**:
- [ ] README está completo
- [ ] Setup instructions funcionam (testar do zero)
- [ ] Links para docs estão corretos

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 8: Validação Final [Não Iniciada ⏳]

### Descrição
Validar todo o setup contra critérios de aceitação do IAD-3.

### Tarefas

#### 8.1 - Validar PNPM Workspaces [Não Iniciada ⏳]
- `pnpm install` detecta todos packages
- `pnpm list --depth=0` mostra 4 workspaces
- Hoisting funciona (zod, typescript no root)

**Comandos**:
```bash
pnpm install
pnpm list --depth=0
```

**Validação**:
- [ ] Install sem erros
- [ ] 4 packages detectados (frontend, backend, shared, agno-agents)
- [ ] Dependencies hoisted para root quando possível

#### 8.2 - Validar Turborepo Pipeline [Não Iniciada ⏳]
- `pnpm build` compila shared → frontend
- `turbo build` usa cache (segunda execução é instantânea)
- `pnpm lint` valida todos packages

**Comandos**:
```bash
pnpm build
# Segunda vez (deve usar cache)
pnpm build
pnpm lint
```

**Validação**:
- [ ] Build compila shared primeiro
- [ ] Frontend usa output do shared
- [ ] Cache funciona (segunda build < 1s)
- [ ] Lint valida TS e Python

#### 8.3 - Validar Dev Environment [Não Iniciada ⏳]
- `pnpm dev` sobe frontend + backend
- Frontend em localhost:3000 responde
- Backend em localhost:8000/health responde
- Hot reload funciona em ambos

**Validação**:
- [ ] `pnpm dev` funciona
- [ ] Frontend acessível
- [ ] Backend /health retorna 200
- [ ] Mudanças refletem automaticamente

#### 8.4 - Validar Dependencies [Não Iniciada ⏳]
- frontend importa shared ✅
- backend importa agno-agents ✅
- Sem circular dependencies ✅

**Validação**:
```typescript
// Frontend
import { DemandSchema } from 'shared' // ✅
```

```python
# Backend
from agno_agents.spec_writer import SpecWriterAgent # ✅
```

**Validação**:
- [ ] Frontend import funciona
- [ ] Backend import funciona
- [ ] Sem erros de tipo TypeScript

#### 8.5 - Validar Critérios de Aceitação IAD-3 [Não Iniciada ⏳]

Conforme definido no refinement:

1. ✅ Estrutura completa criada (4 packages + root configs)
2. ✅ PNPM workspaces funcionando
3. ✅ Turborepo configurado
4. ✅ Frontend scaffold (Nuxt 3 em localhost:3000)
5. ✅ Backend scaffold (FastAPI em localhost:8000)
6. ✅ Shared package (estrutura de schemas)
7. ✅ Agno-agents package (importável pelo backend)
8. ✅ Dev scripts (`pnpm dev` roda tudo)
9. ✅ Build funcional (`pnpm build` sem erros)
10. ✅ Linting configurado (`pnpm lint`)
11. ✅ Documentação (README.md com setup instructions)

**Validação**:
- [ ] Todos os 11 critérios cumpridos

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## ✅ Checklist Final

Antes de considerar IAD-3 completo:

### Estrutura
- [ ] 4 packages criados (frontend, backend, shared, agno-agents)
- [ ] Root configs (package.json, turbo.json, pnpm-workspace.yaml)
- [ ] Tooling (tsconfig.base.json, .eslintrc.js, .prettierrc)
- [ ] .gitignore cobre Node e Python

### Funcionalidade
- [ ] `pnpm install` sem erros
- [ ] `pnpm dev` sobe frontend + backend
- [ ] `pnpm build` compila com sucesso
- [ ] `pnpm lint` valida código

### Dependencies
- [ ] frontend → shared funciona
- [ ] backend → agno-agents funciona
- [ ] Sem circular dependencies

### Documentação
- [ ] README.md completo com setup instructions
- [ ] Todos os critérios de aceitação cumpridos

### Linear
- [ ] Atualizar IAD-3 com status "In Progress" → "Done"
- [ ] Adicionar comentário com resultado da validação

---

## 📊 Ordem de Execução

### Sequencial (deve seguir ordem)
1. FASE 1 (Root) → FASE 2 (Tooling) → FASE 3 (Shared) → FASE 4 (Agno) → FASE 5 (Backend) → FASE 6 (Frontend) → FASE 7 (Scripts) → FASE 8 (Validação)

**Justificativa da Ordem:**
- Root e Tooling primeiro (base para tudo)
- Shared e Agno são leaf packages (sem dependências internas)
- Backend depende de Agno
- Frontend depende de Shared
- Scripts agregam tudo
- Validação no final

### Paralelo (pode fazer junto)
- FASE 3 (Shared) e FASE 4 (Agno) podem ser feitas em paralelo (ambas são leaf packages)

---

## 🔄 Status Legend

- ⏳ **Não Iniciada**: Ainda não começou
- ⏰ **Em Progresso**: Trabalhando atualmente
- ✅ **Completada**: Finalizada e testada
- ⚠️ **Bloqueada**: Aguardando dependência

---

## 📝 Observações Importantes

### Diferenças do Template Original

Este plano é adaptado para **infrastructure setup**, não feature development UI:
- **Não usa Atomic Design** (não há componentes UI nesta issue)
- **Não há testes unitários/E2E** (build config não tem testes, validação é manual)
- **Foco em structure e configuration** (não em lógica de negócio)

### Próximas Issues (Features Reais)

- **IAD-9** (Frontend Base): Usará Atomic Design (atoms → molecules → organisms)
- **IAD-11** (Shared Schemas): Implementará schemas Zod completos
- **IAD-12** (Agno Agents): Implementará agents com lógica real
- **IAD-6/7/8** (Backend Layers): Implementará Clean Architecture completa

---

**Criado**: 20 de Novembro de 2025
**Última Atualização**: 20 de Novembro de 2025
**Feature Slug**: iad-3
**Issue Linear**: IAD-3
