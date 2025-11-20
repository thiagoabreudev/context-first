# Engineer Start - IA do Jeito Certo

Este comando inicia o desenvolvimento de uma funcionalidade no projeto **iadojeitocerto.com.br**.

## 🎯 Contexto do Projeto

- **Produto**: Site de consultoria vendendo Metodologia Metaspecs
- **Stack**: Vue 3 + Nuxt.js 3 + TypeScript + Tailwind CSS + Nuxt Content
- **Arquitetura**: Atomic Design + SSG/ISR
- **Metodologia**: SPARC+DD com Meta Specs

## ⚙️ Configuração Inicial

1. **Branch de Feature**:
   - Se não estivermos em feature branch, peça permissão para criar: `feat/<feature-slug>`
   - Se já estivermos na branch correta, prossiga

2. **Pasta de Sessão**:
   - Certifique-se de que existe: `.claude/sessions/<feature-slug>/`
   - Crie se necessário

3. **Input do Usuário**:
   - Peça ao usuário a issue do **Linear** (team **iadojeitocerto**) ou arquivo de especificação
   - Para ler issue do Linear use: `mcp__linear-server__get_issue`
   - Leia o PRD completo (se disponível em `/specs/prd/`)
   - Team ID: `2b1273da-f961-407a-b0f5-4047378ecb4d`

## 📋 Análise e Entendimento

Analise a especificação (card Linear ou PRD) e construa entendimento completo respondendo:

### Negócio
- **Por que** isso está sendo construído? (valor de negócio, métrica impactada)
- **Qual persona** se beneficia? (CTO / VP Eng / Tech Lead)
- **Qual fase**? (MVP / Fase 2 / Fase 3)
- **Qual métrica** queremos impactar? (conversão, engajamento, performance)

### Funcional
- **Qual resultado esperado**? (comportamento do usuário, output do sistema)
- **Quais componentes** serão criados/modificados?
- **Qual nível Atomic Design**? (Atoms / Molecules / Organisms / Templates / Pages)
- **Quais integrações**? (APIs externas, Nuxt Content, formulários)

### Técnico
- **Stack aprovada**? Verificar contra `metaspecs/technical/stack-tecnologica.md`
- **Padrões arquiteturais**? Verificar contra `metaspecs/technical/arquitetura.md`
- **Dependências novas**? Justificar e documentar
- **Como testar**? (E2E críticos com Playwright, unit com Vitest)

### Validação contra Meta Specs

**OBRIGATÓRIO** - Validar contra:
- [ ] `metaspecs/businnes/visao-produto.md` - Alinhado com proposta de valor?
- [ ] `metaspecs/businnes/perfil-cliente.md` - Atende persona correta?
- [ ] `metaspecs/businnes/features-valores.md` - Está listada? Prioridade correta?
- [ ] `metaspecs/technical/stack-tecnologica.md` - Usa stack aprovada?
- [ ] `metaspecs/technical/arquitetura.md` - Segue Atomic Design e SSG/ISR?
- [ ] `metaspecs/technical/problemas-conhecidos.md` - Sem conflitos?

## 🤔 Perguntas de Esclarecimento

Após análise inicial, formule **3-5 clarificações mais importantes**:

**Exemplo de perguntas**:
- "O componente Hero será um Organism ou Template? Sugiro Organism pois é seção distinta."
- "Validação de email corporativo: apenas regex ou integração com API de validação?"
- "Animações: usar apenas Vue Transitions ou precisamos de biblioteca adicional?"
- "SEO: precisamos de structured data (Schema.org) ou apenas meta tags básicas?"
- "Performance: qual target de bundle size para este componente?"

Apresente seu entendimento E sugestões ao humano simultaneamente.

## 💾 Salvamento do Contexto

Uma vez que tenha entendimento completo:

1. **Criar** `.claude/sessions/<feature-slug>/context.md` com:

```markdown
# Context: [Nome da Feature]

## Por Que
[Valor de negócio, persona atendida, métrica impactada]

## O Que
[Funcionalidades principais, comportamento esperado]

## Como
[Abordagem técnica, componentes, Atomic Design level]

## Validação contra Meta Specs
- [x] Alinhado com visao-produto.md
- [x] Atende persona de perfil-cliente.md
- [x] Listado em features-valores.md (Fase X)
- [x] Usa stack de stack-tecnologica.md
- [x] Segue padrões de arquitetura.md
- [x] Sem conflitos com problemas-conhecidos.md

## Dependências
[Bibliotecas, APIs, componentes existentes]

## Restrições
[Limitações técnicas, performance targets, budget de bundle size]

## Testes
[E2E críticos, unit tests necessários, cobertura esperada]
```

