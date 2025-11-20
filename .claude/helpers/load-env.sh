#!/bin/bash
# Helper para carregar variáveis do .ia.env

# Função para carregar .ia.env
load_ia_env() {
    local env_file="${PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}/.ia.env"

    if [ -f "$env_file" ]; then
        # Exportar variáveis do .ia.env
        export $(grep -v '^#' "$env_file" | xargs)
        echo "✅ Variáveis carregadas de .ia.env"
    else
        echo "⚠️  Arquivo .ia.env não encontrado em $env_file"
        echo "   Crie o arquivo baseado em .ia.env.example"
        return 1
    fi
}

# Carregar automaticamente quando o script for source'd
load_ia_env
