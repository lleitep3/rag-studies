"""
Classe Base para Capacidades
===========================

Define a interface comum e funcionalidades básicas para todas as capacidades
do sistema RAG.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class CapacityResponse:
    """Estrutura padrão para respostas de capacidades"""

    success: bool
    data: Dict[str, Any]
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


class BaseCapacity(ABC):
    """Classe base para todas as capacidades do sistema"""

    def __init__(self, rag_engine):
        """
        Inicializa uma nova capacidade.

        Args:
            rag_engine: Motor RAG para busca e geração
        """
        self.rag = rag_engine
        self.context = {}

    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Retorna o template de prompt da capacidade.

        Returns:
            str: Template do prompt com placeholders para contexto
        """
        pass

    @abstractmethod
    def process_response(self, response: str) -> CapacityResponse:
        """
        Processa a resposta do LLM e retorna dados estruturados.

        Args:
            response (str): Resposta bruta do LLM

        Returns:
            CapacityResponse: Resposta processada e estruturada
        """
        pass

    def prepare_context(self, **kwargs) -> Dict[str, Any]:
        """
        Prepara o contexto para o prompt.

        Args:
            **kwargs: Argumentos específicos da capacidade

        Returns:
            Dict[str, Any]: Contexto processado
        """
        return kwargs

    def execute(self, **kwargs) -> CapacityResponse:
        """
        Executa a capacidade.

        Args:
            **kwargs: Argumentos específicos da capacidade

        Returns:
            CapacityResponse: Resultado da execução
        """
        try:
            # Prepara contexto
            context = self.prepare_context(**kwargs)

            # Obtém o prompt
            prompt_template = self.get_prompt_template()
            
            # Formata o prompt com o contexto
            formatted_prompt = prompt_template.format(**context)

            # Usa o método ask do RAGEngine se ele estiver indexado
            if hasattr(self.rag, 'is_indexed') and self.rag.is_indexed:
                # RAGEngine com documentos indexados - usa ask para obter contexto
                result = self.rag.ask(
                    formatted_prompt,
                    include_sources=False,
                    retriever_kwargs={'k': 3}
                )
                response = result.get('answer', '')
            elif hasattr(self.rag, 'llm'):
                # RAGEngine sem indexação - usa LLM diretamente
                response = self.rag.llm.ask(formatted_prompt)
            else:
                # Fallback - tenta chamar ask do rag diretamente
                response = str(self.rag.ask(formatted_prompt))

            # Processa e retorna
            return self.process_response(response)

        except Exception as e:
            return CapacityResponse(success=False, data={}, errors=[str(e)])
