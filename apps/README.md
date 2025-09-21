# 🚀 RAG Study Apps

Coleção de aplicativos e demos do projeto RAG (Retrieval-Augmented Generation).

## 📱 **Aplicativos Disponíveis**

### 💬 **Interactive Chat** - `interactive-chat/`
> **Chat interativo inteligente com seu código**

Um assistente que conhece todo o seu código e responde perguntas sobre arquitetura, implementação e uso. Perfeito para explorar projetos grandes ou entender código legado.

**Características:**
- 🤖 Chat conversacional no terminal
- 🔍 Busca inteligente no código fonte  
- 📚 Respostas contextualizadas com fontes
- ⚡ Suporte a Ollama (local) e Gemini (cloud)
- 🎨 Interface colorida e amigável

**Como usar:**
```bash
cd interactive-chat
python main.py
```

[📖 **Documentação completa**](interactive-chat/README.md)

---

## 🛠️ **Como Adicionar Novos Apps**

### Estrutura Recomendada
```
apps/
├── seu-novo-app/
│   ├── main.py              # Ponto de entrada
│   ├── README.md           # Documentação específica
│   ├── requirements.txt    # Dependências (se houver)
│   └── ...                # Módulos específicos
└── README.md              # Este arquivo
```

### Padrões Sugeridos
1. **Nome do diretório**: kebab-case (ex: `interactive-chat`, `code-analyzer`)
2. **Ponto de entrada**: `main.py` com função `main()`
3. **Documentação**: `README.md` com instruções claras
4. **Dependências**: Listar em `requirements.txt` se necessário
5. **Módulos locais**: Prefira módulos auto-contidos para facilitar portabilidade

### Template Básico `main.py`
```python
#!/usr/bin/env python3
"""
🎯 Seu Novo App
===============

Descrição do que seu app faz.
"""

import sys
import os
from pathlib import Path

# Adiciona src ao path se necessário
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def main():
    """Função principal"""
    print("🚀 Seu app funcionando!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 💡 **Ideias para Novos Apps**

### 📊 **Code Analyzer** - `code-analyzer/`
- Métricas de código (complexidade, linhas, etc.)
- Identificação de code smells
- Dependências entre módulos

### 🔍 **Semantic Search** - `semantic-search/`
- Busca semântica avançada com embeddings
- Interface web simples
- Comparação de similaridade entre arquivos

### 📝 **Documentation Generator** - `doc-generator/`
- Geração automática de documentação
- Comentários inteligentes para código
- Diagramas de arquitetura

### 🧪 **Test Generator** - `test-generator/`
- Geração de testes unitários
- Casos de teste baseados em código
- Cobertura inteligente

### 📈 **Project Dashboard** - `dashboard/`
- Visão geral do projeto
- Estatísticas de código
- Progresso de desenvolvimento

### 🔄 **Code Refactor Assistant** - `refactor-assistant/`
- Sugestões de refatoração
- Detecção de padrões
- Modernização de código

## 🎯 **Benefícios da Estrutura**

### ✅ **Modularidade**
- Cada app é independente
- Facilita manutenção e desenvolvimento
- Permite reutilização de componentes

### ✅ **Escalabilidade** 
- Fácil adicionar novos apps
- Não afeta apps existentes
- Compartilhamento de recursos do projeto

### ✅ **Organização**
- Separação clara de responsabilidades
- Documentação específica para cada app
- Facilita colaboração em equipe

### ✅ **Experimentação**
- Protótipos rápidos
- Testes de novas ideias
- Demos focados em funcionalidades específicas

## 🤝 **Contribuindo**

1. **Crie uma nova pasta** para seu app em `apps/`
2. **Siga os padrões** de nomenclatura e estrutura
3. **Documente bem** com README.md detalhado
4. **Teste** antes de submeter
5. **Atualize este README** adicionando seu app à lista

## 📚 **Recursos Compartilhados**

Todos os apps têm acesso aos componentes do projeto:

- **📁 Loaders**: `../src/loaders/` - Carregamento de documentos
- **🧠 LLMs**: `../src/llms/` - Modelos de linguagem
- **🗂️ Vector Stores**: `../src/vector_stores/` - Armazenamento vetorial
- **⚙️ Core**: `../src/core/` - RAG Engine e utilitários

## 🔧 **Utilitários Disponíveis**

### ColoredOutput
Para output colorido no terminal (veja `interactive-chat/colored_output.py`).

### Configuração Comum
Carregamento de `.env`, configurações padrão, etc.

---

**💡 Dica**: Comece explorando o `interactive-chat` para entender como os componentes se integram, depois crie seu próprio app!