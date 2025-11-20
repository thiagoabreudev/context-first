# Context: Sistema de Gestão de Turmas e Inscrições

**Feature**: IAD-2
**Fase**: Fase 2 (Pós-MVP)
**Prioridade**: Alta
**Status**: ✅ PRD Aprovado

---

## Por Que

### Valor de Negócio
Atualmente, o processo de venda de workshops é 100% manual:
- Leads preenchem formulário → vendas entra em contato → negocia → fecha venda → envia boleto/pix manualmente → confirma pagamento manualmente

**Problema**: Este processo não escala e perde conversão (fricção alta entre interesse → pagamento)

**Solução**: Sistema automatizado que permite:
- Escalar vendas de workshops sem aumentar time comercial
- Reduzir tempo de conversão de 2-3 semanas para <24h
- Criar previsibilidade de receita com pre-vendas
- Liberar time de vendas para focar em enterprise deals

### Persona Atendida
- ✅ **CTO** (Ricardo Silva) - Quer comprar workshop sem fricção, processo rápido
- ✅ **VP de Engenharia** (Mariana Costa) - Precisa justificar investimento, quer processo transparente
- ✅ **Time Interno** (Vendas/Admin) - Precisa gerenciar turmas e acompanhar inscrições

### Fase do Produto
**Fase 2** - Pós-MVP (MVP já validado e gerando leads)

### Métrica Impactada
- **Taxa de conversão Lead → Inscrição**: de <5% para >15%
- **Taxa de conversão Inscrição → Pagamento**: >70%
- **Tempo médio de conversão**: de 2-3 semanas para <24h
- **Taxa de abandono no checkout**: <30%
- **Tempo de setup de nova turma**: <10min

---

## O Que

### Funcionalidades Principais

#### 1. Listagem Pública de Turmas (`/turmas`)
- Cards de turmas abertas ordenadas por data
- Filtros: data, vagas disponíveis
- Indicadores visuais: "Últimas Vagas" (<5 vagas), "Esgotado"
- SEO otimizado com structured data (Event schema)

#### 2. Detalhes da Turma (`/turmas/[slug]`)
- Informações completas: conteúdo programático, datas, vagas, preço
- Formulário de inscrição integrado
- FAQ específico da turma
- Real-time de vagas disponíveis

#### 3. Fluxo de Inscrição
- Formulário: nome, email, telefone, empresa, cargo, aceite de termos
- Validações: vagas disponíveis, email corporativo, duplicação
- Criação de inscrição no Firestore (status `pendente`)
- Reserva de vaga por 15 minutos
- Criação de preferência no Mercado Pago
- Redirecionamento para checkout

#### 4. Integração com Mercado Pago
- Checkout Pro (PIX, Cartão, Boleto)
- Parcelamento até 12x sem juros
- Webhooks para processar pagamentos
- URLs de retorno: sucesso, pendente, falha

#### 5. Sistema de Notificações por Email (Firebase Extensions)
- Confirmação de inscrição (imediato)
- Pagamento confirmado (webhook)
- Pagamento pendente PIX (webhook)
- Lembrete pré-workshop (1 semana antes)
- Email de boas-vindas (1 dia antes)

#### 6. Gestão de Turmas (Admin via Firebase Console)
- CRUD de turmas: criar, editar, controlar status
- Dashboard de inscrições
- Exportar lista de participantes (CSV)

### Comportamento Esperado

**Happy Path**:
1. Usuário acessa `/turmas`
2. Visualiza turmas disponíveis, filtra por data
3. Clica em "Ver Detalhes"
4. Lê informações, decide se inscrever
5. Preenche formulário de inscrição
6. Sistema cria inscrição, reserva vaga (15min), gera preferência MP
7. É redirecionado para Mercado Pago
8. Escolhe método de pagamento, completa checkout
9. Webhook notifica sistema: `payment.approved`
10. Sistema confirma vaga, envia email de confirmação
11. Usuário recebe email com informações do workshop

---

## Como

### Abordagem Técnica

**Stack Completa**:
- **Frontend**: Nuxt 3 + Vue 3 + TypeScript + Tailwind CSS
- **Database**: Firebase Firestore (collections: `turmas`, `inscricoes`)
- **Pagamentos**: Mercado Pago SDK v2.0 (server-side)
- **Emails**: Firebase Extensions (Trigger Email via Zoho SMTP)
- **Hosting**: Vercel (SSG/ISR)
- **Validação**: Zod schemas

