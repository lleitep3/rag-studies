"""
RAG Engine - Orquestrador principal do sistema RAG

Este módulo implementa a lógica principal para coordenar todos os componentes
do sistema RAG: carregamento, indexação, busca e geração de respostas.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import time
import sys

# Imports locais
sys.path.append(str(Path(__file__).parent.parent))
from loaders.base import BaseLoader
from vector_stores.base import BaseVectorStore
from llms.base import BaseLLM


class RAGEngine:
    """
    Motor principal do sistema RAG
    
    Coordena o fluxo completo:
    1. Carregamento de documentos (Loader)
    2. Indexação em vector store (VectorStore)
    3. Recuperação de contexto relevante (Retriever)
    4. Geração de resposta (LLM)
    """
    
    def __init__(self, 
                 loader: BaseLoader, 
                 vector_store: BaseVectorStore, 
                 llm: BaseLLM,
                 retriever_config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o RAG Engine
        
        Args:
            loader: Instância do carregador de documentos
            vector_store: Instância do vector store
            llm: Instância do modelo de linguagem
            retriever_config: Configurações do retriever
        """
        self.loader = loader
        self.vector_store = vector_store
        self.llm = llm
        self.retriever = None
        self.is_indexed = False
        
        # Configurações padrão do retriever
        self.retriever_config = retriever_config or {
            "search_type": "similarity",
            "k": 4,
            "score_threshold": 0.5
        }
        
        print(f"✅ RAGEngine inicializado")
        print(f"   • Loader: {type(self.loader).__name__}")
        print(f"   • Vector Store: {type(self.vector_store).__name__}")
        print(f"   • LLM: {type(self.llm).__name__} ({self.llm.model_name})")
    
    def setup_pipeline(self, path: str, glob: str) -> Dict[str, Any]:
        """
        Configura o pipeline RAG: carrega documentos e indexa no vector store
        
        Args:
            path: Caminho dos documentos
            glob: Padrão glob para filtrar arquivos
            
        Returns:
            Dict com estatísticas da indexação
        """
        start_time = time.time()
        
        try:
            print(f"\n🔄 Configurando pipeline RAG...")
            print(f"📁 Fonte: {path}")
            print(f"🔍 Padrão: {glob}")
            
            # 1. Carregamento de documentos
            print(f"\n📄 Etapa 1: Carregando documentos...")
            docs = self.loader.load(path, glob)
            
            if not docs:
                raise ValueError("Nenhum documento foi carregado")
            
            print(f"✅ {len(docs)} documentos carregados")
            
            # 2. Indexação no vector store
            print(f"\n🗂️ Etapa 2: Indexando documentos...")
            doc_ids = self.vector_store.add_documents(docs)
            
            print(f"✅ {len(doc_ids)} documentos indexados")
            
            # 3. Configuração do retriever
            print(f"\n🔗 Etapa 3: Configurando retriever...")
            self.retriever = self.vector_store.get_retriever(**self.retriever_config)
            
            print(f"✅ Retriever configurado (tipo: {self.retriever_config['search_type']})")
            
            # 4. Marca como indexado
            self.is_indexed = True
            
            # Estatísticas finais
            elapsed_time = time.time() - start_time
            stats = {
                "documents_loaded": len(docs),
                "documents_indexed": len(doc_ids),
                "elapsed_time": round(elapsed_time, 2),
                "retriever_config": self.retriever_config,
                "status": "success"
            }
            
            print(f"\n🎉 Pipeline configurado com sucesso!")
            print(f"⏱️ Tempo total: {elapsed_time:.2f}s")
            
            return stats
            
        except Exception as e:
            error_msg = f"Erro ao configurar pipeline: {str(e)}"
            print(f"❌ {error_msg}")
            
            return {
                "documents_loaded": 0,
                "documents_indexed": 0,
                "elapsed_time": time.time() - start_time,
                "error": error_msg,
                "status": "error"
            }
    
    def ask(self, question: str, 
            include_sources: bool = True,
            retriever_kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Faz uma pergunta usando o sistema RAG completo
        
        Args:
            question: Pergunta do usuário
            include_sources: Se deve incluir fontes na resposta
            retriever_kwargs: Parâmetros específicos para o retriever
            
        Returns:
            Dict com resposta, contexto e metadados
        """
        start_time = time.time()
        
        if not self.is_indexed:
            return {
                "answer": "Sistema não está indexado. Execute setup_pipeline() primeiro.",
                "question": question,
                "context": "",
                "sources": [],
                "status": "error",
                "elapsed_time": 0
            }
        
        try:
            print(f"\n🤔 Processando pergunta: '{question}'")
            
            # 1. Recuperação de contexto
            print(f"🔍 Buscando contexto relevante...")
            
            if retriever_kwargs:
                # Usa retriever customizado se especificado
                temp_retriever = self.vector_store.get_retriever(**retriever_kwargs)
                retrieved_docs = temp_retriever.invoke(question)
            else:
                # Usa retriever padrão
                retrieved_docs = self.retriever.invoke(question)
            
            print(f"📄 {len(retrieved_docs)} documentos recuperados")
            
            # 2. Preparação do contexto
            context_parts = []
            sources = []
            
            for i, doc in enumerate(retrieved_docs, 1):
                # Adiciona o conteúdo ao contexto
                context_parts.append(f"[DOCUMENTO {i}]\n{doc.page_content}")
                
                # Coleta informações da fonte
                if include_sources:
                    source_info = {
                        "index": i,
                        "source": doc.metadata.get('source', 'N/A'),
                        "file_type": doc.metadata.get('file_type', 'N/A'),
                        "file_size": doc.metadata.get('file_size', 0),
                        "content_preview": doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                    }
                    sources.append(source_info)
            
            # Contexto completo
            full_context = "\n\n".join(context_parts)
            
            # 3. Geração da resposta
            print(f"🧠 Gerando resposta com {self.llm.model_name}...")
            
            answer = self.llm.ask(question, context=full_context)
            
            # 4. Preparação da resposta final
            elapsed_time = time.time() - start_time
            
            result = {
                "answer": answer,
                "question": question,
                "context": full_context,
                "sources": sources if include_sources else [],
                "retrieved_docs_count": len(retrieved_docs),
                "status": "success",
                "elapsed_time": round(elapsed_time, 2),
                "llm_model": self.llm.model_name
            }
            
            print(f"✅ Resposta gerada em {elapsed_time:.2f}s")
            
            return result
            
        except Exception as e:
            error_msg = f"Erro ao processar pergunta: {str(e)}"
            print(f"❌ {error_msg}")
            
            return {
                "answer": f"Erro interno: {error_msg}",
                "question": question,
                "context": "",
                "sources": [],
                "status": "error",
                "elapsed_time": time.time() - start_time,
                "error": error_msg
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o estado atual do sistema
        
        Returns:
            Dict com informações detalhadas do sistema
        """
        vector_stats = self.vector_store.get_collection_stats() if hasattr(self.vector_store, 'get_collection_stats') else {}
        llm_info = self.llm.get_model_info() if hasattr(self.llm, 'get_model_info') else {}
        
        return {
            "status": "indexed" if self.is_indexed else "not_indexed",
            "components": {
                "loader": type(self.loader).__name__,
                "vector_store": type(self.vector_store).__name__,
                "llm": type(self.llm).__name__
            },
            "retriever_config": self.retriever_config,
            "vector_store_stats": vector_stats,
            "llm_info": llm_info,
            "has_retriever": self.retriever is not None
        }
    
    def update_retriever_config(self, **kwargs):
        """
        Atualiza configurações do retriever
        
        Args:
            **kwargs: Novas configurações (search_type, k, score_threshold, etc.)
        """
        self.retriever_config.update(kwargs)
        
        if self.is_indexed:
            # Re-cria o retriever com as novas configurações
            self.retriever = self.vector_store.get_retriever(**self.retriever_config)
            print(f"✅ Retriever reconfigurado: {kwargs}")
        else:
            print(f"⚠️ Configuração salva, mas retriever não está ativo")
    
    def clear_index(self):
        """
        Limpa o índice atual
        """
        try:
            if hasattr(self.vector_store, 'delete_collection'):
                self.vector_store.delete_collection()
            
            self.retriever = None
            self.is_indexed = False
            
            print(f"✅ Índice limpo com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao limpar índice: {str(e)}")            
            
            
# Função utilitária para criar RAGEngine facilmente
def create_rag_engine(loader_type: str,
                     vector_store_type: str,
                     llm_type: str,
                     **kwargs) -> RAGEngine:
    """
    Função utilitária para criar um RAGEngine com componentes especificados
    
    Args:
        loader_type: Tipo de loader ("python")
        vector_store_type: Tipo de vector store ("chroma")
        llm_type: Tipo de LLM ("gemini", "ollama")
        **kwargs: Argumentos específicos dos componentes
        
    Returns:
        RAGEngine: Instância configurada
    """
    from loaders import get_loader
    from vector_stores import get_vector_store  
    from llms import get_llm
    
    # Separar argumentos por componente
    loader_kwargs = kwargs.get('loader_kwargs', {})
    vector_store_kwargs = kwargs.get('vector_store_kwargs', {})
    llm_kwargs = kwargs.get('llm_kwargs', {})
    retriever_kwargs = kwargs.get('retriever_kwargs', {})
    
    # Criar componentes
    loader = get_loader(loader_type, **loader_kwargs)
    vector_store = get_vector_store(vector_store_type, **vector_store_kwargs)
    llm = get_llm(llm_type, **llm_kwargs)
    
    # Criar RAGEngine
    return RAGEngine(
        loader=loader,
        vector_store=vector_store,
        llm=llm,
        retriever_config=retriever_kwargs
    )
