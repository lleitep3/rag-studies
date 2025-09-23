#!/usr/bin/env python3
"""
🤖 Code Assistant
=================

Assistente de código inteligente que usa RAG (Retrieval-Augmented Generation)
para responder perguntas sobre código Python baseado no contexto do projeto.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import time

# Adiciona o src ao path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root / "src"))

from loaders import get_loader
from llms import get_llm
from colored_output import ColoredOutput
from search_engine import SimpleSearchEngine


class CodeAssistant:
    """Assistente de código RAG"""

    def __init__(
        self,
        loader_type: str = "python",
        llm_type: str = "ollama",
        llm_model: str = "llama3.2:1b",
        llm_temperature: float = 0.1,
    ):
        """
        Inicializa o assistente

        Args:
            loader_type: Tipo de loader a usar ("python")
            llm_type: Tipo de LLM ("ollama" ou "gemini")
            llm_model: Nome do modelo
            llm_temperature: Temperatura para geração
        """
        self.loader_type = loader_type
        self.llm_type = llm_type
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature

        self.loader = None
        self.llm = None
        self.search_engine = None
        self.documents = []
        self.is_ready = False

    def setup(self, code_path: str = "./src", file_pattern: str = "**/*.py") -> bool:
        """
        Configura o assistente carregando código e inicializando componentes

        Args:
            code_path: Caminho para o código fonte
            file_pattern: Padrão de arquivos a carregar

        Returns:
            True se configuração foi bem-sucedida
        """
        ColoredOutput.header("RAG Code Assistant")
        print("Um assistente inteligente para seu código Python!\\n")

        try:
            # 1. Inicializar componentes
            ColoredOutput.info("Inicializando componentes...")

            self.loader = get_loader(self.loader_type)
            ColoredOutput.success(f"{self.loader_type.title()}Loader inicializado")

            self.llm = get_llm(
                self.llm_type,
                model_name=self.llm_model,
                temperature=self.llm_temperature,
            )
            ColoredOutput.success(f"{self.llm_type.title()}LLM inicializado")

            # 2. Carregar documentos do projeto
            ColoredOutput.info(f"Carregando código de {code_path}...")

            self.documents = self.loader.load(code_path, file_pattern)

            if not self.documents:
                ColoredOutput.warning(
                    f"Nenhum arquivo encontrado em {code_path} com padrão {file_pattern}"
                )
                return False

            ColoredOutput.success(f"📁 {len(self.documents)} arquivos carregados")

            # 3. Inicializar motor de busca
            self.search_engine = SimpleSearchEngine(self.documents)
            ColoredOutput.success("Motor de busca inicializado")

            # 4. Mostrar estatísticas
            self._show_loading_statistics()

            self.is_ready = True
            ColoredOutput.success("Sistema pronto para uso!")
            return True

        except Exception as e:
            ColoredOutput.error(f"Erro na configuração: {str(e)}")
            return False

    def _show_loading_statistics(self):
        """Mostra estatísticas dos documentos carregados"""
        stats = self.search_engine.get_statistics()

        ColoredOutput.info(f"📊 Estatísticas:")
        print(f"   • Total de linhas: {stats['total_lines']:,}")
        print(f"   • Total de caracteres: {stats['total_chars']:,}")
        print(f"   • Arquivos indexados:")

        for file_info in stats["files"]:
            print(
                f"     - {file_info['path']} ({file_info['lines']} linhas, {file_info['size']} bytes)"
            )

    def ask_question(self, question: str, max_context_docs: int = 3) -> Dict[str, Any]:
        """
        Processa uma pergunta usando RAG

        Args:
            question: Pergunta do usuário
            max_context_docs: Máximo de documentos para contexto

        Returns:
            Dict com resposta, fontes, tempo e status de erro
        """
        if not self.is_ready:
            return {
                "answer": "Sistema não está pronto. Execute setup() primeiro.",
                "sources": [],
                "error": True,
            }

        start_time = time.time()

        try:
            # 1. Buscar contexto relevante
            ColoredOutput.info("🔍 Buscando no código...")
            context, sources = self.search_engine.find_relevant_context(
                question, max_context_docs
            )

            if not context:
                return {
                    "answer": "Não encontrei informações relevantes no código para sua pergunta.",
                    "sources": [],
                    "error": False,
                }

            ColoredOutput.success(
                f"📄 Encontrados {len(sources)} arquivo(s) relevante(s)"
            )

            # 2. Gerar resposta usando LLM
            ColoredOutput.info(f"🧠 Gerando resposta com {self.llm.model_name}...")

            enhanced_question = self._create_enhanced_prompt(question)
            answer = self.llm.ask(enhanced_question, context=context)

            elapsed_time = time.time() - start_time

            return {
                "answer": answer,
                "sources": sources,
                "elapsed_time": round(elapsed_time, 2),
                "error": False,
            }

        except Exception as e:
            return {
                "answer": f"Erro ao processar pergunta: {str(e)}",
                "sources": [],
                "error": True,
            }

    def _create_enhanced_prompt(self, question: str) -> str:
        """Cria prompt aprimorado para o LLM"""
        return f"""
