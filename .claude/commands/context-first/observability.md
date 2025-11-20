---
name: context-first-observability
description: Adicionar observabilidade completa (logging, métricas, tracing) a uma feature
tools: None
---

# Context-First Observability

Adiciona camada completa de observabilidade a uma feature seguindo o pilar **Observability-Driven** da metodologia CONTEXT-FIRST™.

## Quando Usar

- ✅ Feature implementada e testada
- ✅ Código funcionando corretamente
- ✅ Antes de deploy em produção
- ✅ Para features críticas de negócio

## Argumentos

```
/context-first-observability <feature-name>
```

- `feature-name`: Nome da feature (ex: `login`, `payment`, `checkout`)

## O Que Adiciona

### 1. **Structured Logging**

Logging estruturado com contexto completo:

```typescript
import { logger } from '../utils/logger';

// ANTES (sem observabilidade)
export async function login(email: string, password: string) {
  const user = await findUser(email);
  if (!user) throw new Error('User not found');
  return generateToken(user);
}

// DEPOIS (com observabilidade)
export async function login(email: string, password: string) {
  const startTime = Date.now();
  const requestId = generateRequestId();
  
  logger.info('Login attempt started', {
    requestId,
    email,
    timestamp: new Date().toISOString(),
  });
  
  try {
    const user = await findUser(email);
    
    if (!user) {
      logger.warn('Login failed - user not found', {
        requestId,
        email,
        duration: Date.now() - startTime,
      });
      throw new Error('User not found');
    }
    
    const token = generateToken(user);
    
    logger.info('Login successful', {
      requestId,
      userId: user.id,
      email: user.email,
      duration: Date.now() - startTime,
    });
    
    return token;
  } catch (error) {
    logger.error('Login failed with error', {
      requestId,
      email,
      error: error.message,
      stack: error.stack,
      duration: Date.now() - startTime,
    });
    throw error;
  }
}
```

### 2. **Metrics & Counters**

Métricas para monitoramento em tempo real:

```typescript
import { metrics } from '../utils/metrics';

export async function login(email: string, password: string) {
  const startTime = Date.now();
  
  try {
    // ... código de login ...
    
    // Métricas de sucesso
    metrics.increment('auth.login.success', {
      tags: { method: 'password' }
    });
    
    metrics.timing('auth.login.duration', Date.now() - startTime);
    
    metrics.gauge('auth.active_sessions', await getActiveSessions());
    
    return token;
  } catch (error) {
    // Métricas de erro
    metrics.increment('auth.login.failure', {
      tags: { 
        method: 'password',
        reason: error.message 
      }
    });
    
    throw error;
  }
}
```

### 3. **Distributed Tracing**

Rastreamento de requisições através de múltiplos serviços:

```typescript
import { tracer } from '../utils/tracer';

export async function login(email: string, password: string) {
  const span = tracer.startSpan('auth.login');
  
  span.setTag('user.email', email);
  span.setTag('service', 'auth-service');
  
  try {
    // Span filho para busca no DB
    const dbSpan = tracer.startSpan('db.findUser', { childOf: span });
    const user = await findUser(email);
    dbSpan.finish();
    
    if (!user) {
      span.setTag('error', true);
      span.setTag('error.reason', 'user_not_found');
      throw new Error('User not found');
    }
    
    // Span filho para geração de token
    const tokenSpan = tracer.startSpan('auth.generateToken', { childOf: span });
    const token = generateToken(user);
    tokenSpan.finish();
    
    span.setTag('user.id', user.id);
    span.finish();
    
    return token;
  } catch (error) {
    span.setTag('error', true);
    span.setTag('error.message', error.message);
    span.finish();
    throw error;
  }
}
```

### 4. **Health Checks**

Endpoints de health check para monitoramento:

```typescript
// src/health/auth-health.ts
export async function checkAuthHealth() {
  const checks = {
    database: await checkDatabaseConnection(),
    redis: await checkRedisConnection(),
    jwt_secret: !!process.env.JWT_SECRET,
  };
  
  const healthy = Object.values(checks).every(check => check === true);
  
  logger.info('Health check performed', {
    service: 'auth',
    healthy,
    checks,
  });
  
  return {
    status: healthy ? 'healthy' : 'unhealthy',
    checks,
    timestamp: new Date().toISOString(),
  };
}
```

### 5. **Error Tracking**

Rastreamento detalhado de erros:

```typescript
import { errorTracker } from '../utils/error-tracker';

export async function login(email: string, password: string) {
  try {
    // ... código de login ...
  } catch (error) {
    // Enviar erro para Sentry/Rollbar/etc
    errorTracker.captureException(error, {
      context: {
        feature: 'auth.login',
        email,
        timestamp: new Date().toISOString(),
      },
      user: {
        email,
      },
      tags: {
        service: 'auth',
        environment: process.env.NODE_ENV,
      },
    });
    
    throw error;
  }
}
```

## Arquivos Criados/Modificados

### Criados

```
src/utils/
├── logger.ts           # Winston/Pino logger configurado
├── metrics.ts          # StatsD/Prometheus metrics
├── tracer.ts           # OpenTelemetry/Jaeger tracing
└── error-tracker.ts    # Sentry/Rollbar integration

src/health/
└── <feature>-health.ts # Health checks específicos

$METASPECS_DIR/observability/
└── <feature>/
    └── observability.md # Documentação de observabilidade
```

### Modificados

