"""
Testes para o RAGEngine
========================

Testa a funcionalidade principal do motor RAG.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.engine import RAGEngine, create_rag_engine
from langchain.docstore.document import Document


class TestRAGEngine:
    """Testes para a classe RAGEngine"""
    
    @pytest.mark.unit
    def test_init(self, mock_loader, mock_vector_store, mock_llm):
        """Testa inicialização do RAGEngine"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        assert engine.loader == mock_loader
        assert engine.vector_store == mock_vector_store
        assert engine.llm == mock_llm
        assert engine.retriever is None
        assert engine.is_indexed is False
        assert engine.retriever_config["k"] == 4
    
    @pytest.mark.unit
    def test_init_with_custom_retriever_config(self, mock_loader, mock_vector_store, mock_llm):
        """Testa inicialização com configuração customizada do retriever"""
        custom_config = {
            "search_type": "mmr",
            "k": 10,
            "score_threshold": 0.7
        }
        
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm,
            retriever_config=custom_config
        )
        
        assert engine.retriever_config == custom_config
    
    @pytest.mark.unit
    def test_setup_pipeline_success(self, mock_loader, mock_vector_store, mock_llm):
        """Testa setup_pipeline com sucesso"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        # Setup do pipeline
        stats = engine.setup_pipeline("/test/path", "*.py")
        
        # Verifica chamadas
        mock_loader.load.assert_called_once_with("/test/path", "*.py")
        mock_vector_store.add_documents.assert_called_once()
        mock_vector_store.get_retriever.assert_called_once()
        
        # Verifica estatísticas
        assert stats["status"] == "success"
        assert stats["documents_loaded"] == 2
        assert stats["documents_indexed"] == 2
        assert engine.is_indexed is True
        assert engine.retriever is not None
    
    @pytest.mark.unit
    def test_setup_pipeline_no_documents(self, mock_loader, mock_vector_store, mock_llm):
        """Testa setup_pipeline quando não há documentos"""
        mock_loader.load.return_value = []
        
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        stats = engine.setup_pipeline("/test/path", "*.py")
        
        assert stats["status"] == "error"
        assert "Nenhum documento foi carregado" in stats["error"]
        assert engine.is_indexed is False
    
    @pytest.mark.unit
    def test_ask_not_indexed(self, mock_loader, mock_vector_store, mock_llm):
        """Testa ask quando o sistema não está indexado"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        result = engine.ask("Test question")
        
        assert result["status"] == "error"
        assert "não está indexado" in result["answer"]
        mock_llm.ask.assert_not_called()
    
    @pytest.mark.unit
    def test_ask_success(self, mock_loader, mock_vector_store, mock_llm):
        """Testa ask com sucesso"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        # Setup pipeline primeiro
        engine.setup_pipeline("/test/path", "*.py")
        
        # Faz pergunta
        question = "What is the best practice for Python?"
        result = engine.ask(question)
        
        # Verifica resultado
        assert result["status"] == "success"
        assert result["question"] == question
        assert result["answer"] == "This is a test response from the LLM."
        assert result["retrieved_docs_count"] == 1
        assert len(result["sources"]) == 1
        
        # Verifica chamadas
        engine.retriever.invoke.assert_called_once_with(question)
        mock_llm.ask.assert_called_once()
    
    @pytest.mark.unit
    def test_ask_without_sources(self, mock_loader, mock_vector_store, mock_llm):
        """Testa ask sem incluir fontes"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        engine.setup_pipeline("/test/path", "*.py")
        result = engine.ask("Test question", include_sources=False)
        
        assert result["sources"] == []
    
    @pytest.mark.unit
    def test_ask_with_custom_retriever_kwargs(self, mock_loader, mock_vector_store, mock_llm):
        """Testa ask com parâmetros customizados do retriever"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        engine.setup_pipeline("/test/path", "*.py")
        
        custom_kwargs = {"k": 10, "score_threshold": 0.8}
        result = engine.ask("Test question", retriever_kwargs=custom_kwargs)
        
        # Verifica que get_retriever foi chamado com os parâmetros customizados
        calls = mock_vector_store.get_retriever.call_args_list
        assert len(calls) == 2  # Uma vez no setup, outra no ask
        assert calls[1][1] == custom_kwargs
    
    @pytest.mark.unit
    def test_get_system_info(self, mock_loader, mock_vector_store, mock_llm):
        """Testa get_system_info"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        info = engine.get_system_info()
        
        assert info["status"] == "not_indexed"
        assert info["has_retriever"] is False
        assert "loader" in info["components"]
        assert "vector_store" in info["components"]
        assert "llm" in info["components"]
        
        # Após indexação
        engine.setup_pipeline("/test/path", "*.py")
        info = engine.get_system_info()
        
        assert info["status"] == "indexed"
        assert info["has_retriever"] is True
    
    @pytest.mark.unit
    def test_update_retriever_config(self, mock_loader, mock_vector_store, mock_llm):
        """Testa update_retriever_config"""
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        # Atualiza configuração antes de indexar
        engine.update_retriever_config(k=10, search_type="mmr")
        assert engine.retriever_config["k"] == 10
        assert engine.retriever_config["search_type"] == "mmr"
        
        # Após indexação
        engine.setup_pipeline("/test/path", "*.py")
        engine.update_retriever_config(k=5)
        
        # Verifica que retriever foi recriado
        assert mock_vector_store.get_retriever.call_count == 2
    
    @pytest.mark.unit
    def test_clear_index(self, mock_loader, mock_vector_store, mock_llm):
        """Testa clear_index"""
        mock_vector_store.delete_collection = Mock()
        
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        # Setup e depois limpa
        engine.setup_pipeline("/test/path", "*.py")
        assert engine.is_indexed is True
        
        engine.clear_index()
        
        mock_vector_store.delete_collection.assert_called_once()
        assert engine.is_indexed is False
        assert engine.retriever is None
    
    @pytest.mark.unit
    def test_ask_exception_handling(self, mock_loader, mock_vector_store, mock_llm):
        """Testa tratamento de exceções em ask"""
        mock_llm.ask.side_effect = Exception("LLM Error")
        
        engine = RAGEngine(
            loader=mock_loader,
            vector_store=mock_vector_store,
            llm=mock_llm
        )
        
        engine.setup_pipeline("/test/path", "*.py")
        result = engine.ask("Test question")
        
        assert result["status"] == "error"
        assert "LLM Error" in result["error"]
        assert "Erro interno" in result["answer"]


