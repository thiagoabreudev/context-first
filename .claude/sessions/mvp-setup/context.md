# Context: MVP do Site iadojeitocerto.com.br

**Feature ID**: MVP-001
**Status**: In Progress
**Branch**: feat/mvp-setup
**Criado em**: 2024-11-10

---

## Por Que

### Valor de Negócio
Criar o site que vende a consultoria "IA do Jeito Certo" e captura leads qualificados para o workshop de R$ 47.000. O site é simultaneamente:
- **Produto**: Landing page de vendas de alta conversão
- **Case Study**: Validação prática da Metodologia Metaspecs (usando a metodologia para construir o site que vende a metodologia)
- **Gerador de Leads**: Formulário com validação corporativa para filtrar público B2B

### Personas Atendidas
1. **CTO** (Ricardo Silva, 35-50 anos)
   - Busca ROI, escalabilidade, vantagem competitiva
   - Decisor final de compra

2. **VP de Engenharia** (Mariana Costa, 32-45 anos)
   - Foco em padronização, processos, métricas
   - Influenciador de decisão

3. **Tech Lead** (Bruno Oliveira, 28-40 anos)
   - Quer qualidade, produtividade, ferramentas práticas
   - Usuário direto da metodologia

### Fase do Produto
🔴 **MVP - Crítico**

### Métricas Impactadas
- **Taxa de conversão**: > 3% (visita → lead)
- **Qualidade de leads**: > 70% leads qualificados (email corporativo)
- **Performance**: Lighthouse score > 90
- **Engagement**: Bounce rate < 60%, Form fill rate > 10%

---

## O Que

### Funcionalidades Principais (9 Features MVP)

#### 1. Landing Page Hero Section
**O que é**: Seção inicial impactante que captura atenção e comunica proposta de valor
**Componentes**:
- Headline: "Pare de 'Conversar' com a IA. Comece a Construir com Engenharia"
- Subheadline: Proposta de valor (transformar vibe coding em engenharia)
- CTA primário: "Agende uma Análise Gratuita"
- Visual: Ilustração ou imagem de código + IA

#### 2. Seção "O Problema"
**O que é**: Identificação das dores do público-alvo
**Componentes**:
- Dores do vibe coding (inconsistência, retrabalho, baixa previsibilidade)
- Estatísticas reais: "76% dos projetos com agentes falham"
- Identificação com personas: "Se você é CTO, VP Eng ou Tech Lead..."

#### 3. Seção "A Solução" (Metodologia Metaspecs)
**O que é**: Apresentação dos 2 pilares da metodologia
**Componentes**:
- Pilar 1: Context Engineering + Framework WSCI
- Pilar 2: Spec-Driven Development
- Benefícios mensuráveis
- CTA secundário: Download do Whitepaper

#### 4. Seção "Como Funciona" (Workshop)
**O que é**: Detalhes do serviço oferecido
**Componentes**:
- Formato: 2 dias intensivos
- Estrutura: 40% teoria + 60% prática
- Entregáveis concretos
- Metodologia de ensino (hands-on com desafios reais)

#### 5. Seção "Para Quem é?"
**O que é**: Qualificação do público-alvo (ICP)
**Componentes**:
- 3 Personas com cards visuais
- ICP: Startups Série A+, Scale-ups, times 10-100+ devs
- Gatilhos de compra (quando contratar)

#### 6. Seção "A Oferta" (Pricing)
**O que é**: Informações de investimento e valor
**Componentes**:
- Valor: R$ 47.000
- O que está incluído (2 dias, material, follow-up)
- Garantias
- Comparação investimento vs ROI

#### 7. Call-to-Action Final
**O que é**: CTA forte antes do formulário
**Componentes**:
- Headline de conversão
- Senso de urgência (vagas limitadas)
- Proof points finais
- Botão para formulário

#### 8. Formulário de Captura de Leads
**O que é**: Formulário validado para qualificação de leads
**Componentes**:
- Campos: Nome, Email (corporativo), Empresa, Cargo, Mensagem
- Validação client-side e server-side (Zod)
- Bloqueio de emails pessoais (Gmail, Hotmail, Yahoo)
- Confirmação visual de envio
- Integração com API route + Resend (envio de email)

#### 9. Footer Profissional
**O que é**: Footer completo com navegação e info legal
**Componentes**:
- Links de navegação
- Informações de contato
- Links sociais
- Legal (Privacidade, Termos de Uso)

---

## Como

### Abordagem Técnica

**Framework**: Nuxt.js 3.10+ (Vue 3)
**Renderização**: SSG (Static Site Generation) para landing page
**Arquitetura**: Atomic Design (Atoms → Molecules → Organisms → Templates → Pages)

### Componentes a Criar

