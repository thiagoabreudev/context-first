# Commands CONTEXT-FIRST™

**2 commands** para adicionar Observabilidade e Governança às suas features

---

## 📦 Conteúdo

| Command | Arquivo | Quando Usar |
|---------|---------|-------------|
| `/context-first-observability` | `observability.md` | Após implementação |
| `/context-first-governance` | `governance.md` | Antes de produção |

---

## 🚀 Como Instalar

### Opção 1: Manual

```bash
# Copiar para projeto
cp *.md /caminho/do/projeto/.claude/commands/context-first/

# Estrutura final:
.claude/
└── commands/
    └── context-first/
        ├── observability.md
        └── governance.md
```

### Opção 2: Automatizada

```bash
# Criar script de instalação
cat > install-context-first-commands.sh << 'EOF'
#!/bin/bash
mkdir -p .claude/commands/context-first
cp context-first-commands/*.md .claude/commands/context-first/
echo "✅ Context-First commands installed!"
EOF

chmod +x install-context-first-commands.sh
./install-context-first-commands.sh
```

---

## 📖 Guia Rápido

### 1. Implementar Feature

```bash
/engineer start feat-login
/context-first spec "Login endpoint"
/context-first test-first "login endpoint"
/engineer work
# ✅ Feature implementada e testada
```

### 2. Adicionar Observabilidade

```bash
/context-first-observability login
```

**O que adiciona**:
- ✅ Structured logging (Winston/Pino)
- ✅ Metrics (StatsD/Prometheus)
- ✅ Distributed tracing (OpenTelemetry)
- ✅ Health checks
- ✅ Error tracking (Sentry)

### 3. Adicionar Governança

```bash
/context-first-governance login
```

**O que adiciona**:
- ✅ Audit trail completo
- ✅ LGPD/GDPR compliance
- ✅ RBAC (Role-Based Access Control)
- ✅ Data retention policies
- ✅ Explainability (decisões automatizadas)
- ✅ Security controls (rate limiting, fraud detection)

---

## 🎯 Workflow Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. IMPLEMENTAÇÃO                                            │
│    /engineer start feat-login                               │
│    /context-first spec "Login endpoint"                     │
│    /context-first test-first "login endpoint"               │
│    /engineer work                                           │
│    ✅ 12/12 testes passando                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. OBSERVABILIDADE                                          │
│    /context-first-observability login                       │
│    ✅ Logging estruturado                                    │
│    ✅ Métricas                                               │
│    ✅ Tracing                                                │
│    ✅ Health checks                                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. GOVERNANÇA                                               │
│    /context-first-governance login                          │
│    ✅ Audit trail                                            │
│    ✅ Compliance (LGPD/GDPR)                                 │
│    ✅ RBAC                                                   │
│    ✅ Security controls                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. FINALIZAÇÃO                                              │
│    /context-checkpoint                                      │
│    ✅ Feature completa e pronta para produção! 🚀            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 O Que Cada Command Adiciona

### `/context-first-observability`

#### Structured Logging

```typescript
logger.info('Login successful', {
  requestId: 'req_abc123',
  userId: 'user_xyz789',
  email: 'user@example.com',
  duration: 245,
  timestamp: '2025-11-14T12:30:45.123Z'
});
```

#### Metrics

```typescript
metrics.increment('auth.login.success');
metrics.timing('auth.login.duration', 245);
metrics.gauge('auth.active_sessions', 1523);
```

#### Distributed Tracing

```typescript
const span = tracer.startSpan('auth.login');
span.setTag('user.email', email);
// ... código ...
span.finish();
```

#### Health Checks

```typescript
GET /health/auth
{
  "status": "healthy",
  "checks": {
    "database": true,
    "redis": true
  }
}
```

---

### `/context-first-governance`

#### Audit Trail

