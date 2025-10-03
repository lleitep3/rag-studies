"""
Formatação colorida para output do Code Review
"""

from typing import List, Union
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from src.capacities.code_review.reviewer import (
    CodeReviewResult,
    CodeIssue,
    CodeSuggestion,
)

console = Console()


def print_code_with_highlights(
    code: str, issues: List[CodeIssue], suggestions: List[CodeSuggestion]
):
    """Mostra o código com highlights nas linhas com issues/sugestões"""
    syntax = Syntax(code, "python", line_numbers=True)
    console.print(Panel(syntax, title="📝 Código Analisado"))


def print_review_section(
    title: str, items: List[Union[CodeIssue, CodeSuggestion]], style: str
):
    """Imprime uma seção do review em formato de tabela"""
    if not items:
        return

    table = Table(title=title, style=style)
    table.add_column("Linha", style="cyan")
    table.add_column("Categoria", style="yellow")
    table.add_column("Descrição", style="white")

    for item in items:
        line = str(item.line_number) if item.line_number else "-"
        table.add_row(line, item.category, item.description)

    console.print(table)
    console.print()


def print_review_result(result: CodeReviewResult):
    """Imprime o resultado completo do code review"""
    # Cabeçalho
    console.print(Panel("🔍 Resultado da Análise", style="bold blue"))
    console.print()

    # Issues
    print_review_section("⚠️ Problemas Encontrados", result.issues, "red")

    # Sugestões
    print_review_section("💡 Sugestões de Melhoria", result.suggestions, "green")

    # Pontos Positivos
    if result.positives:
        console.print("✅ Pontos Positivos:", style="bold green")
        for positive in result.positives:
            console.print(f"  • {positive}")
        console.print()

    # Resumo
    if result.summary:
        console.print(
            Panel(result.summary, title="📊 Resumo da Análise", style="bold blue")
        )


def print_error(message: str):
    """Imprime mensagem de erro"""
    console.print(f"❌ Erro: {message}", style="bold red")
