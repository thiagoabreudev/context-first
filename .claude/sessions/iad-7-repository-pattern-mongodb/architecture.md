# Architecture: IAD-7 - Repository Pattern + MongoDB

## 📐 Visão Geral de Alto Nível

### Sistema Antes (IAD-6)

```
┌─────────────────────────────────────┐
│       Domain Layer (✅ IAD-6)       │
│  ┌────────┐  ┌─────────────────┐   │
│  │Project │  │ContextBudget    │   │
│  │Demand  │  │DemandStatus     │   │
│  │Metaspec│  │(Value Objects)  │   │
│  │Checkpoint                     │   │
│  └────────┘  └─────────────────┘   │
└─────────────────────────────────────┘

❌ Sem persistência
❌ Sem Application Layer
❌ Sem Infrastructure Layer
```

### Sistema Depois (IAD-7)

```mermaid
graph TB
    subgraph "Domain Layer (IAD-6 ✅)"
        Project[Project Entity]
        Demand[Demand Entity]
        Metaspec[Metaspec Entity]
        Checkpoint[Checkpoint Entity]
        ContextBudget[ContextBudget VO]
        DemandStatus[DemandStatus VO]
    end

    subgraph "Application Layer (IAD-7 - Interfaces)"
        IProjectRepo[IProjectRepository]
        IDemandRepo[IDemandRepository]
        IMetaspecRepo[IMetaspecRepository]
        ICheckpointRepo[ICheckpointRepository]
    end

    subgraph "Infrastructure Layer (IAD-7 - MongoDB)"
        MongoProjectRepo[MongoProjectRepository]
        MongoDemandRepo[MongoDemandRepository]
        MongoMetaspecRepo[MongoMetaspecRepository]
        MongoCheckpointRepo[MongoCheckpointRepository]
    end

    subgraph "External"
        MongoDB[(MongoDB)]
    end

    %% Dependency Rule (arrows point UP)
    MongoProjectRepo -->|implements| IProjectRepo
    MongoDemandRepo -->|implements| IDemandRepo
    MongoMetaspecRepo -->|implements| IMetaspecRepo
    MongoCheckpointRepo -->|implements| ICheckpointRepo

    IProjectRepo -->|uses| Project
    IDemandRepo -->|uses| Demand
    IMetaspecRepo -->|uses| Metaspec
    ICheckpointRepo -->|uses| Checkpoint

    MongoProjectRepo -->|persists to| MongoDB
    MongoDemandRepo -->|persists to| MongoDB
    MongoMetaspecRepo -->|persists to| MongoDB
    MongoCheckpointRepo -->|persists to| MongoDB

    style Domain Layer fill:#e1f5e1
    style Application Layer fill:#e3f2fd
    style Infrastructure Layer fill:#fff3e0
```

## 🏛️ Clean Architecture - Dependency Rule

```
┌─────────────────────────────────────────────────────┐
│  Frameworks & Drivers (External)                    │
│  - MongoDB                                          │
│  - Motor (async driver)                             │
└────────────────┬────────────────────────────────────┘
                 │ depends on (implements)
┌────────────────▼────────────────────────────────────┐
│  Infrastructure Layer                                │
│  - MongoProjectRepository                            │
│  - MongoDemandRepository                             │
│  - MongoMetaspecRepository                           │
│  - MongoCheckpointRepository                         │
│  - Conversões (entity ↔ document)                    │
└────────────────┬────────────────────────────────────┘
                 │ implements
┌────────────────▼────────────────────────────────────┐
│  Application Layer (Interfaces)                      │
│  - IProjectRepository                                │
│  - IDemandRepository                                 │
│  - IMetaspecRepository                               │
│  - ICheckpointRepository                             │
└────────────────┬────────────────────────────────────┘
                 │ uses
┌────────────────▼────────────────────────────────────┐
│  Domain Layer (✅ IAD-6)                             │
│  - Project, Demand, Metaspec, Checkpoint            │
│  - ContextBudget, DemandStatus                       │
│  - Business Rules                                    │
│  - ❌ ZERO dependencies externas                     │
└─────────────────────────────────────────────────────┘
```

