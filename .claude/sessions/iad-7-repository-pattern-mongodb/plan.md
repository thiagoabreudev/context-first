# IAD-7: Repository Pattern + MongoDB

**Importante**: Atualize este arquivo conforme progride na implementação.

---

## FASE 1: Application Layer (Interfaces) [Não Iniciada ⏳]

### Descrição
Criar interfaces de repositórios (ports) no Application Layer. Estas interfaces definem o contrato de persistência que Infrastructure implementará.

### Tarefas

#### 1.1 - Criar estrutura base Application Layer [Não Iniciada ⏳]
- Criar `application/interfaces/__init__.py`
- Preparar estrutura para 4 interfaces

**Arquivos**:
- `src/application/interfaces/__init__.py`

**Testes**:
- N/A (apenas estrutura)

#### 1.2 - Criar IProjectRepository [Não Iniciada ⏳]
- Interface abstrata com ABC
- Métodos: `create`, `get_by_id`, `update`, `delete`
- Type hints completos
- Docstrings detalhadas
- Async methods

**Arquivos**:
- `src/application/interfaces/i_project_repository.py`

**Contrato**:
```python
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.project import Project

class IProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Persiste novo projeto"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """Busca projeto por ID (UUID)"""
        pass

    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Atualiza projeto existente"""
        pass

    @abstractmethod
    async def delete(self, project_id: str) -> None:
        """Remove projeto"""
        pass
```

**Validações**:
- Type hints corretos
- ABC usado corretamente
- @abstractmethod em todos métodos
- Async/await

#### 1.3 - Criar IDemandRepository [Não Iniciada ⏳]
- Interface abstrata com ABC
- Métodos CRUD: `create`, `get_by_id`, `update`, `delete`
- Type hints completos
- Async methods

**Arquivos**:
- `src/application/interfaces/i_demand_repository.py`

**Validações**:
- Imports apenas de domain layer
- Optional[Demand] para get_by_id
- Async/await

#### 1.4 - Criar IMetaspecRepository [Não Iniciada ⏳]
- Interface abstrata com ABC
- Métodos CRUD: `create`, `get_by_id`, `update`, `delete`
- Type hints completos
- Async methods

**Arquivos**:
- `src/application/interfaces/i_metaspec_repository.py`

**Validações**:
- Imports apenas de domain layer
- Optional[Metaspec] para get_by_id
- Async/await

#### 1.5 - Criar ICheckpointRepository [Não Iniciada ⏳]
- Interface abstrata com ABC
- Métodos CRUD: `create`, `get_by_id`, `update`, `delete`
- Type hints completos
- Async methods

**Arquivos**:
- `src/application/interfaces/i_checkpoint_repository.py`

**Validações**:
- Imports apenas de domain layer
- Optional[Checkpoint] para get_by_id
- Async/await

#### 1.6 - Atualizar __init__.py com exports [Não Iniciada ⏳]
- Exportar todas as 4 interfaces
- `__all__` definido corretamente

**Arquivos**:
- `src/application/interfaces/__init__.py`

**Exports**:
```python
from .i_project_repository import IProjectRepository
from .i_demand_repository import IDemandRepository
from .i_metaspec_repository import IMetaspecRepository
from .i_checkpoint_repository import ICheckpointRepository

__all__ = [
    "IProjectRepository",
    "IDemandRepository",
    "IMetaspecRepository",
    "ICheckpointRepository",
]
```

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 2: Dependencies Setup [Não Iniciada ⏳]

### Descrição
Instalar e configurar dependências necessárias (Motor, PyMongo) e preparar ambiente de testes.

### Tarefas

#### 2.1 - Adicionar Motor e PyMongo [Não Iniciada ⏳]
- Atualizar `requirements.txt`
- Instalar no venv

**Arquivos**:
- `requirements.txt`

**Dependências**:
```
# Database - MongoDB (IAD-7)
motor==3.3.2  # MongoDB async driver (official)
pymongo==4.6.1  # Required by Motor
```

**Comandos**:
```bash
cd packages/backend
source venv/bin/activate
pip install motor==3.3.2 pymongo==4.6.1
```

**Validações**:
- Import funciona: `from motor.motor_asyncio import AsyncIOMotorDatabase`
- Versões corretas instaladas

