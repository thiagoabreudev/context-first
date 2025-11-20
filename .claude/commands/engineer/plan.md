# Engineer Plan - IA do Jeito Certo

Este comando cria um plano de implementação detalhado para uma funcionalidade do projeto **iadojeitocerto.com.br**.

<arguments>
#$ARGUMENTS
</arguments>

## 🎯 Contexto

Você já completou a fase `/start` e tem:
- `.claude/sessions/<feature-slug>/context.md` - Entendimento completo
- `.claude/sessions/<feature-slug>/architecture.md` - Design técnico

Agora você criará o **plan.md** dividindo a implementação em fases incrementais.

## 📋 Objetivo

Criar plano de implementação faseado que permite:
- Construir feature incrementalmente
- Testar cada fase conforme avançamos
- Retomar trabalho se sessão for interrompida
- Cada fase completável em ~2 horas

## 🔍 Análise

Leia os arquivos `context.md` e `architecture.md` na pasta `.claude/sessions/<feature-slug>` se ainda não tiver feito.

## 📝 Template do Plan.md

```markdown
# [NOME DA FUNCIONALIDADE]

**Importante**: Atualize este arquivo conforme progride na implementação.

---

## FASE 1: Atoms (Componentes Básicos) [Não Iniciada ⏳]

### Descrição
Criar componentes atômicos (elementos mais básicos da interface) que serão reutilizados em toda a feature.

### Tarefas

#### 1.1 - Criar AtomsButton.vue [Não Iniciada ⏳]
- Props: variant, size, disabled
- Emits: click
- Variantes: primary, secondary, outline
- Tamanhos: sm, md, lg
- TypeScript strict mode
- Tailwind classes

**Arquivos**:
- `components/atoms/Button.vue`

**Testes**:
- Unit test: Variantes renderizam classes corretas
- Unit test: Emit de click funciona
- Unit test: Disabled previne click

#### 1.2 - Criar AtomsInput.vue [Não Iniciada ⏳]
- Props: type, placeholder, modelValue, error, disabled
- Emits: update:modelValue
- Tipos: text, email, tel
- Estados: normal, error, disabled
- TypeScript strict mode
- Tailwind classes

**Arquivos**:
- `components/atoms/Input.vue`

**Testes**:
- Unit test: v-model funciona (two-way binding)
- Unit test: Estados de erro renderizam corretamente

#### 1.3 - Testes Unitários Atoms [Não Iniciada ⏳]
- Configurar Vitest se necessário
- Rodar testes: `npm run test:unit`
- Cobertura target: 100% para Atoms

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 2: Molecules (Componentes Compostos) [Não Iniciada ⏳]

### Descrição
Combinar átomos em moléculas funcionais.

### Tarefas

#### 2.1 - Criar MoleculesFormField.vue [Não Iniciada ⏳]
- Combina: AtomsLabel + AtomsInput + AtomsText (error)
- Props: label, modelValue, error, type, required
- Emits: update:modelValue
- Layout vertical (label → input → error)
- Tailwind spacing

**Arquivos**:
- `components/molecules/FormField.vue`

**Composição**:
```vue
<AtomsLabel :required="required">{{ label }}</AtomsLabel>
<AtomsInput v-model="modelValue" :type="type" :error="!!error" />
<AtomsText v-if="error" variant="error">{{ error }}</AtomsText>
```

**Testes**:
- Unit test: Label obrigatório renderiza asterisco
- Unit test: Erro exibe mensagem correta

#### 2.2 - Criar MoleculesCard.vue (se necessário) [Não Iniciada ⏳]
- Props: title, variant
- Slots: default, footer
- Variantes: elevated, outlined, flat
- Tailwind shadow e border

**Arquivos**:
- `components/molecules/Card.vue`

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 3: Organisms (Seções Completas) [Não Iniciada ⏳]

### Descrição
Criar organismos que formam seções completas e identificáveis da interface.

### Tarefas

#### 3.1 - Criar OrganismsContactForm.vue [Não Iniciada ⏳]
- Combina: Múltiplos MoleculesFormField + AtomsButton
- Composable: useFormValidation (validação com Zod)
- API: Envio via server route `/api/contact`
- Estados: idle, submitting, success, error
- Validações: email corporativo, campos obrigatórios

**Arquivos**:
- `components/organisms/ContactForm.vue`
- `composables/useFormValidation.ts`
- `server/api/contact.post.ts`

**Schema Zod**:
```typescript
const contactSchema = z.object({
  name: z.string().min(3),
  email: z.string().email().refine(isNotPersonalEmail),
  company: z.string().min(2),
  role: z.enum(['CTO', 'VP_ENG', 'TECH_LEAD', 'OTHER']),
  message: z.string().min(10)
})
```

**Testes**:
- Unit test: Validação Zod funciona
- Unit test: isNotPersonalEmail rejeita @gmail.com
- E2E test: Fluxo completo de submissão **[CRÍTICO]**

#### 3.2 - Integração com API de Envio [Não Iniciada ⏳]
- Server route: `/server/api/contact.post.ts`
- Rate limiting: 5 requests/min por IP
- Sanitização de inputs
- Envio de email via Resend ou similar

**Arquivos**:
- `server/api/contact.post.ts`
- `server/utils/rateLimiter.ts`

**Testes**:
- Integration test: API route funciona
- Integration test: Rate limiting previne spam

#### 3.3 - Testes E2E do Fluxo Completo [Não Iniciada ⏳]
- Playwright: Preencher formulário e submeter
- Validar mensagem de sucesso
- Validar mensagem de erro (email inválido)
- Validar rate limiting

**Arquivos**:
- `tests/e2e/contact-form.spec.ts`

**Casos de Teste E2E**:
```typescript
test('submete formulário com sucesso', async ({ page }) => {
  // Preencher e enviar
})

