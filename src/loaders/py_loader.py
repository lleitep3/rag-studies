from .base import BaseLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.docstore.document import Document
from typing import List
import os


class PythonLoader(BaseLoader):
    def load(self, path: str, glob: str) -> List[Document]:
        """
        Carrega arquivos Python de um diretório usando o padrão glob especificado.
        
        Args:
            path: Caminho do diretório para buscar arquivos
            glob: Padrão glob para filtrar arquivos (ex: '**/*.py')
            
        Returns:
            Lista de documentos LangChain carregados
        """
        # Verifica se o diretório existe
        if not os.path.exists(path):
            raise FileNotFoundError(f"Diretório não encontrado: {path}")
            
        # Cria o DirectoryLoader para arquivos Python
        loader = DirectoryLoader(
            path=path,
            glob=glob,
            loader_cls=TextLoader,
            loader_kwargs={
                'encoding': 'utf-8',
                'autodetect_encoding': True
            },
            show_progress=True
        )
        
        try:
            # Carrega os documentos
            documents = loader.load()
            
            # Adiciona metadados extras aos documentos
            for doc in documents:
                # Adiciona informações sobre o tipo de arquivo
                doc.metadata['file_type'] = 'python'
                doc.metadata['loader'] = 'PythonLoader'
                
                # Adiciona informação sobre o tamanho do arquivo
                if 'source' in doc.metadata:
                    try:
                        file_size = os.path.getsize(doc.metadata['source'])
                        doc.metadata['file_size'] = file_size
                    except OSError:
                        doc.metadata['file_size'] = 0
                        
            print(f"✅ Carregados {len(documents)} arquivos Python de {path}")
            return documents
            
        except Exception as e:
            print(f"❌ Erro ao carregar documentos: {str(e)}")
            raise
