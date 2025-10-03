# 🔒 CI/CD - Testes e Segurança

## 📋 Visão Geral

Este repositório usa GitHub Actions para executar automaticamente:
- ✅ **Testes unitários** em múltiplas versões do Python
- 🔒 **Análise de segurança** do código com Bandit
- 🔍 **Verificação de vulnerabilidades** nas dependências com Safety
- 📊 **Relatório de cobertura** de código

## 🚀 Quando Executa

O workflow é executado automaticamente quando:
- 📤 **Push** para branches `main` ou `develop`
- 🔀 **Pull Request** para branch `main`
- 🖱️ **Execução manual** via GitHub Actions UI

## 🧪 Testes

### Executados Automaticamente
- Testes unitários (marcados com `@pytest.mark.unit`)
- Testes que **NÃO** requerem serviços externos (Ollama, ChromaDB)

### Como Executar Localmente
```bash
# Todos os testes unitários
./run_tests.sh -u

# Com cobertura
./run_tests.sh -c

# Apenas testes específicos
pytest tests/capacities/test_code_review.py -v
```

## 🔒 Análise de Segurança

### Bandit
Verifica problemas de segurança no código Python:
- SQL Injection
- Uso de `eval()`
- Senhas hardcoded
- Criptografia fraca

**Executar localmente:**
```bash
bandit -r src/ -ll -i
```

### Safety
Verifica vulnerabilidades conhecidas nas dependências:

**Executar localmente:**
```bash
safety check
```

## 📊 Cobertura de Código

A cobertura é calculada automaticamente e enviada para Codecov (se configurado).

**Meta de cobertura:** 70%

**Executar localmente:**
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## ⚙️ Configuração

### Versões Python Testadas
- Python 3.10
- Python 3.11  
- Python 3.12

### Arquivos de Configuração
- `.github/workflows/ci.yml` - Workflow do GitHub Actions
- `pyproject.toml` - Configurações centralizadas
- `.bandit` - Configuração do Bandit
- `pytest.ini` - Configuração do pytest

## 🏷️ Badges

Adicione estas badges ao README principal:

```markdown
![Tests](https://github.com/SEU_USUARIO/rag-study/workflows/CI%20-%20Testes%20e%20Segurança/badge.svg)
![Coverage](https://codecov.io/gh/SEU_USUARIO/rag-study/branch/main/graph/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
```

## 🐛 Problemas Comuns

### Testes Falhando no CI mas Passando Localmente
- Verifique se está usando a mesma versão do Python
- Certifique-se que não há dependências de serviços externos
- Confirme que todos os arquivos necessários estão commitados

### Análise de Segurança com Falsos Positivos
- Adicione exceções no `.bandit` para códigos específicos
- Use `# nosec` em linhas específicas (com moderação)

## 📝 Manutenção

### Atualizar Dependências
```bash
pip install --upgrade -r requirements.txt
safety check
```

### Adicionar Nova Versão Python
Edite `.github/workflows/ci.yml`:
```yaml
matrix:
  python-version: ['3.10', '3.11', '3.12', '3.13']
```

## 🤝 Contribuindo

1. Sempre execute os testes localmente antes do push
2. Mantenha cobertura acima de 70%
3. Resolva issues de segurança antes do merge
4. Atualize esta documentação quando alterar o CI/CD