test('valida email corporativo', async ({ page }) => {
  // Testar rejeição de @gmail.com
})

test('exibe erro de rate limit', async ({ page }) => {
  // Submeter 6x rapidamente
})
```

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 4: Pages e SEO [Não Iniciada ⏳]

### Descrição
Integrar organism na página e configurar SEO.

### Tarefas

#### 4.1 - Integrar ContactForm em /contato [Não Iniciada ⏳]
- Página: `pages/contato.vue`
- Layout: DefaultLayout
- SEO: Meta tags completas
- Structured data: ContactPage schema

**Arquivos**:
- `pages/contato.vue`

**SEO**:
```typescript
useSeoMeta({
  title: 'Contato - IA do Jeito Certo',
  description: 'Entre em contato para agendar análise...',
  ogTitle: 'Contato - IA do Jeito Certo',
  ogDescription: '...',
  ogImage: '/og-image.jpg'
})
```

#### 4.2 - Performance e Acessibilidade [Não Iniciada ⏳]
- Lighthouse: Target > 90
- WCAG 2.1 AA: Validar com axe-core
- Navegação por teclado
- Screen reader support

**Validações**:
- [ ] Lighthouse Performance > 90
- [ ] Lighthouse Accessibility > 95
- [ ] Navegação por Tab funciona
- [ ] Labels e ARIA attributes corretos

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## ✅ Checklist Final

Antes de considerar a feature completa:

### Código
- [ ] Todos os componentes seguem Atomic Design
- [ ] TypeScript strict mode (sem `any`)
- [ ] Props e Emits tipados
- [ ] Tailwind CSS (sem CSS customizado)
- [ ] Composables para lógica reutilizável

### Testes
- [ ] Unit tests > 80% cobertura
- [ ] E2E tests 100% fluxos críticos
- [ ] Todos os testes passando

### Performance
- [ ] Bundle size < 150kb (MVP)
- [ ] Lighthouse > 90
- [ ] LCP < 2s

### Acessibilidade
- [ ] WCAG 2.1 AA compliance
- [ ] Navegação por teclado
- [ ] Screen reader testado

### SEO
- [ ] Meta tags completas
- [ ] Structured data (se aplicável)
- [ ] Sitemap atualizado

### Documentação
- [ ] Componentes documentados (JSDoc)
- [ ] README atualizado (se necessário)
- [ ] CHANGELOG.md atualizado

---

## 📊 Ordem de Execução

### Sequencial (deve seguir ordem)
1. FASE 1 → FASE 2 → FASE 3 → FASE 4
   (Atomic Design: Atoms → Molecules → Organisms → Pages)

### Paralelo (pode fazer junto)
- Dentro de cada fase, tarefas podem ser paralelas
- Exemplo: AtomsButton e AtomsInput podem ser criados juntos

---

## 🔄 Status Legend

- ⏳ **Não Iniciada**: Ainda não começou
- ⏰ **Em Progresso**: Trabalhando atualmente
- ✅ **Completada**: Finalizada e testada
- ⚠️ **Bloqueada**: Aguardando dependência

---

**Criado**: [DATA]
**Última Atualização**: [DATA]
**Feature Slug**: <feature-slug>
```

## 🎯 Princípios do Planejamento

### Atomic Design SEMPRE

Ordem OBRIGATÓRIA:
1. **Atoms** (elementos básicos)
2. **Molecules** (combinação de atoms)
3. **Organisms** (seções completas)
4. **Templates** (layouts)
5. **Pages** (instâncias com conteúdo)

### Testes em Cada Fase

- **Atoms/Molecules**: Unit tests (Vitest)
- **Organisms**: Unit tests + Integration tests
- **Pages**: E2E tests (Playwright) para fluxos críticos

### Tarefas Pequenas

Cada tarefa deve ser:
- Completável em 30-60 minutos
- Testável isoladamente
- Commitável independentemente

## 🚨 Validação

Antes de salvar `plan.md`, certifique-se:
- [ ] Segue Atomic Design rigorosamente
- [ ] Cada fase tem testes definidos
- [ ] Ordem sequencial/paralela está clara
- [ ] Checklist final está completo
- [ ] Comentários placeholder existem

## 💾 Salvamento

Após criar o plano, salve em:
- `.claude/sessions/<feature-slug>/plan.md`

E informe ao humano que você está pronto para prosseguir para `/work`.
