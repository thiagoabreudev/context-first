# Comandos de Engenharia - IA do Jeito Certo

Este diretório contém comandos customizados para as fases de **Refinement (R)**, **Completion (C)** e **Deployment (D)** da metodologia **SPARC+DD** aplicada ao projeto **iadojeitocerto.com.br**.

## 📋 Comandos Disponíveis

### `/start` - Iniciar Feature
**Fase**: Refinement (R)
**Propósito**: Preparar desenvolvimento de nova feature com análise e arquitetura.

**O que faz**:
- Cria feature branch (`feat/<feature-slug>`)
- Analisa requisitos (PRD, card do **Linear** projeto **iadojeitocerto**)
- Valida contra meta specs
- Faz perguntas de esclarecimento
- Cria `context.md` com entendimento completo
- Cria `architecture.md` com design técnico
- Configuração do Linear em `.claude/linear-config.md`

**Quando usar**:
- Após `/spec` gerar PRD completo
- Antes de começar a codificar
- Para iniciar nova feature

**Uso**:
```
/start <feature-slug>
```

**Output**:
- `.claude/sessions/<feature-slug>/context.md`
- Aguarda aprovação para criar `architecture.md`

---

### `/plan` - Planejar Implementação
**Fase**: Refinement (R)
**Propósito**: Dividir arquitetura em fases incrementais de desenvolvimento.

**O que faz**:
- Lê `context.md` e `architecture.md`
- Divide implementação em fases (2h cada)
- Cria `plan.md` com tarefas detalhadas
- Define ordem sequencial/paralela
- Estabelece checkpoints de teste

**Quando usar**:
- Após `/start` completar arquitetura
- Antes de iniciar `/work`
- Para features complexas com múltiplas partes

**Estrutura do Plan**:
```markdown
## FASE 1: Atoms (Componentes Básicos) [Não Iniciada ⏳]
- [ ] Criar AtomsButton.vue [Não Iniciada ⏳]
- [ ] Criar AtomsInput.vue [Não Iniciada ⏳]
- [ ] Testes unitários Atoms [Não Iniciada ⏳]

## FASE 2: Molecules (Componentes Compostos) [Não Iniciada ⏳]
- [ ] Criar MoleculesFormField.vue [Não Iniciada ⏳]
- [ ] Testes unitários Molecules [Não Iniciada ⏳]

## FASE 3: Organisms (Seções Completas) [Não Iniciada ⏳]
- [ ] Criar OrganismsContactForm.vue [Não Iniciada ⏳]
- [ ] Integração com API de envio [Não Iniciada ⏳]
- [ ] Testes E2E do fluxo completo [Não Iniciada ⏳]
```

**Uso**:
```
/plan <feature-slug>
```

**Output**: `.claude/sessions/<feature-slug>/plan.md`

---

### `/work` - Implementar Feature
**Fase**: Completion (C)
**Propósito**: Executar implementação seguindo o plano definido.

**O que faz**:
- Lê `plan.md` e identifica fase atual
- Implementa código conforme arquitetura
- Segue Atomic Design rigorosamente
- Executa testes (Vitest + Playwright)
- Atualiza `plan.md` com progresso
- Pausa ao fim de cada fase para aprovação

**Quando usar**:
- Após `/plan` criar plano completo
- Para implementar fase por fase
- Durante desenvolvimento ativo

**Validações Obrigatórias**:
- [ ] Código segue padrões Vue 3 + Composition API
- [ ] TypeScript strict mode
- [ ] Atomic Design respeitado
- [ ] Props tipadas com interface
- [ ] Emits declarados com defineEmits
- [ ] Testes unitários para lógica
- [ ] Testes E2E para fluxos críticos
- [ ] Performance targets atingidos

**Uso**:
```
/work .claude/sessions/<feature-slug>
```

**Output**: Código implementado + testes + `plan.md` atualizado

---

### `/pre-pr` - Preparar Pull Request
**Fase**: Deployment (D)
**Propósito**: Validações finais antes de abrir PR.

**O que faz**:
- Valida conformidade com meta specs
- Executa todos os testes (unit + E2E)
- Verifica bundle size e performance
- Valida acessibilidade (WCAG 2.1 AA)
- Executa linting e type checking
- Gera relatório de cobertura
- Atualiza documentação

**Quando usar**:
- Após completar todas as fases do `/work`
- Antes de `/pr`
- Para garantir qualidade final

**Checklist Automático**:
- [ ] Todos os testes passando
- [ ] Cobertura > 80% (unit), 100% (E2E críticos)
- [ ] Lighthouse score > 90
- [ ] Bundle size < 150kb (MVP)
- [ ] Sem erros TypeScript
- [ ] Sem warnings ESLint
- [ ] Acessibilidade validada
- [ ] Documentação atualizada

