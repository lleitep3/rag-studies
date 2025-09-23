
# RAG Code Assistant — Repositório de Estudos

> **Este repositório é dedicado a estudos, experimentação e aprendizado sobre sistemas RAG (Retrieval-Augmented Generation) aplicados à análise inteligente de código Python.**

Aqui você encontrará exemplos, protótipos, testes de conceitos e implementações didáticas, sem compromisso com produção ou estabilidade. O objetivo é explorar ideias, aprender e compartilhar conhecimento sobre RAG, LLMs, busca semântica e arquitetura de sistemas inteligentes.

---


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
- **Python 3.8+**
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
src/
├── 📁 loaders/        # Carregamento de documentos
├── 🧠 llms/           # Modelos de linguagem (Gemini, Ollama)
├── 🗂️ vector_stores/  # Armazenamento vetorial (ChromaDB)
└── ⚙️ core/          # RAGEngine - Orquestrador principal
```

**Padrões de Design:**
- 🏭 **Factory Pattern** - Criação flexível de componentes
- 🔧 **Strategy Pattern** - Múltiplas estratégias de busca
- 📦 **Dependency Injection** - Baixo acoplamento


## 💡 **Funcionalidades**

### ✅ **Implementado**
- 🐍 **PythonLoader** - Carregamento inteligente de código
- 🤖 **Múltiplos LLMs** - Gemini (remoto) + Ollama (local)
- 🔍 **Vector Store** - ChromaDB com embeddings
- 🎯 **RAG Engine** - Pipeline completo
- 💬 **Chat Interativo** - Demo funcional

### 🔧 **Configurações**
- 📝 Múltiplos tipos de busca (similarity, MMR, threshold)
- 🎛️ Parâmetros ajustáveis (chunk size, temperatura)
- 🔄 Troca dinâmica de modelos
- 💾 Persistência automática


## 🛠️ **Instalação**

### 1. Clone o repositório
```bash
git clone <repo-url>
cd rag-study
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
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


## 🎮 **Como usar**

### 🚀 **Aplicativos**
O projeto inclui vários aplicativos organizados em [`apps/`](apps/):

```bash
# Chat interativo inteligente
cd apps/interactive-chat
python main.py
```

📱 **[Ver todos os aplicativos disponíveis →](apps/README.md)**

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


## 📚 **Documentação**

- 📖 **[Conceitos RAG](docs/rag-concepts.md)** - Teoria e fundamentos
- 🏗️ **[Arquitetura](docs/architecture.md)** - Design e componentes
- 🔧 **[Configuração](config.yaml)** - Parâmetros do sistema


## 🤝 **Contribuindo**

### Estrutura para novos componentes
```python
# Novo Loader
class MyLoader(BaseLoader):
    def load(self, path: str, glob: str) -> List[Document]:
        # Implementação
        pass

# Registrar na factory
# src/loaders/__init__.py
if loader_type == "my_type":
    return MyLoader(**kwargs)
```


## 🔬 **Tecnologias**

- 🐍 **Python 3.8+**
- 🦜 **LangChain** - Framework RAG
- 🟢 **Ollama** - LLMs locais
- 💎 **Google Gemini** - LLM remoto
- 🎨 **ChromaDB** - Vector database
- ⚡ **FastAPI** - API framework (futuro)


## 📊 **Status**

```
✅ Core System        - 100% funcional
✅ Demo Interactive   - Completa
✅ Local LLMs        - Ollama integrado
✅ Code Analysis     - Funcionando
🔄 Config System     - Em desenvolvimento
🔄 Advanced Logging  - Planejado
```

---


---

**Este repositório é para fins de estudo e experimentação. Não há garantias de funcionamento em produção. Contribuições, sugestões e dúvidas são bem-vindas!**

**Experimente agora:** `cd apps/interactive-chat && python main.py`
