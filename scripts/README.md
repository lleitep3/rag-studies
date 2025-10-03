# 📜 Scripts do RAG Study

Esta pasta contém scripts utilitários para facilitar o desenvolvimento e manutenção do projeto RAG Study.

## 🛠️ Scripts Disponíveis

### 1. `create_app.py` - Gerador de Apps RAG
**Descrição:** Gera estrutura completa para novos apps RAG com templates prontos para uso.

**Uso:**
```bash
# Criar app básico
python scripts/create_app.py nome-do-app

# Criar app de chat
python scripts/create_app.py chat-bot --type chat

# Criar app de análise
python scripts/create_app.py analyzer --type analysis --author "Seu Nome"

# Criar API
python scripts/create_app.py api-server --type api

# Sobrescrever app existente
python scripts/create_app.py meu-app --force
```

**Tipos de Apps:**
- `basic` - Template simples para qualquer propósito
- `chat` - App de chat interativo com loop de conversação
- `analysis` - App para análise de dados com RAG
- `api` - Template para APIs REST com endpoints RAG

**Arquivos Gerados:**
- `main.py` - Script principal com toda lógica
- `README.md` - Documentação completa
- `requirements.txt` - Dependências Python
- `config.example.json` - Exemplo de configuração

---

### 2. `list_apps.py` - Listador de Apps
**Descrição:** Lista e exibe informações sobre todos os apps RAG criados.

**Uso:**
```bash
# Lista simples em formato tabela
python scripts/list_apps.py

# Lista detalhada com todas as informações
python scripts/list_apps.py --detailed

# Filtrar por tipo
python scripts/list_apps.py --type chat
python scripts/list_apps.py --type analysis --detailed
```

**Informações Exibidas:**
- Status do app (✅ Completo, 🔄 Em progresso, ⚠️ Incompleto)
- Nome e tipo do app
- Tamanho total dos arquivos
- Data de criação e modificação
- Arquivos presentes (main.py, README.md, config, requirements.txt)
- Estatísticas gerais

---

### 3. `run_tests.sh` - Executor de Testes
**Descrição:** Executa a suíte de testes do projeto com coverage.

**Uso:**
```bash
# Executar todos os testes
./scripts/run_tests.sh

# Com relatório de coverage
./scripts/run_tests.sh --coverage
```

---

### 4. `remove_app.py` - Removedor de Apps
**Descrição:** Remove aplicações RAG com confirmação de segurança.

**Uso:**
```bash
# Remover com confirmação
python scripts/remove_app.py nome-do-app

# Remover sem confirmação (CUIDADO!)
python scripts/remove_app.py nome-do-app --force
```

**Características:**
- Solicita confirmação antes de remover (exceto com --force)
- Lista arquivos que serão removidos
- Mostra estatísticas após remoção
- Operação IRREVERSÍVEL

---

### 5. `setup_environment.sh` - Configurador de Ambiente
**Descrição:** Configura o ambiente de desenvolvimento com todas as dependências.

**Uso:**
```bash
# Configurar ambiente
./scripts/setup_environment.sh

# Com ambiente virtual
./scripts/setup_environment.sh --venv
```

---

## 📝 Criando Novos Scripts

Ao criar novos scripts, siga estas diretrizes:

1. **Cabeçalho Descritivo:** Inclua sempre um docstring explicativo no início
2. **Shebang:** Use `#!/usr/bin/env python3` para Python ou `#!/bin/bash` para Bash
3. **Argumentos:** Use `argparse` para Python ou `getopts` para Bash
4. **Tratamento de Erros:** Sempre inclua tratamento de exceções
5. **Documentação:** Atualize este README com informações do novo script

### Template Python:
```python
#!/usr/bin/env python3
"""
📋 Nome do Script
=================

Descrição detalhada do que o script faz.
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Descrição do script",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # ... argumentos ...
    args = parser.parse_args()
    
    # Lógica principal
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Template Bash:
```bash
#!/bin/bash
# Nome do Script - Descrição

set -e  # Exit on error

# Função de ajuda
show_help() {
    cat << EOF
Uso: $0 [opções]

Opções:
    -h  Mostra esta ajuda
    -v  Modo verboso
EOF
}

# Parse de argumentos
while getopts "hv" opt; do
    case $opt in
        h) show_help; exit 0 ;;
        v) VERBOSE=1 ;;
        ?) show_help; exit 1 ;;
    esac
done

# Lógica principal
echo "Executando script..."
```

## 🔧 Manutenção

### Testando Scripts:
```bash
# Python
python -m pytest scripts/test_*.py

# Bash
shellcheck scripts/*.sh
```

### Permissões:
```bash
# Tornar executável
chmod +x scripts/nome_do_script.py
chmod +x scripts/nome_do_script.sh
```

## 📚 Dependências

Os scripts Python dependem do módulo `src` do projeto. Certifique-se de que o ambiente está configurado:

```bash
# Instalar dependências
pip install -r requirements.txt

# Adicionar src ao PYTHONPATH (se necessário)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 🤝 Contribuindo

Para adicionar novos scripts:

1. Crie o script seguindo os templates
2. Teste extensivamente
3. Adicione documentação neste README
4. Faça um PR com descrição clara

---

**Última atualização:** 2025-10-03  
**Mantenedor:** RAG Team