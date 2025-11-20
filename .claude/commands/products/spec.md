# PRD Completo - context-first

Você é um especialista em produto encarregado de criar **PRD (Product Requirements Document)** completo para o projeto **context-first**.

## Objetivo

Transformar um requisito em PRD completo, validado e pronto para desenvolvimento (fase Architecture do SPARC+DD).

## Processo

### 1. Validar Requisitos Atuais

Revise os requisitos fornecidos e valide que contêm informações básicas:

- ✅ **POR QUE** estamos fazendo isso (valor de negócio)
- ✅ **O QUE** está sendo construído (escopo funcional)
- ✅ **COMO** está sendo construído (direção técnica)

**Se requisitos forem insuficientes**: Faça perguntas de esclarecimento e atualize documento/issue antes de prosseguir. **Não assuma nada, apenas pergunte**.

### 2. Validação Contra Specs

**IMPORTANTE**: Os índices JÁ estão em contexto (você rodou `/warm-up`). Consulte-os e leia APENAS documentos relevantes ao requisito.

**Verificações Obrigatórias**:

#### Negócio (`/specs/business/`)
- [ ] **PRODUCT_STRATEGY.md**: Alinhado com visão, roadmap e prioridades?
- [ ] **CUSTOMER_PERSONAS.md**: Atende pelo menos uma persona (CTO/Tech Lead/Developer)?
- [ ] **FEATURE_CATALOG.md**: Feature está listada ou é nova válida?
- [ ] **CUSTOMER_JOURNEY.md**: Encaixa em alguma fase da jornada?

#### Técnico (`/specs/technical/`)
- [ ] **index.md**: Stack aprovada (Nuxt 3, FastAPI, MongoDB, Agno)?
- [ ] **CLAUDE.meta.md**: Segue convenções de código (DDD, Clean Architecture)?
- [ ] **API_SPECIFICATION.md**: Endpoints necessários documentados?
- [ ] **BUSINESS_LOGIC.md**: Regras de negócio respeitadas?
- [ ] **ADRs relevantes**: Sem conflitos com decisões arquiteturais?

**Se houver violação**: 🛑 **PARE** e peça esclarecimento ao usuário antes de prosseguir (Princípio Jidoka).

### 3. Construir PRD Completo

Construa seu entendimento sobre os elementos-chave do PRD. **Importante**: Menos é mais. Se a feature não requer alguns itens, sinta-se livre para pulá-los. Foque no essencial.

#### 📋 Visão Geral
- **Declaração do Problema**: Que dor resolve?
- **Oportunidade**: Por que agora?
- **Usuários-alvo**: Qual(is) persona(s)? (CTO / Tech Lead / Developer / CFO)
- **Objetivos**: O que queremos alcançar?
- **Métricas de Sucesso**: KPIs mensuráveis (activation, retention, NPS, redução de retrabalho)

#### ⚙️ Requisitos Funcionais
- **Funcionalidades Principais**: Lista detalhada
- **User Stories**: Formato "Como [persona], eu quero [ação] para [benefício]"
- **Fluxos de Usuário**: Jornada passo a passo
- **Especificações Técnicas**:
  - **Frontend**: Componentes Vue 3 (Atomic Design: Atoms / Molecules / Organisms)
  - **Backend**: Use Cases, Entities (DDD), API endpoints
  - **AI Agents**: Qual agente usar (Spec Writer / Architect / Coder / Reviewer)
- **Integrações**: Claude API, GitHub, Linear, Clerk

#### 🚀 Requisitos Não-Funcionais
- **Performance**:
  - API latency P95 < 2s
  - Dashboard load < 200ms
  - Agent response streaming < 500ms first chunk
- **Escalabilidade**: Suportar 100+ projetos simultâneos
- **Context Budget**: Custo por usuário < R$ 50/mês (Anthropic API)
- **Security**: HTTPS only, rate limiting, input validation (Zod/Pydantic)

