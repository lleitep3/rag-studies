"""
Testes para Code Review Capacity
=================================

Testa a capacidade de revisão de código.
"""

import pytest
import re
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.capacities.code_review.reviewer import (
    CodeReviewCapacity,
    CodeIssue,
    CodeSuggestion,
    CodeReviewResult
)
from src.capacities.base import CapacityResponse


class TestCodeReviewDataClasses:
    """Testa as dataclasses do módulo"""
    
    @pytest.mark.unit
    def test_code_issue_creation(self):
        """Testa criação de CodeIssue"""
        issue = CodeIssue(
            category="Security",
            description="Password stored in plain text",
            line_number=42,
            severity="high"
        )
        
        assert issue.category == "Security"
        assert issue.description == "Password stored in plain text"
        assert issue.line_number == 42
        assert issue.severity == "high"
    
    @pytest.mark.unit
    def test_code_suggestion_creation(self):
        """Testa criação de CodeSuggestion"""
        suggestion = CodeSuggestion(
            category="Performance",
            description="Use list comprehension",
            line_number=10,
            impact="medium"
        )
        
        assert suggestion.category == "Performance"
        assert suggestion.description == "Use list comprehension"
        assert suggestion.line_number == 10
        assert suggestion.impact == "medium"
    
    @pytest.mark.unit
    def test_code_review_result_creation(self):
        """Testa criação de CodeReviewResult"""
        issues = [CodeIssue("Test", "Issue 1")]
        suggestions = [CodeSuggestion("Test", "Suggestion 1")]
        positives = ["Good naming", "Clean structure"]
        summary = "Overall good code"
        
        result = CodeReviewResult(
            issues=issues,
            suggestions=suggestions,
            positives=positives,
            summary=summary
        )
        
        assert len(result.issues) == 1
        assert len(result.suggestions) == 1
        assert len(result.positives) == 2
        assert result.summary == "Overall good code"


