#!/usr/bin/env python3
"""
📊 Code Analyzer
================

Aplicação de análise de dados com RAG

Criado em: 2025-10-03
Autor: Leandro Leite
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Adiciona src ao path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.helpers.colored_output import ColoredOutput
from src.core.engine import create_rag_engine


class CodeAnalyzerApp:
    """Classe principal do Code Analyzer"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o Code Analyzer.

        Args:
            config: Configurações opcionais do app
        """
        self.config = config or {}
        self.engine = None
        self.is_initialized = False

        ColoredOutput.header("Code Analyzer")
        ColoredOutput.info(f"Versão: 1.0.0")
        ColoredOutput.info(f"Tipo: analysis")

    def setup(self) -> bool:
        """Configura o ambiente e inicializa o engine RAG"""
        try:
            ColoredOutput.info("Inicializando sistema RAG...")

            # Cria o engine RAG
            self.engine = create_rag_engine(
                loader_type=self.config.get("loader_type", "python"),
                vector_store_type=self.config.get("vector_store_type", "chroma"),
                llm_type=self.config.get("llm_type", "ollama"),
                llm_kwargs={"model_name": self.config.get("model_name", "llama3.2:1b")},
            )

            # Indexa dados se necessário
            if self.config.get("index_path"):
                stats = self.engine.setup_pipeline(
                    self.config["index_path"], self.config.get("glob_pattern", "**/*.py")
                )
                ColoredOutput.success(f"Indexados {stats['documents_loaded']} documentos")

            self.is_initialized = True
            ColoredOutput.success("Sistema inicializado com sucesso!")
            return True

        except Exception as e:
            ColoredOutput.error(f"Erro na inicialização: {e}")
            return False

    def run(self) -> int:
        """Executa a lógica principal do app"""
        if not self.is_initialized:
            if not self.setup():
                return 1

        try:
            ColoredOutput.section(
                "Executando Code Analyzer",
                "Este é um template básico. Customize este método para implementar sua lógica.",
            )

            # Análise de dados
            ColoredOutput.info("Iniciando análise...")

            # TODO: Implementar lógica de análise
            ColoredOutput.progress(50, 100, "Análise")

            ColoredOutput.section("Resultados", "Implemente aqui a lógica de análise específica")

            return 0

        except KeyboardInterrupt:
            ColoredOutput.warning("\nInterrompido pelo usuário")
            return 0
        except Exception as e:
            ColoredOutput.error(f"Erro durante execução: {e}")
            return 1

    def cleanup(self):
        """Limpa recursos antes de sair"""
        if self.engine:
            ColoredOutput.info("Limpando recursos...")
            # Adicione lógica de limpeza aqui se necessário

        ColoredOutput.success("Até logo! 👋")


def parse_arguments():
    """Processa argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description="Code Analyzer - Aplicação de análise de dados com RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--config", type=str, help="Arquivo de configuração JSON (opcional)")

    parser.add_argument("--index-path", type=str, help="Caminho para indexar documentos")

    parser.add_argument(
        "--model", type=str, default="llama3.2:1b", help="Modelo LLM a usar (default: llama3.2:1b)"
    )

    parser.add_argument("--verbose", action="store_true", help="Modo verboso")

    return parser.parse_args()


def load_config(args) -> Dict[str, Any]:
    """Carrega configuração dos argumentos ou arquivo"""
    config = {}

    # Se um arquivo de config foi especificado
    if args.config:
        import json

        try:
            with open(args.config, "r") as f:
                config = json.load(f)
            ColoredOutput.success(f"Configuração carregada de {args.config}")
        except Exception as e:
            ColoredOutput.warning(f"Erro ao carregar config: {e}")

    # Sobrescreve com argumentos da linha de comando
    if args.index_path:
        config["index_path"] = args.index_path
    if args.model:
        config["model_name"] = args.model
    config["verbose"] = args.verbose

    return config


def main():
    """Função principal"""
    args = parse_arguments()
    config = load_config(args)

    app = CodeAnalyzerApp(config)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
