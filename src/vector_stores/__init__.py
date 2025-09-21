from .chroma_store import ChromaVectorStore
from .base import BaseVectorStore


def get_vector_store(vector_store_type: str, **kwargs) -> BaseVectorStore:
    """
    Factory function para criar instâncias de Vector Store
    
    Args:
        vector_store_type: Tipo de vector store ("chroma")
        **kwargs: Argumentos de configuração do vector store
        
    Returns:
        BaseVectorStore: Instância do vector store solicitado
        
    Raises:
        ValueError: Se o tipo de vector store não for suportado
    """
    vector_store_type_lower = vector_store_type.lower()
    
    if vector_store_type_lower == "chroma":
        return ChromaVectorStore(**kwargs)
    else:
        available_stores = ["chroma"]
        raise ValueError(
            f"Vector store '{vector_store_type}' não é suportado. "
            f"Vector stores disponíveis: {available_stores}"
        )