**Renderização**:
- `/turmas`: SSG com ISR (revalidate: 60s)
- `/turmas/[slug]`: SSG com ISR (revalidate: 60s)
- `/inscricao/*`: SSG (páginas estáticas de status)

### Componentes - Atomic Design

**Atoms** (NEW):
- `<Badge />` - "Últimas Vagas", "Esgotado"
- `<PriceTag />` - formatação de preço em R$
- `<DateBadge />` - formatação de data

**Molecules** (NEW):
- `<TurmaCard />` - card de turma na listagem
- `<VagasIndicator />` - indicador de vagas com barra de progresso
- `<FormField />` - campo de formulário (REUSE de ContactForm)

**Organisms** (NEW):
- `<TurmasList />` - listagem completa com filtros
- `<TurmaDetailsHero />` - hero da página de detalhes
- `<InscricaoForm />` - formulário completo de inscrição
- `<CheckoutSummary />` - resumo antes de redirecionar para MP

**Pages** (NEW):
- `pages/turmas/index.vue` - Listagem de turmas
- `pages/turmas/[slug].vue` - Detalhes e inscrição
- `pages/inscricao/sucesso.vue` - Confirmação de pagamento
- `pages/inscricao/pendente.vue` - Aguardando pagamento (PIX/boleto)
- `pages/inscricao/falha.vue` - Erro no pagamento

**Server Routes** (NEW):
- `server/api/turmas/index.get.ts` - Listar turmas abertas
- `server/api/turmas/[id].get.ts` - Detalhes de uma turma
- `server/api/turmas/inscrever.post.ts` - Criar inscrição + preferência MP
- `server/api/webhooks/mercadopago.post.ts` - Processar webhooks

**Composables** (NEW):
- `composables/useTurmas.ts` - CRUD de turmas (client-side fetch)
- `composables/useInscricoes.ts` - Gestão de inscrições
- `composables/useMercadoPago.ts` - Utilitários server-side para MP

---

## Validação contra Meta Specs

### ✅ Alinhado com `visao-produto.md`
- **Objetivo Primário**: Converter visitantes em leads → Este sistema automatiza a conversão de leads em clientes pagantes
- **Proposta de Valor**: Transformar "vibe coding" em engenharia → Sistema aplica engenharia rigorosa ao processo de vendas
- **Diferenciação**: Não somos solução mágica → Sistema é processo estruturado e previsível
- **Métrica de Sucesso**: Taxa de conversão → Foco total em conversão Lead → Inscrição → Pagamento

### ✅ Atende persona de `perfil-cliente.md`
- **CTO** (Ricardo Silva):
  - Dor: "Gastamos mais tempo corrigindo do que economizamos" → Sistema automatizado reduz fricção e tempo de compra
  - Motivação: ROI claro e mensurável → Sistema com métricas claras (conversão, abandono, tempo)

- **VP Eng** (Mariana Costa):
  - Dor: "Difícil coordenar múltiplos squads" → Sistema escalável permite múltiplas turmas simultâneas
  - Motivação: Padronização de processos → Sistema cria processo repetível

- **Time Interno**:
  - Necessidade: gerenciar turmas, acompanhar inscrições → Firebase Console + dashboard

### ✅ Listado em `features-valores.md`
- **Feature 10**: Sistema de Gestão de Turmas e Inscrições
- **Fase 2**: Pós-MVP (correto)
- **Prioridade**: 🟡 ALTA (correto)
- **Valor de Negócio**:
  - Automação: Reduz trabalho manual de vendas ✓
  - Escalabilidade: Permite múltiplas turmas simultâneas ✓
  - Conversão: Checkout otimizado reduz fricção ✓
  - Receita: Permite pre-venda e planejamento financeiro ✓

### ✅ Usa stack de `stack-tecnologica.md`
- **Framework**: Nuxt.js 3.10+ ✓ (documentado)
- **Database**: Firebase Firestore ✓ (documentado na seção "Banco de Dados")
- **Pagamentos**: Mercado Pago ✓ (documentado na seção "Pagamentos")
- **Emails**: Firebase Extensions + Zoho SMTP ✓ (documentado)
- **Validação**: Zod schemas ✓ (já em uso)
- **Hosting**: Vercel ✓ (documentado)

### ✅ Segue padrões de `arquitetura.md`
- **Atomic Design**: Atoms → Molecules → Organisms → Pages ✓
- **SSG/ISR**: Páginas `/turmas` com ISR (revalidate: 60s) ✓
- **Composables**: `useTurmas`, `useInscricoes` ✓
- **Server Routes**: API routes RESTful ✓
- **Zod Validation**: Server-side validation ✓
- **Error Handling**: Try/catch + createError ✓

