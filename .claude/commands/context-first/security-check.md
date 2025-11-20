---
name: context-first-security-check
description: Verificar segurança do código antes de commit
tools: Read, Glob, Grep, Bash
---

# Security Check Command

## Uso
```bash
# Verificar arquivo específico
/context-first security-check src/api/auth.js

# Verificar todos os arquivos modificados
/context-first security-check
```

<file_path>
#$ARGUMENTS
</file_path>

---

## Comportamento

### Passo 1: Identificar Arquivos a Verificar

**Se <file_path> estiver vazio**:
- Executar `git diff --name-only` para listar arquivos modificados
- Verificar todos os arquivos modificados

**Se <file_path> estiver preenchido**:
- Verificar apenas <file_path>

---

### Passo 2: Ler Arquivo(s)

Ler conteúdo completo do(s) arquivo(s) a verificar.

---

### Passo 3: Executar Checklist de Segurança

#### 1. Dados Sensíveis

- [ ] **Senhas NÃO estão em logs**
  - Buscar: `log`, `print`, `console.log`, `logger`
  - Verificar se senha/password aparece

- [ ] **Senhas NÃO estão em responses**
  - Buscar: `return`, `response`, `json`
  - Verificar se senha está sendo retornada

- [ ] **Tokens NÃO estão em logs**
  - Buscar: `token`, `jwt`, `api_key`
  - Verificar se tokens aparecem em logs

- [ ] **API keys NÃO estão hardcoded**
  - Buscar: `api_key`, `secret`, `password`
  - Verificar se valores estão hardcoded (não em .env)

---

#### 2. Injeções

- [ ] **SQL injection prevenido**
  - Buscar: `execute`, `query`, `raw`
  - Verificar se usa parameterized queries

- [ ] **NoSQL injection prevenido**
  - Buscar: `find`, `findOne`, `update`
  - Verificar se inputs são sanitizados

- [ ] **XSS prevenido**
  - Buscar: `innerHTML`, `dangerouslySetInnerHTML`
  - Verificar se inputs são escapados

- [ ] **Command injection prevenido**
  - Buscar: `exec`, `spawn`, `system`
  - Verificar se inputs são validados

---

#### 3. Autenticação/Autorização

- [ ] **Endpoints protegidos requerem autenticação**
  - Buscar: `@app.post`, `@app.get`, `router.post`
  - Verificar se tem decorator de autenticação

- [ ] **Autorização verificada**
  - Verificar se usuário tem permissão para ação
  - Buscar: `check_permission`, `authorize`

- [ ] **JWT validado corretamente**
  - Buscar: `jwt.decode`, `verify_token`
  - Verificar se valida signature e expiration

- [ ] **Rate limiting configurado**
  - Buscar: `rate_limit`, `throttle`
  - Verificar se endpoints críticos têm rate limiting

---

#### 4. Validação de Inputs

- [ ] **Todos os inputs validados**
  - Buscar: `request.json`, `request.form`, `req.body`
  - Verificar se tem validação

- [ ] **Tipos validados**
  - Verificar se usa Pydantic, Joi, Zod, etc.

- [ ] **Tamanhos validados**
  - Verificar se tem min/max length

- [ ] **Formatos validados**
  - Verificar se valida email, URL, etc.

---

### Passo 4: Calcular Security Score

**Pontuação**:
- Cada item do checklist = 1 ponto
- Total de itens = 16
- **Security Score** = (itens passando / 16) × 10

**Classificação**:
- **9-10**: Excelente ✅
- **8-9**: Bom ✅
- **7-8**: Aceitável ⚠️
- **< 7**: Crítico ❌ (BLOQUEAR commit)

---

### Passo 5: Gerar Relatório

```
🔒 Security Check - <file_path>

Security Score: X/10

Issues Found:

  🔴 CRITICAL (N)
    ├─ Line 42: Password logged in plain text
    │  Code: logger.info(f"Login attempt: {email} / {password}")
    │  Fix: Remove password from log
    │
    └─ Line 87: SQL query without parameterization
       Code: cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
       Fix: Use parameterized query
  
  🟡 WARNING (N)
    ├─ Line 15: JWT secret in code (should be in .env)
    │  Code: JWT_SECRET = "my-secret-key"
    │  Fix: Move to environment variable
    │
    └─ Line 103: No rate limiting on login endpoint
       Fix: Add @rate_limit(max=5, window=60)

  ℹ️ INFO (N)
    └─ Line 55: Consider adding input validation
       Fix: Use Pydantic model for request validation

Recommendations:
  1. Fix CRITICAL issues before commit
  2. Move secrets to environment variables
  3. Add input validation with Pydantic/Joi
  4. Add rate limiting to authentication endpoints

Decision:
  ✅ Security score >= 8: APPROVED for commit
  ❌ Security score < 8: BLOCKED - fix issues first
```

---

### Passo 6: Decisão

**Se Security Score >= 8**:
```
✅ APPROVED for commit

Security score is acceptable. You may proceed with commit.

Recommendations to improve to 10/10:
  - Fix WARNING issues
  - Add missing validations
```

**Se Security Score < 8**:
```
❌ BLOCKED - Security issues must be fixed

CRITICAL issues found that MUST be fixed before commit:
  1. Password logged in plain text (Line 42)
  2. SQL injection vulnerability (Line 87)

Actions required:
  1. Fix CRITICAL issues
  2. Run /context-first security-check again
  3. Only commit after score >= 8
```

---

## Exemplo de Uso

### Exemplo 1: Verificar Arquivo Específico

```bash
/context-first security-check src/api/auth.py
```

**Output**:
```
🔒 Security Check - src/api/auth.py

Security Score: 9/10 ✅

Issues Found:

  🟡 WARNING (1)
    └─ Line 15: JWT secret should be in .env
       Code: JWT_SECRET = "my-secret-key"
       Fix: Move to environment variable

Recommendations:
  1. Move JWT_SECRET to .env file
  2. Load using: os.getenv('JWT_SECRET')

✅ APPROVED for commit

Security score is excellent. Minor improvement suggested.
```

---

### Exemplo 2: Verificar Todos os Arquivos Modificados

```bash
/context-first security-check
```

**Output**:
```
🔒 Security Check - Multiple Files

Files checked (3):
  - src/api/auth.py
  - src/api/users.py
  - src/utils/validators.py

Overall Security Score: 7.5/10 ⚠️

Issues Found:

  🔴 CRITICAL (2)
    ├─ src/api/auth.py:42 - Password in logs
    └─ src/api/users.py:87 - SQL injection vulnerability
  
  🟡 WARNING (3)
    ├─ src/api/auth.py:15 - JWT secret hardcoded
    ├─ src/api/users.py:103 - No rate limiting
    └─ src/utils/validators.py:25 - Weak email validation

❌ BLOCKED - Fix CRITICAL issues first

Actions required:
  1. Remove password from logs (auth.py:42)
  2. Use parameterized queries (users.py:87)
  3. Run security check again
```

---

## Relacionado

- [/engineer work](../engineer/work.md) - Implementar fixes
- [/context-first validate-spec](./validate-spec.md) - Validar contra metaspecs
- [@security-engineer](../../agents/security-engineer.md) - Agente de segurança
