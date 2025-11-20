---
name: context-first-governance
description: Adicionar governança completa (auditoria, compliance, segurança) a uma feature
tools: None
---

# Context-First Governance

Adiciona camada completa de governança a uma feature seguindo o pilar **eXplainability & Governance** da metodologia CONTEXT-FIRST™.

## Quando Usar

- ✅ Feature com dados sensíveis (PII, financeiros, saúde)
- ✅ Features reguladas (LGPD, GDPR, PCI-DSS)
- ✅ Features críticas de negócio
- ✅ Antes de deploy em produção

## Argumentos

```
/context-first-governance <feature-name>
```

- `feature-name`: Nome da feature (ex: `login`, `payment`, `user-data`)

## O Que Adiciona

### 1. **Audit Trail**

Rastreamento completo de todas as ações:

```typescript
import { auditLog } from '../utils/audit';

// ANTES (sem governança)
export async function updateUserEmail(userId: string, newEmail: string) {
  await db.user.update({
    where: { id: userId },
    data: { email: newEmail },
  });
}

// DEPOIS (com governança)
export async function updateUserEmail(
  userId: string, 
  newEmail: string,
  context: AuditContext
) {
  const oldUser = await db.user.findUnique({ where: { id: userId } });
  
  // Registrar tentativa
  await auditLog.record({
    action: 'user.email.update.attempt',
    actor: context.actorId,
    subject: userId,
    resource: 'user.email',
    timestamp: new Date(),
    metadata: {
      oldValue: oldUser.email,
      newValue: newEmail,
      ipAddress: context.ipAddress,
      userAgent: context.userAgent,
    },
  });
  
  try {
    await db.user.update({
      where: { id: userId },
      data: { email: newEmail },
    });
    
    // Registrar sucesso
    await auditLog.record({
      action: 'user.email.update.success',
      actor: context.actorId,
      subject: userId,
      resource: 'user.email',
      timestamp: new Date(),
      metadata: {
        oldValue: oldUser.email,
        newValue: newEmail,
      },
    });
  } catch (error) {
    // Registrar falha
    await auditLog.record({
      action: 'user.email.update.failure',
      actor: context.actorId,
      subject: userId,
      resource: 'user.email',
      timestamp: new Date(),
      metadata: {
        error: error.message,
      },
    });
    
    throw error;
  }
}
```

### 2. **Data Privacy & Compliance**

Proteção de dados sensíveis (LGPD/GDPR):

```typescript
import { dataProtection } from '../utils/data-protection';

export async function getUserData(userId: string, context: AuditContext) {
  // Verificar permissão
  const hasPermission = await checkPermission(
    context.actorId,
    'user.data.read',
    userId
  );
  
  if (!hasPermission) {
    await auditLog.record({
      action: 'user.data.read.denied',
      actor: context.actorId,
      subject: userId,
      reason: 'insufficient_permissions',
    });
    
    throw new ForbiddenError('Insufficient permissions');
  }
  
  // Buscar dados
  const user = await db.user.findUnique({ where: { id: userId } });
  
  // Registrar acesso a dados sensíveis
  await auditLog.record({
    action: 'user.data.read.success',
    actor: context.actorId,
    subject: userId,
    resource: 'user.pii',
    dataCategories: ['email', 'phone', 'address'],
    legalBasis: 'legitimate_interest', // LGPD/GDPR
  });
  
  // Mascarar dados se necessário
  if (context.maskSensitiveData) {
    return dataProtection.mask(user, ['cpf', 'creditCard']);
  }
  
  return user;
}
```

### 3. **Access Control & Authorization**

Controle de acesso granular:

```typescript
import { rbac } from '../utils/rbac';

export async function deleteUser(userId: string, context: AuditContext) {
  // Verificar permissão (RBAC)
  const hasPermission = await rbac.check({
    actor: context.actorId,
    action: 'user.delete',
    resource: userId,
  });
  
  if (!hasPermission) {
    await auditLog.record({
      action: 'user.delete.denied',
      actor: context.actorId,
      subject: userId,
      reason: 'rbac_denied',
    });
    
    throw new ForbiddenError('Permission denied');
  }
  
  // Verificar regras de negócio
  const user = await db.user.findUnique({ where: { id: userId } });
  
  if (user.role === 'admin' && context.actorRole !== 'super_admin') {
    await auditLog.record({
      action: 'user.delete.denied',
      actor: context.actorId,
      subject: userId,
      reason: 'cannot_delete_admin',
    });
    
    throw new ForbiddenError('Cannot delete admin user');
  }
  
  // Executar deleção
  await db.user.delete({ where: { id: userId } });
  
  // Registrar deleção
  await auditLog.record({
    action: 'user.delete.success',
    actor: context.actorId,
    subject: userId,
    severity: 'high',
    metadata: {
      deletedUser: {
        email: user.email,
        role: user.role,
        createdAt: user.createdAt,
      },
    },
  });
}
```

