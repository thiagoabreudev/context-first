# Comandos de Produto - IA do Jeito Certo

Este diretório contém comandos customizados para a fase de **Specification (S)** da metodologia **SPARC+DD** aplicada ao projeto **iadojeitocerto.com.br**.

## 📋 Comandos Disponíveis

### `/warm-up` - Aquecimento do Projeto
**Propósito**: Carregar contexto essencial do projeto em memória.

**O que faz**:
- Carrega índices das Meta Specs (businnes + technical)
- Lista documentos em `/docs` para referência futura
- Apresenta stack tecnológica e princípio Jidoka
- Prepara Claude Code para trabalhar com validação contra meta specs

**Quando usar**:
- Início de TODA nova sessão de desenvolvimento
- Antes de qualquer comando de produto (`/collect`, `/refine`, `/spec`, `/check`)

**Uso**:
```
/warm-up
```

---

### `/collect` - Coleta de Ideias
**Propósito**: Capturar rapidamente novas ideias de features ou bugs no backlog.

**O que faz**:
- Faz perguntas de esclarecimento mínimas
- Cria rascunho de issue com título e descrição
- Salva no **Linear** projeto **iadojeitocerto** (ou arquivo markdown como fallback)
- Configuração do Linear em `.claude/linear-config.md`

**Quando usar**:
- Quando surge ideia nova de feature
- Ao identificar bug
- Para capturar requisitos iniciais SEM validação profunda

**Quando NÃO usar**:
- Se você já tem requisito detalhado → use `/refine` ou `/spec`
- Para validar feature → use `/check`

**Uso**:
```
/collect Implementar formulário de contato com validação de email corporativo
```

**Output**: Issue no **Linear** projeto **iadojeitocerto** ou arquivo em `/specs/backlog/`

---

### `/refine` - Refinamento de Requisitos
**Propósito**: Transformar requisito inicial em especificação refinada e validada.

**O que faz**:
- Faz perguntas de esclarecimento profundas
- Valida contra meta specs (negócio + técnico)
- Gera especificação no formato POR QUE / O QUE / COMO
- Salva requisitos refinados

**Quando usar**:
- Após `/collect`, quando precisar detalhar requisito
- Quando requisito inicial está vago
- Antes de criar PRD completo

**Validações**:
- ✅ Alinhamento com visão do produto
- ✅ Atende persona específica
- ✅ Usa stack aprovada
- ✅ Segue Atomic Design

**Uso**:
```
/refine <issue-id-do-linear>
/refine /specs/backlog/formulario-contato.md
```

**Output**: Requisitos refinados salvos na issue/arquivo

---

### `/spec` - PRD Completo
**Propósito**: Criar Product Requirements Document (PRD) completo, pronto para desenvolvimento.

**O que faz**:
- Valida que requisitos têm POR QUE / O QUE / COMO
- Valida contra TODAS as meta specs
- Gera PRD completo com todos os detalhes técnicos e de negócio
- Template estruturado para fase de Architecture

**Quando usar**:
- Após `/refine`, quando requisito está maduro
- Antes de iniciar implementação (fase Architecture do SPARC+DD)
- Para features complexas que precisam especificação completa

**Seções do PRD**:
- 📋 Visão Geral (problema, personas, métricas)
- ⚙️ Requisitos Funcionais (user stories, fluxos)
- 🚀 Requisitos Não-Funcionais (performance, SEO, segurança)
- 🎨 Design e UX (responsividade, Atomic Design)
- 🔧 Considerações Técnicas (stack, componentes, dados)
- 📊 Projeto e Execução (riscos, testes, DoD)
- 🔒 Restrições e Suposições
- ✅ Validação contra Meta Specs

**Uso**:
```
/spec <issue-id-do-linear>
/spec /specs/refined/formulario-contato.md
```

**Output**: PRD completo salvo em `/specs/prd/[nome-feature].md`

**Próximo passo**: Fase de Architecture (`/draft-arch` ou `/arch`)

---

### `/check` - Verificação contra Meta Specs
**Propósito**: Validar feature ou requisito contra meta especificações do projeto.

**O que faz**:
- Analisa alinhamento com meta specs de negócio
- Analisa alinhamento com meta specs técnicas
- Identifica desalinhamentos e violações
- Fornece recomendações

**Quando usar**:
- Para validar ideia de feature ANTES de especificar
- Para revisar PRD existente
- Quando em dúvida se feature está alinhada
- Durante code review para validar implementação

**Checklist de Validação**:
- [ ] Alinhada com `visao-produto.md`?
- [ ] Atende persona de `perfil-cliente.md`?
- [ ] Listada em `features-valores.md`?
- [ ] Usa stack de `stack-tecnologica.md`?
- [ ] Segue padrões de `arquitetura.md`?
- [ ] Sem conflitos com `problemas-conhecidos.md`?