```typescript
await auditLog.record({
  action: 'user.email.update.success',
  actor: context.actorId,
  subject: userId,
  resource: 'user.email',
  metadata: {
    oldValue: 'old@example.com',
    newValue: 'new@example.com'
  }
});
```

#### LGPD/GDPR Compliance

```typescript
await auditLog.record({
  action: 'user.data.accessed',
  actor: context.actorId,
  subject: userId,
  dataCategories: ['email', 'phone', 'address'],
  legalBasis: 'legitimate_interest' // LGPD
});
```

#### RBAC

```typescript
const hasPermission = await rbac.check({
  actor: context.actorId,
  action: 'user.delete',
  resource: userId
});

if (!hasPermission) {
  throw new ForbiddenError('Permission denied');
}
```

#### Explainability

```typescript
const explanation = explainer.explain({
  decision: 'denied',
  factors: [
    {
      factor: 'credit_score',
      value: 580,
      threshold: 650,
      weight: 0.4,
      impact: 'negative'
    }
  ]
});
```

---

## 📋 Arquivos Criados

### Por `/context-first-observability`

```
src/utils/
├── logger.ts              # Winston/Pino
├── metrics.ts             # StatsD/Prometheus
├── tracer.ts              # OpenTelemetry
└── error-tracker.ts       # Sentry

src/health/
└── <feature>-health.ts    # Health checks

metaspecs/observability/
└── <feature>/
    └── observability.md   # Documentação
```

### Por `/context-first-governance`

```
src/utils/
├── audit.ts               # Audit logging
├── data-protection.ts     # LGPD/GDPR
├── rbac.ts                # Access control
├── retention.ts           # Data retention
├── explainer.ts           # Explainability
└── security.ts            # Security controls

src/governance/
└── <feature>/
    ├── policies.ts        # Políticas
    └── compliance.ts      # Compliance

metaspecs/governance/
└── <feature>/
    ├── governance.md      # Documentação
    ├── audit-trail.md     # Eventos auditados
    ├── compliance.md      # Compliance
    └── security.md        # Segurança
```

---

## 🎓 Como Ensinar no Workshop

### **Dia 2 - Manhã** (Observabilidade)

**Teoria** (30 min):
- Por que observabilidade?
- 3 pilares: Logs, Metrics, Traces
- Demo ao vivo

**Prática** (60 min):
- Participantes aplicam em feature própria
- `/context-first-observability <feature>`
- Verificar logs, métricas, traces

**Review** (30 min):
- Discussão de resultados
- Boas práticas

### **Dia 2 - Tarde** (Governança)

**Teoria** (30 min):
- LGPD/GDPR na prática
- Audit trail
- RBAC
- Demo ao vivo

**Prática** (60 min):
- Participantes aplicam em feature própria
- `/context-first-governance <feature>`
- Verificar audit logs, compliance

**Review** (30 min):
- Discussão de resultados
- Compliance checklist

---

## ✅ Benefícios

### Observabilidade

| Antes | Depois |
|-------|--------|
| "Por que falhou?" 🤷 | "Falhou no DB, linha 45, usuário X" ✅ |
| 2 horas debugando | 5 minutos olhando logs |
| Usuário reclama → Investiga | Alerta dispara → Corrige |

### Governança

| Antes | Depois |
|-------|--------|
| Compliance manual | Compliance by design ✅ |
| "Quem acessou?" 🤷 | Query em audit_logs → Resposta |
| Fraude acontece → Detecta | Fraude detectada → Bloqueia |
| Decisão opaca | Decisão explicada ✅ |

---

## 💡 Dicas Pro

### 1. **Sempre Adicione RequestID**

```typescript
const requestId = req.headers['x-request-id'] || generateRequestId();
logger.info('...', { requestId, ... });
```

### 2. **Log Contexto, Não Apenas Mensagem**

```typescript
// ❌ Ruim
logger.info('User logged in');

// ✅ Bom
logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  duration: 245,
  ip: req.ip
});
```