### 4. **Data Retention & Deletion**

Políticas de retenção de dados:

```typescript
import { retention } from '../utils/retention';

// Política de retenção
export const USER_DATA_RETENTION = {
  active_users: 'indefinite',
  inactive_users: '2_years',
  deleted_users: '30_days', // Soft delete
  audit_logs: '7_years', // Compliance
  metrics: '1_year',
};

// Implementação
export async function applyRetentionPolicy() {
  const cutoffDate = new Date();
  cutoffDate.setFullYear(cutoffDate.getFullYear() - 2);
  
  // Encontrar usuários inativos
  const inactiveUsers = await db.user.findMany({
    where: {
      lastLoginAt: { lt: cutoffDate },
      deletedAt: null,
    },
  });
  
  for (const user of inactiveUsers) {
    // Anonimizar dados
    await db.user.update({
      where: { id: user.id },
      data: {
        email: `deleted_${user.id}@example.com`,
        name: '[DELETED]',
        phone: null,
        address: null,
        cpf: null,
      },
    });
    
    // Registrar anonimização
    await auditLog.record({
      action: 'user.data.anonymized',
      subject: user.id,
      reason: 'retention_policy',
      policy: 'inactive_users_2_years',
    });
  }
}
```

### 5. **Explainability & Transparency**

Explicação de decisões automatizadas:

```typescript
import { explainer } from '../utils/explainer';

export async function approveLoan(
  userId: string,
  amount: number,
  context: AuditContext
) {
  const user = await db.user.findUnique({ where: { id: userId } });
  
  // Calcular score
  const creditScore = await calculateCreditScore(user);
  const incomeRatio = amount / user.monthlyIncome;
  const hasDefaultHistory = await checkDefaultHistory(user);
  
  // Decisão
  const approved = 
    creditScore >= 650 &&
    incomeRatio <= 0.3 &&
    !hasDefaultHistory;
  
  // Explicação da decisão
  const explanation = explainer.explain({
    decision: approved ? 'approved' : 'denied',
    factors: [
      {
        factor: 'credit_score',
        value: creditScore,
        threshold: 650,
        weight: 0.4,
        impact: creditScore >= 650 ? 'positive' : 'negative',
      },
      {
        factor: 'income_ratio',
        value: incomeRatio,
        threshold: 0.3,
        weight: 0.3,
        impact: incomeRatio <= 0.3 ? 'positive' : 'negative',
      },
      {
        factor: 'default_history',
        value: hasDefaultHistory,
        threshold: false,
        weight: 0.3,
        impact: !hasDefaultHistory ? 'positive' : 'negative',
      },
    ],
  });
  
  // Registrar decisão com explicação
  await auditLog.record({
    action: 'loan.decision',
    actor: 'system',
    subject: userId,
    decision: approved ? 'approved' : 'denied',
    explanation: explanation,
    metadata: {
      amount,
      creditScore,
      incomeRatio,
      hasDefaultHistory,
    },
  });
  
  return {
    approved,
    explanation,
  };
}
```

### 6. **Security Controls**

Controles de segurança:

```typescript
import { security } from '../utils/security';

export async function processPayment(
  userId: string,
  amount: number,
  context: AuditContext
) {
  // Rate limiting
  const rateLimitOk = await security.checkRateLimit({
    key: `payment:${userId}`,
    limit: 5,
    window: '1m',
  });
  
  if (!rateLimitOk) {
    await auditLog.record({
      action: 'payment.rate_limit_exceeded',
      actor: userId,
      severity: 'medium',
    });
    
    throw new RateLimitError('Too many payment attempts');
  }
  
  // Validar input
  const validationResult = security.validateInput({
    amount: { type: 'number', min: 0.01, max: 100000 },
  }, { amount });
  
  if (!validationResult.valid) {
    await auditLog.record({
      action: 'payment.invalid_input',
      actor: userId,
      errors: validationResult.errors,
    });
    
    throw new ValidationError(validationResult.errors);
  }
  
  // Detectar fraude
  const fraudScore = await security.detectFraud({
    userId,
    amount,
    ipAddress: context.ipAddress,
    deviceFingerprint: context.deviceFingerprint,
  });
  
  if (fraudScore > 0.8) {
    await auditLog.record({
      action: 'payment.fraud_detected',
      actor: userId,
      severity: 'critical',
      fraudScore,
    });
    
    throw new FraudError('Suspicious activity detected');
  }
  
  // Processar pagamento
  const result = await processPaymentInternal(userId, amount);
  
  await auditLog.record({
    action: 'payment.processed',
    actor: userId,
    amount,
    fraudScore,
  });
  
  return result;
}
```

