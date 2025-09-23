#!/usr/bin/env python3
"""
🤖 Interactive RAG Chat - Main Application
==========================================

Aplicativo principal do chat interativo com o Code Assistant RAG.
Coordena todos os módulos e fornece uma experiência completa de chat.
"""

import sys
import os
from pathlib import Path
import argparse

# Adiciona módulos locais ao path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from colored_output import ColoredOutput
from code_assistant import CodeAssistant
from chat_interface import ChatInterface


def parse_arguments():
    """Processa argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description="RAG Code Assistant - Chat Interativo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                          # Configuração padrão
  python main.py --llm ollama             # Força uso do Ollama
  python main.py --model llama3.2:3b      # Usa modelo específico
  python main.py --path ../other-project  # Carrega código de outro projeto
  python main.py --pattern "**/*.py"      # Padrão personalizado de arquivos

Modelos disponíveis (Ollama):
  - llama3.2:1b (rápido, menor qualidade)
  - llama3.2:3b (balanceado)
  - gemma2:2b (alternativa Google)
        """,
    )

    parser.add_argument(
        "--path",
        "-p",
        default="../../src",
        help="Caminho para o código fonte (default: ../../src)",
    )

    parser.add_argument(
        "--pattern",
        "-f",
        default="**/*.py",
        help="Padrão de arquivos a carregar (default: **/*.py)",
    )

    parser.add_argument(
        "--llm",
        "-l",
        choices=["ollama", "gemini"],
        default="ollama",
        help="Tipo de LLM a usar (default: ollama)",
    )

    parser.add_argument(
        "--model",
        "-m",
        default="llama3.2:1b",
        help="Nome do modelo LLM (default: llama3.2:1b)",
    )

    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.1,
        help="Temperatura para geração de texto (default: 0.1)",
    )

    parser.add_argument(
        "--max-docs",
        "-d",
        type=int,
        default=3,
        help="Máximo de documentos para contexto (default: 3)",
    )

    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Modo silencioso (menos output)"
    )

    return parser.parse_args()


def check_requirements(args):
    """Verifica se os pré-requisitos estão atendidos"""
    issues = []

    # Verifica se o caminho do código existe
    code_path = Path(args.path)
    if not code_path.exists():
        issues.append(f"Caminho do código não existe: {code_path}")
    elif not code_path.is_dir():
        issues.append(f"Caminho não é um diretório: {code_path}")

    # Verifica se Ollama está disponível (se necessário)
    if args.llm == "ollama":
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                issues.append("Ollama não está rodando ou não está acessível")
        except Exception:
            issues.append("Não foi possível verificar o status do Ollama")

    # Verifica se modelo Gemini está configurado (se necessário)
    if args.llm == "gemini":
        if not os.getenv("GOOGLE_API_KEY"):
            issues.append("GOOGLE_API_KEY não está configurada para usar Gemini")

    return issues


def show_welcome_message(args):
    """Mostra mensagem de boas-vindas"""
    print("\n" + "🤖" + "=" * 60 + "🤖")
    ColoredOutput.print_colored(
        "   RAG CODE ASSISTANT - Chat Interativo", ColoredOutput.CYAN, bold=True
    )
    print("🤖" + "=" * 60 + "🤖")

    if not args.quiet:
        ColoredOutput.info("⚙️ Configurações:")
        print(f"   • Código fonte: {args.path}")
        print(f"   • Padrão de arquivos: {args.pattern}")
        print(f"   • LLM: {args.llm}")
        print(f"   • Modelo: {args.model}")
        print(f"   • Temperatura: {args.temperature}")
        print(f"   • Max documentos por consulta: {args.max_docs}")


def main():
    """Função principal"""
    try:
        # Parse argumentos
        args = parse_arguments()

        # Mostra mensagem de boas-vindas
        show_welcome_message(args)

        # Verifica pré-requisitos
        if not args.quiet:
            ColoredOutput.info("🔍 Verificando pré-requisitos...")

        issues = check_requirements(args)
        if issues:
            ColoredOutput.error("❌ Problemas encontrados:")
            for issue in issues:
                print(f"   • {issue}")

            ColoredOutput.info("\n💡 Possíveis soluções:")
            if any("Ollama" in issue for issue in issues):
                print("   • Inicie o Ollama: ollama serve")
                print("   • Verifique se o modelo está instalado: ollama list")
            if any("GOOGLE_API_KEY" in issue for issue in issues):
                print("   • Configure sua chave: export GOOGLE_API_KEY=sua_chave")
                print("   • Ou use arquivo .env com GOOGLE_API_KEY=sua_chave")
            if any("Caminho" in issue for issue in issues):
                print(f"   • Verifique se {args.path} existe e contém arquivos Python")
                print("   • Ou especifique outro caminho com --path")

            return 1

        # Cria e configura assistente
        assistant = CodeAssistant(
            loader_type="python",
            llm_type=args.llm,
            llm_model=args.model,
            llm_temperature=args.temperature,
        )

        # Configura sistema
        if not assistant.setup(args.path, args.pattern):
            ColoredOutput.error("❌ Falha na configuração do sistema")
            return 1

        # Cria e inicia interface de chat
        interface = ChatInterface(assistant)
        interface.start_chat()

        return 0

    except KeyboardInterrupt:
        print("\n")
        ColoredOutput.warning("Aplicativo interrompido pelo usuário")
        return 0
    except Exception as e:
        ColoredOutput.error(f"Erro fatal: {str(e)}")
        if not args.quiet if "args" in locals() else True:
            import traceback

            traceback.print_exc()
        return 1


def quick_start():
    """Função para início rápido com configuração padrão"""
    print("\n🚀 RAG Code Assistant - Início Rápido")
    print("=" * 40)

    # Configuração padrão
    assistant = CodeAssistant()

    if assistant.setup():
        ColoredOutput.success("✅ Sistema configurado com sucesso!")
        ColoredOutput.info("💡 Inicie o chat interativo com: python main.py")
    else:
        ColoredOutput.error("❌ Falha na configuração")


if __name__ == "__main__":
    sys.exit(main())
