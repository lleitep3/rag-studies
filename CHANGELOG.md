# 📋 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.2.0] - 2024-10-03

### 🎉 Adicionado
- **Code Review Engine Funcional**
  - Implementados parsers para extrair issues, sugestões e pontos positivos
  - Detecção inteligente de severidade baseada em palavras-chave
  - Suporte a múltiplos formatos de resposta do LLM
  - 99% de cobertura de testes no módulo

- **Suite de Testes Completa**
  - 50+ testes unitários implementados
  - Fixtures compartilhadas via `conftest.py`
  - Cobertura de 62% do código
  - Script `run_tests.sh` com múltiplas opções

- **CI/CD com GitHub Actions**
  - Pipeline automatizado para testes e segurança
  - Execução em Python 3.10, 3.11 e 3.12
  - Análise de segurança com Bandit
  - Verificação de vulnerabilidades com Safety
  - Upload de cobertura para Codecov (opcional)

- **Configurações do Projeto**
  - `pyproject.toml` com configurações centralizadas
  - `.bandit` para análise de segurança
  - `pytest.ini` para configuração de testes
  - `.github/README.md` com documentação do CI/CD

### 🔧 Modificado
- **CodeReviewCapacity**
  - Corrigido método `prepare_context()` para usar `ask()` ao invés de `search()`
  - Adicionada compatibilidade com `self.rag_engine` e `self.rag`
  - Melhorado tratamento de exceções

- **Requirements**
  - Atualizado `requirements.txt` com todas as dependências necessárias
  - Separadas dependências de produção e desenvolvimento
  - Adicionadas ferramentas de teste e segurança

- **README Principal**
  - Redesign completo com badges e métricas
  - Adicionadas seções de testes e qualidade
  - Incluído guia de contribuição atualizado
  - Quick Start simplificado

### 🐛 Corrigido
- Sintaxe de docstring incorreta em `reviewer.py`
- Imports faltantes nos testes
- Referências inconsistentes entre `rag` e `rag_engine`
- Testes falhando por falta de mocks adequados

### 📊 Métricas
- **Testes**: 47/49 passando (96% de sucesso)
- **Cobertura**: 62% do código
- **Segurança**: 0 vulnerabilidades detectadas
- **CI/CD**: Funcionando em 3 versões do Python

## [0.1.0] - 2024-10-02

### 🎉 Inicial
- Sistema RAG básico com PythonLoader
- Integração com Ollama e Google Gemini
- ChromaDB como vector store
- Chat interativo funcional
- Estrutura modular com padrões de design

---

## Roadmap Futuro

### [0.3.0] - Planejado
- [ ] API REST com FastAPI
- [ ] Interface web com Streamlit/Gradio
- [ ] Suporte a mais linguagens (JavaScript, Go, Rust)
- [ ] Integração com GitHub/GitLab
- [ ] Métricas de código avançadas

### [0.4.0] - Conceitual
- [ ] Modo multi-usuário
- [ ] Dashboard de análise
- [ ] Integração com IDEs (VSCode, PyCharm)
- [ ] Pipeline de CI/CD customizável
- [ ] Exportação de relatórios (PDF, HTML)