#### 🎨 Design e UX
- **Diretrizes UI/UX**: Princípios de design do produto
- **Responsividade**: Mobile-first, breakpoints
- **Sistema de Design**: Tailwind CSS + componentes customizados
- **Wireframes/Mockups**: Referências visuais (se aplicável)

#### 🔧 Considerações Técnicas
- **Arquitetura**: Atomic Design, SSG/ISR
- **Stack**: Vue 3, Nuxt.js 3, TypeScript, Tailwind
- **Componentes**: Quais criar/modificar (atoms → organisms)
- **Integrações**: APIs externas, Nuxt Content
- **Dados**: Estrutura de dados, validação (Zod)
- **Dependências**: Bibliotecas necessárias

#### 📊 Projeto e Execução
- **Riscos**: O que pode dar errado?
- **Mitigação**: Como prevenir/resolver riscos
- **Critérios de Lançamento**: Definition of Done
- **Rollout**: Estratégia de deploy (preview → production)
- **Testes**: E2E críticos, unit tests, cobertura

#### 🔒 Restrições e Suposições
- **Restrições Técnicas**: Limitações conhecidas (ver problemas-conhecidos.md)
- **Restrições de Negócio**: Budget, timeline, recursos
- **Suposições**: O que assumimos ser verdade

### 4. Apresentar Entendimento ao Usuário

Apresente seu entendimento completo ao usuário, junto com quaisquer esclarecimentos necessários. **Iterate** até ter 100% de clareza.

### 5. Gerar PRD Final

Depois que o usuário aprovar, você deve:

**Salvar PRD em**:
- **Método 1 (Recomendado)**: Atualizar issue do **Linear** via MCP
  - Team: **iadojeitocerto** (ID: `2b1273da-f961-407a-b0f5-4047378ecb4d`)
  - Use a ferramenta: `mcp__linear-server__update_issue`
- **Método 2**: Editar arquivo existente (se requisito veio de arquivo)
- **Método 3 (Fallback)**: Criar arquivo em `/specs/prd/[titulo-slug].md`

**Template do PRD**:

```markdown
# PRD: [Nome da Feature]

**Versão**: 1.0.0
**Data**: [YYYY-MM-DD]
**Owner**: Product Team
**Status**: 📝 Draft / ✅ Aprovado / 🚧 Em Desenvolvimento

---

## 📋 Visão Geral

### Problema
[Que dor estamos resolvendo?]

### Oportunidade
[Por que agora? Qual o valor de negócio?]

### Personas Atendidas
- [ ] CTO (Ricardo Silva)
- [ ] VP de Engenharia (Mariana Costa)
- [ ] Tech Lead (Bruno Oliveira)

### Objetivos
1. [Objetivo 1]
2. [Objetivo 2]

### Métricas de Sucesso
- **Métrica 1**: [target - ex: conversão > 3%]
- **Métrica 2**: [target - ex: bounce rate < 60%]

---

## ⚙️ Requisitos Funcionais

### Funcionalidades Principais
1. [Funcionalidade 1 detalhada]
2. [Funcionalidade 2 detalhada]

### User Stories
```gherkin
# US-001: [Título]
Como [persona]
Eu quero [ação]
Para [benefício]

