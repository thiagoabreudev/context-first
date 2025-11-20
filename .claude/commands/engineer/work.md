# Engineer Work - IA do Jeito Certo

Estamos trabalhando em uma funcionalidade especificada na seguinte pasta:

<folder>
#$ARGUMENTS
</folder>

## 🎯 Objetivo

Implementar a feature incrementalmente, fase por fase, seguindo o plano definido e garantindo qualidade em cada etapa.

## 📋 Processo

### 1. Ler Documentação da Feature

Leia todos os arquivos markdown na pasta `.claude/sessions/<feature-slug>/`:
- `context.md` - Entendimento e validação contra meta specs
- `architecture.md` - Design técnico e componentes
- `plan.md` - Plano de implementação faseado

### 2. Identificar Fase Atual

Revise `plan.md` e identifique qual fase está atualmente **Em Progresso ⏰**.

Se nenhuma fase estiver em progresso, identifique a primeira fase **Não Iniciada ⏳** e proponha iniciar.

### 3. Apresentar Plano ao Usuário

Antes de começar a codificar, apresente ao usuário:

```markdown
## 📋 Próxima Fase

**Fase**: [Número e nome da fase]
**Status Atual**: Não Iniciada ⏳

### Tarefas
1. [Tarefa 1]
2. [Tarefa 2]
3. [Tarefa 3]

### Abordagem
[Explicar como você vai abordar esta fase]

### Validações
- [ ] TypeScript strict mode
- [ ] Atomic Design [Atoms/Molecules/Organisms]
- [ ] Tailwind CSS
- [ ] Testes [Unit/E2E]

**Posso começar?**
```

Aguarde aprovação do usuário antes de começar.

---

## 🔧 Implementação

### Padrões Obrigatórios

#### Vue 3 + Composition API

**Estrutura de Componente**:
```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed } from 'vue'
import type { PropType } from 'vue'

// 2. Interface de Props
interface Props {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

// 3. Props e Emits
const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
  change: [value: string]
}>()

// 4. Estado Reativo
const isHovered = ref(false)

// 5. Computed Properties
const buttonClasses = computed(() => ({
  'px-4 py-2': props.size === 'sm',
  'px-6 py-3': props.size === 'md',
  'px-8 py-4': props.size === 'lg',
  'bg-primary-600': props.variant === 'primary',
  'bg-gray-100': props.variant === 'secondary',
  'opacity-50 cursor-not-allowed': props.disabled
}))

// 6. Métodos
const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <slot />
  </button>
</template>
```

#### TypeScript Strict Mode

**NUNCA use `any`**:
```typescript
// ❌ ERRADO
const data: any = {}

// ✅ CORRETO
interface Data {
  name: string
  value: number
}
const data: Data = { name: 'test', value: 42 }
```

**Type Guards para Validação**:
```typescript
function isNotPersonalEmail(email: string): boolean {
  const personalDomains = ['gmail.com', 'hotmail.com', 'yahoo.com']
  const domain = email.split('@')[1]
  return !personalDomains.includes(domain)
}
```

#### Composables para Lógica Reutilizável

**Estrutura**:
```typescript
// composables/useFormValidation.ts
import { ref, computed } from 'vue'
import { z } from 'zod'

export const useFormValidation = <T extends z.ZodType>(schema: T) => {
  const errors = ref<Record<string, string>>({})
  const isValid = computed(() => Object.keys(errors.value).length === 0)

  const validate = (data: z.infer<T>): boolean => {
    try {
      schema.parse(data)
      errors.value = {}
      return true
    } catch (error) {
      if (error instanceof z.ZodError) {
        errors.value = error.flatten().fieldErrors as Record<string, string>
      }
      return false
    }
  }

  return {
    errors,
    isValid,
    validate
  }
}
```

#### Tailwind CSS (SEM CSS customizado)

**Classes utilitárias SEMPRE**:
```vue
<template>
  <!-- ✅ CORRETO: Tailwind classes -->
  <div class="flex flex-col gap-4 p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold text-gray-900">
      Título
    </h2>
  </div>

  <!-- ❌ ERRADO: CSS customizado -->
  <div class="custom-container">
    <h2 class="custom-title">Título</h2>
  </div>
</template>

<style scoped>
/* ❌ NUNCA fazer isso (exceto casos MUITO raros) */
.custom-container {
  display: flex;
  padding: 1.5rem;
}
</style>
```

