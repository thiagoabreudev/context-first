# Aquecimento do Projeto - context-first

Para se preparar para esta sessão de desenvolvimento da plataforma **context-first**, por favor:

## 1. Specs (Fonte Canônica de Verdade)

Leia os seguintes arquivos na ordem:

1. **`/projects/context-first/index.md`** - Índice do projeto com visão geral e links
2. **`/specs/business/README.md`** - Índice de documentação empresarial
3. **`/specs/technical/README.md`** - Índice de documentação técnica

**IMPORTANTE**: NÃO leia todos os documentos referenciados agora. Apenas memorize a estrutura para consultar documentos específicos quando necessário durante o desenvolvimento.

**Estrutura das Specs**:
- `/specs/business/` - O QUE e POR QUE construir (visão, personas, features, strategy)
- `/specs/technical/` - COMO construir (stack, arquitetura, ADRs, API specs)

## 2. Contexto Empresarial (Quick Reference)

**Arquivos-chave em /specs/business/**:
- `PRODUCT_STRATEGY.md` - Visão 5 anos, posicionamento, roadmap
- `CUSTOMER_PERSONAS.md` - CTO, Tech Lead, Developer, CFO
- `CUSTOMER_JOURNEY.md` - Awareness → Retention
- `FEATURE_CATALOG.md` - Features MVP → V2.0

## 3. Contexto Técnico (Quick Reference)

**Stack Tecnológica** (conforme `/specs/technical/index.md`):
- **Frontend:** Nuxt 3 + Vue 3 + TypeScript + Tailwind + shadcn-vue
- **Backend:** FastAPI + Python 3.11+ + DDD + Clean Architecture
- **Database:** MongoDB (Atlas)
- **AI:** Agno framework + Anthropic Claude (Haiku/Sonnet/Opus)
- **Real-time:** WebSockets + Redis Pub/Sub
- **Auth:** Clerk
- **Deploy:** Vercel (front), Railway/Render (back)

**Arquivos-chave em /specs/technical/**:
- `CLAUDE.meta.md` ⭐ - Guia de desenvolvimento com IA (LEIA PRIMEIRO)
- `CODEBASE_GUIDE.md` - Estrutura de código, fluxos de dados
- `API_SPECIFICATION.md` - Endpoints REST + WebSocket
- `BUSINESS_LOGIC.md` - Regras de negócio, domínio
- `adr/` - 8 ADRs (decisões arquiteturais)

## 4. Princípio Jidoka

> "Qualquer pessoa tem não apenas o direito, mas a **responsabilidade** de parar toda a linha quando detecta um problema"

Se você identificar **desalinhamento com specs** durante qualquer fase:
1. 🛑 PARE o trabalho
2. 📝 DOCUMENTE o conflito
3. 💬 ALERTE o usuário
4. ✅ RESOLVA: Ajuste spec OU ajuste implementação
5. ▶️ CONTINUE alinhado

## 5. Princípio CONTEXT-FIRST™

> "Context management vem ANTES do código"

**SEMPRE antes de implementar:**
1. Ler specs relacionadas (`/specs/business/`, `/specs/technical/`)
2. Entender business logic (`BUSINESS_LOGIC.md`)
3. Verificar ADRs (`/specs/technical/adr/`)
4. DEPOIS implementar seguindo `CLAUDE.meta.md`

---

## 6. Integrações Ativas

### Linear (via MCP)

✅ **MCP Linear Conectado** - Use para gerenciar issues:

**Ferramentas Disponíveis:**
- `mcp__linear-server__search_teams` - Buscar team context-first
- `mcp__linear-server__create_issue` - Criar nova issue
- `mcp__linear-server__search_issues` - Buscar issues existentes
- `mcp__linear-server__get_issue` - Detalhes de uma issue
- `mcp__linear-server__update_issue` - Atualizar issue

**Uso Típico:**
```bash
# Coletar nova ideia
/collect [descrição]

# Sistema cria issue no Linear automaticamente via MCP
# Retorna: Linear Issue ID + URL
```

---

**Projeto**: context-first
**Tipo**: SaaS B2B - AI Development Governance & Orchestration Platform
**Objetivo**: Orquestrar ciclo completo SPARC+DD com governança, qualidade e previsibilidade
**Meta Conceito**: Usar a MESMA metodologia (CONTEXT-FIRST™) para construir a plataforma que vende a metodologia

Argumentos fornecidos: #$ARGUMENTS