### 3. **Registre Tentativas E Resultados**

```typescript
// Tentativa
await auditLog.record({ action: 'feature.attempt', ... });

try {
  // Execução
  const result = await doSomething();
  
  // Sucesso
  await auditLog.record({ action: 'feature.success', ... });
} catch (error) {
  // Falha
  await auditLog.record({ action: 'feature.failure', ... });
}
```

### 4. **Documente Base Legal (LGPD)**

```typescript
await auditLog.record({
  action: 'user.data.accessed',
  legalBasis: 'legitimate_interest', // ou 'consent', 'contract'
  dataCategories: ['email', 'phone']
});
```

---

## 📊 Métricas de Sucesso

| Métrica | Sem Obs/Gov | Com CONTEXT-FIRST™ |
|---------|-------------|---------------------|
| Tempo de debug | 2h | 5min (96% ↓) |
| Compliance | Manual | Automatizado ✅ |
| Auditoria | Impossível | Completa ✅ |
| Transparência | Opaca | Explicável ✅ |
| Segurança | Reativa | Proativa ✅ |

---

## 🆘 Troubleshooting

### "Logs não aparecem"

```bash
# Verificar configuração do logger
cat src/utils/logger.ts

# Verificar se está sendo chamado
grep -r "logger.info" src/
```

### "Métricas não são enviadas"

```bash
# Verificar configuração do StatsD
echo $STATSD_HOST
echo $STATSD_PORT

# Testar conexão
nc -zv $STATSD_HOST 8125
```

### "Audit logs não são gravados"

```bash
# Verificar tabela no DB
psql -c "SELECT * FROM audit_logs LIMIT 10;"

# Verificar se está sendo chamado
grep -r "auditLog.record" src/
```

---

## 📚 Referências

### Observabilidade

- **Winston**: https://github.com/winstonjs/winston
- **Pino**: https://github.com/pinojs/pino
- **StatsD**: https://github.com/statsd/statsd
- **Prometheus**: https://prometheus.io/
- **OpenTelemetry**: https://opentelemetry.io/
- **Sentry**: https://sentry.io/

### Governança

- **LGPD**: https://www.gov.br/lgpd/
- **GDPR**: https://gdpr.eu/
- **PCI-DSS**: https://www.pcisecuritystandards.org/
- **OWASP**: https://owasp.org/

---

## ✅ Checklist de Implementação

### Para Claude Code

- [ ] Copiar 2 commands para `.claude/commands/context-first/`
- [ ] Testar `/context-first-observability`
- [ ] Testar `/context-first-governance`
- [ ] Documentar no `CLAUDE.md` do projeto

### Para Workshop

- [ ] Adicionar módulo "Observabilidade" (Dia 2 - Manhã)
- [ ] Adicionar módulo "Governança" (Dia 2 - Tarde)
- [ ] Preparar demos ao vivo
- [ ] Criar exercícios práticos

### Para Metodologia

- [ ] Atualizar documentação CONTEXT-FIRST™
- [ ] Incluir Observability-Driven como pilar
- [ ] Incluir eXplainability & Governance como pilar
- [ ] Atualizar whitepaper

---

## 🎯 Resumo Executivo

**Commands CONTEXT-FIRST™**:

1. ✅ **Observability** → Logs + Metrics + Traces + Health
2. ✅ **Governance** → Audit + Compliance + RBAC + Security

**Resultado**:
- ✅ Features observáveis e debugáveis
- ✅ Compliance automatizado (LGPD/GDPR)
- ✅ Auditoria completa
- ✅ Segurança proativa
- ✅ Decisões explicáveis

**Sua metodologia agora está completa com Observabilidade e Governança profissionais!** 🚀

---

**Versão**: 1.0.0  
**Data**: 2025-11-14  
**Autor**: IA do Jeito Certo  
**Licença**: Uso interno para workshop CONTEXT-FIRST™