#### 2.2 - Configurar fixtures pytest [Não Iniciada ⏳]
- Adicionar fixtures MongoDB em `conftest.py`
- `mongodb_client` (session scope)
- `mongodb_database` (function scope, limpa entre testes)

**Arquivos**:
- `tests/conftest.py`

**Fixtures**:
```python
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="session")
async def mongodb_client():
    """Cliente MongoDB compartilhado"""
    client = AsyncIOMotorClient(
        "mongodb://context_first_app:app_password_change_in_production@localhost:27017/context_first_dev?authSource=context_first_dev"
    )
    yield client
    client.close()

@pytest.fixture(scope="function")
async def mongodb_database(mongodb_client):
    """Database limpo para cada teste"""
    db = mongodb_client['context_first_test']

    # Limpar antes
    await db['projects'].delete_many({})
    await db['demands'].delete_many({})
    await db['metaspecs'].delete_many({})
    await db['checkpoints'].delete_many({})

    yield db
```

**Validações**:
- MongoDB deve estar rodando (via docker-compose)
- Fixtures funcionam corretamente

#### 2.3 - Verificar MongoDB está rodando [Não Iniciada ⏳]
- Subir Docker Compose se necessário
- Verificar conectividade

**Comandos**:
```bash
# Subir MongoDB
pnpm db:up

# Verificar
pnpm db:mongo
# Dentro do mongosh:
# show dbs
```

**Validações**:
- MongoDB acessível em localhost:27017
- Database `context_first_dev` existe

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 3: Infrastructure Layer - MongoProjectRepository [Não Iniciada ⏳]

### Descrição
Implementar primeiro repository completo (MongoProjectRepository) com testes. Servirá de template para os outros 3.

### Tarefas

#### 3.1 - Criar estrutura Infrastructure Layer [Não Iniciada ⏳]
- Criar `infrastructure/persistence/mongodb/__init__.py`

**Arquivos**:
- `src/infrastructure/persistence/mongodb/__init__.py`

#### 3.2 - Implementar MongoProjectRepository [Não Iniciada ⏳]
- Implementa `IProjectRepository`
- Métodos: `create`, `get_by_id`, `update`, `delete`
- Conversões: `_to_document`, `_to_entity`
- ContextBudget como subdocumento
- UUID string no campo `id`

**Arquivos**:
- `src/infrastructure/persistence/mongodb/mongo_project_repository.py`

**Métodos Privados**:
```python
def _to_document(self, project: Project) -> dict:
    """Entity → MongoDB document"""
    return {
        'id': project.id,  # UUID string
        'name': project.name,
        'description': project.description,
        'owner_id': project.owner_id,
        'context_budget': {  # Subdocumento
            'max_tokens': project.context_budget.max_tokens,
            'used_tokens': project.context_budget.used_tokens
        },
        'created_at': project.created_at,
        'updated_at': project.updated_at
    }

def _to_entity(self, document: dict) -> Project:
    """MongoDB document → Entity"""
    return Project(
        id=document['id'],
        name=document['name'],
        description=document['description'],
        owner_id=document['owner_id'],
        context_budget=ContextBudget(
            max_tokens=document['context_budget']['max_tokens'],
            used_tokens=document['context_budget']['used_tokens']
        ),
        created_at=document['created_at'],
        updated_at=document.get('updated_at')
    )
```

**Validações**:
- Implementa interface corretamente
- Type hints completos
- Async/await
- Conversões corretas

#### 3.3 - Testes de Integração MongoProjectRepository [Não Iniciada ⏳]
- Test: Create → Get (persistência)
- Test: Update → Get (atualização)
- Test: Delete → Get (remoção)
- Test: Get not found (retorna None)
- Test: ContextBudget conversion (Value Object)

**Arquivos**:
- `tests/infrastructure/persistence/mongodb/__init__.py`
- `tests/infrastructure/persistence/mongodb/test_mongo_project_repository.py`

