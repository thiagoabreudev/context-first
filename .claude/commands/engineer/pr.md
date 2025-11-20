# Pull Request - IA do Jeito Certo

Agora vamos abrir um Pull Request para revisão e merge da feature.

## 🎯 Objetivo

Criar PR completo e bem documentado, facilitando revisão e aprovação.

## 📋 Processo

### 1. Garantir que Testes Passam

Executar suíte completa de testes:

```bash
npm run test:unit && npm run test:e2e
```

**Se algum teste falhar**: PARE e corrija antes de prosseguir.

### 2. Commit Final

**Verificar mudanças**:
```bash
git status
git diff
```

**Adicionar arquivos** (APENAS os que você modificou):
```bash
# ❌ NUNCA fazer:
git add .

# ✅ SEMPRE fazer:
git add components/atoms/Button.vue
git add components/molecules/FormField.vue
git add tests/unit/components/atoms/Button.spec.ts
git add .claude/sessions/<feature-slug>/plan.md
```

**Commit com mensagem descritiva**:
```bash
git commit -m "feat(contact-form): adicionar formulário de contato com validação

- Criar componentes Atoms: Button, Input, Label
- Criar componentes Molecules: FormField
- Criar componente Organism: ContactForm
- Adicionar validação Zod para email corporativo
- Implementar server route /api/contact com rate limiting
- Testes E2E para fluxo completo de submissão

Resolves #123"
```

**Formato da Mensagem de Commit**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: Nova feature
- `fix`: Correção de bug
- `refactor`: Refatoração (sem mudança de comportamento)
- `docs`: Apenas documentação
- `test`: Adicionar/corrigir testes
- `chore`: Manutenção (deps, configs)

### 3. Push para Remote

```bash
git push origin feat/<feature-slug>
```

Se branch ainda não existe no remote:
```bash
git push -u origin feat/<feature-slug>
```

### 4. Atualizar Linear (se usando)

Mover card do projeto **iadojeitocerto** para status "In Review":

```bash
# Via API do Linear
# Credenciais no .env: LINEAR_API_KEY e LINEAR_TEAM_ID
# Ver configuração em .claude/linear-config.md
# Isso será feito automaticamente pelo script
```

### 5. Abrir Pull Request

**Usar GitHub CLI** (recomendado):
```bash
gh pr create --title "[Feature]: Formulário de Contato" --body "$(cat .claude/sessions/<feature-slug>/pr-template.md)"
```

**Ou manualmente** no GitHub Web UI.

## 📝 Template de PR

Criar arquivo `.claude/sessions/<feature-slug>/pr-template.md` com:

```markdown
# [Feature]: Formulário de Contato com Validação

## 📋 Resumo

Este PR adiciona um formulário de contato completo à landing page, permitindo que visitantes (CTOs, VPs de Eng, Tech Leads) enviem mensagens para agendar análise do workshop.

O formulário implementa validação de email corporativo (rejeita @gmail, @hotmail, etc.) e rate limiting para prevenir spam.

## ✅ Validação contra Meta Specs

- [x] Alinhado com `metaspecs/businnes/visao-produto.md` (objetivo: gerar leads qualificados)
- [x] Atende persona: **CTO** (Ricardo Silva) e **VP de Engenharia** (Mariana Costa)
- [x] Listado em `metaspecs/businnes/features-valores.md` (Feature #8 - MVP)
- [x] Usa stack de `metaspecs/technical/stack-tecnologica.md` (Vue 3 + Nuxt + Tailwind + Zod)
- [x] Segue padrões de `metaspecs/technical/arquitetura.md` (Atomic Design + SSG/ISR)
- [x] Estratégia de testes conforme `metaspecs/technical/estrategia-testes.md`
- [x] Sem conflitos com `metaspecs/technical/problemas-conhecidos.md`

## 🎨 Componentes Criados/Modificados

### Atoms
- `components/atoms/Button.vue` - Botão reutilizável com variantes
- `components/atoms/Input.vue` - Input de texto/email com estados
- `components/atoms/Label.vue` - Label com indicador de required
- `components/atoms/Text.vue` - Texto com variantes (error, help)

### Molecules
- `components/molecules/FormField.vue` - Combina Label + Input + Error message

### Organisms
- `components/organisms/ContactForm.vue` - Formulário completo com validação

### Composables
- `composables/useFormValidation.ts` - Validação com Zod schema

### Server
- `server/api/contact.post.ts` - API route com rate limiting
- `server/utils/rateLimiter.ts` - Utility para rate limiting por IP

### Pages
- `pages/contato.vue` - Página de contato com SEO completo

## 🧪 Testes

### Unit Tests (Vitest)
- ✅ `tests/unit/components/atoms/Button.spec.ts` (5 testes)
- ✅ `tests/unit/components/atoms/Input.spec.ts` (4 testes)
- ✅ `tests/unit/components/molecules/FormField.spec.ts` (3 testes)
- ✅ `tests/unit/composables/useFormValidation.spec.ts` (6 testes)

**Cobertura**: 87% (target: 80%)

### E2E Tests (Playwright)
- ✅ `tests/e2e/contact-form.spec.ts` (5 testes)
  - Submissão com sucesso
  - Validação de email corporativo
  - Validação de campos obrigatórios
  - Rate limiting após 5 tentativas
  - Mensagem de sucesso exibida

**Cobertura**: 100% dos fluxos críticos

## 📊 Performance

- **Bundle Size**: +12kb (total: 142kb - dentro do target de 150kb)
- **Lighthouse Performance**: 94 (target: > 90)
- **LCP**: 1.8s (target: < 2s)
- **Lighthouse Accessibility**: 96 (target: > 95)

## 🔒 Segurança

- ✅ Rate limiting: 5 requests/min por IP
- ✅ Validação de inputs com Zod
- ✅ Sanitização de dados antes de envio
- ✅ CORS configurado corretamente
- ✅ Sem exposição de credenciais

## ♿ Acessibilidade

- ✅ WCAG 2.1 AA compliant
- ✅ Navegação por teclado (Tab, Enter, Esc)
- ✅ Focus visible em todos os elementos interativos
- ✅ Labels associados a inputs (for/id)
- ✅ ARIA attributes corretos
- ✅ Mensagens de erro anunciadas por screen readers
- ✅ Contraste 4.5:1 em todos os textos

## 🔍 SEO

- ✅ Meta tags completas (title, description)
- ✅ Open Graph tags (og:title, og:description, og:image)
- ✅ Canonical URL
- ✅ Structured data: ContactPage schema (Schema.org)
- ✅ Sitemap atualizado

## 📝 Checklist

- [x] TypeScript sem erros (`npm run typecheck`)
- [x] ESLint sem erros (`npm run lint`)
- [x] Código formatado (`npm run format`)
- [x] Todos os testes passando (unit + E2E)
- [x] Performance targets atingidos
- [x] Acessibilidade validada (axe-core)
- [x] Meta specs validadas
- [x] CHANGELOG.md atualizado
- [x] Documentação atualizada

## 🎯 Métricas de Sucesso

Conforme `metaspecs/businnes/features-valores.md`:
- **Target**: Form fill rate > 10%
- **Target**: Conversão geral > 3%
- **Medição**: Google Analytics 4 + Vercel Analytics

## 📸 Screenshots

(Adicionar screenshots do formulário em desktop e mobile se possível)

## 🔗 Links Relacionados

- Issue: #123
- PRD: `/specs/prd/contact-form.md`
- Figma: (link do design se houver)
- Preview Deploy: (Vercel irá adicionar automaticamente)

## 📚 Documentação

- Atomic Design hierarchy seguido rigorosamente
- Composables documentados com JSDoc
- Server routes com comentários explicativos

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 6. Aguardar Code Review Automatizado

Após abrir PR, aguardar 3-5 minutos para code review automatizado (GitHub Actions, Vercel, etc.).

**Verificar**:
- [ ] Vercel preview deploy bem-sucedido
- [ ] GitHub Actions CI passou
- [ ] Lighthouse CI passou (se configurado)
- [ ] Comentários de bots (se houver)

## 7. Abordar Comentários de Code Review

**Se houver comentários automatizados**:

1. **Analisar** cada comentário
2. **Categorizar**:
   - 🔴 Crítico: Deve corrigir
   - 🟡 Importante: Deve corrigir ou justificar
   - 🟢 Sugestão: Pode ignorar com justificativa

3. **Apresentar ao usuário**:
   ```markdown
   ## 📝 Code Review Automatizado

   **Comentários Recebidos**: 5

   ### 🔴 Crítico (2)
   1. Bundle size excedeu 150kb (+5kb over limit)
      - **Ação**: Lazy load de componentes pesados
   2. Acessibilidade: Falta aria-label em botão de submit
      - **Ação**: Adicionar aria-label

   ### 🟡 Importante (2)
   3. Performance: LCP de 2.3s em mobile
      - **Ação**: Otimizar imagens
   4. TypeScript: Tipo `any` em função helper
      - **Ação**: Tipar corretamente

   ### 🟢 Sugestão (1)
   5. Refatoração: Extrair função de validação
      - **Decisão**: Manter como está (já está em composable)

   **Posso fazer as correções críticas e importantes?**
   ```

4. **Fazer correções**
5. **Commit e push**:
   ```bash
   git add <files>
   git commit -m "fix(contact-form): corrigir issues de code review

   - Lazy load de OrganismsContactForm
   - Adicionar aria-label em button submit
   - Otimizar imagens (next-gen formats)
   - Tipar função helper corretamente"

   git push
   ```

6. **Re-aguardar** code review

## 8. Mensagem de Conclusão

Após PR aberto e code review abordado:

```markdown
## ✅ Pull Request Criado

**Feature**: Formulário de Contato
**Status**: ✅ Pronto para Revisão

### Detalhes
- **PR**: #124
- **URL**: https://github.com/user/iadojeitocerto/pull/124
- **Preview Deploy**: https://iadojeitocerto-pr-124.vercel.app
- **Linear**: Card movido para "In Review"

### Resumo
- ✅ Testes passando (18 unit + 5 E2E)
- ✅ Performance targets atingidos
- ✅ Acessibilidade WCAG 2.1 AA
- ✅ Code review automatizado: Aprovado
- ✅ Meta specs validadas

### Próximos Passos
1. Aguardar revisão manual do time
2. Abordar comentários se houver
3. Merge para main
4. Deploy para production (automático via Vercel)

O PR está pronto para sua revisão final e merge manual.

**Link**: https://github.com/user/iadojeitocerto/pull/124
```

## 🚨 Regra de Ouro

**SEMPRE faça commit APENAS dos arquivos que você alterou.**

❌ NUNCA use `git add .` para prevenir commits de arquivos que não deveriam ser commitados.

✅ SEMPRE adicione arquivos explicitamente: `git add path/to/file.vue`

## 🎯 Checklist Final

Antes de considerar PR completo:

- [ ] Testes passando
- [ ] Mudanças commitadas
- [ ] Branch pushed para remote
- [ ] Linear card em "In Review" (se usando)
- [ ] PR aberto no GitHub
- [ ] Template de PR completo
- [ ] Code review automatizado passou
- [ ] Comentários abordados (se houver)
- [ ] Preview deploy funcionando

**Após tudo isso, o PR está pronto para revisão manual e merge!**