#### Átomos (Atoms)
```
components/atoms/
├── Button.vue          # Botões reutilizáveis (primary, secondary, outline)
├── Input.vue           # Input de texto
├── Label.vue           # Labels de formulário
├── Heading.vue         # Headings tipográficos (h1-h6)
├── Text.vue            # Parágrafos e textos
└── Icon.vue            # Wrapper para Nuxt Icon
```

#### Moléculas (Molecules)
```
components/molecules/
├── FormField.vue       # Input + Label + Error message
├── Card.vue            # Card genérico (container)
├── StatCard.vue        # Card com estatística
└── PersonaCard.vue     # Card de persona
```

#### Organismos (Organisms)
```
components/organisms/
├── Header.vue          # Header do site (logo + nav)
├── Footer.vue          # Footer completo
├── Hero.vue            # Seção Hero
├── ProblemSection.vue  # Seção Problema
├── SolutionSection.vue # Seção Solução
├── HowItWorksSection.vue # Seção Como Funciona
├── ForWhoSection.vue   # Seção Para Quem
├── PricingSection.vue  # Seção Pricing
├── CTASection.vue      # CTA final
└── ContactForm.vue     # Formulário completo
```

#### Pages
```
pages/
└── index.vue           # Landing page (composição de todos os organismos)
```

### Nível Atomic Design
- **Landing Page**: Composition de Organisms em Page
- **Organisms**: Seções completas (Hero, Problem, Solution, etc.)
- **Molecules**: Componentes compostos (FormField, Card)
- **Atoms**: Elementos base (Button, Input, Heading)

### Integrações

#### 1. Formulário → Backend
```
Client (ContactForm.vue)
  → POST /api/contact
    → Validação (Zod schema)
    → Rate Limiting
    → Send Email (Resend API)
    → Return success/error
```

#### 2. Analytics
- Google Analytics 4: tracking de eventos (pageview, form_submit, whitepaper_download)
- Vercel Analytics: Core Web Vitals

#### 3. Email (Resend)
- Envio de notificação ao recebermos lead
- Template HTML com dados do formulário

---

## Validação contra Meta Specs

### ✅ Negócio (Business)

- [x] **visao-produto.md**: Alinhado
  - Proposta de valor: Transformar vibe coding em engenharia ✅
  - Objetivo: Gerar leads qualificados ✅
  - Diferenciação: Metodologia proprietária (Metaspecs) ✅

- [x] **perfil-cliente.md**: Atende 3 personas
  - CTO: Seção de ROI e pricing ✅
  - VP Eng: Seção de processos e metodologia ✅
  - Tech Lead: Seção de qualidade e ferramentas ✅

- [x] **features-valores.md**: Todas as 9 features MVP listadas
  - Hero Section ✅
  - Problema ✅
  - Solução ✅
  - Como Funciona ✅
  - Para Quem ✅
  - Pricing ✅
  - CTA Final ✅
  - Formulário ✅
  - Footer ✅

### ✅ Técnico (Technical)

- [x] **stack-tecnologica.md**: Stack aprovada
  - Nuxt.js 3.10+ ✅
  - TypeScript strict mode ✅
  - Tailwind CSS 3+ ✅
  - Vee-Validate + Zod ✅
  - Resend (email) ✅
  - Nuxt Icon ✅
  - VueUse ✅

- [x] **arquitetura.md**: Padrões seguidos
  - SSG (Static Site Generation) ✅
  - Atomic Design ✅
  - Composables > Store ✅
  - Server Routes para API ✅
  - Performance targets definidos ✅

- [x] **problemas-conhecidos.md**: Sem conflitos
  - Validação de email simplificada (sem DNS check) - Documentado ✅
  - Rate limiting baseado em IP - Documentado ✅
  - Sem CAPTCHA no MVP - Aceitável ✅

---

## Dependências

### Runtime (package.json)
```json
{
  "nuxt": "^3.10.0",
  "vue": "^3.4.0",
  "@nuxtjs/tailwindcss": "^6.11.0",
  "@nuxt/icon": "^1.0.0",
  "@vueuse/core": "^10.7.0",
  "vee-validate": "^4.12.0",
  "@vee-validate/zod": "^4.12.0",
  "zod": "^3.22.0",
  "resend": "^3.0.0"
}
```

### DevDependencies
```json
{
  "typescript": "^5.3.0",
  "@nuxt/devtools": "^1.0.0",
  "prettier": "^3.2.0",
  "prettier-plugin-tailwindcss": "^0.5.0",
  "@tailwindcss/typography": "^0.5.10",
  "@tailwindcss/forms": "^0.5.7"
}
```

### Serviços Externos
- **Resend**: Envio de emails (contato do formulário)
- **Vercel**: Hosting + Analytics
- **Google Analytics**: Tracking de eventos

