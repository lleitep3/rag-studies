# Documentação do RAG Code Assistant

## 📚 Visão Geral

Esta documentação está organizada por tópicos para facilitar a navegação:

## 🧠 **Conceitos Fundamentais**
- **[RAG Concepts](rag-concepts.md)** - O que é RAG, como funciona, analogias e fundamentos teóricos

## 🏗️ **Arquitetura Técnica** 
- **[Architecture](architecture.md)** - Design do sistema, componentes, padrões de software e fluxos de dados

## 🎯 **Para Desenvolvedores**

### Entendendo o Sistema
1. Comece com [RAG Concepts](rag-concepts.md) se você é novo em RAG
2. Consulte [Architecture](architecture.md) para entender a implementação
3. Veja o código principal em `../src/`

### Expandindo o Sistema
- **Novo Loader**: Herde de `BaseLoader`, implemente `load()`
- **Novo LLM**: Herde de `BaseLLM`, implemente `ask()`
- **Novo Vector Store**: Herde de `BaseVectorStore`

### Estrutura de Arquivos
```
docs/
├── README.md          # Este arquivo (índice)
├── rag-concepts.md    # Conceitos e teoria RAG
└── architecture.md    # Arquitetura e implementação

src/                   # Código principal
├── loaders/           # Carregadores de documentos
├── llms/             # Modelos de linguagem
├── vector_stores/    # Armazenamento vetorial
└── core/             # RAG Engine
```

## 🤝 **Contribuições**

Sinta-se à vontade para:
- Melhorar a documentação
- Adicionar novos componentes
- Reportar bugs
- Sugerir melhorias

---

**💡 Dica**: Comece pela [demo interativa](../demo.py) para ver o sistema funcionando!