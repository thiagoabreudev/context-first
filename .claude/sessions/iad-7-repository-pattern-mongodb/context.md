# Context: IAD-7 - Repository Pattern + MongoDB

## Por Que

**Valor de Negócio**:
- Criar foundation para Use Cases (IAD-8) - bloqueia próxima etapa
- Isolar lógica de persistência do Domain Layer (manter pureza)
- Seguir Clean Architecture e Dependency Rule
- Habilitar desenvolvimento de features com persistência

**Persona Atendida**: Desenvolvedores (backend team)

**Métrica Impactada**: Development velocity

**Fase**: MVP (foundational - critical path)

## O Que

**Funcionalidades Principais**:

1. **Interfaces de Repositório** (Application Layer):
   - `IProjectRepository` - CRUD para Project entity
   - `IDemandRepository` - CRUD para Demand entity
   - `IMetaspecRepository` - CRUD para Metaspec entity
   - `ICheckpointRepository` - CRUD para Checkpoint entity

2. **Implementações MongoDB** (Infrastructure Layer):
   - `MongoProjectRepository` - Implementa IProjectRepository
   - `MongoDemandRepository` - Implementa IDemandRepository
   - `MongoMetaspecRepository` - Implementa IMetaspecRepository
   - `MongoCheckpointRepository` - Implementa ICheckpointRepository

3. **Conversões**:
   - `_to_document()` - Entity → MongoDB document
   - `_to_entity()` - MongoDB document → Entity

**Comportamento Esperado**:
- Persistir e recuperar entities do MongoDB
- Manter Domain Layer puro (sem dependências de MongoDB)
- Conversões transparentes entre domain e infrastructure

## Como

**Abordagem Técnica**: Clean Architecture + Repository Pattern

**Camadas**:
```
Domain Layer (✅ IAD-6)
    ↑ usa
Application Layer (IAD-7 - interfaces)
    ↑ implementa
Infrastructure Layer (IAD-7 - MongoDB)
```

**Componentes**:

1. **Application Layer**:
   - `application/interfaces/i_project_repository.py`
   - `application/interfaces/i_demand_repository.py`
   - `application/interfaces/i_metaspec_repository.py`
   - `application/interfaces/i_checkpoint_repository.py`

2. **Infrastructure Layer**:
   - `infrastructure/persistence/mongodb/mongo_project_repository.py`
   - `infrastructure/persistence/mongodb/mongo_demand_repository.py`
   - `infrastructure/persistence/mongodb/mongo_metaspec_repository.py`
   - `infrastructure/persistence/mongodb/mongo_checkpoint_repository.py`

**Padrões**:
- Repository Pattern (isolar persistência)
- Dependency Inversion (depender de abstrações)
- UUID strings como IDs (domain-first)
- Subdocumentos para Value Objects

## Validação contra Meta Specs

Este projeto é "Context-First Platform", não tem metaspecs de "iadojeitocerto.com.br".

Validação contra ADRs do projeto:
- [x] **ADR-002**: Clean Architecture + Repository Pattern
- [x] **ADR-003**: MongoDB como database principal
- [x] **Dependency Rule**: Application → Domain, Infrastructure → Application
- [x] **Domain puro**: Zero imports de infrastructure no domain
- [x] **Stack aprovada**: Motor (MongoDB async), pytest

## Dependências

**Novas bibliotecas**:
- `motor==3.3.2` - MongoDB async driver
- `pymongo==4.6.1` - Dependency do Motor

**Bibliotecas existentes**:
- `pytest` (já instalado)
- `pytest-asyncio` (já instalado)
- `pytest-cov` (já instalado)

**Componentes existentes**:
- Domain Layer (IAD-6) - 4 entities, 2 value objects
- Docker Compose (MongoDB já configurado)

## Restrições

**Técnicas**:
- CRUD básico apenas (queries específicas vêm depois)
- Testes de integração com MongoDB real (via Docker Compose)
- Coverage > 95%
- Zero dependências de MongoDB no Domain Layer

**Performance**:
- Queries < 50ms (índices configurados)
- Conversões entity ↔ document eficientes

**Escopo Negativo** (NÃO fazer):
- ❌ Use Cases (IAD-8)
- ❌ DTOs (IAD-8)
- ❌ Queries complexas (find_by_status, etc)
- ❌ Dependency Injection setup (IAD-8)
- ❌ Redis repositories
- ❌ S3 repositories

## Testes

**Testes de Integração** (MongoDB real):
- `test_mongo_project_repository.py` - CRUD completo
- `test_mongo_demand_repository.py` - CRUD completo
- `test_mongo_metaspec_repository.py` - CRUD completo
- `test_mongo_checkpoint_repository.py` - CRUD completo

**Cenários Críticos**:
- Create → Get (verificar persistência)
- Update → Get (verificar atualização)
- Delete → Get (verificar remoção)
- Conversões entity ↔ document (Value Objects, enums, datetimes)

**Cobertura Esperada**: > 95% para repositories

**Setup**:
- Docker Compose para MongoDB (já existe)
- Fixtures pytest (`mongodb_client`, `mongodb_database`)
- Limpeza automática entre testes