---

## 🧪 Testes

### Unit Tests (Vitest)

**Estrutura de Teste**:
```typescript
// tests/unit/components/atoms/Button.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from '~/components/atoms/Button.vue'

describe('AtomsButton', () => {
  it('renderiza com variante primary', () => {
    const wrapper = mount(Button, {
      props: { variant: 'primary' }
    })
    expect(wrapper.classes()).toContain('bg-primary-600')
  })

  it('emite evento click quando clicado', async () => {
    const wrapper = mount(Button)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('não emite click quando disabled', async () => {
    const wrapper = mount(Button, {
      props: { disabled: true }
    })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeFalsy()
  })
})
```

**Rodar Testes**:
```bash
npm run test:unit
npm run test:unit -- --coverage
```

### E2E Tests (Playwright)

**Estrutura de Teste**:
```typescript
// tests/e2e/contact-form.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Formulário de Contato', () => {
  test('submete formulário com sucesso', async ({ page }) => {
    await page.goto('/contato')

    // Preencher formulário
    await page.fill('[name="name"]', 'Ricardo Silva')
    await page.fill('[name="email"]', 'ricardo@empresa.com.br')
    await page.fill('[name="company"]', 'Empresa Tech LTDA')
    await page.selectOption('[name="role"]', 'CTO')
    await page.fill('[name="message"]', 'Gostaria de agendar uma análise.')

    // Submeter
    await page.click('button[type="submit"]')

    // Validar sucesso
    await expect(page.locator('.success-message')).toBeVisible()
    await expect(page.locator('.success-message')).toContainText('Mensagem enviada')
  })

  test('valida email corporativo', async ({ page }) => {
    await page.goto('/contato')

    await page.fill('[name="email"]', 'teste@gmail.com')
    await page.blur('[name="email"]')

    await expect(page.locator('.error-message')).toContainText('email corporativo')
  })

  test('valida campos obrigatórios', async ({ page }) => {
    await page.goto('/contato')

    await page.click('button[type="submit"]')

    // Deve exibir erros
    await expect(page.locator('.error-message')).toHaveCount(4) // name, email, company, message
  })
})
```

**Rodar Testes E2E**:
```bash
npm run test:e2e
npm run test:e2e -- --headed  # Com interface gráfica
```

---

## ✅ Checklist de Qualidade (A Cada Tarefa)

### Antes de Codificar
- [ ] Li e entendi a tarefa no `plan.md`
- [ ] Identifiquei nível Atomic Design (Atom/Molecule/Organism)
- [ ] Revisei padrões em `metaspecs/technical/arquitetura.md`

### Durante Codificação
- [ ] TypeScript strict mode (sem `any`)
- [ ] Props tipadas com interface
- [ ] Emits declarados com defineEmits
- [ ] Tailwind CSS (sem style tags)
- [ ] Composables para lógica complexa
- [ ] Comentários JSDoc em funções complexas

### Após Codificação
- [ ] Type checking: `npm run typecheck`
- [ ] Linting: `npm run lint`
- [ ] Testes escritos e passando
- [ ] Componente funciona no browser (teste manual)

### Fim da Tarefa
- [ ] Atualizar `plan.md` marcando tarefa como ✅
- [ ] Adicionar comentários sobre decisões/aprendizados
- [ ] Pausar e pedir aprovação do usuário
- [ ] Commit: `git commit -m "feat(atoms): adicionar Button component"`

---

## 🔄 Fluxo de Trabalho Recomendado

### Ao Iniciar uma Fase

1. **Revisar** `plan.md` e entender todas as tarefas da fase
2. **Marcar fase** como **Em Progresso ⏰** no `plan.md`
3. **Apresentar** plano ao usuário
4. **Aguardar** aprovação

### Durante uma Tarefa

1. **Implementar** código conforme padrões
2. **Testar** manualmente no browser
3. **Escrever** testes (unit ou E2E)
4. **Validar** com type checking e linting
5. **Apresentar** ao usuário para aprovação

### Ao Finalizar uma Tarefa

1. **Marcar** tarefa como **Completada ✅** no `plan.md`
2. **Adicionar** comentários sobre decisões
3. **Commit** da tarefa
4. **Pausar** e pedir aprovação do usuário antes de próxima tarefa