Critérios de Aceitação:
- Dado que [contexto]
- Quando [ação]
- Então [resultado esperado]
```

### Fluxo de Usuário
1. Usuário acessa [página/componente]
2. Usuário interage com [elemento]
3. Sistema [resposta]
4. Resultado: [estado final]

---

## 🚀 Requisitos Não-Funcionais

### Performance
- LCP < 2s
- Lighthouse Score > 90
- Bundle size < 150kb (MVP)

### Acessibilidade
- WCAG 2.1 AA compliance
- Navegação por teclado
- Screen reader support

### SEO
- Meta tags completas
- Structured data (Schema.org)
- Sitemap atualizado

### Segurança
- Rate limiting (conforme arquitetura.md)
- Validação de inputs (Zod)
- Sanitização de dados

---

## 🎨 Design e UX

### Princípios de Design
[Conforme visao-produto.md]

### Responsividade
- Mobile-first
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)

### Componentes Atomic Design
- **Atoms**: [lista de átomos necessários]
- **Molecules**: [lista de moléculas necessárias]
- **Organisms**: [lista de organismos necessários]
- **Templates**: [layout utilizado]

---

## 🔧 Considerações Técnicas

### Stack
- Framework: Nuxt.js 3.10+
- Linguagem: TypeScript (strict mode)
- Estilização: Tailwind CSS 3+
- [Outros conforme necessário]

### Arquitetura
- Renderização: SSG / ISR
- Componentes: Atomic Design
- Estado: Composables
- Conteúdo: Nuxt Content (se aplicável)

### Componentes Afetados
```
components/
├── atoms/
│   └── [listar átomos criados/modificados]
├── molecules/
│   └── [listar moléculas criadas/modificadas]
└── organisms/
    └── [listar organismos criados/modificados]

pages/
└── [listar páginas criadas/modificadas]
```

### Integrações
- [API 1]: [propósito]
- [API 2]: [propósito]

### Dados e Validação
```typescript
// Exemplo de schema Zod
interface FeatureData {
  field1: string
  field2: number
}
```

---

## 📊 Projeto e Execução

### Riscos e Mitigação
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| [Risco 1] | Alta/Média/Baixa | Alto/Médio/Baixo | [Estratégia] |

### Critérios de Lançamento (DoD)
- [ ] Funcionalidades implementadas conforme spec
- [ ] Testes E2E críticos passando
- [ ] Performance targets atingidos
- [ ] Acessibilidade validada
- [ ] Code review aprovado
- [ ] Documentação atualizada

### Estratégia de Rollout
1. Deploy em preview (Vercel)
2. Testes internos
3. Deploy em production
4. Monitoramento de métricas

### Testes
**E2E (Playwright)**:
- [ ] [Caso de teste crítico 1]
- [ ] [Caso de teste crítico 2]

**Unit (Vitest)**:
- [ ] [Teste de lógica de negócio]
- [ ] [Teste de validação]

**Cobertura Target**: 80%+ unit, 100% fluxos críticos

---

## 🔒 Restrições e Suposições

### Restrições Técnicas
- [Limitação 1 - ver problemas-conhecidos.md]
- [Limitação 2]

### Restrições de Negócio
- Budget: [valor]
- Timeline: [prazo]
- Recursos: [equipe disponível]

### Suposições
- Assumimos que [suposição 1]
- Assumimos que [suposição 2]

---

## ✅ Validação contra Meta Specs

- [x] Alinhado com `visao-produto.md` (proposta de valor, objetivos)
- [x] Atende persona(s) de `perfil-cliente.md`
- [x] Listado em `features-valores.md` (Fase: MVP/2/3)
- [x] Usa stack de `stack-tecnologica.md`
- [x] Segue padrões de `arquitetura.md`
- [x] Estratégia de testes conforme `estrategia-testes.md`
- [x] Sem conflitos com `problemas-conhecidos.md`

---

## 📝 Changelog

| Versão | Data | Mudanças | Autor |
|--------|------|----------|-------|
| 1.0.0 | YYYY-MM-DD | Criação inicial do PRD | [Nome] |

---

**Próximos Passos**: Este PRD está pronto para fase de **Architecture** (comando `/draft-arch` ou `/arch`) do SPARC+DD.
```

---

**Requisito para Análise**:

<requirement>
#$ARGUMENTS
</requirement>

---

**Próximos Passos**: Após criar PRD, o usuário pode iniciar fase **Architecture** do SPARC+DD com `/draft-arch` ou `/arch`.