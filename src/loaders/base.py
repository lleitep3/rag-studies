from abc import ABC, abstractmethod
from typing import List
from langchain.docstore.document import Document


class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str, glob: str) -> List[Document]:
        """Carrega documentos de um caminho específico com um padrão glob.
        
        Args:
            path: Caminho do diretório para buscar arquivos
            glob: Padrão glob para filtrar arquivos (ex: '**/*.py', '**/*.md')
            
        Returns:
            List[Document]: Lista de documentos LangChain carregados
            
        Raises:
            FileNotFoundError: Se o diretório não existir
            Exception: Para outros erros de carregamento
        """
        pass