### ✅ Sem conflitos com `problemas-conhecidos.md`
- **Rate Limiting**: Já implementado no site (5 req/hr) → Aplicar no endpoint de inscrição ✓
- **Email Corporate**: Validação já existe no formulário de contato → Reutilizar ✓
- **Firebase Tier**: 200 emails/dia gratuito → Suficiente para MVP, upgrade se necessário ✓
- **Vercel Limits**: 100GB bandwidth/mês → Suficiente para MVP ✓

---

## Dependências

### Bibliotecas Novas
```json
{
  "dependencies": {
    "mercadopago": "^2.0.0"
  }
}
```

### APIs Externas
- **Firebase Firestore**: Collections `turmas` e `inscricoes`
- **Firebase Extensions**: Trigger Email (já configurado com Zoho)
- **Mercado Pago API**:
  - Criar preferência de checkout
  - Processar webhooks de pagamento
  - Consultar status de pagamento (fallback)

### Componentes Existentes (Reutilizar)
- `components/molecules/FormField.vue` - do ContactForm
- `composables/useContactForm.ts` - padrão de validação Zod
- `server/api/contact.post.ts` - padrão de rate limiting e validação

---

## Restrições

### Restrições Técnicas
1. **Firebase Firestore**: limite de 1 write/s por documento
   - **Mitigação**: Usar Firestore Transactions para operações críticas (controle de vagas)

2. **Mercado Pago**: webhooks só funcionam em produção (não em localhost)
   - **Mitigação**: Usar Mercado Pago sandbox para testes, simular webhooks manualmente

3. **Firebase Extensions**: limite de 200 emails/dia no tier gratuito
   - **Mitigação**: Monitorar volume, upgrade para Blaze se necessário (~$10/mês para 10k emails)

4. **Vercel**: serverless functions têm timeout de 10s
   - **Mitigação**: Otimizar processamento de webhooks (<2s target)

### Restrições de Negócio
- **Budget**: R$ 0 adicional de infra (usar tiers gratuitos)
- **Timeline**: 4-6 semanas para MVP completo
- **Recursos**: 1 desenvolvedor full-time
- **Dependências**: conta Mercado Pago aprovada (pode levar 7-10 dias)

### Performance Targets
- **Listagem de turmas**: carregamento < 1s
- **Detalhes da turma**: carregamento < 1.5s
- **Criação de inscrição**: resposta < 500ms
- **Webhook processing**: < 2s
- **Lighthouse Score**: > 90

### Bundle Size Budget
- **Atoms/Molecules**: < 5kb cada
- **Organisms**: < 20kb cada
- **Pages**: < 50kb cada (sem Mercado Pago SDK no client-side)

---

## Testes

### E2E Críticos (Playwright)
```typescript
// tests/e2e/turmas/fluxo-completo.spec.ts

test('Fluxo completo: listar → detalhes → inscrever → MP checkout', async ({ page }) => {
  // 1. Listar turmas
  await page.goto('/turmas')
  await expect(page.locator('[data-test="turma-card"]').first()).toBeVisible()

  // 2. Ver detalhes
  await page.locator('[data-test="turma-card"]').first().click()
  await expect(page).toHaveURL(/\/turmas\//)

  // 3. Preencher inscrição
  await page.fill('[data-test="nome"]', 'João Silva')
  await page.fill('[data-test="email"]', 'joao@empresa.com.br')
  await page.fill('[data-test="telefone"]', '11999999999')
  await page.fill('[data-test="empresa"]', 'Empresa LTDA')
  await page.fill('[data-test="cargo"]', 'CTO')
  await page.check('[data-test="aceitar-termos"]')

  // 4. Submeter
  await page.click('[data-test="btn-inscrever"]')

  // 5. Verificar redirecionamento para Mercado Pago
  await page.waitForURL(/mercadopago\.com/)
})

test('Webhook atualiza status de inscrição', async ({ request }) => {
  // Mock webhook payload
  const payload = {
    type: 'payment',
    data: { id: '12345' }
  }

  // Enviar webhook
  const response = await request.post('/api/webhooks/mercadopago', {
    data: payload,
    headers: {
      'x-signature': 'mock-signature' // Mock da assinatura do MP
    }
  })

  expect(response.status()).toBe(200)

  // Verificar Firestore (requer helper de teste)
  // const inscricao = await getInscricaoById('abc123')
  // expect(inscricao.status).toBe('paga')
})

test('Sistema de reserva libera vaga após 15min', async () => {
  // Criar inscrição pendente com reserva expirada
  // Executar job de limpeza
  // Verificar que vaga foi liberada
})
```

