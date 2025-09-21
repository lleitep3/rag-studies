# 💬 Interactive RAG Chat

Um assistente de código inteligente que responde perguntas sobre seu projeto Python usando RAG (Retrieval-Augmented Generation).

## 🎯 **O que faz?**

- **Analisa seu código** Python e cria um índice inteligente
- **Responde perguntas** sobre arquitetura, implementação e uso
- **Busca contexto relevante** automaticamente
- **Interface colorida** e amigável no terminal
- **Suporte a múltiplos LLMs** (Ollama local, Google Gemini)

## 🚀 **Como usar**

### Início Rápido
```bash
# Navegue para a pasta do app
cd apps/interactive-chat

# Execute com configuração padrão
python main.py
```

### Opções Avançadas
```bash
# Usar modelo mais potente
python main.py --model llama3.2:3b

# Carregar código de outro projeto
python main.py --path /caminho/para/projeto

# Usar Google Gemini
python main.py --llm gemini --model gemini-1.5-flash

# Modo silencioso
python main.py --quiet
```

### Argumentos Disponíveis
- `--path, -p`: Caminho para código fonte (default: ../../src)
- `--pattern, -f`: Padrão de arquivos (default: **/*.py)
- `--llm, -l`: Tipo de LLM (ollama, gemini)
- `--model, -m`: Nome do modelo (default: llama3.2:1b)
- `--temperature, -t`: Temperatura de geração (default: 0.1)
- `--max-docs, -d`: Max documentos por consulta (default: 3)
- `--quiet, -q`: Modo silencioso

## 🎮 **Comandos no Chat**

Durante o chat, você pode usar estes comandos:

- `help` - Mostra todos os comandos
- `examples` - Exemplos de perguntas
- `stats` - Estatísticas do sistema
- `files` - Lista arquivos carregados
- `search` - Busca por palavras-chave
- `reload` - Recarrega documentos
- `info` - Informações detalhadas
- `quit` - Sair do chat

## 💡 **Exemplos de Perguntas**

- "Como funciona o PythonLoader?"
- "Qual a diferença entre GeminiLLM e OllamaLLM?"
- "Como implementar um novo loader?"
- "Explique o padrão Factory usado no projeto"
- "Como o RAGEngine funciona?"

## 🔧 **Pré-requisitos**

### Para Ollama (Recomendado)
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo
ollama pull llama3.2:1b

# Iniciar servidor
ollama serve
```

### Para Google Gemini
```bash
# Configurar chave da API
export GOOGLE_API_KEY="sua_chave_aqui"

# Ou criar arquivo .env
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

## 📁 **Estrutura do App**

```
interactive-chat/
├── main.py              # 🎯 Aplicativo principal
├── code_assistant.py    # 🤖 Assistente RAG principal
├── chat_interface.py    # 💬 Interface de chat
├── search_engine.py     # 🔍 Motor de busca
├── colored_output.py    # 🎨 Utilitário de cores
└── README.md           # 📖 Esta documentação
```

## 🛠️ **Arquitetura**

### Fluxo Principal
1. **Carregamento**: PythonLoader lê arquivos Python
2. **Indexação**: SimpleSearchEngine cria índice por palavras-chave
3. **Chat**: ChatInterface gerencia interação do usuário
4. **Busca**: Encontra documentos relevantes para pergunta
5. **Geração**: LLM gera resposta baseada no contexto
6. **Apresentação**: ColoredOutput exibe resultado formatado

### Componentes
- **CodeAssistant**: Orquestra todo o pipeline RAG
- **SearchEngine**: Busca simples mas eficaz por relevância
- **ChatInterface**: UX rica com comandos e exemplos
- **ColoredOutput**: Interface visual atrativa

## 🎨 **Personalização**

### Modificar Exemplos
Edite `chat_interface.py`, seção `example_questions`:
```python
self.example_questions = [
    "Sua pergunta customizada aqui",
    # ... mais exemplos
]
```

### Adicionar Comandos
No `ChatInterface.__init__()`:
```python
self.commands['meucomando'] = self._meu_comando

def _meu_comando(self):
    # Sua implementação
    pass
```

### Customizar Motor de Busca
Modifique `SimpleSearchEngine.keyword_mapping` para ajustar relevância.

## 🚀 **Performance**

- **llama3.2:1b**: ~2-5s por resposta, qualidade boa
- **llama3.2:3b**: ~5-10s por resposta, qualidade superior  
- **gemini-1.5-flash**: ~1-3s, mas requer internet e quota

## 📝 **Logs e Debug**

Para debug detalhado, remova `--quiet`:
```bash
python main.py --path ../../src
```

Para erros de conexão:
```bash
# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar modelos instalados
ollama list
```

## 🤝 **Contribuindo**

1. **Novos LLMs**: Adicione em `../src/llms/`
2. **Novos Loaders**: Adicione em `../src/loaders/`
3. **Melhorias na Interface**: Modifique `chat_interface.py`
4. **Motor de Busca**: Evolua `search_engine.py`

---

💡 **Dica**: Comece com o modelo `llama3.2:1b` para testes rápidos, depois evolua para modelos mais potentes conforme necessário!