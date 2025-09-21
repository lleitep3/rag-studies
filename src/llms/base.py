from abc import ABC, abstractmethod


class BaseLLM(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def ask(self, question: str, context: str = "") -> str:
        """Faz uma pergunta ao modelo LLM e retorna a resposta.
        
        Args:
            question: Pergunta a ser feita ao modelo
            context: Contexto adicional para auxiliar a resposta (usado em RAG)
            
        Returns:
            str: Resposta gerada pelo modelo
            
        Raises:
            Exception: Em caso de erro na consulta ao modelo
        """
        pass