2. **Pedir revisão** do humano

3. **Iterar** até aprovação explícita

## 📝 Atualização de Requisitos

Se discussão revelar mudanças necessárias nos requisitos:

1. **Pedir permissão** ao humano
2. **Atualizar**:
   - Issue do **Linear** via MCP
     - Team: **iadojeitocerto** (ID: `2b1273da-f961-407a-b0f5-4047378ecb4d`)
     - Use: `mcp__linear-server__update_issue`
   - OU arquivo de especificação (se veio de arquivo)
   - OU PRD em `/specs/prd/<feature-slug>.md`

<feature_slug>
#$ARGUMENTS
</feature_slug>

## Arquitetura

Dado seu entendimento do que será construído, você agora procederá ao desenvolvimento da arquitetura da funcionalidade. O documento de arquitetura deve mapear o que está sendo construído, os componentes, as dependências, os padrões, as tecnologias, as restrições, as suposições, os trade-offs, as alternativas, as consequências.

É aqui que você colocará seu chapéu de pensamento ultra e considerará o melhor caminho para construir a funcionalidade, considerando também os padrões e melhores práticas deste projeto.

Nesta seção, espera-se que você analise o código fonte relevante, entenda sua estrutura e propósito, e então construa uma arquitetura que se alinha com os padrões e melhores práticas do projeto.

### Princípios de Clean Architecture (OBRIGATÓRIO)

**ANTES de criar a arquitetura, você DEVE:**

1. **Ler os princípios arquiteturais**:
   - [metaspecs/technical/architecture/clean-architecture-principles.md](../../../metaspecs/technical/architecture/clean-architecture-principles.md)
   - Entender os 12 princípios (Clean Code, DDD, SOLID, Patterns)

2. **⚠️ VALIDAR Architecture Decision Records (ADRs)**:

   **Se a feature envolve bots, configuração ou credenciais, você DEVE:**

   a) **Listar ADRs existentes**:
   ```bash
   ls -la metaspecs/technical/architecture/adrs/
   ```

   b) **Ler ADRs relevantes**:
   - **ADR-0001**: DCA Bots Independentes de trading_configs
     - 🚫 NUNCA: Bots usando `config_repository.get_by_id()`
     - ✅ SEMPRE: Bots independentes de `trading_configs` collection

   - **ADR-0002**: Credenciais em users Collection
     - 🚫 NUNCA: `os.getenv('MB_API_ID')` em bot services
     - ✅ SEMPRE: `user_entity.mb_api_id_encrypted`

   - **ADR-0003**: Injetar db ao invés de Repositories
     - 🚫 NUNCA: `.config_repository.db` (code smell)
     - ✅ SEMPRE: Injetar `db` diretamente

   c) **Validar compliance automaticamente**:
   ```bash
   ./scripts/validate_adrs.sh
   ```

   d) **Incluir ADR compliance no architecture.md**:
   ```markdown
   ## ADR Compliance

   ### ✅ ADRs Validados
   - ADR-0001: Bots independentes de trading_configs - COMPLIANT
   - ADR-0002: Credenciais em users collection - COMPLIANT
   - ADR-0003: db injection pattern - COMPLIANT

   ### 🔴 Violações Identificadas
   (Se houver, listar e propor correções)
   ```

3. **Aplicar a Dependency Rule**:
   ```
   Frameworks (AGNO, MongoDB, FastAPI)
       ↓ depende de
   Infrastructure (tools/, infrastructure/)
       ↓ depende de
   Application (workflows/)
       ↓ depende de
   Domain (domain/)
       ↑ NÃO DEPENDE DE NADA
   ```