**Regra de Ouro**: Dependências apontam PARA CIMA (← Inner Layers).

Domain NUNCA depende de Application ou Infrastructure.

## 📁 Estrutura de Diretórios Proposta

```
packages/backend/src/
│
├── domain/                           # ✅ IAD-6 (existe)
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── demand.py
│   │   ├── metaspec.py
│   │   └── checkpoint.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── context_budget.py
│   │   └── demand_status.py
│   └── exceptions.py
│
├── application/                      # IAD-7 (criar interfaces)
│   ├── interfaces/                   # ⬅️ CRIAR
│   │   ├── __init__.py              # ⬅️ CRIAR
│   │   ├── i_project_repository.py  # ⬅️ CRIAR
│   │   ├── i_demand_repository.py   # ⬅️ CRIAR
│   │   ├── i_metaspec_repository.py # ⬅️ CRIAR
│   │   └── i_checkpoint_repository.py # ⬅️ CRIAR
│   ├── use_cases/                    # IAD-8 (vazio por enquanto)
│   └── dtos/                         # IAD-8 (vazio por enquanto)
│
└── infrastructure/                   # IAD-7 (criar implementações)
    └── persistence/
        └── mongodb/                  # ⬅️ CRIAR
            ├── __init__.py          # ⬅️ CRIAR
            ├── mongo_project_repository.py    # ⬅️ CRIAR
            ├── mongo_demand_repository.py     # ⬅️ CRIAR
            ├── mongo_metaspec_repository.py   # ⬅️ CRIAR
            └── mongo_checkpoint_repository.py # ⬅️ CRIAR
```

### Arquivos de Teste

```
packages/backend/tests/
├── domain/                           # ✅ IAD-6 (existe)
│   ├── entities/
│   └── value_objects/
│
├── infrastructure/                   # IAD-7 (criar testes)
│   └── persistence/
│       └── mongodb/                  # ⬅️ CRIAR
│           ├── __init__.py
│           ├── test_mongo_project_repository.py    # ⬅️ CRIAR
│           ├── test_mongo_demand_repository.py     # ⬅️ CRIAR
│           ├── test_mongo_metaspec_repository.py   # ⬅️ CRIAR
│           └── test_mongo_checkpoint_repository.py # ⬅️ CRIAR
│
└── conftest.py                       # ⬅️ ATUALIZAR (adicionar fixtures MongoDB)
```

## 🔧 Componentes e Relações

### 1. Application Layer - Interfaces (Ports)

#### IProjectRepository

```python
# application/interfaces/i_project_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.project import Project

class IProjectRepository(ABC):
    """
    Interface de persistência para Project entity.

    Segue Repository Pattern e Dependency Inversion Principle.
    Infrastructure implementa, Application/Domain dependem da abstração.
    """

    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Persiste novo projeto"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """Busca projeto por ID (UUID string)"""
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

**Responsabilidade**: Definir contrato de persistência.

**Padrões Aplicados**:
- Repository Pattern (isolar persistência)
- Dependency Inversion (abstração)
- Interface Segregation (métodos coesos)

#### Interfaces Similares

- `IDemandRepository`
- `IMetaspecRepository`
- `ICheckpointRepository`

Todas seguem mesmo contrato CRUD.

### 2. Infrastructure Layer - Implementações (Adapters)

#### MongoProjectRepository

```python
# infrastructure/persistence/mongodb/mongo_project_repository.py
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from application.interfaces.i_project_repository import IProjectRepository
from domain.entities.project import Project
from domain.value_objects.context_budget import ContextBudget

