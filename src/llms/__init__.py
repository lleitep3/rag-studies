from .gemini_llm import GeminiLLM
from .ollama_llm import OllamaLLM
from .base import BaseLLM


def get_llm(llm_type: str, **kwargs) -> BaseLLM:
    """
    Factory function para criar instâncias de LLM

    Args:
        llm_type: Tipo de LLM ("gemini", "ollama")
        **kwargs: Argumentos de configuração do LLM

    Returns:
        BaseLLM: Instância do LLM solicitado

    Raises:
        ValueError: Se o tipo de LLM não for suportado
    """
    llm_type_lower = llm_type.lower()
    print(f"🔍 Criando LLM do tipo '{llm_type_lower}' com args: {kwargs}")
    if llm_type_lower == "gemini":
        return GeminiLLM(**kwargs)
    elif llm_type_lower == "ollama":
        return OllamaLLM(**kwargs)
    else:
        available_llms = ["gemini", "ollama"]
        raise ValueError(
            f"LLM '{llm_type}' não é suportado. " f"LLMs disponíveis: {available_llms}"
        )