4. **Estruturar a solução em camadas**:
   - **Domain Layer** (src/domain/):
     - calculations.py - Funções puras de cálculo (SEM @tool, SEM Motor, SEM AGNO)
     - validations.py - Funções puras de validação
     - services/ - Domain Services (lógica de negócio complexa)
     - repositories.py - Interfaces (ports) para persistência
     - models.py - Entidades e Value Objects

   - **Application Layer** (src/workflows/):
     - base.py - BaseWorkflow (Template Method Pattern)
     - <workflow_name>.py - Casos de uso específicos
     - Orquestram domain services, não contêm lógica de negócio

   - **Infrastructure Layer** (src/infrastructure/, src/tools/):
     - repositories/ - Implementações de repositórios (MongoDB, etc)
     - exchanges/ - Implementações de ExchangeInterface
     - tools/ - Adapters para AGNO (thin wrappers)

5. **Validar princípios SOLID**:
   - [ ] **SRP**: Cada classe tem UMA responsabilidade
   - [ ] **OCP**: Extensível via interfaces, não modificação
   - [ ] **LSP**: Implementações substituíveis por interfaces
   - [ ] **ISP**: Interfaces segregadas (não gordas)
   - [ ] **DIP**: Depende de abstrações (repositories, services)

6. **Aplicar padrões quando apropriado**:
   - Repository Pattern - Para persistência
   - Template Method - Para workflows com comportamento comum
   - Strategy Pattern - Para algoritmos intercambiáveis
   - Factory Pattern - Para criação complexa de objetos
   - Adapter Pattern - Para integração com externos (Exchange, AGNO)
   - Domain Services - Para lógica que não pertence a entidades

7. **Criar seção "Architecture Review" no architecture.md**:
   - Identificar possíveis violações de Clean Architecture
   - Propor correções
   - Justificar decisões arquiteturais com ADRs (Architecture Decision Records)

Dicas:
   - Use Glob e Grep para encontrar arquivos específicos baseados nas respostas de descoberta
   - Use Read para ler código relevante em batch
   - Mergulhe fundo em funcionalidades e padrões similares
   - Analise detalhes específicos de implementação
   - Use WebSearch e ou context7 para melhores práticas ou documentação de bibliotecas (se necessário)
   - **Sempre valide se a solução respeita a Dependency Rule**
   - **Domain NUNCA deve importar de tools/, infrastructure/, workflows/**

Seu documento de arquitetura deve incluir:
    - Uma visão geral de alto nível do sistema (antes e depois da mudança)
    - **Diagrama de dependências entre camadas (Clean Architecture)**
    - Componentes afetados e suas relações, dependências
    - **Estrutura de diretórios proposta (domain/, workflows/, infrastructure/)**
    - Padrões e melhores práticas que serão mantidos ou introduzidos
    - **Identificação de violações arquiteturais e correções propostas**
    - Dependências externas que serão usadas ou que precisam ser adicionadas ao projeto
    - Restrições e suposições
    - Trade-offs e alternativas
    - **ADRs (Architecture Decision Records) para decisões importantes**
    - Consequências negativas (se houver) da implementação deste design
    - Lista dos principais arquivos a serem editados/criados

Se ajudar a construir um diagrama MERMAID, sinta-se livre para fazê-lo.

Se, a qualquer momento, você tiver dúvidas ou encontrar algo que contradiga o que entendeu anteriormente, peça esclarecimentos ao humano.

Uma vez que tenha um bom entendimento do que está sendo construído, salve-o no arquivo .claude/sessions/<feature_slug>/architecture.md e peça ao humano para revisar.

Se o humano concordar com seu entendimento, você pode prosseguir para o próximo passo. Caso contrário, continue iterando juntos até obter aprovação explícita para seguir em frente.

Uma vez que o architecture.md esteja finalizado, informe ao humano que você está pronto para prosseguir para o próximo passo.

## Pesquisa

Se você não tem certeza de como uma biblioteca específica funciona, você pode usar WebSearch ou WebFetch para buscar informações sobre ela. Também consulte:
- **Meta-specs** do projeto (metaspecs/business/ e metaspecs/technical/)
- **Documentação AGNO**: https://docs.agno.dev (framework de agentes AI)
- **FastAPI docs**: https://fastapi.tiangolo.com (API framework)
- **Motor docs**: https://motor.readthedocs.io (MongoDB async driver)
- **pytest docs**: https://docs.pytest.org (testing framework)
- **Mercado Bitcoin API v4**: docs/mercadobitcoin-swagger.yaml

Não tente adivinhar.

<feature_slug>
#$ARGUMENTS
</feature_slug>
