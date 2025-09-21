from abc import ABC, abstractmethod
from typing import List
from langchain.docstore.document import Document
from langchain.schema.retriever import BaseRetriever


class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Adiciona documentos ao vector store.
        
        Args:
            documents: Lista de documentos LangChain para indexar
            
        Returns:
            List[str]: Lista de IDs dos documentos adicionados
            
        Raises:
            Exception: Em caso de erro na indexação
        """
        pass

    @abstractmethod
    def get_retriever(self, **kwargs) -> BaseRetriever:
        """Retorna um objeto retriever para buscar documentos.
        
        Args:
            **kwargs: Argumentos de configuração do retriever
            
        Returns:
            BaseRetriever: Objeto retriever configurado para busca
            
        Raises:
            ValueError: Se o vector store não estiver inicializado
            Exception: Em caso de erro na criação do retriever
        """
        pass
