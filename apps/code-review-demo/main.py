#!/usr/bin/env python3
"""
Demo de Code Review
==================

Demonstração da capacidade de Code Review do sistema RAG.
"""

import sys
import os
from pathlib import Path
import argparse
from typing import List, Optional

# Adiciona src ao path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.core.engine import create_rag_engine
from src.capacities.code_review import CodeReviewCapacity
from output_formatter import (
    print_review_result,
    print_error,
    print_code_with_highlights,
)


def parse_arguments():
    """Processa argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Code Review Demo - Análise de código Python com RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("path", help="Arquivo ou diretório para analisar")

    parser.add_argument(
        "--focus",
        "-f",
        help="Áreas de foco separadas por vírgula (ex: security,performance)",
        default="general",
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Procura arquivos recursivamente em subdiretórios",
    )

    parser.add_argument(
        "--pattern",
        "-p",
        default="*.py",
        help="Padrão para filtrar arquivos (default: *.py)",
    )

    return parser.parse_args()


def find_python_files(
    start_path: str, pattern: str = "*.py", recursive: bool = False
) -> List[Path]:
    """Encontra arquivos Python no caminho especificado"""
    path = Path(start_path)

    if path.is_file():
        return [path] if path.match(pattern) else []

    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))


def review_file(
    reviewer: CodeReviewCapacity,
    file_path: Path,
    focus_areas: Optional[List[str]] = None,
):
    """Analisa um arquivo específico"""
    try:
        # Lê o arquivo
        code = file_path.read_text()

        # Mostra cabeçalho
        print("\n" + "=" * 80)
        print(f"📝 Analisando: {file_path}")
        print("=" * 80 + "\n")

        # Executa review
        result = reviewer.execute(
            code=code, file_path=str(file_path), focus_areas=focus_areas
        )

        if result.success:
            # Mostra código com highlights
            print_code_with_highlights(
                code, result.data["review"].issues, result.data["review"].suggestions
            )

            # Mostra resultados
            print_review_result(result.data["review"])

        else:
            print_error(result.errors[0])

    except Exception as e:
        print_error(f"Erro ao analisar {file_path}: {str(e)}")


def main():
    """Função principal"""
    try:
        # Parse argumentos
        args = parse_arguments()

        # Prepara áreas de foco
        focus_areas = [area.strip() for area in args.focus.split(",")]

        # Cria engine RAG
        engine = create_rag_engine(
            loader_type="python", llm_type="ollama", vector_store_type="chroma"
        )

        if not engine:
            print_error("Falha ao criar o motor RAG")
            return 1

        print("✅ Motor RAG criado com sucesso")
        print(f"Áreas de foco: {focus_areas}")

        # Cria revisor
        reviewer = CodeReviewCapacity(engine, focus_areas=focus_areas)

        # Encontra arquivos
        files = find_python_files(
            args.path, pattern=args.pattern, recursive=args.recursive
        )

        if not files:
            print_error(f"Nenhum arquivo Python encontrado em: {args.path}")
            return 1

        # Analisa cada arquivo
        for file_path in files:
            review_file(reviewer, file_path, focus_areas)

        return 0

    except KeyboardInterrupt:
        print("\nRevisão interrompida pelo usuário")
        return 0

    except Exception as e:
        print_error(f"Erro fatal: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
