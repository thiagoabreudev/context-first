# Context-First Methodology

Comandos Claude para metodologia Context-First: Spec-Driven Development com IA.

## Configuração Inicial

### 1. Configurar Variáveis de Ambiente

Copie o arquivo `.ia.env.example` para `.ia.env`:

```bash
cp .ia.env.example .ia.env
```

Edite `.ia.env` e configure o caminho para suas metaspecs:

```bash
METASPECS_DIR=/caminho/para/suas/metaspecs
```

### 2. Estrutura de Diretórios

```
context-first/
├── .claude/               # Comandos Claude
│   ├── commands/
│   │   ├── context-first/ # Comandos principais
│   │   ├── context/       # Gestão de contexto
│   │   └── ...
│   └── helpers/          # Scripts auxiliares
├── .ia.env               # Variáveis de ambiente (não versionado)
├── .ia.env.example       # Template de configuração
└── README.md            # Este arquivo
```

### 3. Metaspecs (Repositório Separado)

As metaspecs ficam em um repositório separado, configurado via `METASPECS_DIR`:

```
metaspecs/
├── business/             # Regras de negócio
│   ├── authentication/
│   ├── strategies/
│   └── ...
├── technical/            # Especificações técnicas
│   ├── architecture/
│   ├── api/
│   └── ...
├── observability/        # Specs de observabilidade
└── governance/           # Specs de governança
```

## Comandos Disponíveis

### Context-First Commands

#### `/context-first test-first <feature>`
Criar testes ANTES do código (TDD adaptado para IA).

```bash
/context-first test-first "Criar endpoint POST /api/login"
```

#### `/context-first validate-spec [arquivo]`
Validar código contra metaspecs (regras de negócio).

```bash
# Validar arquivo específico
/context-first validate-spec src/workflows/candle_buy.py

# Validar todos os arquivos modificados
/context-first validate-spec
```

#### `/context-first observability <feature>`
Adicionar observabilidade completa (logging, métricas, tracing).

```bash
/context-first observability login
```

#### `/context-first governance <feature>`
Adicionar governança completa (auditoria, compliance, segurança).

```bash
/context-first governance payment
```

#### `/context-first security-check [arquivo]`
Verificar segurança do código antes de commit.

```bash
/context-first security-check
```

### Context Management

#### `/context status`
Monitorar uso atual da janela de contexto.

#### `/context checkpoint`
Salvar estado completo e preparar para chaveamento de contexto.

#### `/context clean`
Remover informações desnecessárias do contexto.

#### `/context compact`
Compactar contexto resumindo conversa em NOTES.md.

#### `/context budget <feature> <tokens>`
Definir orçamento de tokens para uma feature.

```bash
/context budget login 50000
```

## Como Funciona

### 1. Carregamento de Variáveis

Todos os comandos automaticamente carregam `METASPECS_DIR` do arquivo `.ia.env`:

```bash
# Carregado automaticamente
export $(grep -v '^#' .ia.env | xargs)
```

### 2. Referência às Metaspecs

Comandos usam `$METASPECS_DIR` para acessar as especificações:

```bash
# Exemplo interno
metaspec_file="$METASPECS_DIR/business/authentication/login.md"
```

### 3. Validação de Specs

O comando `validate-spec` lê as metaspecs e valida:

- **Must Do**: O que o código DEVE fazer
- **Must Not Do**: O que o código NÃO DEVE fazer
- **Edge Cases**: Casos extremos que devem ser tratados

### 4. Test-First

O comando `test-first`:

1. Lê metaspecs relevantes de `$METASPECS_DIR`
2. Identifica behaviors (Must Do, Must Not Do, Edge Cases)
3. Gera arquivo de teste completo
4. Você implementa o código para passar nos testes

## Exemplo de Uso Completo

### 1. Criar Feature com Test-First

```bash
/context-first test-first "Endpoint POST /api/login com JWT"
```

Saída:
```
✅ Tests created: tests/api/test_login.py
15 tests generated based on:
  - $METASPECS_DIR/business/authentication/login.md
  - $METASPECS_DIR/technical/api/security.md
```

### 2. Implementar Código

(Você escreve o código para passar nos testes)

### 3. Validar Contra Specs

```bash
/context-first validate-spec src/api/auth.py
```

Saída:
```
📋 Spec Validation - src/api/auth.py
Overall Compliance: 95% ✅
✅ APPROVED
```

### 4. Adicionar Observabilidade

```bash
/context-first observability login
```

### 5. Adicionar Governança

```bash
/context-first governance login
```

### 6. Security Check

```bash
/context-first security-check
```

## Integração com Git

Os comandos respeitam o `.gitignore`:

```gitignore
# Arquivo .ia.env não é versionado
.ia.env
```

## Troubleshooting

### Erro: "METASPECS_DIR não encontrado"

Certifique-se de que:
1. O arquivo `.ia.env` existe na raiz do projeto
2. A variável `METASPECS_DIR` está configurada
3. O caminho aponta para um diretório válido

### Erro: "Metaspec não encontrada"

Verifique:
1. O caminho em `METASPECS_DIR` está correto
2. O diretório de metaspecs contém os arquivos esperados
3. A estrutura de diretórios está correta

## Contribuindo

Para adicionar novos comandos:

1. Crie o arquivo em `.claude/commands/`
2. Use `$METASPECS_DIR` para referenciar metaspecs
3. Adicione documentação neste README

## Licença

MIT
