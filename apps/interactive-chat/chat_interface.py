#!/usr/bin/env python3
"""
💬 Chat Interface
=================

Interface de chat interativo para o Code Assistant.
Fornece comandos, exemplos e navegação amigável.
"""

from typing import Dict, Any, List
from colored_output import ColoredOutput
from code_assistant import CodeAssistant


class ChatInterface:
    """Interface de chat interativo"""

    def __init__(self, assistant: CodeAssistant):
        """Inicializa interface com assistente"""
        self.assistant = assistant
        self.commands = {
            "help": self._show_help,
            "stats": self._show_stats,
            "files": self._show_files,
            "examples": self._show_examples,
            "search": self._search_keywords,
            "reload": self._reload_documents,
            "info": self._show_system_info,
            "quit": self._quit_chat,
        }

        self.example_questions = [
            "Como funciona o PythonLoader?",
            "Qual a diferença entre GeminiLLM e OllamaLLM?",
            "Como criar um novo tipo de LLM?",
            "Como o RAGEngine funciona?",
            "Quais são as classes abstratas do projeto?",
            "Como implementar um novo loader?",
            "Qual a estrutura do vector store?",
            "Como usar a factory function get_llm?",
            "Explique o padrão Factory usado no projeto",
            "Como adicionar um novo tipo de embedding?",
        ]

        self.running = False

    def start_chat(self):
        """Inicia o chat interativo"""
        if not self.assistant.is_ready:
            ColoredOutput.error("Assistente não está configurado!")
            return

        self.running = True
        self._show_banner()
        self._show_initial_help()

        while self.running:
            try:
                self._chat_loop()
            except KeyboardInterrupt:
                print("\n")
                ColoredOutput.warning("Interrompido pelo usuário")
                ColoredOutput.success("👋 Até logo!")
                break
            except Exception as e:
                ColoredOutput.error(f"Erro inesperado: {str(e)}")
                break

    def _chat_loop(self):
        """Loop principal do chat"""
        print("\n" + "-" * 50)
        ColoredOutput.print_colored("💬 Sua pergunta: ", ColoredOutput.CYAN, bold=True)
        user_input = input().strip()

        if not user_input:
            return

        # Verifica se é comando
        if user_input.lower() in self.commands:
            self.commands[user_input.lower()]()
            return

        # Processa pergunta normal
        ColoredOutput.question(user_input)
        result = self.assistant.ask_question(user_input)
        self._display_result(result)

    def _display_result(self, result: Dict[str, Any]):
        """Exibe resultado da pergunta"""
        if result["error"]:
            ColoredOutput.error(result["answer"])
        else:
            # Mostra resposta
            print("")
            ColoredOutput.answer("Resposta:")
            print(result["answer"])

            # Mostra fontes
            if result["sources"]:
                print(f"\n📚 Fontes consultadas:")
                for source in result["sources"]:
                    print(
                        f"   • {source['file']} ({source['lines']} linhas, score: {source['score']})"
                    )

            # Tempo de processamento
            if "elapsed_time" in result:
                ColoredOutput.info(f"⏱️ Tempo de resposta: {result['elapsed_time']}s")

    def _show_banner(self):
        """Mostra banner inicial"""
        print("\n" + "🤖" + "=" * 58 + "🤖")
        ColoredOutput.print_colored(
            "   RAG CODE ASSISTANT - Chat Interativo", ColoredOutput.CYAN, bold=True
        )
        print("🤖" + "=" * 58 + "🤖")

    def _show_initial_help(self):
        """Mostra ajuda inicial"""
        ColoredOutput.success("🚀 Chat Interativo Iniciado!")

        ColoredOutput.info("📝 Comandos disponíveis:")
        print("   • Digite sua pergunta e pressione Enter")
        print("   • 'help' - Mostra todos os comandos")
        print("   • 'examples' - Exemplos de perguntas")
        print("   • 'quit' - Sair do chat")

        # Mostra algumas perguntas de exemplo
        self._show_examples(show_all=False)

    def _show_help(self):
        """Mostra todos os comandos disponíveis"""
        ColoredOutput.info("🔧 Comandos disponíveis:")
        commands_help = {
            "help": "Mostra esta lista de comandos",
            "examples": "Mostra exemplos de perguntas que você pode fazer",
            "stats": "Estatísticas do sistema (arquivos, linhas, etc.)",
            "files": "Lista todos os arquivos carregados",
            "search": "Busca por palavras-chave específicas",
            "reload": "Recarrega todos os documentos do projeto",
            "info": "Informações detalhadas do sistema",
            "quit": "Sair do chat",
        }

        for cmd, description in commands_help.items():
            print(f"   • {cmd} - {description}")

        ColoredOutput.info("\n💡 Dicas:")
        print("   • Seja específico nas perguntas para melhores resultados")
        print("   • Mencione nomes de classes/métodos quando souber")
        print("   • Use 'search' para encontrar arquivos por palavras-chave")

    def _show_examples(self, show_all: bool = True):
        """Mostra exemplos de perguntas"""
        ColoredOutput.info("💡 Exemplos de perguntas que você pode fazer:")

        examples_to_show = (
            self.example_questions if show_all else self.example_questions[:5]
        )

        for i, example in enumerate(examples_to_show, 1):
            print(f"   {i}. {example}")

        if not show_all and len(self.example_questions) > 5:
            print(
                f"   ... e mais {len(self.example_questions) - 5} exemplos (digite 'examples' para ver todos)"
            )

    def _show_stats(self):
        """Mostra estatísticas do sistema"""
        info = self.assistant.get_system_info()

        if not info.get("ready", False):
            ColoredOutput.error("Sistema não configurado")
            return

        ColoredOutput.info("📊 Estatísticas do Sistema:")
        print(f"   • Arquivos carregados: {info['documents_count']}")
        print(f"   • Total de linhas: {info['total_lines']:,}")
        print(f"   • Total de caracteres: {info['total_chars']:,}")
        print(f"   • LLM: {info['llm_model']} ({info['llm_type']})")
        print(f"   • Loader: {info['loader_type']}")
        print(f"   • Status: ✅ Pronto")

    def _show_files(self):
        """Lista arquivos carregados"""
        info = self.assistant.get_system_info()

        if not info.get("ready", False):
            ColoredOutput.warning("Sistema não configurado")
            return

        files = info.get("files", [])
        if not files:
            ColoredOutput.warning("Nenhum arquivo carregado")
            return

        ColoredOutput.info(f"📁 Arquivos carregados ({len(files)}):")
        for i, file_path in enumerate(files, 1):
            print(f"   {i}. {file_path}")

    def _search_keywords(self):
        """Busca por palavras-chave"""
        ColoredOutput.info("🔍 Busca por palavras-chave")
        ColoredOutput.print_colored(
            "Digite as palavras-chave separadas por espaço: ", ColoredOutput.CYAN
        )

        try:
            keywords_input = input().strip()
            if not keywords_input:
                return

            keywords = keywords_input.split()
            results = self.assistant.search_keywords(keywords, max_results=10)

            if not results:
                ColoredOutput.warning("Nenhum resultado encontrado")
                return

            ColoredOutput.success(f"📄 Encontrados {len(results)} arquivo(s):")
            for i, result in enumerate(results, 1):
                print(f"\n   {i}. {result['file']}")
                print(f"      • Matches: {result['matches']}")
                print(
                    f"      • Palavras encontradas: {', '.join(result['matched_keywords'])}"
                )
                print(f"      • Preview: {result['preview'][:100]}...")

        except (EOFError, KeyboardInterrupt):
            print("\nBusca cancelada")

    def _reload_documents(self):
        """Recarrega documentos"""
        ColoredOutput.info("🔄 Recarregando documentos...")

        if self.assistant.reload_documents():
            ColoredOutput.success("Documentos recarregados com sucesso!")
        else:
            ColoredOutput.error("Falha ao recarregar documentos")

    def _show_system_info(self):
        """Mostra informações detalhadas do sistema"""
        info = self.assistant.get_system_info()

        if not info.get("ready", False):
            ColoredOutput.error("Sistema não configurado")
            return

        ColoredOutput.info("🔧 Informações do Sistema:")
        print(f"\n📝 Configuração:")
        print(f"   • LLM Type: {info['llm_type']}")
        print(f"   • LLM Model: {info['llm_model']}")
        print(f"   • Loader Type: {info['loader_type']}")

        print(f"\n📊 Dados:")
        print(f"   • Documentos: {info['documents_count']}")
        print(f"   • Linhas: {info['total_lines']:,}")
        print(f"   • Caracteres: {info['total_chars']:,}")

        print(f"\n📁 Arquivos principais:")
        files = info.get("files", [])
        for file_path in files[:10]:  # Mostra apenas os primeiros 10
            print(f"   • {file_path}")

        if len(files) > 10:
            print(f"   ... e mais {len(files) - 10} arquivo(s)")

    def _quit_chat(self):
        """Sai do chat"""
        ColoredOutput.success("👋 Até logo!")
        self.running = False


def demo():
    """Demonstração da interface de chat"""
    print("\n💬 Demonstração da Chat Interface")
    print("=" * 40)

    # Simula assistente configurado
    from .code_assistant import CodeAssistant

    assistant = CodeAssistant()
    if assistant.setup("../../src"):
        interface = ChatInterface(assistant)

        # Simula alguns comandos
        print("\nTestando comandos...")
        interface._show_help()
        interface._show_examples(show_all=False)
        interface._show_stats()


if __name__ == "__main__":
    demo()