**Testes Críticos**:
```python
@pytest.mark.asyncio
async def test_create_and_get_project(mongodb_database):
    """Persistência básica funciona"""
    repo = MongoProjectRepository(mongodb_database)
    project = Project(
        id=str(uuid.uuid4()),
        name="Test Project",
        description="Test",
        owner_id="user_123",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow()
    )

    await repo.create(project)
    found = await repo.get_by_id(project.id)

    assert found is not None
    assert found.name == "Test Project"
    assert found.context_budget.max_tokens == 100000

@pytest.mark.asyncio
async def test_update_project(mongodb_database):
    """Atualização funciona"""
    # Create, update, verify

@pytest.mark.asyncio
async def test_delete_project(mongodb_database):
    """Deleção funciona"""
    # Create, delete, verify None

@pytest.mark.asyncio
async def test_context_budget_conversion(mongodb_database):
    """ContextBudget Value Object converte corretamente"""
    # Verify subdocument structure
```

**Validações**:
- Todos os testes passam
- Coverage > 95%
- MongoDB limpo entre testes

#### 3.4 - Rodar testes e validar coverage [Não Iniciada ⏳]
- Rodar: `pytest tests/infrastructure/persistence/mongodb/ -v --cov=src/infrastructure`
- Coverage > 95%

**Comandos**:
```bash
cd packages/backend
source venv/bin/activate

# Subir MongoDB
pnpm db:up

# Rodar testes
pytest tests/infrastructure/persistence/mongodb/ -v --cov=src/infrastructure --cov-fail-under=95

# Ver coverage HTML
pytest tests/infrastructure/persistence/mongodb/ --cov=src/infrastructure --cov-report=html
open htmlcov/index.html
```

**Validações**:
- Todos testes passam
- Coverage > 95%
- Conversões funcionando

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 4: Infrastructure Layer - MongoDemandRepository [Não Iniciada ⏳]

### Descrição
Implementar MongoDemandRepository seguindo padrão do MongoProjectRepository. Atenção para conversão de DemandStatus enum.

### Tarefas

#### 4.1 - Implementar MongoDemandRepository [Não Iniciada ⏳]
- Implementa `IDemandRepository`
- Métodos CRUD
- Conversões: `_to_document`, `_to_entity`
- DemandStatus enum → string
- ContextBudget opcional (Optional[ContextBudget])

**Arquivos**:
- `src/infrastructure/persistence/mongodb/mongo_demand_repository.py`

**Conversão Especial - DemandStatus**:
```python
def _to_document(self, demand: Demand) -> dict:
    return {
        'id': demand.id,
        'project_id': demand.project_id,
        'title': demand.title,
        'description': demand.description,
        'status': demand.status.value,  # Enum → string
        'context_budget': {
            'max_tokens': demand.context_budget.max_tokens,
            'used_tokens': demand.context_budget.used_tokens
        } if demand.context_budget else None,  # Opcional
        'created_at': demand.created_at,
        'updated_at': demand.updated_at
    }

def _to_entity(self, document: dict) -> Demand:
    return Demand(
        id=document['id'],
        project_id=document['project_id'],
        title=document['title'],
        description=document['description'],
        status=DemandStatus(document['status']),  # string → Enum
        context_budget=ContextBudget(
            max_tokens=document['context_budget']['max_tokens'],
            used_tokens=document['context_budget']['used_tokens']
        ) if document.get('context_budget') else None,
        created_at=document['created_at'],
        updated_at=document.get('updated_at')
    )
```

**Validações**:
- DemandStatus converte corretamente
- ContextBudget opcional funciona (None e preenchido)

#### 4.2 - Testes de Integração MongoDemandRepository [Não Iniciada ⏳]
- Test: CRUD básico
- Test: DemandStatus conversion (enum ↔ string)
- Test: Optional ContextBudget (None e preenchido)

**Arquivos**:
- `tests/infrastructure/persistence/mongodb/test_mongo_demand_repository.py`

**Testes Críticos**:
```python
@pytest.mark.asyncio
async def test_demand_status_conversion(mongodb_database):
    """DemandStatus enum converte para string e volta"""
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(
        id=str(uuid.uuid4()),
        project_id="proj_123",
        title="Test Demand",
        description="Test",
        status=DemandStatus.SPEC_APPROVED,  # Enum
        created_at=datetime.utcnow()
    )

    await repo.create(demand)
    found = await repo.get_by_id(demand.id)

    assert found.status == DemandStatus.SPEC_APPROVED
    assert isinstance(found.status, DemandStatus)

@pytest.mark.asyncio
async def test_optional_context_budget(mongodb_database):
    """ContextBudget opcional funciona (None)"""
    repo = MongoDemandRepository(mongodb_database)
    demand = Demand(..., context_budget=None)

    await repo.create(demand)
    found = await repo.get_by_id(demand.id)

    assert found.context_budget is None
```