## Arquivos Criados/Modificados

### Criados

```
src/utils/
├── audit.ts              # Audit logging
├── data-protection.ts    # LGPD/GDPR compliance
├── rbac.ts               # Role-based access control
├── retention.ts          # Data retention policies
├── explainer.ts          # Decision explainability
└── security.ts           # Security controls

src/governance/
└── <feature>/
    ├── policies.ts       # Políticas de governança
    └── compliance.ts     # Verificações de compliance

$METASPECS_DIR/governance/
└── <feature>/
    ├── governance.md     # Documentação de governança
    ├── audit-trail.md    # Eventos auditados
    ├── compliance.md     # Requisitos de compliance
    └── security.md       # Controles de segurança
```

### Modificados

```
src/<feature>/
└── <feature>.ts          # Código com governança adicionada

src/<feature>/
└── <feature>.test.ts     # Testes de governança
```

## Metaspec Criada

Cria documentação em `$METASPECS_DIR/governance/<feature>/governance.md`:

```markdown
# Governance: <Feature>

## Audit Trail

### Eventos Auditados

| Evento | Severidade | Dados Registrados |
|--------|------------|-------------------|
| Feature attempt | INFO | actor, subject, input |
| Feature success | INFO | actor, subject, output, duration |
| Feature failure | ERROR | actor, subject, error, reason |
| Access denied | WARN | actor, subject, reason |
| Data accessed | INFO | actor, subject, dataCategories |
| Data modified | MEDIUM | actor, subject, oldValue, newValue |
| Data deleted | HIGH | actor, subject, deletedData |

### Retenção de Logs

- Logs de auditoria: **7 anos** (compliance)
- Logs de acesso: **1 ano**
- Logs de erro: **6 meses**

## Compliance

### LGPD/GDPR

- ✅ Consentimento registrado
- ✅ Base legal documentada
- ✅ Dados sensíveis protegidos
- ✅ Direito ao esquecimento implementado
- ✅ Portabilidade de dados disponível

### PCI-DSS (se aplicável)

- ✅ Dados de cartão criptografados
- ✅ Tokenização implementada
- ✅ Logs de acesso mantidos

## Access Control

### Permissões Necessárias

| Ação | Permissão | Roles |
|------|-----------|-------|
| Read | `feature.read` | user, admin |
| Create | `feature.create` | user, admin |
| Update | `feature.update` | owner, admin |
| Delete | `feature.delete` | admin |

### RBAC Rules

```typescript
{
  "user": ["feature.read", "feature.create"],
  "admin": ["feature.*"],
  "super_admin": ["*"]
}
```

## Data Protection

### Dados Sensíveis

- Email (PII)
- Telefone (PII)
- CPF (PII sensível)
- Endereço (PII)

### Proteções Aplicadas

- ✅ Criptografia em repouso (AES-256)
- ✅ Criptografia em trânsito (TLS 1.3)
- ✅ Mascaramento em logs
- ✅ Tokenização de dados sensíveis

## Retention Policies

| Tipo de Dado | Retenção | Ação Após Expiração |
|--------------|----------|---------------------|
| Dados ativos | Indefinido | - |
| Dados inativos | 2 anos | Anonimizar |
| Dados deletados | 30 dias | Purgar permanentemente |
| Logs de auditoria | 7 anos | Arquivar |

## Security Controls

### Rate Limiting

- **Limite**: 5 requisições/minuto por usuário
- **Ação**: Bloquear + registrar

### Input Validation

- ✅ Validação de tipos
- ✅ Sanitização de input
- ✅ Proteção contra injection

### Fraud Detection

- ✅ Score de fraude calculado
- ✅ Bloqueio automático se score > 0.8
- ✅ Revisão manual se score > 0.5

## Explainability

### Decisões Automatizadas

Todas as decisões automatizadas incluem:

1. **Fatores considerados**
2. **Pesos de cada fator**
3. **Impacto (positivo/negativo)**
4. **Threshold aplicado**
5. **Decisão final**

### Exemplo

```json
{
  "decision": "denied",
  "factors": [
    {
      "factor": "credit_score",
      "value": 580,
      "threshold": 650,
      "weight": 0.4,
      "impact": "negative"
    }
  ]
}
```
```