---

## Restrições

### Técnicas
1. **TypeScript strict mode**: Sem uso de `any`
2. **Tailwind CSS only**: Sem CSS customizado (exceto casos raros)
3. **Bundle size**: < 150kb total
4. **Performance**:
   - LCP < 2.5s
   - FID < 100ms
   - CLS < 0.1

### De Negócio
1. **Email corporativo obrigatório**: Bloquear @gmail.com, @hotmail.com, @yahoo.com
2. **Formulário simples**: Sem múltiplas etapas (MVP)
3. **Sem autenticação**: Landing page pública, sem login
4. **Sem blog no MVP**: Apenas landing page (blog vem na Fase 2)

### Performance Targets
| Métrica | Target | Crítico |
|---------|--------|---------|
| Lighthouse Performance | > 95 | > 90 |
| FCP | < 1.5s | < 2.5s |
| LCP | < 2.0s | < 2.5s |
| CLS | < 0.05 | < 0.1 |
| FID | < 50ms | < 100ms |
| Bundle Size | < 150kb | < 200kb |

---

## Testes

### E2E Críticos (Playwright)
1. **Fluxo de Formulário**:
   - Preencher formulário com dados válidos → Sucesso ✅
   - Tentar enviar com email pessoal (@gmail.com) → Erro de validação ✅
   - Campos obrigatórios vazios → Múltiplos erros exibidos ✅

2. **Navigation**:
   - Click em CTA Hero → Scroll to formulário ✅
   - Click em "Download Whitepaper" → Download triggered ✅

3. **Responsividade**:
   - Testar mobile, tablet, desktop ✅

### Unit Tests (Vitest)
1. **Átomos**:
   - Button: variantes, disabled state, eventos ✅
   - Input: tipos, validação, eventos ✅

2. **Validação**:
   - Schema Zod: email corporativo, campos obrigatórios ✅
   - Composable de validação ✅

### Cobertura Esperada
- **MVP**: E2E 100% fluxos críticos, Unit > 60%
- **Pós-MVP**: Unit > 80%

---

## Assets Necessários

### Imagens
- [ ] Logo iadojeitocerto.com.br (SVG)
- [ ] Hero image/ilustração (IA + código)
- [ ] Ilustração Problema (código caótico)
- [ ] Ilustração Solução (código organizado)
- [ ] Fotos de personas (ou ilustrações)
- [ ] OG image (Open Graph, 1200x630px)
- [ ] Favicon (múltiplos tamanhos)

### Documentos
- [ ] Whitepaper PDF ("Metodologia Metaspecs")

### Conteúdo
- [x] Copywriting da landing page (disponível em `/docs/Conteúdo da Landing Page.md`)

---

## Próximos Passos

Após aprovação deste contexto:
1. **Criar architecture.md** - Design técnico detalhado dos componentes
2. **Setup do Projeto** - Inicializar Nuxt 3 + configurações
3. **Criar plan.md** - Plano de implementação faseado
4. **Implementar fase por fase** - Desenvolvimento incremental

---

## Perguntas de Esclarecimento

### 1. Assets de Design ✅
**P**: Temos logo e ilustrações prontas ou precisamos criar/usar placeholders no MVP?
**R**: Não temos. Usar placeholders no MVP.
**Ação**: Criar componentes com placeholders SVG/texto que podem ser substituídos facilmente depois.

### 2. Whitepaper PDF ✅
**P**: O whitepaper já está pronto em PDF ou vamos usar um dos arquivos markdown em `/docs/` como base?
**R**: Criar a partir dos docs existentes.
**Ação**: Converter `/docs/Whitepaper Técnico: A Metodologia Metaspecs.md` para PDF formatado. Tarefa pós-implementação.

### 3. Domínio e Email ✅
**P**: O domínio `iadojeitocerto.com.br` já está registrado? Email `contato@iadojeitocerto.com.br` configurado no Resend?
**R**: Sim, configurado.
**Ação**: Usar `contato@iadojeitocerto.com.br` como destinatário no formulário.

### 4. Google Analytics ✅
**P**: Já temos GA4 Measurement ID ou precisamos criar?
**R**: Criar durante o setup. Por enquanto, preparar integração mas deixar opcional.
**Ação**: Configurar GA4 como opcional via env var `GA_MEASUREMENT_ID`.

### 5. Formulário - Destino ✅
**P**: O formulário envia email para `contato@iadojeitocerto.com.br` apenas, ou também salva em algum CRM/planilha?
**R**: MVP apenas email. CRM na Fase 2.
**Ação**: Endpoint `/api/contact` envia email via Resend. Integração com CRM (Linear, HubSpot) fica para Fase 2.

---

**Status**: ✅ Contexto completo - Aguardando aprovação do usuário
