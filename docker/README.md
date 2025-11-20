# Docker Setup - MongoDB + Redis

Setup local de MongoDB e Redis usando Docker Compose para desenvolvimento.

## 🎯 Serviços Disponíveis

### MongoDB (porta 27017)
- **Image**: `mongo:7.0`
- **Admin UI**: http://localhost:8081 (Mongo Express)
- **User Admin**: `admin` / `dev_password_change_in_production`
- **User App**: `context_first_app` / `app_password_change_in_production`
- **Database**: `context_first_dev`

### Redis (porta 6379)
- **Image**: `redis:7-alpine`
- **Password**: `dev_redis_password`
- **Persistence**: AOF enabled

### Mongo Express (porta 8081)
- **Interface Web**: http://localhost:8081
- **Sem autenticação** (apenas para dev local)

## 🚀 Comandos

### Subir databases
```bash
pnpm db:up
```

### Ver logs
```bash
pnpm db:logs
```

### Parar databases
```bash
pnpm db:down
```

### Resetar tudo (apaga dados!)
```bash
pnpm db:reset
```

### Acessar MongoDB CLI
```bash
pnpm db:mongo

# Dentro do mongosh:
use context_first_dev
db.projects.find()
db.demands.find()
```

### Acessar Redis CLI
```bash
pnpm db:redis

# Dentro do redis-cli:
KEYS *
GET some_key
```

## 📊 Estrutura do MongoDB

### Collections Criadas Automaticamente

**projects**
- Índice: `user_id` + `created_at`
- Validação: Schema obrigatório

**demands**
- Índice: `project_id` + `status`
- Índice: `project_id` + `created_at`
- Validação: Schema com enum de status

**checkpoints**
- Índice: `project_id` + `created_at`
- TTL Index: `expires_at` (auto-delete após expiração)

## 🔒 Segurança

### ⚠️ IMPORTANTE

As senhas configuradas são **APENAS PARA DESENVOLVIMENTO LOCAL**!

**NUNCA use estas senhas em produção!**

Para produção, use:
- MongoDB Atlas (cloud managed)
- Redis Upstash (cloud managed)
- Senhas fortes e únicas
- Secrets management (AWS Secrets Manager, etc)

## 🐳 Volumes Docker

Dados são persistidos em volumes Docker:
- `mongodb_data`: Dados do MongoDB
- `mongodb_config`: Config do MongoDB
- `redis_data`: Dados do Redis (AOF)

**Para limpar volumes:**
```bash
docker-compose down -v
```

## 🔍 Troubleshooting

### MongoDB não inicia

```bash
# Ver logs
docker logs context-first-mongodb

# Reiniciar
docker-compose restart mongodb
```

### Redis não conecta

```bash
# Testar conexão
docker exec -it context-first-redis redis-cli -a dev_redis_password ping
# Deve retornar: PONG
```

### Porta já em uso

```bash
# Verificar quem está usando porta 27017
lsof -i :27017

# Matar processo (se necessário)
kill -9 <PID>
```

### Reset completo

```bash
# Parar tudo
docker-compose down -v

# Remover volumes órfãos
docker volume prune

# Subir novamente
docker-compose up -d
```

## 📚 Referências

- [MongoDB Docker Official](https://hub.docker.com/_/mongo)
- [Redis Docker Official](https://hub.docker.com/_/redis)
- [Mongo Express](https://github.com/mongo-express/mongo-express)

---

**Gerado com Metodologia CONTEXT-FIRST™**