**Validações**:
- Todos testes passam
- Coverage > 95%

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 5: Infrastructure Layer - MongoMetaspecRepository [Não Iniciada ⏳]

### Descrição
Implementar MongoMetaspecRepository. Atenção para conversão de MetaspecType enum.

### Tarefas

#### 5.1 - Implementar MongoMetaspecRepository [Não Iniciada ⏳]
- Implementa `IMetaspecRepository`
- Métodos CRUD
- Conversões: `_to_document`, `_to_entity`
- MetaspecType enum → string
- Version (int)

**Arquivos**:
- `src/infrastructure/persistence/mongodb/mongo_metaspec_repository.py`

**Conversão Especial - MetaspecType**:
```python
def _to_document(self, metaspec: Metaspec) -> dict:
    return {
        'id': metaspec.id,
        'demand_id': metaspec.demand_id,
        'type': metaspec.type.value,  # Enum → string
        'content': metaspec.content,
        'version': metaspec.version,
        'created_at': metaspec.created_at,
        'updated_at': metaspec.updated_at
    }

def _to_entity(self, document: dict) -> Metaspec:
    return Metaspec(
        id=document['id'],
        demand_id=document['demand_id'],
        type=MetaspecType(document['type']),  # string → Enum
        content=document['content'],
        version=document['version'],
        created_at=document['created_at'],
        updated_at=document.get('updated_at')
    )
```

**Validações**:
- MetaspecType converte corretamente
- Version (int) persiste corretamente

#### 5.2 - Testes de Integração MongoMetaspecRepository [Não Iniciada ⏳]
- Test: CRUD básico
- Test: MetaspecType conversion (enum ↔ string)
- Test: Version incrementa corretamente

**Arquivos**:
- `tests/infrastructure/persistence/mongodb/test_mongo_metaspec_repository.py`

**Testes Críticos**:
```python
@pytest.mark.asyncio
async def test_metaspec_type_conversion(mongodb_database):
    """MetaspecType enum converte corretamente"""
    # Similar ao test de DemandStatus

@pytest.mark.asyncio
async def test_metaspec_version(mongodb_database):
    """Version persiste corretamente"""
    # Create metaspec v1
    # Update to v2
    # Verify version field
```

**Validações**:
- Todos testes passam
- Coverage > 95%

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 6: Infrastructure Layer - MongoCheckpointRepository [Não Iniciada ⏳]

### Descrição
Implementar MongoCheckpointRepository. Atenção para context_snapshot (JSON string) e expires_at (TTL).

### Tarefas

#### 6.1 - Implementar MongoCheckpointRepository [Não Iniciada ⏳]
- Implementa `ICheckpointRepository`
- Métodos CRUD
- Conversões: `_to_document`, `_to_entity`
- context_snapshot (string)
- expires_at (Optional[datetime])

**Arquivos**:
- `src/infrastructure/persistence/mongodb/mongo_checkpoint_repository.py`

**Conversão Especial - expires_at**:
```python
def _to_document(self, checkpoint: Checkpoint) -> dict:
    return {
        'id': checkpoint.id,
        'demand_id': checkpoint.demand_id,
        'context_snapshot': checkpoint.context_snapshot,
        'tokens_used': checkpoint.tokens_used,
        'created_at': checkpoint.created_at,
        'expires_at': checkpoint.expires_at  # Opcional (TTL)
    }

def _to_entity(self, document: dict) -> Checkpoint:
    return Checkpoint(
        id=document['id'],
        demand_id=document['demand_id'],
        context_snapshot=document['context_snapshot'],
        tokens_used=document['tokens_used'],
        created_at=document['created_at'],
        expires_at=document.get('expires_at')  # Opcional
    )
```

**Validações**:
- context_snapshot (JSON string) persiste corretamente
- expires_at opcional funciona

#### 6.2 - Testes de Integração MongoCheckpointRepository [Não Iniciada ⏳]
- Test: CRUD básico
- Test: context_snapshot (JSON string)
- Test: expires_at opcional
- Test: is_expired() method funciona

**Arquivos**:
- `tests/infrastructure/persistence/mongodb/test_mongo_checkpoint_repository.py`

