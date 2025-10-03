# 🔍 Code Review Demo

Uma demonstração da capacidade de Code Review usando RAG (Retrieval-Augmented Generation) para análise inteligente de código Python.

## 🎯 **O que faz?**

- **Analisa código Python** em tempo real
- **Identifica problemas** de qualidade, segurança e performance
- **Sugere melhorias** baseadas em boas práticas
- **Destaca pontos positivos** do código
- **Interface colorida** com highlighting de código
- **Múltiplos focos** de análise (geral, segurança, performance)

## 🚀 **Como usar**

### Início Rápido
```bash
# Navegue para a pasta do app
cd apps/code-review-demo

# Instale dependências
pip install -r requirements.txt

# Analise o arquivo de exemplo
python main.py example.py

# Ou analise com foco em segurança
python main.py example.py --focus security
```

### Opções Avançadas
```bash
# Analisar diretório completo
python main.py ../../src

# Busca recursiva com padrão específico
python main.py ../../src --recursive --pattern "*.py"

# Múltiplos focos de análise
python main.py example.py --focus security,performance
```

### Argumentos Disponíveis
- `path`: Arquivo ou diretório para analisar
- `--focus, -f`: Áreas de foco (general, security, performance)
- `--recursive, -r`: Procura arquivos recursivamente
- `--pattern, -p`: Padrão para filtrar arquivos (default: *.py)

## 💡 **Exemplos de Análise**

A demo inclui um arquivo `example.py` com problemas comuns para testar:

1. **Problemas de Qualidade**
   - Falta de type hints
   - Documentação inadequada
   - Nomes pouco descritivos

2. **Problemas de Segurança**
   - Uso de `eval()` sem validação
   - Senhas em texto plano
   - Comparações inseguras

3. **Problemas de Performance**
   - Estruturas de dados ineficientes
   - Operações redundantes
   - Gargalos potenciais

## 🔧 **Pré-requisitos**

### Obrigatórios
- **Python 3.8+**
- **Ollama** instalado e rodando
  ```bash
  # Instalar Ollama
  curl -fsSL https://ollama.ai/install.sh | sh

  # Baixar modelo
  ollama pull llama3.2:1b

  # Iniciar servidor
  ollama serve
  ```

### Dependências Python
```bash
pip install -r requirements.txt
```

## 📁 **Estrutura do App**

```
code-review-demo/
├── main.py              # 🎯 Script principal
├── output_formatter.py  # 🎨 Formatação colorida
├── example.py          # 📝 Código de exemplo
├── requirements.txt    # 📦 Dependências
└── README.md          # 📖 Esta documentação
```

## 🏗️ **Arquitetura**

### Fluxo da Análise
1. **Leitura**: Carrega arquivo(s) Python
2. **Contexto**: Busca informações relevantes do projeto
3. **Análise**: Aplica prompts especializados via RAG
4. **Processamento**: Estrutura resultados
5. **Visualização**: Apresenta análise formatada

### Capacidades de Análise

1. **Análise Geral**
   - Qualidade do código
   - Boas práticas Python
   - Arquitetura e design
   - Performance básica
   - Segurança básica

2. **Análise de Segurança**
   - Vulnerabilidades
   - Riscos de segurança
   - Conformidade OWASP
   - Melhores práticas

3. **Análise de Performance**
   - Complexidade (Big O)
   - Uso de recursos
   - Otimizações
   - Impacto estimado

## 🎨 **Output**

A análise é apresentada em um formato rico e colorido:
- **Código** com syntax highlighting
- **Problemas** em tabela organizada
- **Sugestões** categorizadas
- **Pontos positivos** destacados
- **Resumo** geral da análise

## 🤝 **Contribuindo**

Este é um projeto de estudos! Sinta-se à vontade para:
- Adicionar novas áreas de análise
- Melhorar os prompts existentes
- Implementar parsers mais robustos
- Adicionar novas visualizações
- Sugerir melhorias

---

💡 **Dica**: Comece analisando o arquivo `example.py` para ver todos os tipos de feedback que o revisor pode fornecer!