Você é um assistente especializado em código Python e arquitetura de software.
Responda à pergunta baseando-se no código fornecido.

PERGUNTA: {question}

INSTRUÇÕES:
- Base sua resposta no código fornecido
- Seja específico e técnico
- Inclua exemplos de código quando relevante
- Mencione nomes de classes e métodos específicos
- Se não houver informação suficiente, diga claramente
- Use formatação markdown para melhor legibilidade

RESPOSTA:"""

    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações do sistema"""
        if not self.is_ready:
            return {"ready": False}

        stats = self.search_engine.get_statistics()

        return {
            "ready": True,
            "loader_type": self.loader_type,
            "llm_type": self.llm_type,
            "llm_model": self.llm_model,
            "documents_count": len(self.documents),
            "total_lines": stats["total_lines"],
            "total_chars": stats["total_chars"],
            "files": [f["path"] for f in stats["files"]],
        }

    def search_keywords(
        self, keywords: List[str], max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca por palavras-chave específicas

        Args:
            keywords: Lista de palavras-chave
            max_results: Máximo de resultados

        Returns:
            Lista de arquivos encontrados
        """
        if not self.is_ready:
            return []

        return self.search_engine.search_by_keywords(keywords, max_results)

    def reload_documents(
        self, code_path: str = "./src", file_pattern: str = "**/*.py"
    ) -> bool:
        """
        Recarrega documentos (útil se código foi modificado)

        Args:
            code_path: Caminho para o código
            file_pattern: Padrão de arquivos

        Returns:
            True se recarregamento foi bem-sucedido
        """
        try:
            ColoredOutput.info("Recarregando documentos...")

            self.documents = self.loader.load(code_path, file_pattern)

            if not self.documents:
                ColoredOutput.warning(f"Nenhum arquivo encontrado em {code_path}")
                return False

            self.search_engine = SimpleSearchEngine(self.documents)

            ColoredOutput.success(f"📁 {len(self.documents)} arquivos recarregados")
            return True

        except Exception as e:
            ColoredOutput.error(f"Erro ao recarregar: {str(e)}")
            return False


def demo():
    """Demonstração do Code Assistant"""
    print("\n🤖 Demonstração do Code Assistant")
    print("=" * 40)

    assistant = CodeAssistant()

    if assistant.setup("../../src"):
        # Testa pergunta
        result = assistant.ask_question("Como funciona o PythonLoader?")

        print(f"\nResposta: {result['answer'][:100]}...")
        print(f"Fontes: {len(result.get('sources', []))}")
        print(f"Tempo: {result.get('elapsed_time', 0)}s")

        # Info do sistema
        info = assistant.get_system_info()
        print(f"\nSistema pronto: {info['ready']}")
        print(f"Documentos: {info.get('documents_count', 0)}")


if __name__ == "__main__":
    demo()