**Uso**:
```
/check Adicionar modo dark no site
/check /specs/prd/hero-section.md
```

**Output**: Relatório de alinhamento/desalinhamento

---

## 🔄 Fluxo Recomendado

### Para Feature Nova

```
1. /warm-up
   ↓
2. /collect [ideia inicial]
   ↓ (issue criada)
3. /refine <issue-id>
   ↓ (requisitos detalhados)
4. /spec <issue-id>
   ↓ (PRD completo)
5. /check <prd-path> (opcional - validação final)
   ↓
6. Fase Architecture (próximos comandos: /draft-arch, /arch)
```

### Para Validação Rápida

```
1. /warm-up
   ↓
2. /check [descrição da feature]
   ↓ (se aprovado)
3. /collect ou /spec (dependendo da complexidade)
```

### Para Requisito Existente

```
1. /warm-up
   ↓
2. /refine <arquivo-ou-issue>
   ↓
3. /spec <arquivo-ou-issue>
```

---

## 🎯 Contexto do Projeto

### Produto
Site **iadojeitocerto.com.br** - Consultoria B2B vendendo Metodologia Metaspecs através de workshops imersivos.

### Objetivo
Gerar leads qualificados (CTOs, VPs de Eng, Tech Leads) para workshop de R$ 47.000.

### Stack Tecnológica
- **Framework**: Nuxt.js 3.10+ (Vue 3)
- **Linguagem**: TypeScript (strict mode)
- **Estilização**: Tailwind CSS 3+
- **Conteúdo**: Nuxt Content (markdown)
- **Componentes**: Atomic Design
- **Hospedagem**: Vercel

### Personas Principais
1. **CTO (Ricardo Silva)**: Foco em ROI, escalabilidade, vantagem competitiva
2. **VP Eng (Mariana Costa)**: Foco em padronização, processos, métricas
3. **Tech Lead (Bruno Oliveira)**: Foco em qualidade, produtividade, ferramentas práticas

### Métricas de Sucesso
- Taxa de conversão > 3%
- Leads qualificados > 70%
- Lighthouse score > 90
- Bounce rate < 60%

---

## 📚 Meta Specs de Referência

### Negócio (`/specs/business/`)
- **visao-produto.md**: Propósito, objetivos, proposta de valor
- **perfil-cliente.md**: ICP, 3 personas, jornada do cliente
- **features-valores.md**: 15 features em 3 fases (MVP, Fase 2, Fase 3)

### Técnico (`/specs/technical/`)
- **stack-tecnologica.md**: Vue 3, Nuxt, Tailwind, dependências
- **arquitetura.md**: SSG + ISR, Atomic Design, padrões de código
- **estrategia-testes.md**: Vitest + Playwright, casos prioritários
- **problemas-conhecidos.md**: Limitações técnicas aceitas, tech debt

---

## 🚨 Princípio Jidoka

> "Qualquer pessoa tem não apenas o direito, mas a **responsabilidade** de parar toda a linha quando detecta um problema"

**Aplicado aos comandos**:

Se você identificar **desalinhamento com meta specs** durante qualquer fase:
1. 🛑 **PARE** o trabalho
2. 📝 **DOCUMENTE** o conflito
3. 💬 **ALERTE** o usuário
4. ✅ **RESOLVA**: Ajuste meta spec OU ajuste requisito
5. ▶️ **CONTINUE** alinhado

**Nunca** prossiga sabendo que há desalinhamento.

---

## 💡 Dicas

### Para Product Managers
- Sempre rode `/warm-up` no início da sessão
- Use `/check` ANTES de especificar feature nova
- Valide features contra personas (qual CTO/VP/TechLead se beneficia?)
- Lembre-se: **Menos é mais**. Foque no MVP.

### Para Desenvolvedores
- `/warm-up` é obrigatório antes de qualquer comando
- Use `/spec` para gerar PRD completo antes de codificar
- Atomic Design é mandatório (Atoms → Molecules → Organisms)
- Sempre valide contra `problemas-conhecidos.md`

### Para Stakeholders
- Use `/check` para validar alinhamento estratégico de features
- PRDs gerados com `/spec` são documentos oficiais de requisitos
- Mudanças em features devem passar por `/refine` + `/spec` novamente

---

## 🔗 Próximos Comandos (Fases SPARC+DD)

Após completar fase **Specification (S)** com estes comandos, as próximas fases são:

- **P - PseudoCode**: (comandos a serem criados)
- **A - Architecture**: `/draft-arch`, `/arch`
- **R - Refinement**: `/start`, `/plan`
- **C - Completion**: `/work`, `/review`, `/troubleshoot`
- **D - Deployment**: `/docs`, `/code-review`, `/test-review`, `/pr`, `/deploy`
- **D - Documentation**: `/docs`, `/changelog`

---

**Última Atualização**: 2024-11-10
**Versão**: 1.0.0
**Status**: ✅ Ativo
