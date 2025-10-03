# 📱 RAG Study Apps

Coleção de aplicativos e demos do projeto com RAG (Retrieval-Augmented Generation).

## 🚀 **Apps Disponíveis**

### 1. 🔍 **Code Review Demo** - `code-review-demo/`
> **Sistema de revisão automatizada de código**

**Status:** 🔄 Em desenvolvimento  
**Descrição:** Análise automatizada de código Python com detecção de problemas de segurança, performance e qualidade.

**Como usar:**
```bash
cd code-review-demo
python main.py example.py

# Análise recursiva
python main.py ../../src --recursive

# Foco em segurança
python main.py example.py --focus security
```

**Funcionalidades:**
- Detecção de vulnerabilidades de segurança
- Análise de performance
- Sugestões de melhorias arquiteturais
- Identificação de boas práticas

[📖 **Documentação completa**](code-review-demo/README.md)

---

### 2. 💬 **Interactive Chat** - `interactive-chat/`
> **Chat interativo inteligente com seu código**

**Status:** 🔄 Em desenvolvimento  
**Descrição:** Code assistente que conversa sobre seu código priorizando seus padrões. Perfeito para explorar projetos grandes.

**Como usar:**
```bash
cd interactive-chat
python main.py
```

**Comandos especiais:**
- `/help` - Mostra ajuda
- `/clear` - Limpa histórico
- `/exit` - Sai do chat
- `/model <nome>` - Troca o modelo

[📖 **Documentação completa**](interactive-chat/README.md)

---

### 3. 📊 **Code Analyzer** - `code-analyzer/`
> **Análise de dados e extração de insights**

**Status:** ✅ Completo [`NEW`]  
**Descrição:** Aplicação de análise de dados usando RAG para extrair insights e padrões do código.

**Como usar:**
```bash
cd code-analyzer

# Com indexação de código
python main.py --index-path ../../src --model llama3.2:1b

# Com arquivo de configuração
python main.py --config config.json
```

**Funcionalidades:**
- Análise estatística de código
- Extração de padrões
- Geração de relatórios
- Visualização de métricas (em desenvolvimento)

---

## 🔧 **Gerenciamento de Apps** [`NEW`]

### Criar Novo App (Método Rápido - Recomendado)
Use o gerador automático de apps:

```bash
# App básico
python ../scripts/create_app.py nome-do-app

# App de chat
python ../scripts/create_app.py chat-app --type chat --author "Seu Nome"

# App de análise
python ../scripts/create_app.py analyzer --type analysis

# API REST
python ../scripts/create_app.py api-server --type api
```

**Tipos disponíveis:**
- 🎯 **basic** - Template simples para qualquer propósito
- 💬 **chat** - Chat interativo com loop de conversação
- 📊 **analysis** - Análise de dados com RAG
- 🌐 **api** - API REST com endpoints RAG

### Listar Apps
```bash
# Lista simples
python ../scripts/list_apps.py

# Lista detalhada
python ../scripts/list_apps.py --detailed

# Filtrar por tipo
python ../scripts/list_apps.py --type chat
```

### Remover Apps
```bash
# Com confirmação
python ../scripts/remove_app.py nome-do-app

# Sem confirmação (cuidado!)
python ../scripts/remove_app.py nome-do-app --force
```

## 🔧 **Como Adicionar Novos Apps Manualmente**

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