class TestCreateRAGEngine:
    """Testes para a função utilitária create_rag_engine"""
    
    @pytest.mark.unit
    def test_create_rag_engine(self):
        """Testa criação do RAGEngine via função utilitária"""
        # Configura mocks
        mock_loader = Mock()
        mock_vector_store = Mock()
        mock_llm = Mock()
        mock_llm.model_name = "test_model"
        
        # Patch dos módulos importados dentro da função
        with patch('loaders.get_loader') as mock_get_loader, \
             patch('vector_stores.get_vector_store') as mock_get_vector_store, \
             patch('llms.get_llm') as mock_get_llm:
            
            mock_get_loader.return_value = mock_loader
            mock_get_vector_store.return_value = mock_vector_store
            mock_get_llm.return_value = mock_llm
            
            # Cria engine
            engine = create_rag_engine(
                loader_type="python",
                vector_store_type="chroma",
                llm_type="ollama",
                loader_kwargs={"test": "value"},
                llm_kwargs={"model": "test"}
            )
            
            # Verifica chamadas
            mock_get_loader.assert_called_once_with("python", test="value")
            mock_get_vector_store.assert_called_once_with("chroma")
            mock_get_llm.assert_called_once_with("ollama", model="test")
            
            # Verifica engine criado
            assert isinstance(engine, RAGEngine)
            assert engine.loader == mock_loader
            assert engine.vector_store == mock_vector_store
            assert engine.llm == mock_llm
