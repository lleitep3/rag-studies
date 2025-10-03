# 📊 Code Analyzer

> **Aplicação RAG do tipo analysis**

## 📋 Sobre

Este app foi gerado automaticamente em 2025-10-03 usando o RAG App Generator.
É um template do tipo **analysis** pronto para ser customizado.

## 🚀 Como Usar

### Instalação
```bash
# Navegue para a pasta do app
cd apps/code-analyzer

# Instale as dependências (se necessário)
pip install -r requirements.txt
```

### Execução Básica
```bash
python main.py
```

### Com Parâmetros
```bash
# Indexar documentos
python main.py --index-path ../../src --model llama3.2:1b

# Modo verboso
python main.py --verbose

# Com arquivo de configuração
python main.py --config config.json
```

## ⚙️ Configuração

Crie um arquivo `config.json` (opcional):
```json
{
    "loader_type": "python",
    "vector_store_type": "chroma",
    "llm_type": "ollama",
    "model_name": "llama3.2:1b",
    "index_path": "../../src",
    "glob_pattern": "**/*.py",
    "verbose": true
}
```

## 🏗️ Estrutura

```
code-analyzer/
├── main.py              # Script principal
├── README.md           # Esta documentação
├── requirements.txt    # Dependências Python
└── config.json        # Configuração (opcional)
```

## 🎯 Funcionalidades

- ✅ Análise de documentos
- ✅ Extração de insights
- ✅ Relatórios formatados
- 🔄 Visualizações (TODO)
- 🔄 Export para PDF/HTML (TODO)

## 🔧 Customização

Para customizar este app:

1. **Modifique `main.py`**:
   - Método `run()` - Implementar lógica principal
   - Método `setup()` - Configurar inicialização
   - Adicionar novos métodos conforme necessário

2. **Adicione novos módulos**:
   - Crie arquivos Python adicionais
   - Importe no `main.py`

3. **Atualize dependências**:
   - Adicione pacotes necessários em `requirements.txt`

## 📝 TODO

- [ ] Implementar lógica específica do app
- [ ] Adicionar tratamento de erros robusto
- [ ] Criar testes unitários
- [ ] Adicionar logging
- [ ] Documentar APIs/interfaces

## 🤝 Contribuindo

Para contribuir com este app:
1. Implemente as funcionalidades pendentes
2. Adicione testes
3. Atualize a documentação
4. Faça um PR

## 📄 Licença

Parte do projeto RAG Study - Leandro Leite

---

**Criado em:** 2025-10-03
**Tipo:** analysis
**Versão:** 1.0.0
