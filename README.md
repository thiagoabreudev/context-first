# Context-First Platform

> AI Development Governance & Orchestration Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Turborepo](https://img.shields.io/badge/built%20with-turborepo-blueviolet.svg)](https://turbo.build)

---

## 🎯 Sobre o Projeto

Plataforma SaaS que transforma a Metodologia CONTEXT-FIRST™ e Metaspecs em produto escalável, orquestrando ciclo completo SPARC+DD de desenvolvimento assistido por IA com governança, qualidade e previsibilidade.

**Status:** MVP em Desenvolvimento (IAD-3 ✅)

## 📁 Estrutura do Monorepo

```
context-first/
├── packages/
│   ├── frontend/           # Nuxt 3 app
│   ├── backend/            # FastAPI app
│   ├── shared/             # Schemas Zod, types TS
│   └── agno-agents/        # AI agents (Agno framework)
├── specs/                  # Documentação (business + technical)
├── .claude/                # Comandos e metodologia CONTEXT-FIRST™
├── turbo.json              # Turborepo pipeline config
└── package.json            # Root package
```

### Package Dependencies

```
frontend → shared (types)
backend → agno-agents (AI agents)
```

## 🛠️ Stack Tecnológica

**Frontend:**
- Nuxt 3 + Vue 3 + TypeScript
- Tailwind CSS
- Pinia (state management)

**Backend:**
- FastAPI + Python 3.11+
- Clean Architecture + DDD
- MongoDB (Atlas)
- Redis (Upstash)

**AI/LLM:**
- Anthropic Claude (Haiku, Sonnet, Opus)
- Agno framework (multi-agent orchestration)

**Infra:**
- Monorepo: Turborepo + PNPM workspaces
- Deploy: Vercel (frontend) + Railway/Render (backend)
- Storage: AWS S3 (checkpoints)
- Auth: Clerk

## 🚀 Pré-requisitos

- **Node.js**: >= 18.0.0
- **PNPM**: >= 8.0.0 ([Install](https://pnpm.io/installation))
- **Python**: >= 3.11
- **Git**: Latest

### Instalação do PNPM

```bash
npm install -g pnpm@8.15.0
```

## 📦 Setup Inicial

### 1. Clone o repositório

```bash
git clone https://github.com/[org]/context-first.git
cd context-first
```

### 2. Install Node dependencies (monorepo)

```bash
pnpm install
```

Isso instalará dependencies para:
- Root
- `packages/frontend`
- `packages/shared`

### 3. Setup Python Backend

```bash
cd packages/backend

# Criar virtual environment
python -m venv venv

# Ativar venv (macOS/Linux)
source venv/bin/activate

# Ativar venv (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Setup Agno Agents (editable install)

```bash
# Ainda com venv ativo
pip install -e ../agno-agents
```

### 5. Configurar variáveis de ambiente

#### Frontend (.env)

```bash
# packages/frontend/.env
API_BASE_URL=http://localhost:8000
```

#### Backend (.env)

```bash
# packages/backend/.env
# TODO: Adicionar em IAD-8 (MongoDB, Redis, S3, Anthropic)
```

## 💻 Desenvolvimento

### Rodar tudo (Frontend + Backend)

```bash
# Na raiz do monorepo
pnpm dev
```

Isso roda em paralelo:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Rodar apenas Frontend

```bash
pnpm dev:frontend
# ou
pnpm --filter frontend dev
```

### Rodar apenas Backend

```bash
# Na raiz
pnpm dev:backend

# OU manualmente
cd packages/backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

### Rodar package específico

```bash
# Build shared
pnpm --filter shared build

# Dev frontend
pnpm --filter frontend dev
```

## 🏗️ Build

### Build de produção

```bash
pnpm build
```

Turborepo executará builds em ordem de dependência:
1. `shared` (TypeScript → JavaScript)
2. `frontend` (Nuxt build)
3. `backend` (sem build, Python runtime)

### Build com cache

Segunda execução usa cache (< 1s):

```bash
pnpm build  # Primeira vez: ~30s
pnpm build  # Segunda vez: ~1s (cache)
```

## 🧪 Testes

```bash
# Rodar todos os testes (quando implementados)
pnpm test

# Por package
pnpm --filter frontend test
pnpm --filter backend test
```

## 🎨 Linting & Formatting

```bash
# Lint todos os packages
pnpm lint

# Lint específico
pnpm --filter frontend lint

# Python (backend)
cd packages/backend
ruff check .
black --check .
```

## 📚 Documentação

### Documentação Empresarial

- [README](./specs/business/README.md)
- [Product Strategy](./specs/business/PRODUCT_STRATEGY.md)
- [Customer Personas](./specs/business/CUSTOMER_PERSONAS.md)

### Documentação Técnica

- [README](./specs/technical/README.md)
- [Overview Técnico](./specs/technical/index.md)
- [CLAUDE.meta.md](./specs/technical/CLAUDE.meta.md) ⭐ - Guia para IA
- [CODEBASE_GUIDE.md](./specs/technical/CODEBASE_GUIDE.md)
- [API Specification](./specs/technical/API_SPECIFICATION.md)

### ADRs (Architecture Decision Records)

- [ADR-001: Monorepo com Turborepo](./specs/technical/adr/001-monorepo-structure.md)
- [ADR-002: FastAPI + DDD + Clean Architecture](./specs/technical/adr/002-backend-architecture.md)
- [ADR-003: MongoDB como Database Principal](./specs/technical/adr/003-mongodb-choice.md)
- [ADR-004: Agno como Framework de IA](./specs/technical/adr/004-agno-framework.md)
- [Todos os ADRs](./specs/technical/adr/)

## 🗺️ Roadmap

### ✅ MVP (Q4 2025 - Mês 4)

- [x] IAD-3: Monorepo setup (Turborepo + PNPM)
- [ ] IAD-6: Domain Layer (Entities, Value Objects)
- [ ] IAD-7: Application Layer (Use Cases, DTOs)
- [ ] IAD-8: Infrastructure Layer (MongoDB, Redis, S3)
- [ ] IAD-9: Frontend Base (Components, Pages, Stores)
- [ ] IAD-12: Agno Agents (Spec Writer, Architect, Coder, Reviewer)

### V1.1 (Q1 2026 - Meses 5-6)

- [ ] /work (Coder agent completo)
- [ ] Linear/Jira integration
- [ ] Template marketplace (beta)

## 🤝 Contribuindo

Leia [CONTRIBUTING.md](./specs/technical/CONTRIBUTING.md) para:
- Processo de Pull Request
- Padrões de código
- Convenções de commit
- CI/CD workflow

## 🐛 Troubleshooting

### PNPM não detecta workspaces

```bash
# Verificar workspaces
pnpm list --depth=0

# Reinstalar
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Backend não inicia

```bash
# Verificar venv
cd packages/backend
source venv/bin/activate
python --version  # Deve ser >= 3.11

# Reinstalar dependencies
pip install -r requirements.txt
pip install -e ../agno-agents
```

### Frontend não encontra 'shared'

```bash
# Build shared primeiro
pnpm --filter shared build

# Restart frontend
pnpm --filter frontend dev
```

### Mais problemas?

Consulte [TROUBLESHOOTING.md](./specs/technical/TROUBLESHOOTING.md)

## 📊 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `pnpm dev` | Roda frontend + backend em paralelo |
| `pnpm dev:frontend` | Roda apenas frontend (Nuxt) |
| `pnpm dev:backend` | Roda apenas backend (FastAPI) |
| `pnpm build` | Build de produção (todos packages) |
| `pnpm test` | Roda todos os testes |
| `pnpm lint` | Lint todos os packages |
| `pnpm clean` | Limpa build artifacts + node_modules |

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links

- **Website**: https://contextfirst.dev
- **Docs**: https://docs.contextfirst.dev
- **Linear**: [Link ao configurar]
- **Discord**: [Link ao configurar]

---

# Context-First Methodology Commands

## Configuração Inicial

### 1. Configurar Variáveis de Ambiente

Copie o arquivo `.ia.env.example` para `.ia.env`:

```bash
cp .ia.env.example .ia.env
```

Edite `.ia.env` e configure o caminho para suas metaspecs:

```bash
METASPECS_DIR=/caminho/para/suas/metaspecs
```

### 2. Estrutura de Diretórios

```
context-first/
├── .claude/               # Comandos Claude
│   ├── commands/
│   │   ├── context-first/ # Comandos principais
│   │   ├── context/       # Gestão de contexto
│   │   └── ...
│   └── helpers/          # Scripts auxiliares
├── .ia.env               # Variáveis de ambiente (não versionado)
├── .ia.env.example       # Template de configuração
└── README.md            # Este arquivo
```

### 3. Metaspecs (Repositório Separado)

As metaspecs ficam em um repositório separado, configurado via `METASPECS_DIR`:

```
metaspecs/
├── business/             # Regras de negócio
│   ├── authentication/
│   ├── strategies/
│   └── ...
├── technical/            # Especificações técnicas
│   ├── architecture/
│   ├── api/
│   └── ...
├── observability/        # Specs de observabilidade
└── governance/           # Specs de governança
```

## Comandos Disponíveis

### Context-First Commands

#### `/context-first test-first <feature>`
Criar testes ANTES do código (TDD adaptado para IA).

```bash
/context-first test-first "Criar endpoint POST /api/login"
```

#### `/context-first validate-spec [arquivo]`
Validar código contra metaspecs (regras de negócio).

```bash
# Validar arquivo específico
/context-first validate-spec src/workflows/candle_buy.py

# Validar todos os arquivos modificados
/context-first validate-spec
```

#### `/context-first observability <feature>`
Adicionar observabilidade completa (logging, métricas, tracing).

```bash
/context-first observability login
```

#### `/context-first governance <feature>`
Adicionar governança completa (auditoria, compliance, segurança).

```bash
/context-first governance payment
```

#### `/context-first security-check [arquivo]`
Verificar segurança do código antes de commit.

```bash
/context-first security-check
```

### Context Management

#### `/context status`
Monitorar uso atual da janela de contexto.

#### `/context checkpoint`
Salvar estado completo e preparar para chaveamento de contexto.

#### `/context clean`
Remover informações desnecessárias do contexto.

#### `/context compact`
Compactar contexto resumindo conversa em NOTES.md.

#### `/context budget <feature> <tokens>`
Definir orçamento de tokens para uma feature.

```bash
/context budget login 50000
```

## Como Funciona

### 1. Carregamento de Variáveis

Todos os comandos automaticamente carregam `METASPECS_DIR` do arquivo `.ia.env`:

```bash
# Carregado automaticamente
export $(grep -v '^#' .ia.env | xargs)
```

### 2. Referência às Metaspecs

Comandos usam `$METASPECS_DIR` para acessar as especificações:

```bash
# Exemplo interno
metaspec_file="$METASPECS_DIR/business/authentication/login.md"
```

### 3. Validação de Specs

O comando `validate-spec` lê as metaspecs e valida:

- **Must Do**: O que o código DEVE fazer
- **Must Not Do**: O que o código NÃO DEVE fazer
- **Edge Cases**: Casos extremos que devem ser tratados

### 4. Test-First

O comando `test-first`:

1. Lê metaspecs relevantes de `$METASPECS_DIR`
2. Identifica behaviors (Must Do, Must Not Do, Edge Cases)
3. Gera arquivo de teste completo
4. Você implementa o código para passar nos testes

## Exemplo de Uso Completo

### 1. Criar Feature com Test-First

```bash
/context-first test-first "Endpoint POST /api/login com JWT"
```

Saída:
```
✅ Tests created: tests/api/test_login.py
15 tests generated based on:
  - $METASPECS_DIR/business/authentication/login.md
  - $METASPECS_DIR/technical/api/security.md
```

### 2. Implementar Código

(Você escreve o código para passar nos testes)

### 3. Validar Contra Specs

```bash
/context-first validate-spec src/api/auth.py
```

Saída:
```
📋 Spec Validation - src/api/auth.py
Overall Compliance: 95% ✅
✅ APPROVED
```

### 4. Adicionar Observabilidade

```bash
/context-first observability login
```

### 5. Adicionar Governança

```bash
/context-first governance login
```

### 6. Security Check

```bash
/context-first security-check
```

## Integração com Git

Os comandos respeitam o `.gitignore`:

```gitignore
# Arquivo .ia.env não é versionado
.ia.env
```

## Troubleshooting

### Erro: "METASPECS_DIR não encontrado"

Certifique-se de que:
1. O arquivo `.ia.env` existe na raiz do projeto
2. A variável `METASPECS_DIR` está configurada
3. O caminho aponta para um diretório válido

### Erro: "Metaspec não encontrada"

Verifique:
1. O caminho em `METASPECS_DIR` está correto
2. O diretório de metaspecs contém os arquivos esperados
3. A estrutura de diretórios está correta

## Contribuindo

Para adicionar novos comandos:

1. Crie o arquivo em `.claude/commands/`
2. Use `$METASPECS_DIR` para referenciar metaspecs
3. Adicione documentação neste README

## Licença

MIT
