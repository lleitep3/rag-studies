"""
Implementação concreta do Vector Store usando ChromaDB
"""

import os
from typing import List, Optional, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema.retriever import BaseRetriever
from .base import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    """
    Implementação do Vector Store usando ChromaDB
    
    Esta classe fornece funcionalidades completas de armazenamento vetorial
    usando ChromaDB como backend, com embeddings do Google Gemini.
    """
    
    def __init__(self, 
                 persist_directory: str = "./vector_store_data/chroma",
                 collection_name: str = "rag_documents",
                 embedding_model: str = "models/embedding-001",
                 chunk_size: int = 1500,
                 chunk_overlap: int = 200):
        """
        Inicializa o ChromaDB Vector Store
        
        Args:
            persist_directory: Diretório para persistir os dados do ChromaDB
            collection_name: Nome da coleção no ChromaDB
            embedding_model: Nome do modelo de embeddings do Google
            chunk_size: Tamanho dos chunks de texto
            chunk_overlap: Sobreposição entre chunks
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Verifica se a API key está configurada
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY não encontrada nas variáveis de ambiente. "
                "Configure sua chave da API do Google no arquivo .env"
            )
        
        # Cria diretório de persistência se não existir
        os.makedirs(persist_directory, exist_ok=True)
        
        # Inicializa componentes
        self._initialize_embeddings()
        self._initialize_text_splitter()
        self._initialize_vectorstore()
        
    def _initialize_embeddings(self):
        """Inicializa o modelo de embeddings"""
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=self.embedding_model
            )
            print(f"✅ Modelo de embeddings {self.embedding_model} inicializado")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar embeddings: {str(e)}")
            raise
    
    def _initialize_text_splitter(self):
        """Inicializa o text splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        print(f"✅ Text splitter configurado (chunk_size={self.chunk_size}, overlap={self.chunk_overlap})")
    
    def _initialize_vectorstore(self):
        """Inicializa o vector store ChromaDB"""
        try:
            # Tenta carregar vector store existente
            if self._has_existing_data():
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                collection = self.vectorstore._collection
                doc_count = collection.count()
                print(f"✅ ChromaDB carregado com {doc_count} documentos existentes")
            else:
                # Cria novo vector store vazio
                self.vectorstore = None
                print("✅ ChromaDB inicializado (vazio)")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar ChromaDB: {str(e)}")
            raise
    
    def _has_existing_data(self) -> bool:
        """Verifica se já existem dados no diretório de persistência"""
        chroma_db_path = os.path.join(self.persist_directory, "chroma.sqlite3")
        return os.path.exists(chroma_db_path) and os.path.getsize(chroma_db_path) > 0
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Adiciona documentos ao vector store
        
        Args:
            documents: Lista de documentos LangChain
            
        Returns:
            List[str]: Lista de IDs dos documentos adicionados
        """
        if not documents:
            print("⚠️ Nenhum documento fornecido para indexação")
            return []
        
        try:
            print(f"📄 Processando {len(documents)} documentos...")
            
            # Divide documentos em chunks
            all_chunks = []
            for doc in documents:
                chunks = self.text_splitter.split_documents([doc])
                all_chunks.extend(chunks)
            
            print(f"✂️ Documentos divididos em {len(all_chunks)} chunks")
            
            # Se não existe vector store, cria um novo
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=all_chunks,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
                print(f"🆕 Novo vector store criado com {len(all_chunks)} chunks")
            else:
                # Adiciona ao vector store existente
                self.vectorstore.add_documents(all_chunks)
                print(f"➕ {len(all_chunks)} chunks adicionados ao vector store existente")
            
            # Persiste os dados
            self.vectorstore.persist()
            
            # Retorna estatísticas
            collection = self.vectorstore._collection
            total_docs = collection.count()
            print(f"✅ Vector store atualizado - Total: {total_docs} chunks")
            
            # Retorna IDs dos documentos (simulado)
            return [f"doc_{i}" for i in range(len(all_chunks))]
            
        except Exception as e:
            error_msg = f"Erro ao adicionar documentos: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def get_retriever(self, 
                     search_type: str = "similarity",
                     k: int = 4,
                     score_threshold: float = 0.5) -> BaseRetriever:
        """
        Retorna um objeto retriever para buscar documentos
        
        Args:
            search_type: Tipo de busca ("similarity", "similarity_score_threshold", "mmr")
            k: Número de documentos a retornar
            score_threshold: Threshold mínimo para similarity_score_threshold
            
        Returns:
            BaseRetriever: Objeto retriever configurado
        """
        if self.vectorstore is None:
            raise ValueError("Vector store não foi inicializado. Adicione documentos primeiro.")
        
        try:
            if search_type == "similarity":
                retriever = self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": k}
                )
            elif search_type == "similarity_score_threshold":
                retriever = self.vectorstore.as_retriever(
                    search_type="similarity_score_threshold",
                    search_kwargs={
                        "k": k,
                        "score_threshold": score_threshold
                    }
                )
            elif search_type == "mmr":
                retriever = self.vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": k,
                        "fetch_k": k * 2  # Busca mais documentos para diversidade
                    }
                )
            else:
                raise ValueError(f"Tipo de busca não suportado: {search_type}")
            
            print(f"🔍 Retriever criado (tipo: {search_type}, k: {k})")
            return retriever
            
        except Exception as e:
            error_msg = f"Erro ao criar retriever: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 4) -> List[Document]:
        """
        Busca por similaridade
        
        Args:
            query: Texto da consulta
            k: Número de documentos a retornar
            
        Returns:
            List[Document]: Documentos mais similares
        """
        if self.vectorstore is None:
            raise ValueError("Vector store não foi inicializado. Adicione documentos primeiro.")
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            print(f"🔍 Busca por similaridade: encontrados {len(results)} documentos")
            return results
            
        except Exception as e:
            error_msg = f"Erro na busca por similaridade: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def similarity_search_with_score(self, 
                                   query: str, 
                                   k: int = 4) -> List[tuple]:
        """
        Busca por similaridade com scores
        
        Args:
            query: Texto da consulta
            k: Número de documentos a retornar
            
        Returns:
            List[tuple]: Lista de (documento, score)
        """
        if self.vectorstore is None:
            raise ValueError("Vector store não foi inicializado. Adicione documentos primeiro.")
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            print(f"🔍 Busca com scores: encontrados {len(results)} documentos")
            return results
            
        except Exception as e:
            error_msg = f"Erro na busca com scores: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas da coleção
        
        Returns:
            Dict com estatísticas da coleção
        """
        if self.vectorstore is None:
            return {
                "total_documents": 0,
                "collection_name": self.collection_name,
                "status": "empty"
            }
        
        try:
            collection = self.vectorstore._collection
            doc_count = collection.count()
            
            return {
                "total_documents": doc_count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory,
                "embedding_model": self.embedding_model,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "status": "active" if doc_count > 0 else "empty"
            }
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {str(e)}")
            return {
                "total_documents": 0,
                "collection_name": self.collection_name,
                "status": "error",
                "error": str(e)
            }
    
    def delete_collection(self):
        """Remove completamente a coleção e seus dados"""
        try:
            if self.vectorstore is not None:
                self.vectorstore.delete_collection()
                self.vectorstore = None
                print(f"🗑️ Coleção '{self.collection_name}' removida com sucesso")
            else:
                print("⚠️ Nenhuma coleção para remover")
                
        except Exception as e:
            error_msg = f"Erro ao remover coleção: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)


# Função utilitária para criar instâncias facilmente
def create_chroma_store(persist_directory: str = "./vector_store_data/chroma",
                       collection_name: str = "rag_documents",
                       **kwargs) -> ChromaVectorStore:
    """
    Função utilitária para criar uma instância do ChromaVectorStore
    
    Args:
        persist_directory: Diretório de persistência
        collection_name: Nome da coleção
        **kwargs: Argumentos adicionais
        
    Returns:
        ChromaVectorStore: Instância configurada
    """
    return ChromaVectorStore(
        persist_directory=persist_directory,
        collection_name=collection_name,
        **kwargs
    )