class TestCodeReviewCapacity:
    """Testa a classe CodeReviewCapacity"""
    
    @pytest.fixture
    def mock_rag_engine(self):
        """Mock do RAGEngine"""
        engine = Mock()
        engine.ask.return_value = {
            "answer": "Review response",
            "context": "Project context",
            "status": "success"
        }
        return engine
    
    @pytest.mark.unit
    def test_init(self, mock_rag_engine):
        """Testa inicialização"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        assert capacity.rag_engine == mock_rag_engine
        assert capacity.focus_areas == ["general"]
    
    @pytest.mark.unit
    def test_init_with_focus_areas(self, mock_rag_engine):
        """Testa inicialização com focus areas"""
        capacity = CodeReviewCapacity(
            mock_rag_engine,
            focus_areas=["security", "performance"]
        )
        
        assert capacity.focus_areas == ["security", "performance"]
    
    @pytest.mark.unit
    def test_get_prompt_template_general(self, mock_rag_engine):
        """Testa seleção de prompt geral"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        prompt = capacity.get_prompt_template()
        assert "Você é um revisor de código especializado" in prompt
    
    @pytest.mark.unit
    def test_get_prompt_template_security(self, mock_rag_engine):
        """Testa seleção de prompt de segurança"""
        capacity = CodeReviewCapacity(
            mock_rag_engine,
            focus_areas=["security"]
        )
        
        prompt = capacity.get_prompt_template()
        assert "especialista em segurança" in prompt
    
    @pytest.mark.unit
    def test_get_prompt_template_performance(self, mock_rag_engine):
        """Testa seleção de prompt de performance"""
        capacity = CodeReviewCapacity(
            mock_rag_engine,
            focus_areas=["performance"]
        )
        
        prompt = capacity.get_prompt_template()
        assert "otimização de código" in prompt
    
    @pytest.mark.unit
    def test_prepare_context(self, mock_rag_engine):
        """Testa preparação de contexto"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        code = "def test(): pass"
        context = capacity.prepare_context(code, file_path="test.py")
        
        assert context["code"] == code
        assert context["file_path"] == "test.py"
        assert "project_context" in context
        
        # Verifica que ask foi chamado
        mock_rag_engine.ask.assert_called_once()
    
    @pytest.mark.unit
    def test_prepare_context_no_index(self, mock_rag_engine):
        """Testa preparação de contexto quando não há índice"""
        mock_rag_engine.ask.side_effect = Exception("Not indexed")
        
        capacity = CodeReviewCapacity(mock_rag_engine)
        context = capacity.prepare_context("code")
        
        assert context["project_context"] == ""
    
    @pytest.mark.unit
    def test_parse_issues(self, mock_rag_engine, sample_review_response):
        """Testa parsing de issues"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        issues = capacity._parse_issues(sample_review_response)
        
        assert len(issues) == 3
        assert issues[0].category == "Segurança"
        assert "senha em texto plano" in issues[0].description
        assert issues[0].line_number == 11
        assert issues[0].severity == "high"
    
    @pytest.mark.unit
    def test_parse_suggestions(self, mock_rag_engine, sample_review_response):
        """Testa parsing de sugestões"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        suggestions = capacity._parse_suggestions(sample_review_response)
        
        assert len(suggestions) == 3
        assert suggestions[0].category == "Segurança"
        assert "hash bcrypt" in suggestions[0].description
        assert suggestions[0].line_number == 11
    
    @pytest.mark.unit
    def test_parse_positives(self, mock_rag_engine, sample_review_response):
        """Testa parsing de pontos positivos"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        positives = capacity._parse_positives(sample_review_response)
        
        assert len(positives) == 3
        assert "Estrutura de classe bem organizada" in positives
        assert "Nomes de variáveis descritivos" in positives
    
    @pytest.mark.unit
    def test_parse_summary(self, mock_rag_engine, sample_review_response):
        """Testa parsing de resumo"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        summary = capacity._parse_summary(sample_review_response)
        
        assert "problemas críticos de segurança" in summary
        assert "senhas em texto plano" in summary
    
    @pytest.mark.unit
    def test_process_response_success(self, mock_rag_engine, sample_review_response):
        """Testa processamento completo da resposta"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        response = capacity.process_response(sample_review_response)
        
        assert response.success is True
        assert "review" in response.data
        
        review = response.data["review"]
        assert isinstance(review, CodeReviewResult)
        assert len(review.issues) == 3
        assert len(review.suggestions) == 3
        assert len(review.positives) == 3
        assert review.summary != ""
    
    @pytest.mark.unit
    def test_process_response_error(self, mock_rag_engine):
        """Testa processamento com erro"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        # Força um erro no parsing
        with patch.object(capacity, '_parse_issues', side_effect=Exception("Parse error")):
            response = capacity.process_response("Invalid response")
        
        assert response.success is False
        assert len(response.errors) == 1
        assert "Parse error" in response.errors[0]
    
    @pytest.mark.unit
    def test_parse_issues_empty(self, mock_rag_engine):
        """Testa parsing quando não há issues"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        response = "RESUMO: Código perfeito sem problemas."
        issues = capacity._parse_issues(response)
        
        assert issues == []
    
    @pytest.mark.unit
    def test_parse_different_formats(self, mock_rag_engine):
        """Testa parsing com diferentes formatos de resposta"""
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        # Formato com asterisco
        response = """
        PROBLEMAS ENCONTRADOS:
        * Segurança: SQL injection vulnerability (L45)
        * Performance: N+1 query problem (L120)
        """
        
        issues = capacity._parse_issues(response)
        assert len(issues) >= 1
        
        # Formato sem número de linha
        response = """
        SUGESTÕES DE MELHORIA:
        - [Documentação] Adicione docstrings às funções
        - [Testes] Implemente testes unitários
        """
        
        suggestions = capacity._parse_suggestions(response)
        assert len(suggestions) >= 1
        assert suggestions[0].line_number is None


class TestIntegration:
    """Testes de integração"""
    
    @pytest.fixture
    def mock_rag_engine(self):
        """Mock do RAGEngine para testes de integração"""
        engine = Mock()
        engine.ask.return_value = {
            "answer": "Review response",
            "context": "Project context",
            "status": "success"
        }
        return engine
    
    @pytest.mark.integration
    def test_full_review_flow(self, mock_rag_engine, sample_code):
        """Testa fluxo completo de review"""
        # Configura mock para retornar uma resposta completa
        mock_rag_engine.ask.return_value = {
            "answer": """
            PROBLEMAS ENCONTRADOS:
            - [Segurança] Senha armazenada em texto plano (linha 11)
            
            SUGESTÕES DE MELHORIA:
            - [Segurança] Use bcrypt para hash de senhas (linha 11)
            
            PONTOS POSITIVOS:
            - Código bem estruturado
            
            RESUMO:
            Código com problemas de segurança que precisam ser corrigidos.
            """,
            "context": "Security best practices",
            "status": "success"
        }
        
        capacity = CodeReviewCapacity(mock_rag_engine)
        
        # Executa review através do método execute (se existir)
        # ou simula o fluxo completo
        context = capacity.prepare_context(sample_code)
        
        # Simula resposta do LLM
        llm_response = mock_rag_engine.ask.return_value["answer"]
        
        # Processa resposta
        result = capacity.process_response(llm_response)
        
        assert result.success is True
        assert len(result.data["review"].issues) > 0
        assert len(result.data["review"].suggestions) > 0
        assert len(result.data["review"].positives) > 0