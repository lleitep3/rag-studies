# 🚀 RAG Study - Sistema de Análise de Código com IA

![CI Status](https://github.com/SEU_USUARIO/rag-study/workflows/🔒%20CI%20-%20Testes%20e%20Segurança/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Coverage](https://img.shields.io/badge/coverage-62%25-green)
![Security](https://img.shields.io/badge/security-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

> **Sistema completo de RAG (Retrieval-Augmented Generation) para análise inteligente de código, com capacidades de code review automatizado, chat interativo e busca semântica.**

## ✨ **Destaques**

- 🔍 **Code Review Automatizado** - Análise de segurança, performance e qualidade
- 💬 **Chat Interativo** - Converse sobre seu código com IA
- 🔧 **Gerador de Apps RAG** - Crie novos apps em segundos [`NEW`]
- 📁 **Gerenciamento de Apps** - Liste, crie e remova apps facilmente [`NEW`]
- 🎨 **Interface Colorida** - Output rico e formatado [`NEW`]
- 🧪 **96% dos Testes Passando** - Suite completa com 62% de cobertura
- 🔒 **Segurança Validada** - CI/CD com Bandit e Safety
- 🏃 **100% Local** - Funciona com Ollama sem dependências externas

---

## 🎯 **Aplicações Disponíveis**

### 1. 🔍 **Code Review Demo** [`NEW`]
Análise automatizada de código Python com detecção de problemas e sugestões:

```bash
cd apps/code-review-demo
python main.py example.py

# Análise focada em segurança
python main.py src/ --focus security --recursive
```

**Capacidades:**
- Detecta problemas de segurança (SQL injection, senhas em texto plano)
- Identifica problemas de performance
- Sugere melhorias de arquitetura
- Destaca pontos positivos do código

### 2. 💬 **Interactive Chat**
Assistente de código conversacional:

```bash
cd apps/interactive-chat
python main.py
```

### 3. 📊 **Code Analyzer** [`NEW`]
Análise de dados e insights com RAG:

```bash
cd apps/code-analyzer
python main.py --index-path ../../src --model llama3.2:1b
```

## 🎯 **Sobre o Projeto**

Este projeto é um assistente de código inteligente que:
- 📖 **Lê e entende** código Python
- 🤔 **Responde perguntas** sobre arquitetura e implementação
- 🔍 **Busca contextualmente** em toda a base de código
- 💬 **Conversa naturalmente** sobre desenvolvimento
- 🖥️ **Roda localmente** sem dependências externas

> **Atenção:** Este projeto é experimental e serve para fins de estudo. Sinta-se à vontade para explorar, modificar e contribuir com novas ideias!


## 🚀 **Como começar**

### Demo Interativa
```bash
# Clone e entre no projeto
git clone <repo-url>
cd rag-study

# Instale dependências
pip install -r requirements.txt

# Execute o chat interativo
cd apps/interactive-chat
python main.py
```

**Exemplos de perguntas:**
- "Como funciona o PythonLoader?"
- "Diferença entre GeminiLLM e OllamaLLM?"
- "Como adicionar um novo loader?"
- "Como usar o RAGEngine?"


## 📋 **Pré-requisitos**

### Obrigatórios
- **Python 3.10+** (Testado em 3.10, 3.11, 3.12)
- **Ollama** instalado e rodando
  ```bash
  # Instalar Ollama
  curl -fsSL https://ollama.ai/install.sh | sh

  # Baixar modelo (recomendado)
  ollama pull llama3.2:1b

  # Iniciar servidor
  ollama serve
  ```

### Opcionais (para funcionalidades completas)
- **Google AI API Key** (para Gemini)
- **ChromaDB embeddings** (para vector store completo)


## 🏗️ **Arquitetura**

```
rag-study/
├── 📱 apps/                 # Aplicações prontas para uso
│   ├── code-review-demo/   # Revisor de código automatizado
│   └── interactive-chat/    # Chat conversacional
├── 🧠 src/                  # Core do sistema
│   ├── capacities/          # Capacidades especializadas
│   │   └── code_review/     # Engine de code review
│   ├── core/                # RAGEngine principal
│   ├── llms/                # Integrações LLM (Ollama, Gemini)
│   ├── loaders/             # Carregadores de documentos
│   └── vector_stores/       # Armazenamento vetorial
├── 🧪 tests/                # Suite de testes completa
│   ├── capacities/          # Testes de capacidades
│   ├── core/                # Testes do engine
│   └── llms/                # Testes de LLMs
├── 🔧 scripts/              # Scripts utilitários [`NEW`]
│   ├── create_app.py        # Gerador de apps RAG
│   ├── list_apps.py         # Listador de apps
│   └── remove_app.py        # Removedor de apps
└── 🔧 .github/              # CI/CD com GitHub Actions
```

**Padrões de Design:**
- 🏭 **Factory Pattern** - Criação flexível de componentes
- 🔧 **Strategy Pattern** - Múltiplas estratégias de busca
- 📦 **Dependency Injection** - Baixo acoplamento


## 💡 **Funcionalidades**

### ✅ **Implementado e Testado**
- 🐍 **PythonLoader** - Carregamento inteligente de código
- 🤖 **Múltiplos LLMs** - Ollama (local) + Gemini (remoto)
- 🔍 **Vector Store** - ChromaDB com embeddings HuggingFace
- 🎯 **RAG Engine** - Pipeline completo com 88% de cobertura
- 💬 **Chat Interativo** - Interface conversacional
- 🔒 **Code Review** - Análise automatizada com parsers funcionais
- 🧪 **Suite de Testes** - 50+ testes unitários
- 🚀 **CI/CD** - GitHub Actions com análise de segurança
- 🔧 **Gerador de Apps** - Criação automática de novos apps [`NEW`]
- 📁 **Gerenciador de Apps** - Lista e remove apps facilmente [`NEW`]
- 🎨 **ColoredOutput** - Interface colorida e formatada [`NEW`]

### 🔧 **Configurações**
- 📝 Múltiplos tipos de busca (similarity, MMR, threshold)
- 🎛️ Parâmetros ajustáveis (chunk size, temperatura)
- 🔄 Troca dinâmica de modelos
- 💾 Persistência automática


## 🛠️ **Instalação Rápida**

### 1. Clone o repositório
```bash
git clone <repo-url>
cd rag-study
```

### 2. Instale as dependências
```bash
# Dependências principais
pip install -r requirements.txt

# Ferramentas de desenvolvimento (opcional)
pip install pytest pytest-cov bandit safety
```

### 3. Configure o ambiente (opcional)
```bash
# Para usar Gemini (opcional)
cp .env.example .env
# Edite .env com sua GOOGLE_API_KEY
```

### 4. Instale e configure Ollama
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo leve (recomendado)
ollama pull llama3.2:1b

# Ou modelo maior (melhor qualidade)
ollama pull gemma3:4b

# Iniciar servidor
ollama serve
```


## 🎮 **Como Usar**

### 🚀 **Aplicações Prontas**

#### Code Review Automatizado
```bash
cd apps/code-review-demo

# Analisar arquivo específico
python main.py example.py

# Análise recursiva de diretório
python main.py ../../src --recursive

# Foco em segurança
python main.py example.py --focus security
```

#### Chat Interativo
```bash
cd apps/interactive-chat
python main.py
```

📱 **[Ver documentação completa dos apps →](apps/README.md)**

### Uso Programático
```python
from src.core.engine import create_rag_engine

# Criar sistema RAG
engine = create_rag_engine(
    loader_type="python",
    vector_store_type="chroma",
    llm_type="ollama",
    llm_kwargs={"model_name": "llama3.2:1b"}
)

# Indexar código
stats = engine.setup_pipeline("./src", "**/*.py")

# Fazer perguntas
result = engine.ask("Como funciona o PythonLoader?")
print(result['answer'])
```


## 🔧 **Gerenciamento de Apps** [`NEW`]

### Criar Novo App
Use o gerador automático para criar apps com estrutura completa:

```bash
# App básico
python scripts/create_app.py meu-app

# App de chat interativo
python scripts/create_app.py chat-bot --type chat

# App de análise de dados
python scripts/create_app.py analyzer --type analysis --author "Seu Nome"

# API REST
python scripts/create_app.py api-server --type api
```

**Tipos disponíveis:**
- 🎯 **basic** - Template simples para qualquer propósito
- 💬 **chat** - Chat interativo com loop de conversação
- 📊 **analysis** - Análise de dados com RAG
- 🌐 **api** - API REST com endpoints RAG

**Arquivos gerados automaticamente:**
- `main.py` - Script principal com lógica completa
- `README.md` - Documentação detalhada
- `requirements.txt` - Dependências Python
- `config.example.json` - Configuração de exemplo

### Listar Apps Existentes
```bash
# Lista simples em tabela
python scripts/list_apps.py

# Lista detalhada
python scripts/list_apps.py --detailed

# Filtrar por tipo
python scripts/list_apps.py --type chat
```

### Remover Apps
```bash
# Com confirmação
python scripts/remove_app.py nome-do-app

# Sem confirmação (cuidado!)
python scripts/remove_app.py nome-do-app --force
```

📁 **[Ver documentação completa dos scripts →](scripts/README.md)**


## 🧪 **Testes e Qualidade**

### Executar Testes
```bash
# Todos os testes unitários
./run_tests.sh -u

# Com cobertura
./run_tests.sh -c

# Testes específicos
pytest tests/capacities/test_code_review.py -v
```

### Análise de Segurança
```bash
# Verificar código
bandit -r src/ -ll

# Verificar dependências
safety check
```

### Métricas Atuais
- ✅ **47/49 testes passando** (96% de sucesso)
- 📊 **62% de cobertura** de código
- 🔒 **0 vulnerabilidades** detectadas
- 🎯 **99% de cobertura** no módulo code_review

## 📚 **Documentação**

- 📖 **[Conceitos RAG](docs/rag-concepts.md)** - Teoria e fundamentos
- 🏗️ **[Arquitetura](docs/architecture.md)** - Design e componentes
- 🔧 **[CI/CD Guide](.github/README.md)** - Integração contínua
- 🔍 **[Code Review Demo](apps/code-review-demo/README.md)** - Guia do revisor


## 🤝 **Contribuindo**

### Checklist para Contribuições
- [ ] Adicione testes unitários (mínimo 70% cobertura)
- [ ] Execute `./run_tests.sh -u` localmente
- [ ] Verifique segurança com `bandit -r src/`
- [ ] Atualize documentação relevante
- [ ] Adicione docstrings nas funções públicas

### Estrutura para Novos Componentes
```python
# Nova Capacidade
class MyCapacity(BaseCapacity):
    def get_prompt_template(self) -> str:
        return "Seu template aqui"
    
    def process_response(self, response: str) -> CapacityResponse:
        # Processar resposta
        return CapacityResponse(success=True, data={})

# Adicionar testes em tests/capacities/test_my_capacity.py
```


## 🔬 **Stack Tecnológica**

### Core
- 🐍 **Python 3.10-3.12** - Linguagem principal
- 🦜 **LangChain** - Framework RAG
- 🟢 **Ollama** - LLMs locais (llama3.2, gemma)
- 💎 **Google Gemini** - LLM remoto opcional
- 🎨 **ChromaDB** - Vector database
- 🤗 **HuggingFace** - Embeddings (all-MiniLM-L6-v2)

### Qualidade & Testes
- 🧪 **Pytest** - Framework de testes
- 📊 **Coverage.py** - Análise de cobertura
- 🔒 **Bandit** - Análise de segurança
- 🔍 **Safety** - Verificação de dependências
- 🚀 **GitHub Actions** - CI/CD automatizado


## 📊 **Status do Projeto**

### Funcionalidades
```
✅ Core RAG System     - 100% funcional com 88% cobertura
✅ Code Review Engine  - Parsers implementados e testados
✅ Interactive Chat    - Interface conversacional completa
✅ Local LLMs         - Ollama totalmente integrado
✅ Test Suite         - 50+ testes automatizados
✅ CI/CD Pipeline     - GitHub Actions configurado
✅ Security Checks    - Bandit + Safety integrados
✅ App Generator      - Criação automática de apps [`NEW`]
✅ App Manager        - Gerenciamento completo [`NEW`]
✅ ColoredOutput     - Interface rica em cores [`NEW`]
🔄 API REST          - Em desenvolvimento
🔄 Web Interface     - Planejado
```

### Métricas de Qualidade
- 🎯 **Cobertura de Código:** 62% (Meta: 70%)
- ✅ **Testes Passando:** 96% (47/49)
- 🔒 **Vulnerabilidades:** 0 detectadas
- 📦 **Dependências:** Todas atualizadas
- 🏃 **CI/CD:** Funcionando em 3 versões Python

## 🚀 **Quick Start**

```bash
# 1. Clone e instale
git clone <repo-url> && cd rag-study
pip install -r requirements.txt

# 2. Configure Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
ollama serve

# 3. Crie seu primeiro app (NOVO!)
python scripts/create_app.py meu-chat --type chat
cd apps/meu-chat
python main.py --help

# 4. Ou experimente apps prontos
cd apps/code-review-demo
python main.py example.py

# 5. Liste todos os apps disponíveis
python scripts/list_apps.py
```

## 📝 **Licença**

Este projeto é open-source para fins educacionais. Sinta-se livre para usar, modificar e distribuir.

## 🙏 **Agradecimentos**

- Comunidade LangChain
- Equipe Ollama
- Contribuidores do ChromaDB
- Todos que compartilham conhecimento sobre RAG e LLMs

---

<p align="center">
  <strong>⭐ Se este projeto foi útil, considere dar uma estrela!</strong><br>
  <em>Desenvolvido com ❤️ para a comunidade de IA</em>
</p>

<p align="center">
  <a href="https://github.com/SEU_USUARIO/rag-study/issues">Reportar Bug</a> •
  <a href="https://github.com/SEU_USUARIO/rag-study/pulls">Contribuir</a> •
  <a href=".github/README.md">CI/CD Docs</a>
</p>
