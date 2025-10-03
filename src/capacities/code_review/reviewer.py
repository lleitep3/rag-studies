"""Capacidade de Code Review
========================

Implementa a capacidade de análise e revisão de código usando RAG.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..base import BaseCapacity, CapacityResponse
from . import prompts


@dataclass
class CodeIssue:
    """Representa um problema encontrado no código"""

    category: str
    description: str
    line_number: Optional[int] = None
    severity: str = "medium"


@dataclass
class CodeSuggestion:
    """Representa uma sugestão de melhoria"""

    category: str
    description: str
    line_number: Optional[int] = None
    impact: str = "medium"


@dataclass
class CodeReviewResult:
    """Resultado completo da revisão de código"""

    issues: List[CodeIssue]
    suggestions: List[CodeSuggestion]
    positives: List[str]
    summary: str


class CodeReviewCapacity(BaseCapacity):
    """
    Capacidade de revisão de código que usa RAG para:
    1. Entender o contexto do projeto
    2. Analisar código fonte
    3. Gerar revisões detalhadas
    """

    def __init__(self, rag_engine, focus_areas: Optional[List[str]] = None):
        """
        Inicializa a capacidade de code review.

        Args:
            rag_engine: Motor RAG para busca e geração
            focus_areas: Lista de áreas específicas para focar (security, performance, etc)
        """
        super().__init__(rag_engine)
        self.rag_engine = rag_engine  # Mantém referência adicional para compatibilidade
        self.focus_areas = focus_areas or ["general"]

    def get_prompt_template(self) -> str:
        """Seleciona o prompt apropriado baseado nas áreas de foco"""
        if "security" in self.focus_areas:
            return prompts.SECURITY_FOCUSED_PROMPT
        elif "performance" in self.focus_areas:
            return prompts.PERFORMANCE_FOCUSED_PROMPT
        return prompts.MAIN_REVIEW_PROMPT

    def prepare_context(self, code: str, **kwargs) -> Dict[str, Any]:
        """
        Prepara o contexto para a revisão.

        Args:
            code: Código fonte a ser revisado
            **kwargs: Contexto adicional

        Returns:
            Dict com contexto preparado
        """
        # Busca informações do projeto usando ask ao invés de search
        try:
            result = self.rag.ask(
                "What are the project architecture guidelines, coding standards and best practices?",
                include_sources=True,
                retriever_kwargs={"k": 3}
            )
            project_context = result.get("context", "")
        except:
            # Se não houver contexto indexado, usa string vazia
            project_context = ""

        return {"code": code, "project_context": project_context, **kwargs}

    def _parse_issues(self, text: str) -> List[CodeIssue]:
        """Extrai issues do texto da resposta"""
        issues = []
        
        # Busca pela seção de problemas
        problems_section = re.search(
            r"PROBLEMAS ENCONTRADOS:(.+?)(?:SUGESTÕES|PONTOS|RESUMO|$)",
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if problems_section:
            problems_text = problems_section.group(1)
            
            # Padrões para capturar issues
            patterns = [
                r"- \[([^\]]+)\] ([^(\n]+)(?:\(linha (\d+)\))?",  # - [Category] Description (linha X)
                r"- ([A-Z][\w\s]+): ([^(\n]+)(?:\(linha (\d+)\))?",  # - Category: Description (linha X)
                r"\* ([A-Z][\w\s]+): ([^(\n]+)(?:\(L(\d+)\))?",     # * Category: Description (L123)
            ]
            
            for pattern in patterns:
                for match in re.finditer(pattern, problems_text):
                    category = match.group(1).strip()
                    description = match.group(2).strip()
                    line_num = int(match.group(3)) if match.group(3) else None
                    
                    # Determina severidade baseado em palavras-chave
                    severity = "high" if any(word in description.lower() 
                                            for word in ["crítico", "segurança", "vulnerável", "eval", "sql", "senha", "password", "token", "secret"]) \
                              else "medium"
                    
                    issues.append(CodeIssue(
                        category=category,
                        description=description,
                        line_number=line_num,
                        severity=severity
                    ))
        
        return issues

    def _parse_suggestions(self, text: str) -> List[CodeSuggestion]:
        """Extrai sugestões do texto da resposta"""
        suggestions = []
        
        # Busca pela seção de sugestões
        suggestions_section = re.search(
            r"SUGESTÕES DE MELHORIA:(.+?)(?:PONTOS|RESUMO|$)",
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if suggestions_section:
            suggestions_text = suggestions_section.group(1)
            
            # Padrões para capturar sugestões
            patterns = [
                r"- \[([^\]]+)\] ([^(\n]+)(?:\(linha (\d+)\))?",  # - [Category] Suggestion (linha X)
                r"- ([A-Z][\w\s]+): ([^(\n]+)(?:\(linha (\d+)\))?",  # - Category: Suggestion (linha X)
                r"\* ([A-Z][\w\s]+): ([^(\n]+)(?:\(L(\d+)\))?",     # * Category: Suggestion (L123)
            ]
            
            for pattern in patterns:
                for match in re.finditer(pattern, suggestions_text):
                    category = match.group(1).strip()
                    description = match.group(2).strip()
                    line_num = int(match.group(3)) if match.group(3) else None
                    
                    # Determina impacto baseado em palavras-chave
                    impact = "high" if any(word in description.lower() 
                                          for word in ["performance", "segurança", "arquitetura", "crítico"]) \
                            else "medium"
                    
                    suggestions.append(CodeSuggestion(
                        category=category,
                        description=description,
                        line_number=line_num,
                        impact=impact
                    ))
        
        return suggestions

    def _parse_positives(self, text: str) -> List[str]:
        """Extrai pontos positivos do texto da resposta"""
        positives = []
        
        # Busca pela seção de pontos positivos
        positives_section = re.search(
            r"PONTOS POSITIVOS:(.+?)(?:RESUMO|$)",
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if positives_section:
            positives_text = positives_section.group(1)
            
            # Captura cada ponto positivo
            for line in positives_text.split('\n'):
                line = line.strip()
                if line and line.startswith(('-', '*', '•')):
                    # Remove o marcador e limpa o texto
                    positive = re.sub(r'^[-*•]\s*(?:\[[^\]]+\]\s*)?', '', line).strip()
                    if positive:
                        positives.append(positive)
        
        return positives
    
    def _parse_summary(self, text: str) -> str:
        """Extrai o resumo do texto da resposta"""
        # Busca pela seção de resumo
        summary_section = re.search(
            r"RESUMO:(.+?)$",
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if summary_section:
            summary = summary_section.group(1).strip()
            # Remove quebras de linha excessivas
            summary = ' '.join(summary.split())
            return summary
        
        return "Análise de código concluída."

    def process_response(self, response: str) -> CapacityResponse:
        """
        Processa a resposta do LLM e estrutura o resultado.

        Args:
            response: Texto da resposta do LLM

        Returns:
            CapacityResponse com resultados estruturados
        """
        try:
            # Parse das seções
            issues = self._parse_issues(response)
            suggestions = self._parse_suggestions(response)
            positives = self._parse_positives(response)
            summary = self._parse_summary(response)

            result = CodeReviewResult(
                issues=issues,
                suggestions=suggestions,
                positives=positives,
                summary=summary,
            )

            return CapacityResponse(success=True, data={"review": result})

        except Exception as e:
            return CapacityResponse(
                success=False, data={}, errors=[f"Erro ao processar resposta: {str(e)}"]
            )
