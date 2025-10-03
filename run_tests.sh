#!/bin/bash
# Script para executar testes do projeto RAG Study

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     RAG Study - Suite de Testes       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# Função para exibir ajuda
show_help() {
    echo "Uso: $0 [OPÇÕES]"
    echo
    echo "Opções:"
    echo "  -h, --help         Mostra esta ajuda"
    echo "  -u, --unit         Executa apenas testes unitários"
    echo "  -i, --integration  Executa apenas testes de integração"
    echo "  -c, --coverage     Executa com relatório de cobertura"
    echo "  -v, --verbose      Modo verboso"
    echo "  -f, --file FILE    Executa apenas um arquivo de teste específico"
    echo "  -k, --keyword KEY  Executa apenas testes que contenham KEY no nome"
    echo "  --no-ollama        Pula testes que requerem Ollama"
    echo "  --no-chroma        Pula testes que requerem ChromaDB"
    echo
    echo "Exemplos:"
    echo "  $0                      # Executa todos os testes"
    echo "  $0 -u                   # Apenas testes unitários"
    echo "  $0 -c                   # Com cobertura"
    echo "  $0 -f test_engine.py    # Apenas testes do engine"
    echo "  $0 -k parse             # Apenas testes com 'parse' no nome"
}

# Variáveis padrão
PYTEST_ARGS=""
COVERAGE=false
MARKERS=""

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--unit)
            MARKERS="$MARKERS -m unit"
            echo -e "${YELLOW}→ Executando apenas testes unitários${NC}"
            shift
            ;;
        -i|--integration)
            MARKERS="$MARKERS -m integration"
            echo -e "${YELLOW}→ Executando apenas testes de integração${NC}"
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            echo -e "${YELLOW}→ Modo cobertura ativado${NC}"
            shift
            ;;
        -v|--verbose)
            PYTEST_ARGS="$PYTEST_ARGS -vv"
            shift
            ;;
        -f|--file)
            PYTEST_ARGS="$PYTEST_ARGS tests/*/$2"
            echo -e "${YELLOW}→ Executando arquivo: $2${NC}"
            shift 2
            ;;
        -k|--keyword)
            PYTEST_ARGS="$PYTEST_ARGS -k $2"
            echo -e "${YELLOW}→ Filtro por palavra-chave: $2${NC}"
            shift 2
            ;;
        --no-ollama)
            MARKERS="$MARKERS -m 'not requires_ollama'"
            echo -e "${YELLOW}→ Pulando testes que requerem Ollama${NC}"
            shift
            ;;
        --no-chroma)
            MARKERS="$MARKERS -m 'not requires_chroma'"
            echo -e "${YELLOW}→ Pulando testes que requerem ChromaDB${NC}"
            shift
            ;;
        *)
            echo -e "${RED}Opção desconhecida: $1${NC}"
            echo "Use -h ou --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

# Verificar se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest não está instalado!${NC}"
    echo -e "${YELLOW}→ Instale com: pip install pytest pytest-cov pytest-mock${NC}"
    exit 1
fi

# Construir comando pytest
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="pytest --cov=src --cov-report=term-missing --cov-report=html $MARKERS $PYTEST_ARGS"
else
    PYTEST_CMD="pytest $MARKERS $PYTEST_ARGS"
fi

# Executar testes
echo -e "${BLUE}→ Executando comando: $PYTEST_CMD${NC}"
echo -e "${BLUE}────────────────────────────────────────${NC}"
echo

# Executar pytest e capturar código de saída
eval $PYTEST_CMD
TEST_EXIT_CODE=$?

echo
echo -e "${BLUE}────────────────────────────────────────${NC}"

# Mostrar resultado
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
    
    if [ "$COVERAGE" = true ]; then
        echo -e "${BLUE}→ Relatório de cobertura HTML: htmlcov/index.html${NC}"
    fi
else
    echo -e "${RED}❌ Alguns testes falharam!${NC}"
    echo -e "${YELLOW}→ Código de saída: $TEST_EXIT_CODE${NC}"
fi

echo

exit $TEST_EXIT_CODE