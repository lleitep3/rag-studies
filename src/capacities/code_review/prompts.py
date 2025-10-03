"""
Prompts para Code Review
=======================

Define os templates de prompts utilizados na capacidade de Code Review.
"""

MAIN_REVIEW_PROMPT = """
Você é um revisor de código especializado em Python. Analise o código a seguir considerando:

CONTEXTO DO PROJETO:
{project_context}

CÓDIGO PARA REVISAR:
{code}

ASPECTOS A CONSIDERAR:
1. Qualidade e Legibilidade
   - Clareza do código
   - Nomes de variáveis/funções
   - Documentação e comentários
   - Complexidade e simplicidade

2. Boas Práticas Python
   - PEP 8
   - Pythonic code
   - Type hints
   - Docstrings

3. Arquitetura e Design
   - Princípios SOLID
   - Padrões de projeto
   - Modularidade
   - Acoplamento e coesão

4. Performance
   - Complexidade algorítmica
   - Uso de memória
   - Otimizações possíveis

5. Segurança
   - Validações de entrada
   - Tratamento de erros
   - Vulnerabilidades comuns

Por favor, forneça sua análise no seguinte formato:

PROBLEMAS ENCONTRADOS:
- [Categoria] Descrição do problema (linha X)
- ...

SUGESTÕES DE MELHORIA:
- [Categoria] Sugestão específica (linha X)
- ...

PONTOS POSITIVOS:
- [Categoria] Aspecto positivo encontrado
- ...

RESUMO:
Breve resumo da qualidade geral do código e principais pontos de atenção.
"""

SECURITY_FOCUSED_PROMPT = """
Você é um especialista em segurança de código Python. Analise o seguinte código focando especificamente em aspectos de segurança:

CÓDIGO:
{code}

Por favor, identifique:

1. Vulnerabilidades
   - Injeção de código
   - Vazamento de dados
   - Práticas inseguras

2. Riscos de Segurança
   - Permissões
   - Validações
   - Criptografia

3. Conformidade
   - OWASP Top 10
   - Boas práticas de segurança
   - Requisitos regulatórios

Forneça sua análise no formato:

VULNERABILIDADES CRÍTICAS:
- ...

RISCOS MODERADOS:
- ...

SUGESTÕES DE CORREÇÃO:
- ...
"""

PERFORMANCE_FOCUSED_PROMPT = """
Você é um especialista em otimização de código Python. Analise o seguinte código focando em performance:

CÓDIGO:
{code}

CONTEXTO DE USO:
{usage_context}

Por favor, analise:

1. Complexidade
   - Big O notation
   - Gargalos potenciais

2. Uso de Recursos
   - Memória
   - CPU
   - I/O

3. Otimizações
   - Algoritmos
   - Estruturas de dados
   - Caching

Forneça sua análise no formato:

MÉTRICAS DE COMPLEXIDADE:
- ...

GARGALOS IDENTIFICADOS:
- ...

SUGESTÕES DE OTIMIZAÇÃO:
- ...

IMPACTO ESTIMADO:
- ...
"""
