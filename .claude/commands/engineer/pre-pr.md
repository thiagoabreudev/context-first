# Pre-PR - IA do Jeito Certo

Estamos finalizando o trabalho nesta feature branch e nos preparando para um pull request. Agora é hora de fazer verificações finais e garantir qualidade máxima.

## 🎯 Objetivo

Garantir que a feature está 100% pronta para revisão através de validações automatizadas e manuais.

## ✅ Checklist de Validação

### 1. Meta Specs Compliance

Validar alinhamento com meta specs do projeto:

**Comando**: `/check <feature-description>`

**Verificações**:
- [ ] Alinhado com `metaspecs/businnes/visao-produto.md`
- [ ] Atende persona de `metaspecs/businnes/perfil-cliente.md`
- [ ] Listado em `metaspecs/businnes/features-valores.md`
- [ ] Usa stack de `metaspecs/technical/stack-tecnologica.md`
- [ ] Segue padrões de `metaspecs/technical/arquitetura.md`
- [ ] Sem conflitos com `metaspecs/technical/problemas-conhecidos.md`

### 2. Código e Qualidade

**Type Checking**:
```bash
npm run typecheck
```
- [ ] Sem erros TypeScript
- [ ] Sem uso de `any`

**Linting**:
```bash
npm run lint
```
- [ ] Sem erros ESLint
- [ ] Sem warnings críticos

**Formatação**:
```bash
npm run format  # ou prettier --write .
```
- [ ] Código formatado consistentemente

### 3. Testes

**Unit Tests**:
```bash
npm run test:unit
npm run test:unit -- --coverage
```
- [ ] Todos os testes passando
- [ ] Cobertura > 80%
- [ ] Sem testes pulados (skip)

**E2E Tests (Fluxos Críticos)**:
```bash
npm run test:e2e
```
- [ ] Todos os testes E2E passando
- [ ] 100% dos fluxos críticos cobertos

### 4. Performance

**Build e Bundle Analysis**:
```bash
npm run build
npm run analyze  # se disponível
```
- [ ] Build sem erros
- [ ] Bundle size < 150kb (MVP) ou conforme target definido
- [ ] Sem warnings de chunk size

**Lighthouse CI** (se configurado):
```bash
npx lighthouse https://preview-url.vercel.app --only-categories=performance,accessibility,seo
```
- [ ] Performance > 90
- [ ] Accessibility > 95
- [ ] SEO > 90
- [ ] LCP < 2s

### 5. Acessibilidade

**Validação Manual**:
- [ ] Navegação por teclado funciona (Tab, Enter, Esc)
- [ ] Focus visible em elementos interativos
- [ ] Labels em inputs de formulário
- [ ] Contraste adequado (mínimo 4.5:1)

**Validação Automatizada** (axe-core):
```typescript
// Em teste E2E
import { injectAxe, checkA11y } from 'axe-playwright'

test('valida acessibilidade', async ({ page }) => {
  await page.goto('/contato')
  await injectAxe(page)
  await checkA11y(page)
})
```
- [ ] Sem violações WCAG 2.1 AA

### 6. SEO

**Meta Tags**:
- [ ] Title presente e descritivo (< 60 chars)
- [ ] Description presente (< 160 chars)
- [ ] Open Graph tags (og:title, og:description, og:image)
- [ ] Canonical URL definida

**Structured Data** (se aplicável):
```bash
# Validar no Google Rich Results Test
# https://search.google.com/test/rich-results
```
- [ ] Schema.org markup válido
- [ ] Sem erros no validador

**Sitemap**:
- [ ] Página adicionada ao sitemap.xml (se necessário)

### 7. Documentação

**README.md** (se mudanças significativas):
- [ ] Atualizado com novas features
- [ ] Instruções de uso atualizadas

**CHANGELOG.md**:
- [ ] Entrada adicionada no formato:
  ```markdown
  ## [Unreleased]
  ### Added
  - Formulário de contato com validação de email corporativo (#123)
  ### Changed
  - Hero section agora usa componente Organism (#124)
  ```

**JSDoc** (em funções complexas):
- [ ] Funções públicas têm documentação
- [ ] Composables têm exemplos de uso

### 8. Plan.md

**Atualização Final**:
- [ ] Todas as fases marcadas como Completada ✅
- [ ] Comentários adicionados sobre decisões importantes
- [ ] Aprendizados documentados

## 🚨 Correções Necessárias

Se alguma validação falhar, **PARE** e corrija antes de prosseguir.

### Fluxo de Correção

1. **Identificar** problemas através dos comandos acima
2. **Priorizar** correções (crítico → importante → sugestão)
3. **Corrigir** um por um
4. **Re-validar** após cada correção
5. **Documentar** mudanças no plan.md

## 📊 Relatório Final

Ao completar todas as validações, gere um relatório:

```markdown
## ✅ Pre-PR Checklist - Feature: [Nome]

### Meta Specs
- [x] Alinhado com visão do produto
- [x] Atende persona: CTO
- [x] Fase: MVP
- [x] Stack aprovada
- [x] Atomic Design seguido

### Código
- [x] TypeScript: 0 erros
- [x] ESLint: 0 erros, 2 warnings (não-críticos)
- [x] Formatação: OK

### Testes
- [x] Unit: 15/15 passando (cobertura 87%)
- [x] E2E: 3/3 passando (100% fluxos críticos)

### Performance
- [x] Build: Sucesso
- [x] Bundle size: +12kb (total 142kb - OK)
- [x] Lighthouse Performance: 94
- [x] LCP: 1.8s

### Acessibilidade
- [x] Navegação por teclado: OK
- [x] axe-core: 0 violações
- [x] WCAG 2.1 AA: Compliant

### SEO
- [x] Meta tags: Completas
- [x] Open Graph: OK
- [x] Structured data: Validado

### Documentação
- [x] CHANGELOG.md: Atualizado
- [x] plan.md: Completo
- [x] JSDoc: Funções públicas documentadas

---

**Status**: ✅ PRONTO PARA PR

Todas as validações passaram. Posso proceder com `/pr`?
```

## 💡 Dicas

- **Automatize**: Configure scripts no `package.json` para rodar todas as validações
  ```json
  {
    "scripts": {
      "prepr": "npm run typecheck && npm run lint && npm run test:unit && npm run test:e2e && npm run build"
    }
  }
  ```

- **CI/CD**: Certifique-se de que as mesmas validações rodam no GitHub Actions

- **Preview Deploy**: Use Vercel preview URL para testar em ambiente real

## 🎯 Próximo Passo

Após todas as validações passarem e obter aprovação do usuário, execute `/pr` para abrir o Pull Request.