**Uso**:
```
/pre-pr
```

**Output**: Relatório de validação + correções necessárias

---

### `/pr` - Abrir Pull Request
**Fase**: Deployment (D)
**Propósito**: Criar PR no GitHub com descrição completa.

**O que faz**:
- Executa commit de todas as mudanças
- Move card do **Linear** projeto **iadojeitocerto** para "In Review"
- Cria PR no GitHub com template
- Aguarda code review automatizado
- Corrige issues identificados
- Faz push de correções

**Quando usar**:
- Após `/pre-pr` validar tudo
- Quando feature está 100% completa
- Para submeter para revisão

**Template de PR**:
```markdown
# [Feature]: [Nome da Feature]

## 📋 Resumo
[Descrição de 2-3 parágrafos]

## ✅ Validação contra Meta Specs
- [x] Alinhado com visao-produto.md
- [x] Atende persona de perfil-cliente.md
- [x] Listado em features-valores.md (Fase X)
- [x] Usa stack de stack-tecnologica.md
- [x] Segue padrões de arquitetura.md

## 🎨 Componentes Criados/Modificados
### Atoms
- `components/atoms/Button.vue`
- `components/atoms/Input.vue`

### Molecules
- `components/molecules/FormField.vue`

### Organisms
- `components/organisms/ContactForm.vue`

## 🧪 Testes
- Unit tests: 15 passando (cobertura 85%)
- E2E tests: 3 passando (100% fluxos críticos)

## 📊 Performance
- Lighthouse: 95
- Bundle size: +12kb
- LCP: 1.8s

## 📝 Checklist
- [x] Testes passando
- [x] TypeScript sem erros
- [x] ESLint sem warnings
- [x] Acessibilidade validada
- [x] Documentação atualizada
- [x] Meta specs validadas

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Uso**:
```
/pr
```

**Output**: PR aberto no GitHub + link

---

## 🔄 Fluxo Completo

### Desenvolvimento de Feature Nova

```
1. /warm-up
   ↓ (carregar meta specs)
2. /spec <requisito>
   ↓ (gerar PRD completo)
3. /start <feature-slug>
   ↓ (criar context.md + architecture.md)
4. /plan <feature-slug>
   ↓ (criar plan.md com fases)
5. /work .claude/sessions/<feature-slug>
   ↓ (implementar fase por fase)
6. /pre-pr
   ↓ (validar tudo)
7. /pr
   ↓ (abrir pull request)
```

### Retomar Feature Interrompida

```
1. /warm-up
   ↓
2. /work .claude/sessions/<feature-slug>
   ↓ (continua da última fase)
```

---

## 🎯 Contexto Técnico

### Stack Tecnológica
- **Framework**: Nuxt.js 3.10+ (Vue 3)
- **Linguagem**: TypeScript (strict mode)
- **Estilização**: Tailwind CSS 3+
- **Conteúdo**: Nuxt Content (markdown)
- **Validação**: Vee-Validate + Zod
- **Animações**: Vue Transitions + VueUse
- **Ícones**: Nuxt Icon + Iconify
- **Testes**: Vitest (unit) + Playwright (E2E)
- **Hospedagem**: Vercel

### Arquitetura Obrigatória: Atomic Design

```
components/
├── atoms/           # Elementos básicos (Button, Input, Icon)
├── molecules/       # Grupos de átomos (FormField, Card)
├── organisms/       # Seções completas (Header, Hero, ContactForm)
└── templates/       # Layouts (DefaultLayout, BlogLayout)

pages/              # Instâncias de templates (Nuxt auto-managed)
```

### Padrões de Código Vue 3

**Composables** (lógica reutilizável):
```typescript
// composables/useFormValidation.ts
export const useFormValidation = () => {
  const errors = ref<Record<string, string>>({})

  const validateEmail = (email: string): boolean => {
    // lógica de validação
    return isValid
  }

  return { errors, validateEmail }
}
```

**Componentes** (Atomic Design):
```vue
<!-- components/atoms/Button.vue -->
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <button
    :disabled="disabled"
    :class="buttonClasses"
    @click="emit('click', $event)"
  >
    <slot />
  </button>