class MongoProjectRepository(IProjectRepository):
    """
    Implementação MongoDB do IProjectRepository.

    Responsabilidades:
    - Conversão entity ↔ document
    - Operações CRUD no MongoDB
    - Isolamento de detalhes de persistência
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Injetar database, não client.

        Args:
            db: MongoDB database instance (do Motor)
        """
        self._collection = db['projects']

    async def create(self, project: Project) -> Project:
        """
        Persiste novo projeto.

        Flow:
        1. Converte entity → document (_to_document)
        2. Insert no MongoDB
        3. Retorna entity original (com ID já gerado no domain)
        """
        document = self._to_document(project)
        await self._collection.insert_one(document)
        return project

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        """
        Busca projeto por UUID.

        Flow:
        1. Query MongoDB por campo 'id' (UUID string)
        2. Se encontrou, converte document → entity (_to_entity)
        3. Se não encontrou, retorna None
        """
        document = await self._collection.find_one({'id': project_id})
        return self._to_entity(document) if document else None

    async def update(self, project: Project) -> Project:
        """
        Atualiza projeto existente.

        Flow:
        1. Converte entity → document
        2. Replace document no MongoDB (por 'id')
        3. Retorna entity atualizada
        """
        document = self._to_document(project)
        await self._collection.replace_one(
            {'id': project.id},
            document
        )
        return project

    async def delete(self, project_id: str) -> None:
        """Remove projeto por UUID"""
        await self._collection.delete_one({'id': project_id})

    # Private methods - Conversões

    def _to_document(self, project: Project) -> dict:
        """
        Converte Project entity → MongoDB document.

        Decisões:
        - UUID string mantido no campo 'id'
        - MongoDB gera _id (ObjectId) automaticamente
        - ContextBudget como subdocumento (espelha domain)
        - Datetime mantido (MongoDB suporta nativamente)
        """
        return {
            'id': project.id,  # UUID string
            'name': project.name,
            'description': project.description,
            'owner_id': project.owner_id,
            'context_budget': {  # Subdocumento (Value Object)
                'max_tokens': project.context_budget.max_tokens,
                'used_tokens': project.context_budget.used_tokens
            },
            'created_at': project.created_at,
            'updated_at': project.updated_at
        }

    def _to_entity(self, document: dict) -> Project:
        """
        Converte MongoDB document → Project entity.

        Reconstrói Value Objects a partir de subdocumentos.
        """
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
            updated_at=document.get('updated_at')  # Opcional
        )
```

**Responsabilidades**:
- Implementar contrato de IProjectRepository
- Converter entre domain e infrastructure
- Executar operações MongoDB via Motor

**Padrões Aplicados**:
- Adapter Pattern (adapta MongoDB para interface domain)
- Repository Pattern (implementação concreta)
- Single Responsibility (apenas persistência)

#### Implementações Similares

- `MongoDemandRepository` - Converte DemandStatus enum para string
- `MongoMetaspecRepository` - Converte MetaspecType enum para string
- `MongoCheckpointRepository` - Lida com expires_at (TTL)

### 3. Conversões Especiais

#### Value Objects → Subdocumentos

```python
# ContextBudget
entity.context_budget = ContextBudget(max_tokens=100000, used_tokens=5000)

# ↓ to_document

document['context_budget'] = {
    'max_tokens': 100000,
    'used_tokens': 5000
}
```

#### Enums → Strings

```python
# DemandStatus
entity.status = DemandStatus.SPEC_APPROVED

# ↓ to_document

document['status'] = 'spec_approved'  # String

# ↓ to_entity

entity.status = DemandStatus(document['status'])  # Enum reconstruction
```

#### UUIDs

```python
# Domain
project.id = "550e8400-e29b-41d4-a716-446655440000"  # UUID string

# MongoDB document
{
    "_id": ObjectId("67..."),  # MongoDB interno (ignorar)
    "id": "550e8400-...",      # UUID (usado para queries)
    ...
}
```

## 🎨 Padrões e Princípios

### Repository Pattern

**Definição**: Encapsula lógica de acesso a dados, fornecendo interface similar a coleção.

**Benefícios**:
- Isola domain de detalhes de persistência
- Facilita testes (mock repositories)
- Centraliza lógica de conversão
- Permite trocar implementação (MongoDB → PostgreSQL)

### Dependency Inversion Principle (DIP)

```
❌ ERRADO:
Domain → MongoRepository (concrete)