## Testes Adicionados

```typescript
describe('Governance - Login', () => {
  it('should record audit log on success', async () => {
    const auditSpy = jest.spyOn(auditLog, 'record');
    
    await login('user@example.com', 'password123', context);
    
    expect(auditSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        action: 'auth.login.success',
        actor: context.actorId,
        subject: expect.any(String),
      })
    );
  });
  
  it('should enforce RBAC', async () => {
    const context = { actorId: 'user123', actorRole: 'user' };
    
    await expect(
      deleteUser('admin456', context)
    ).rejects.toThrow(ForbiddenError);
  });
  
  it('should mask sensitive data', async () => {
    const user = await getUserData('user123', { maskSensitiveData: true });
    
    expect(user.cpf).toBe('***.***.***-**');
  });
  
  it('should explain automated decision', async () => {
    const result = await approveLoan('user123', 50000, context);
    
    expect(result.explanation).toHaveProperty('factors');
    expect(result.explanation.factors).toHaveLength(3);
  });
});
```

## Output

```
✅ GOVERNANCE ADDED

Feature: login
Files modified: 3
Files created: 8

Added:
  ✅ Audit trail (all actions logged)
  ✅ Data protection (LGPD/GDPR compliant)
  ✅ Access control (RBAC)
  ✅ Retention policies
  ✅ Explainability (automated decisions)
  ✅ Security controls (rate limiting, fraud detection)

Audit Events:
  - login.attempt (INFO)
  - login.success (INFO)
  - login.failure (WARN)
  - login.denied (WARN)

Compliance:
  ✅ LGPD compliant
  ✅ GDPR compliant
  ✅ Audit logs retained for 7 years

Access Control:
  - auth.login.execute: [user, admin]
  - RBAC rules configured

Data Protection:
  - Email: masked in logs
  - Password: never logged
  - Encryption: AES-256

Security:
  - Rate limit: 5 req/min
  - Input validation: enabled
  - Fraud detection: enabled

Tests:
  ✅ 12 governance tests added
  ✅ All tests passing

Documentation:
  📄 $METASPECS_DIR/governance/login/governance.md
  📄 $METASPECS_DIR/governance/login/audit-trail.md
  📄 $METASPECS_DIR/governance/login/compliance.md
  📄 $METASPECS_DIR/governance/login/security.md

Next steps:
  1. Review compliance documentation
  2. Configure audit log retention
  3. Set up security monitoring
  4. Test in staging environment
```

## Benefícios

### 1. **Compliance Automático**

```
Antes: Compliance manual, propenso a erros
Depois: Compliance by design, automatizado
```

### 2. **Auditoria Completa**

```
Pergunta: "Quem acessou dados do usuário X em 2024?"
Resposta: Query em audit_logs → Resposta em segundos
```

### 3. **Transparência**

```
Usuário: "Por que meu empréstimo foi negado?"
Sistema: "Score de crédito abaixo de 650 (peso 40%)"
```

### 4. **Segurança Proativa**

```
Antes: Fraude acontece → Detecta depois
Depois: Fraude detectada → Bloqueia automaticamente
```

## Dicas Pro

### 1. **Sempre Registre Tentativas E Resultados**

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

### 2. **Documente Base Legal (LGPD)**

```typescript
await auditLog.record({
  action: 'user.data.accessed',
  legalBasis: 'legitimate_interest', // ou 'consent', 'contract', etc
  dataCategories: ['email', 'phone'],
});
```

### 3. **Explique Decisões Automatizadas**

```typescript
// Sempre que IA/algoritmo tomar decisão
const explanation = explainer.explain({ ... });
await auditLog.record({ decision, explanation });
```

## Implementação

1. **Analisar** requisitos de compliance
2. **Identificar** dados sensíveis
3. **Adicionar** audit trail
4. **Implementar** RBAC
5. **Configurar** retention policies
6. **Adicionar** explainability
7. **Configurar** security controls
8. **Documentar** em metaspecs
9. **Testar** governança