### Ao Finalizar uma Fase

1. **Validar** que todas as tarefas estão ✅
2. **Executar** todos os testes da fase
3. **Verificar** checklist de qualidade
4. **Marcar** fase como **Completada ✅** no `plan.md`
5. **Commit** da fase completa
6. **Pausar** e pedir aprovação antes de próxima fase

---

## 🚨 Regras de Bloqueio

### 🔴 CRÍTICO - NUNCA Prosseguir Se

- [ ] TypeScript tem erros (`npm run typecheck` falha)
- [ ] Testes estão falhando
- [ ] Violação de Atomic Design (ex: Organism usando outro Organism diretamente)
- [ ] Uso de `any` em TypeScript
- [ ] CSS customizado sem justificativa forte

### 🟡 IMPORTANTE - Corrigir Antes de PR

- [ ] Falta de type hints em Props/Emits
- [ ] Falta de testes para lógica complexa
- [ ] Falta de JSDoc em funções complexas
- [ ] Performance target não atingido (bundle size, LCP)

### 🟢 SUGESTÃO - Pode Prosseguir mas Anotar

- [ ] Oportunidades de extração para composable
- [ ] Possível refatoração futura
- [ ] Magic numbers (usar constantes)

---

## 💾 Atualização do Plan.md

**A CADA tarefa completada**, atualize `plan.md`:

```markdown
#### 1.1 - Criar AtomsButton.vue [Completada ✅]
- Props: variant, size, disabled
- Emits: click
- Variantes: primary, secondary, outline
- Tamanhos: sm, md, lg
- TypeScript strict mode
- Tailwind classes

**Arquivos**:
- `components/atoms/Button.vue` ✅

**Testes**:
- Unit test: Variantes renderizam classes corretas ✅
- Unit test: Emit de click funciona ✅
- Unit test: Disabled previne click ✅

**Comentários**:
- Decisão: Usar computed property para classes dinâmicas (melhor performance)
- Aprendizado: defineEmits com TypeScript requer generic type
```

---

## 📊 Quando Pausar e Pedir Aprovação

**SEMPRE pausar após**:
- ✅ Completar uma tarefa
- ✅ Completar uma fase
- ⚠️ Encontrar bloqueio ou dúvida
- ⚠️ Identificar necessidade de mudança na arquitetura

**Formato da Mensagem**:
```markdown
## ✅ Tarefa Completada

**Fase**: [Número e nome]
**Tarefa**: [Descrição]

### O Que Foi Feito
- [Item 1]
- [Item 2]

### Arquivos Modificados
- `path/to/file.vue`
- `path/to/test.spec.ts`

### Testes
- [x] Type checking passou
- [x] Linting passou
- [x] Testes unitários passando (3/3)
- [x] Teste manual no browser OK

### Próximo Passo
[Qual tarefa vem a seguir]

**Posso continuar?**
```

---

## 📚 Documentação de Referência

### Nuxt 3
- **Composables**: https://nuxt.com/docs/guide/directory-structure/composables
- **Components**: https://nuxt.com/docs/guide/directory-structure/components
- **Server Routes**: https://nuxt.com/docs/guide/directory-structure/server

### Vue 3
- **Composition API**: https://vuejs.org/guide/extras/composition-api-faq.html
- **TypeScript**: https://vuejs.org/guide/typescript/composition-api.html
- **Testing**: https://test-utils.vuejs.org/

### Tailwind CSS
- **Configuration**: https://tailwindcss.com/docs/configuration
- **Utility Classes**: https://tailwindcss.com/docs/utility-first

### Testing
- **Vitest**: https://vitest.dev/guide/
- **Playwright**: https://playwright.dev/docs/intro

---

## 🎯 Lembrete Final

- **Atomic Design é obrigatório**: Atoms → Molecules → Organisms → Templates → Pages
- **TypeScript strict**: Sem `any`, sempre tipagem completa
- **Tailwind CSS**: Sem CSS customizado (exceto casos raros)
- **Testes contínuos**: Cada fase deve ter testes passando
- **Pausar frequentemente**: Melhor pedir aprovação demais do que de menos

**Agora, veja a fase atual e apresente seu plano ao usuário!**