✅ CERTO:
Domain → IRepository (interface)
         ↑
MongoRepository (implementa)
```

### Single Responsibility Principle (SRP)

Cada repository tem UMA responsabilidade:
- `MongoProjectRepository` → Persistência de Projects
- `MongoDemandRepository` → Persistência de Demands
- etc.

### Interface Segregation Principle (ISP)

Interfaces segregadas (não gordas):
- `IProjectRepository` → Apenas CRUD de Projects
- Não há `ISuperRepository` com métodos de todas entities

## 🔍 Decisões Arquiteturais (ADRs)

### ADR-007: UUID Strings como IDs (Domain-First)

**Status**: Aceito

**Context**: Domain entities precisam de IDs. Opções: ObjectId (MongoDB) vs UUID (application-generated).

**Decision**: Usar UUID strings gerados no domain/application.

**Rationale**:
- Domain permanece independente de MongoDB
- Portável (fácil migrar para PostgreSQL)
- Segue Clean Architecture (domain-first)

**Consequences**:
- Positive: Clean Architecture respeitada, portabilidade
- Negative: Documento MongoDB tem 2 IDs (_id e id), pequeno overhead

### ADR-008: Value Objects como Subdocumentos

**Status**: Aceito

**Context**: Como persistir Value Objects (ContextBudget, etc)?

**Decision**: Subdocumentos no MongoDB.

**Rationale**:
- Espelha estrutura do domain
- Mais limpo que flatten (prefixos)
- MongoDB suporta nativamente

**Consequences**:
- Positive: Código limpo, fácil manutenção
- Negative: Queries aninhadas (`context_budget.max_tokens`)

### ADR-009: Motor (Async) ao invés de PyMongo (Sync)

**Status**: Aceito

**Context**: FastAPI é async. PyMongo é sync.

**Decision**: Usar Motor (async driver oficial).

**Rationale**:
- Compatível com FastAPI async
- Performance (não bloqueia event loop)
- Oficial (mantido por MongoDB)

**Consequences**:
- Positive: Performance, compatibilidade
- Negative: Sintaxe levemente diferente de PyMongo

### ADR-010: CRUD Básico Apenas (MVP)

**Status**: Aceito

**Context**: Implementar queries complexas agora ou depois?

**Decision**: CRUD básico apenas (IAD-7). Queries específicas em IAD-8+.

**Rationale**:
- YAGNI (You Aren't Gonna Need It)
- Use Cases ainda não existem
- Queries específicas quando necessário

**Consequences**:
- Positive: MVP rápido, menos código
- Negative: Precisará adicionar métodos depois

## 🧪 Estratégia de Testes

### Testes de Integração (MongoDB Real)

**Por Que Integração?**:
- Repositories interagem com MongoDB real
- Testes unitários com mocks não validam conversões
- Docker Compose já configurado (zero esforço)

**Setup** (`conftest.py`):

```python
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="session")
async def mongodb_client():
    """Cliente MongoDB compartilhado para sessão de testes"""
    client = AsyncIOMotorClient(
        "mongodb://context_first_app:app_password_change_in_production@localhost:27017/context_first_dev?authSource=context_first_dev"
    )
    yield client
    client.close()

@pytest.fixture(scope="function")
async def mongodb_database(mongodb_client):
    """
    Database limpo para cada teste.

    Garante isolamento entre testes.
    """
    db = mongodb_client['context_first_test']

    # Limpar antes
    await db['projects'].delete_many({})
    await db['demands'].delete_many({})
    await db['metaspecs'].delete_many({})
    await db['checkpoints'].delete_many({})

    yield db

    # Opcional: limpar depois também
```

**Exemplo de Teste**:

```python
# tests/infrastructure/persistence/mongodb/test_mongo_project_repository.py
import pytest
import uuid
from datetime import datetime
from infrastructure.persistence.mongodb.mongo_project_repository import MongoProjectRepository
from domain.entities.project import Project
from domain.value_objects.context_budget import ContextBudget