</template>
```

### Performance Targets

| Métrica | Target MVP | Medição |
|---------|-----------|---------|
| Lighthouse Score | > 90 | Lighthouse CI |
| LCP (Largest Contentful Paint) | < 2s | Web Vitals |
| Bundle Size | < 150kb | Vite build |
| Cobertura Unit Tests | > 80% | Vitest coverage |
| Cobertura E2E Críticos | 100% | Playwright |

### Acessibilidade (WCAG 2.1 AA)

- [ ] Navegação por teclado
- [ ] Screen reader support
- [ ] Contraste adequado (mínimo 4.5:1)
- [ ] Labels em form inputs
- [ ] ARIA attributes quando necessário
- [ ] Focus visible

---

## 🚨 Validações Obrigatórias

### A Cada Fase do `/work`

1. **Antes de Codificar**:
   - [ ] Validar contra `architecture.md`
   - [ ] Confirmar Atomic Design level
   - [ ] Revisar padrões em `metaspecs/technical/arquitetura.md`

2. **Durante Codificação**:
   - [ ] TypeScript strict mode
   - [ ] Props e Emits tipados
   - [ ] Composition API (setup script)
   - [ ] Tailwind classes (sem CSS customizado)
   - [ ] Comentários JSDoc em funções complexas

3. **Após Codificação**:
   - [ ] Testes unitários (Vitest)
   - [ ] Testes E2E se fluxo crítico (Playwright)
   - [ ] Type checking (`npm run typecheck`)
   - [ ] Linting (`npm run lint`)

4. **Fim da Fase**:
   - [ ] Atualizar `plan.md` com progresso
   - [ ] Documentar decisões/aprendizados
   - [ ] Pausar e pedir aprovação do usuário
   - [ ] Commit da fase (`git commit -m "feat: fase X - [descrição]"`)

### Antes do `/pre-pr`

- [ ] Todas as fases do `plan.md` completadas ✅
- [ ] Todos os testes passando
- [ ] Performance targets atingidos
- [ ] Acessibilidade validada
- [ ] Documentação atualizada

---

## 💡 Dicas

### Para Desenvolvedores

- **Atomic Design é mandatório**: Sempre identifique o nível correto (Atom/Molecule/Organism)
- **TypeScript Strict**: Não use `any`, sempre tipagem completa
- **Composables > Mixins**: Use Composition API
- **Props Validation**: Sempre defina interface para props
- **Testes First**: Para fluxos críticos, escreva teste E2E antes de implementar
- **Performance Budget**: Monitore bundle size a cada nova dependência

### Para Atomic Design

**Como identificar o nível**:
- **Atom**: Pode ser decomposto? Não → Atom (Button, Input, Icon)
- **Molecule**: Combinação de 2+ átomos com função específica (FormField = Label + Input + ErrorText)
- **Organism**: Seção completa e identificável (Header, Hero, ContactForm)
- **Template**: Layout que compõe organismos (DefaultLayout, BlogLayout)
- **Page**: Instância de template com conteúdo real (index.vue, about.vue)

**Nomenclatura Auto-Import do Nuxt**:
```
components/atoms/Button.vue     → <AtomsButton />
components/molecules/Card.vue   → <MoleculesCard />
components/organisms/Hero.vue   → <OrganismsHero />
```

### Para Testes

**Unit Tests (Vitest)**:
```typescript
// tests/unit/composables/useFormValidation.spec.ts
import { describe, it, expect } from 'vitest'
import { useFormValidation } from '~/composables/useFormValidation'

describe('useFormValidation', () => {
  it('valida email corporativo corretamente', () => {
    const { validateEmail } = useFormValidation()
    expect(validateEmail('user@company.com')).toBe(true)
    expect(validateEmail('user@gmail.com')).toBe(false)
  })
})
```

**E2E Tests (Playwright)**:
```typescript
// tests/e2e/contact-form.spec.ts
import { test, expect } from '@playwright/test'

test('submete formulário de contato com sucesso', async ({ page }) => {
  await page.goto('/contato')

  await page.fill('[name="name"]', 'Ricardo Silva')
  await page.fill('[name="email"]', 'ricardo@empresa.com')
  await page.click('button[type="submit"]')

  await expect(page.locator('.success-message')).toBeVisible()
})
```

---

## 🔗 Links Relacionados

### Documentação Interna
- [Meta Specs de Negócio](../../metaspecs/businnes/)
- [Meta Specs Técnicas](../../metaspecs/technical/)
- [CLAUDE.md](../../CLAUDE.md)
- [Comandos de Produto](../products/)

### Documentação Externa
- **Vue 3**: https://vuejs.org/guide/introduction.html
- **Nuxt 3**: https://nuxt.com/docs/getting-started/introduction
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Atomic Design**: https://atomicdesign.bradfrost.com/chapter-2/
- **Vitest**: https://vitest.dev/
- **Playwright**: https://playwright.dev/
- **TypeScript**: https://www.typescriptlang.org/docs/

---

**Última Atualização**: 2024-11-10
**Versão**: 1.0.0
**Status**: ✅ Ativo