**Testes Críticos**:
```python
@pytest.mark.asyncio
async def test_checkpoint_json_snapshot(mongodb_database):
    """context_snapshot (JSON) persiste corretamente"""
    repo = MongoCheckpointRepository(mongodb_database)
    snapshot = '{"messages": [], "state": "active"}'
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        demand_id="demand_123",
        context_snapshot=snapshot,
        tokens_used=1000,
        created_at=datetime.utcnow()
    )

    await repo.create(checkpoint)
    found = await repo.get_by_id(checkpoint.id)

    assert found.context_snapshot == snapshot
    assert '"messages"' in found.context_snapshot

@pytest.mark.asyncio
async def test_checkpoint_expires_at(mongodb_database):
    """expires_at opcional funciona"""
    # Test com expires_at = None
    # Test com expires_at = future date
```

**Validações**:
- Todos testes passam
- Coverage > 95%

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 7: Infrastructure Layer - Exports e Índices [Não Iniciada ⏳]

### Descrição
Finalizar Infrastructure Layer com exports e configurar índices MongoDB para performance.

### Tarefas

#### 7.1 - Atualizar __init__.py com exports [Não Iniciada ⏳]
- Exportar todos os 4 repositories
- `__all__` definido

**Arquivos**:
- `src/infrastructure/persistence/mongodb/__init__.py`

**Exports**:
```python
from .mongo_project_repository import MongoProjectRepository
from .mongo_demand_repository import MongoDemandRepository
from .mongo_metaspec_repository import MongoMetaspecRepository
from .mongo_checkpoint_repository import MongoCheckpointRepository

__all__ = [
    "MongoProjectRepository",
    "MongoDemandRepository",
    "MongoMetaspecRepository",
    "MongoCheckpointRepository",
]
```

**Validações**:
- Imports funcionam: `from infrastructure.persistence.mongodb import MongoProjectRepository`

#### 7.2 - Configurar índices MongoDB [Não Iniciada ⏳]
- Atualizar `docker/mongo-init.js`
- Índices para performance
- Índice único em `id` (UUID)
- Índices compostos para queries comuns

**Arquivos**:
- `docker/mongo-init.js`

**Índices**:
```javascript
// projects collection
db.projects.createIndex({ id: 1 }, { unique: true });
db.projects.createIndex({ owner_id: 1, created_at: -1 });

// demands collection
db.demands.createIndex({ id: 1 }, { unique: true });
db.demands.createIndex({ project_id: 1, status: 1 });
db.demands.createIndex({ project_id: 1, created_at: -1 });

// metaspecs collection
db.metaspecs.createIndex({ id: 1 }, { unique: true });
db.metaspecs.createIndex({ demand_id: 1, version: -1 });

// checkpoints collection
db.checkpoints.createIndex({ id: 1 }, { unique: true });
db.checkpoints.createIndex({ demand_id: 1, created_at: -1 });
db.checkpoints.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 });  // TTL
```

**Validações**:
- Índices criados corretamente
- Queries usam índices (explain plan)

#### 7.3 - Recriar MongoDB com índices [Não Iniciada ⏳]
- Parar e resetar MongoDB
- Índices são criados automaticamente

**Comandos**:
```bash
pnpm db:reset  # Reinicia MongoDB com mongo-init.js atualizado
pnpm db:mongo

# Dentro do mongosh:
use context_first_dev
db.projects.getIndexes()
db.demands.getIndexes()
```

**Validações**:
- Todos os índices existem
- Índices únicos em `id` campos

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## FASE 8: Testes Finais e Validação [Não Iniciada ⏳]

### Descrição
Rodar suite completa de testes, validar coverage e fazer cleanup.

### Tarefas

#### 8.1 - Rodar suite completa de testes [Não Iniciada ⏳]
- Todos os testes (domain + infrastructure)
- Coverage global

**Comandos**:
```bash
cd packages/backend
source venv/bin/activate

# Subir MongoDB
pnpm db:up

# Rodar TODOS os testes
pytest -v --cov=src --cov-report=term --cov-report=html

# Verificar coverage HTML
open htmlcov/index.html
```

**Validações**:
- Todos testes passam (domain + infrastructure)
- Coverage > 95% para infrastructure/persistence
- Coverage mantido > 99% para domain (IAD-6)