```
src/<feature>/
└── <feature>.ts        # Código com observabilidade adicionada

src/<feature>/
└── <feature>.test.ts   # Testes de observabilidade
```

## Metaspec Criada

Cria documentação em `$METASPECS_DIR/observability/<feature>/observability.md`:

```markdown
# Observability: <Feature>

## Logs Estruturados

### Eventos Logados

| Evento | Level | Campos |
|--------|-------|--------|
| Feature started | INFO | requestId, timestamp, input |
| Feature succeeded | INFO | requestId, duration, output |
| Feature failed | ERROR | requestId, error, stack, duration |

### Exemplo de Log

```json
{
  "level": "info",
  "message": "Login successful",
  "requestId": "req_abc123",
  "userId": "user_xyz789",
  "email": "user@example.com",
  "duration": 245,
  "timestamp": "2025-11-14T12:30:45.123Z"
}
```

## Métricas

### Counters

- `auth.login.success` - Logins bem-sucedidos
- `auth.login.failure` - Logins falhos

### Timings

- `auth.login.duration` - Tempo de execução (ms)

### Gauges

- `auth.active_sessions` - Sessões ativas

## Tracing

### Spans

- `auth.login` (root span)
  - `db.findUser` (child span)
  - `auth.generateToken` (child span)

### Tags

- `user.email`
- `user.id`
- `service: auth-service`
- `error: true/false`

## Health Checks

### Endpoint

`GET /health/auth`

### Response

```json
{
  "status": "healthy",
  "checks": {
    "database": true,
    "redis": true,
    "jwt_secret": true
  },
  "timestamp": "2025-11-14T12:30:45.123Z"
}
```

## Alertas Recomendados

1. **Taxa de Erro > 5%**: Alerta crítico
2. **Latência P95 > 500ms**: Alerta warning
3. **Health check falhou**: Alerta crítico
4. **Sessões ativas > 10000**: Alerta info
```

## Testes Adicionados

```typescript
describe('Observability - Login', () => {
  it('should log successful login', async () => {
    const logSpy = jest.spyOn(logger, 'info');
    
    await login('user@example.com', 'password123');
    
    expect(logSpy).toHaveBeenCalledWith(
      'Login successful',
      expect.objectContaining({
        requestId: expect.any(String),
        userId: expect.any(String),
        duration: expect.any(Number),
      })
    );
  });
  
  it('should increment success metric', async () => {
    const metricSpy = jest.spyOn(metrics, 'increment');
    
    await login('user@example.com', 'password123');
    
    expect(metricSpy).toHaveBeenCalledWith('auth.login.success');
  });
  
  it('should create trace span', async () => {
    const spanSpy = jest.spyOn(tracer, 'startSpan');
    
    await login('user@example.com', 'password123');
    
    expect(spanSpy).toHaveBeenCalledWith('auth.login');
  });
});
```

## Output

```
✅ OBSERVABILITY ADDED

Feature: login
Files modified: 3
Files created: 5

Added:
  ✅ Structured logging (Winston)
  ✅ Metrics (StatsD)
  ✅ Distributed tracing (OpenTelemetry)
  ✅ Health checks
  ✅ Error tracking (Sentry)

Logs:
  - Login attempt started (INFO)
  - Login successful (INFO)
  - Login failed (ERROR/WARN)

Metrics:
  - auth.login.success (counter)
  - auth.login.failure (counter)
  - auth.login.duration (timing)
  - auth.active_sessions (gauge)

Traces:
  - auth.login (root span)
    - db.findUser (child)
    - auth.generateToken (child)

Health Check:
  GET /health/auth

Tests:
  ✅ 8 observability tests added
  ✅ All tests passing

Documentation:
  📄 $METASPECS_DIR/observability/login/observability.md

Next steps:
  1. Configure monitoring dashboard
  2. Set up alerts
  3. Test in staging environment
```

## Integração com Stack

### Winston (Logging)

```typescript
import winston from 'winston';

export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});
```

### StatsD (Metrics)

```typescript
import StatsD from 'node-statsd';

export const metrics = new StatsD({
  host: process.env.STATSD_HOST,
  port: 8125,
});
```

### OpenTelemetry (Tracing)

```typescript
import { trace } from '@opentelemetry/api';

export const tracer = trace.getTracer('auth-service');
```

## Benefícios

### 1. **Visibilidade Total**

```
Antes: "Por que falhou?" 🤷
Depois: "Falhou no DB, linha 45, usuário X, às 12:30" ✅
```

### 2. **Debug Rápido**

```
Antes: 2 horas debugando
Depois: 5 minutos olhando logs estruturados
```

### 3. **Proatividade**

```
Antes: Usuário reclama → Investiga → Corrige
Depois: Alerta dispara → Corrige → Usuário nem percebe
```

### 4. **Métricas de Negócio**

```
- Taxa de conversão
- Tempo médio de resposta
- Usuários ativos
- Taxa de erro por feature
```

## Dicas Pro

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
  ip: req.ip,
});
```

### 3. **Métricas em Tudo**

```typescript
// Sucesso, erro, latência, contadores
metrics.increment('feature.success');
metrics.increment('feature.failure');
metrics.timing('feature.duration', duration);
metrics.gauge('feature.active', count);
```

## Implementação

1. **Analisar** código da feature
2. **Identificar** pontos críticos
3. **Adicionar** logging estruturado
4. **Adicionar** métricas
5. **Adicionar** tracing
6. **Criar** health checks
7. **Documentar** em metaspec
8. **Testar** observabilidade