### Unit Tests (Vitest)
```typescript
// tests/unit/composables/useTurmas.spec.ts
describe('useTurmas', () => {
  test('filtra turmas abertas', () => {
    // Test logic
  })

  test('ordena por data (próximas primeiro)', () => {
    // Test logic
  })
})

// tests/unit/composables/useInscricoes.spec.ts
describe('useInscricoes', () => {
  test('calcula tempo restante de reserva', () => {
    // Test logic
  })

  test('valida email corporativo', () => {
    // Test logic
  })
})

// tests/unit/server/utils/mercadopago.spec.ts
describe('Mercado Pago utils', () => {
  test('cria preferência com dados corretos', () => {
    // Test logic
  })

  test('valida assinatura de webhook', () => {
    // Test logic
  })
})
```

### Cobertura Target
- **Unit tests**: 80%+ de cobertura
- **E2E**: 100% dos fluxos críticos
  - Listar turmas
  - Ver detalhes
  - Inscrever-se
  - Processar pagamento (webhook)
  - Sistema de reserva

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Overselling** (vender mais vagas que disponível) | Média | Alto | Firestore Transactions atomicas + sistema de reserva com timeout |
| **Webhook duplicado** | Alta | Médio | Idempotency usando `payment_id` como chave única |
| **Webhook perdido** (Mercado Pago não notifica) | Baixa | Alto | Cronjob para checar inscrições `pendente` com >1h e buscar status na API do MP |
| **Usuário abandona checkout** | Alta | Médio | Sistema de reserva libera vaga após 15min + email de recuperação |
| **Falha no envio de email** | Média | Médio | Firebase Extension tem retry automático + fallback manual via console |
| **Conflito de vagas (race condition)** | Baixa | Alto | Usar Firestore Transactions para decrementar `vagasDisponiveis` atomicamente |
| **Mercado Pago fora do ar** | Baixa | Alto | Mostrar mensagem de erro amigável + capturar lead para contato manual |

---

## Próximos Passos

1. **Criar conta Mercado Pago**: aplicar para conta de produção (7-10 dias)
2. **Configurar Firebase Extensions**: setup de email templates no Firebase Console
3. **Desenvolver arquitetura detalhada**: `architecture.md` com diagramas, componentes, flows
4. **Implementar em sprints**:
   - Sprint 1: Listagem de turmas + detalhes (sem inscrição)
   - Sprint 2: Formulário de inscrição + integração Firestore
   - Sprint 3: Integração Mercado Pago + webhooks
   - Sprint 4: Sistema de emails + páginas de status
   - Sprint 5: Testes E2E + refinamentos
5. **Deploy staging**: ambiente de testes com Mercado Pago sandbox
6. **Go-live**: soft launch → beta privado → public launch

---

## Questões para Esclarecimento

### 1. Estrutura de Preço
**Pergunta**: O preço será sempre fixo (ex: R$ 47.000) ou teremos múltiplas opções de pricing por turma (ex: early bird, lote 1, lote 2)?

**Sugestão**: Para MVP, manter preço fixo por turma (mais simples). Fase 2 pode adicionar pricing dinâmico.

### 2. Controle de Vagas
**Pergunta**: Além do sistema de reserva de 15min, queremos algum controle manual? (ex: admin pode reservar vagas para clientes VIP)

**Sugestão**: MVP sem controle manual. Admin pode criar inscrições manualmente via Firebase Console se necessário.

### 3. Certificado de Participação
**Pergunta**: O PRD menciona "Certificado de participação (PDF)" na Fase 2.5. Isso está fora do escopo deste MVP, correto?

**Sugestão**: Confirmar que certificados ficam para Fase 2.5. MVP foca apenas em vendas e inscrições.

### 4. Multi-participante
**Pergunta**: Uma empresa pode inscrever múltiplos participantes em uma única compra? Ou cada participante precisa se inscrever individualmente?

**Sugestão**: Para MVP, 1 inscrição = 1 participante = 1 pagamento. Multi-participante fica para Fase 2.

### 5. Cancelamento e Reembolso
**Pergunta**: Qual a política de cancelamento? Usuário pode cancelar até quantos dias antes? Reembolso é manual ou automático?

**Sugestão**: Criar política clara (ex: até 7 dias antes, reembolso integral via contato com suporte). Processo manual no MVP.

---

**Status**: ✅ Contexto completo. Aguardando aprovação para prosseguir para fase de Arquitetura.