#### 8.2 - Validar Clean Architecture [Não Iniciada ⏳]
- Domain não importa de infrastructure
- Application não importa de infrastructure (apenas interfaces)
- Infrastructure importa de application (interfaces) e domain

**Verificações**:
```bash
# Domain não deve importar infrastructure
grep -r "from infrastructure" packages/backend/src/domain/
# Deve retornar vazio

# Domain não deve importar application
grep -r "from application" packages/backend/src/domain/
# Deve retornar vazio

# Application/interfaces não deve importar infrastructure
grep -r "from infrastructure" packages/backend/src/application/interfaces/
# Deve retornar vazio
```

**Validações**:
- Zero imports violando Dependency Rule
- Clean Architecture mantida

#### 8.3 - Lint e Format [Não Iniciada ⏳]
- Black formatting
- Ruff linting

**Comandos**:
```bash
cd packages/backend
source venv/bin/activate

# Format
black src/ tests/

# Lint
ruff check src/ tests/
```

**Validações**:
- Zero erros de lint
- Código formatado

### Comentários
(Adicionar aprendizados e decisões aqui após completar fase)

---

## ✅ Checklist Final

Antes de considerar IAD-7 completo:

### Código
- [ ] 4 interfaces criadas (Application Layer)
- [ ] 4 implementações MongoDB (Infrastructure Layer)
- [ ] Type hints completos (no `Any`)
- [ ] Async/await em todos métodos
- [ ] Conversões entity ↔ document funcionando
- [ ] Clean Architecture respeitada (Dependency Rule)

### Testes
- [ ] Todos testes passando (99 domain + ~40 infrastructure)
- [ ] Coverage > 95% para infrastructure/persistence
- [ ] Coverage > 99% para domain (mantido)
- [ ] Fixtures MongoDB funcionando
- [ ] MongoDB limpo entre testes

### Performance
- [ ] Índices MongoDB configurados
- [ ] Índice único em `id` (UUID)
- [ ] TTL index em checkpoints.expires_at
- [ ] Queries < 50ms

### Dependencies
- [ ] Motor 3.3.2 instalado
- [ ] PyMongo 4.6.1 instalado
- [ ] requirements.txt atualizado

### Documentation
- [ ] Docstrings em interfaces
- [ ] Docstrings em implementações
- [ ] Comentários em conversões complexas
- [ ] Architecture review aprovado

### Git
- [ ] Feature branch criada (`feat/iad-7-repository-pattern-mongodb`)
- [ ] Commits incrementais por fase
- [ ] Mensagens de commit descritivas

---

## 📊 Ordem de Execução

### Sequencial (deve seguir ordem)
1. FASE 1 → FASE 2 → FASE 3 → FASE 4 → FASE 5 → FASE 6 → FASE 7 → FASE 8
   (Interfaces → Dependencies → Repositories → Finalization)

### Paralelo (pode fazer junto)
- FASE 1: Tarefas 1.2-1.5 (interfaces) podem ser paralelas
- FASE 4-6: Após FASE 3 servir de template, repositories podem ser paralelos

### Critical Path
- FASE 1 → FASE 2 → FASE 3 (MongoProjectRepository como template)

---

## 🔄 Status Legend

- ⏳ **Não Iniciada**: Ainda não começou
- ⏰ **Em Progresso**: Trabalhando atualmente
- ✅ **Completada**: Finalizada e testada
- ⚠️ **Bloqueada**: Aguardando dependência

---

## 📈 Estimativas de Tempo

| Fase | Estimativa | Complexidade |
|------|------------|--------------|
| FASE 1 | 1h | Baixa (interfaces simples) |
| FASE 2 | 30min | Baixa (dependencies) |
| FASE 3 | 2h | Média (primeiro repository) |
| FASE 4 | 1h | Baixa (seguir template) |
| FASE 5 | 1h | Baixa (seguir template) |
| FASE 6 | 1h | Baixa (seguir template) |
| FASE 7 | 30min | Baixa (exports e índices) |
| FASE 8 | 1h | Baixa (validação final) |
| **TOTAL** | **~8h** | MVP |

---

**Criado**: 2025-11-20
**Última Atualização**: 2025-11-20
**Feature Slug**: iad-7-repository-pattern-mongodb
**Issue**: https://linear.app/crypeteras/issue/IAD-7