@pytest.mark.asyncio
async def test_create_and_get_project(mongodb_database):
    """Test: Create → Get (verificar persistência)"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(
        id=str(uuid.uuid4()),
        name="Test Project",
        description="Integration test",
        owner_id="user_123",
        context_budget=ContextBudget(max_tokens=100000, used_tokens=0),
        created_at=datetime.utcnow()
    )

    # Act
    await repo.create(project)
    found = await repo.get_by_id(project.id)

    # Assert
    assert found is not None
    assert found.id == project.id
    assert found.name == "Test Project"
    assert found.context_budget.max_tokens == 100000

@pytest.mark.asyncio
async def test_update_project(mongodb_database):
    """Test: Create → Update → Get (verificar atualização)"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(...)
    await repo.create(project)

    # Act
    project.name = "Updated Name"
    await repo.update(project)
    found = await repo.get_by_id(project.id)

    # Assert
    assert found.name == "Updated Name"

@pytest.mark.asyncio
async def test_delete_project(mongodb_database):
    """Test: Create → Delete → Get (verificar remoção)"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    project = Project(...)
    await repo.create(project)

    # Act
    await repo.delete(project.id)
    found = await repo.get_by_id(project.id)

    # Assert
    assert found is None

@pytest.mark.asyncio
async def test_context_budget_conversion(mongodb_database):
    """Test: Conversão ContextBudget (Value Object → subdocumento)"""
    # Arrange
    repo = MongoProjectRepository(mongodb_database)
    budget = ContextBudget(max_tokens=50000, used_tokens=10000)
    project = Project(..., context_budget=budget)

    # Act
    await repo.create(project)
    found = await repo.get_by_id(project.id)

    # Assert
    assert isinstance(found.context_budget, ContextBudget)
    assert found.context_budget.max_tokens == 50000
    assert found.context_budget.remaining_tokens == 40000
```

### Coverage Target

- **Repositories**: > 95%
- **Conversões**: 100% (crítico)

### Rodar Testes

```bash
# 1. Subir MongoDB
pnpm db:up

# 2. Rodar testes
cd packages/backend
source venv/bin/activate
pytest tests/infrastructure/persistence/ -v --cov=src/infrastructure --cov-fail-under=95

# 3. Ver coverage HTML
pytest tests/infrastructure/persistence/ --cov=src/infrastructure --cov-report=html
open htmlcov/index.html
```

## 🚀 Dependências Externas

### Novas Dependências

Adicionar em `requirements.txt`:

```
# Database - MongoDB (IAD-7)
motor==3.3.2  # MongoDB async driver (official)
pymongo==4.6.1  # Required by Motor
```

### Dependências Existentes

- `pytest==8.3.3` ✅
- `pytest-asyncio==0.24.0` ✅
- `pytest-cov==6.0.0` ✅
- `fastapi==0.115.0` ✅

### Configuração MongoDB

Atualizar `docker/mongo-init.js` com índices:

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
db.checkpoints.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 });
```

## ⚠️ Restrições e Suposições

### Restrições

1. **CRUD básico apenas**: Queries complexas vêm depois (IAD-8+)
2. **MongoDB async**: Usar Motor, não PyMongo sync
3. **UUID strings**: IDs gerados no domain, não ObjectId
4. **Clean Architecture**: Zero imports de infrastructure no domain
5. **Testes de integração**: MongoDB real via Docker Compose

### Suposições

1. Docker Compose está funcionando
2. MongoDB 7.0 já configurado
3. Domain Layer (IAD-6) está completo e testado
4. Use Cases (IAD-8) usarão estas interfaces

## 🔄 Trade-offs e Alternativas

### Trade-off 1: MongoDB vs PostgreSQL

**Escolhido**: MongoDB

**Alternativa**: PostgreSQL

**Razão**:
- ADR-003 já decidiu MongoDB
- Document model espelha domain entities
- Subdocumentos para Value Objects

**Consequência**:
- Positive: Flexível, espelha domain
- Negative: Queries relacionais complexas

### Trade-off 2: Testes Integração vs Unit (Mocks)

**Escolhido**: Integração (MongoDB real)

**Alternativa**: Unit tests com mocks

**Razão**:
- Valida conversões reais
- Docker Compose já existe (zero custo)
- Confiança maior

**Consequência**:
- Positive: Confiança, valida conversões
- Negative: Testes mais lentos (~500ms vs ~50ms)

### Trade-off 3: CRUD Now vs Queries Now

**Escolhido**: CRUD básico apenas (IAD-7)

**Alternativa**: Implementar queries complexas agora

**Razão**:
- YAGNI (Use Cases não existem)
- MVP mais rápido

**Consequência**:
- Positive: Entrega rápida
- Negative: Precisará adicionar métodos depois

## 🔍 Architecture Review

### ✅ Clean Architecture Compliance

- [x] **Dependency Rule**: Application → Domain, Infrastructure → Application
- [x] **Domain puro**: Zero imports de external libs
- [x] **Abstrações**: Interfaces no Application Layer
- [x] **Inversão de Dependência**: Infrastructure depende de interfaces

### ✅ SOLID Compliance

- [x] **SRP**: Cada repository uma responsabilidade
- [x] **OCP**: Extensível via novas implementações (PostgresRepository)
- [x] **LSP**: MongoRepository substituível por qualquer IRepository
- [x] **ISP**: Interfaces segregadas (não gordas)
- [x] **DIP**: Depende de IRepository, não de MongoRepository

### ✅ Patterns Aplicados

- [x] Repository Pattern
- [x] Dependency Inversion
- [x] Adapter Pattern (MongoDB → Domain)

### ❌ Possíveis Violações (NENHUMA IDENTIFICADA)

Nenhuma violação de Clean Architecture identificada neste design.

## 📝 Lista de Arquivos a Criar/Editar

### Criar (14 arquivos)

**Application Layer - Interfaces**:
1. `src/application/interfaces/__init__.py`
2. `src/application/interfaces/i_project_repository.py`
3. `src/application/interfaces/i_demand_repository.py`
4. `src/application/interfaces/i_metaspec_repository.py`
5. `src/application/interfaces/i_checkpoint_repository.py`

**Infrastructure Layer - Implementações**:
6. `src/infrastructure/persistence/mongodb/__init__.py`
7. `src/infrastructure/persistence/mongodb/mongo_project_repository.py`
8. `src/infrastructure/persistence/mongodb/mongo_demand_repository.py`
9. `src/infrastructure/persistence/mongodb/mongo_metaspec_repository.py`
10. `src/infrastructure/persistence/mongodb/mongo_checkpoint_repository.py`

**Tests**:
11. `tests/infrastructure/persistence/mongodb/__init__.py`
12. `tests/infrastructure/persistence/mongodb/test_mongo_project_repository.py`
13. `tests/infrastructure/persistence/mongodb/test_mongo_demand_repository.py`
14. `tests/infrastructure/persistence/mongodb/test_mongo_metaspec_repository.py`
15. `tests/infrastructure/persistence/mongodb/test_mongo_checkpoint_repository.py`

### Editar (2 arquivos)

1. `requirements.txt` - Adicionar motor, pymongo
2. `tests/conftest.py` - Adicionar fixtures MongoDB
3. `docker/mongo-init.js` - Adicionar índices de performance

## 🎯 Próximos Passos (Após IAD-7)

1. **IAD-8**: Application Layer (Use Cases, DTOs)
   - Use Cases usarão estas interfaces
   - Dependency Injection (FastAPI Depends)

2. **Queries Específicas**: Adicionar quando necessário
   - `find_by_owner(owner_id)` → Para dashboard
   - `find_demands_by_status(project_id, status)` → Para kanban
   - etc.

---

**Arquitetura aprovada? Pronto para implementar!** 🚀
