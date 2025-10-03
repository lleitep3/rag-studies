"""
Testes para OllamaLLM
=====================

Testa a implementação do LLM usando Ollama.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

# Adiciona src ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.llms.ollama_llm import OllamaLLM, create_ollama_llm


class TestOllamaLLM:
    """Testes para a classe OllamaLLM"""
    
    @pytest.fixture
    def mock_ollama(self):
        """Mock do módulo ollama"""
        with patch('src.llms.ollama_llm.ollama') as mock:
            # Configura lista de modelos
            model_obj = Mock()
            model_obj.model = "llama3.2:1b"
            
            models_response = Mock()
            models_response.models = [model_obj]
            
            mock.list.return_value = models_response
            mock.pull.return_value = None
            
            yield mock
    
    @pytest.fixture
    def mock_langchain_ollama(self):
        """Mock do LangChainOllamaLLM"""
        with patch('src.llms.ollama_llm.LangChainOllamaLLM') as mock:
            instance = Mock()
            instance.invoke.return_value = "Test response"
            mock.return_value = instance
            yield mock
    
    @pytest.mark.unit
    def test_init_success(self, mock_ollama, mock_langchain_ollama):
        """Testa inicialização bem-sucedida"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        assert llm.model_name == "llama3.2:1b"
        assert llm.temperature == 0.1
        assert llm.base_url == "http://localhost:11434"
        
        # Verifica que checou disponibilidade
        mock_ollama.list.assert_called()
        mock_langchain_ollama.assert_called_once()
    
    @pytest.mark.unit
    def test_init_custom_params(self, mock_ollama, mock_langchain_ollama):
        """Testa inicialização com parâmetros customizados"""
        llm = OllamaLLM(
            model_name="llama3.2:1b",
            temperature=0.5,
            base_url="http://custom:11434",
            max_tokens=2048
        )
        
        assert llm.temperature == 0.5
        assert llm.base_url == "http://custom:11434"
        assert llm.kwargs["max_tokens"] == 2048
    
    @pytest.mark.unit
    def test_check_ollama_availability_fail(self):
        """Testa quando Ollama não está disponível"""
        with patch('src.llms.ollama_llm.ollama') as mock_ollama:
            mock_ollama.list.side_effect = Exception("Connection refused")
            
            with pytest.raises(ConnectionError) as exc_info:
                OllamaLLM(model_name="test")
            
            assert "Ollama não está disponível" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_model_not_available_pulls(self, mock_ollama, mock_langchain_ollama):
        """Testa download automático quando modelo não está disponível"""
        # Configura para modelo não estar na lista
        models_response = Mock()
        models_response.models = []
        mock_ollama.list.return_value = models_response
        
        llm = OllamaLLM(model_name="new_model:latest")
        
        # Verifica que tentou fazer pull
        mock_ollama.pull.assert_called_once_with("new_model:latest")
    
    @pytest.mark.unit
    def test_model_pull_fails(self, mock_ollama):
        """Testa quando download do modelo falha"""
        models_response = Mock()
        models_response.models = []
        mock_ollama.list.return_value = models_response
        mock_ollama.pull.side_effect = Exception("Download failed")
        
        with pytest.raises(ValueError) as exc_info:
            OllamaLLM(model_name="unavailable_model")
        
        assert "Não foi possível baixar o modelo" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_ask_simple(self, mock_ollama, mock_langchain_ollama):
        """Testa pergunta simples sem contexto"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        # Configura resposta do mock
        llm.llm.invoke.return_value = "This is a test answer"
        
        response = llm.ask("What is Python?")
        
        assert response == "This is a test answer"
        llm.llm.invoke.assert_called_once_with("What is Python?")
    
    @pytest.mark.unit
    def test_ask_with_context(self, mock_ollama, mock_langchain_ollama):
        """Testa pergunta com contexto RAG"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        llm.llm.invoke.return_value = "Answer based on context"
        
        response = llm.ask(
            "What is the function?",
            context="def test(): return 42"
        )
        
        assert response == "Answer based on context"
        
        # Verifica que o prompt foi construído com contexto
        call_args = llm.llm.invoke.call_args[0][0]
        assert "CONTEXTO:" in call_args
        assert "def test(): return 42" in call_args
        assert "What is the function?" in call_args
    
    @pytest.mark.unit
    def test_ask_error_handling(self, mock_ollama, mock_langchain_ollama):
        """Testa tratamento de erros em ask"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        llm.llm.invoke.side_effect = Exception("Model error")
        
        with pytest.raises(Exception) as exc_info:
            llm.ask("Test question")
        
        assert "Erro ao consultar o modelo Ollama" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_ask_with_system_prompt(self, mock_ollama, mock_langchain_ollama):
        """Testa pergunta com system prompt customizado"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        llm.llm.invoke.return_value = "Specialized response"
        
        response = llm.ask_with_system_prompt(
            "Explain recursion",
            "You are a Python expert. Be concise."
        )
        
        assert response == "Specialized response"
        
        call_args = llm.llm.invoke.call_args[0][0]
        assert "You are a Python expert" in call_args
        assert "Explain recursion" in call_args
    
    @pytest.mark.unit
    def test_get_model_info(self, mock_ollama, mock_langchain_ollama):
        """Testa obtenção de informações do modelo"""
        llm = OllamaLLM(
            model_name="llama3.2:1b",
            temperature=0.3,
            base_url="http://test:11434"
        )
        
        info = llm.get_model_info()
        
        assert info["model_name"] == "llama3.2:1b"
        assert info["provider"] == "Ollama (Local)"
        assert info["temperature"] == 0.3
        assert info["base_url"] == "http://test:11434"
    
    @pytest.mark.unit
    def test_update_config(self, mock_ollama, mock_langchain_ollama):
        """Testa atualização de configuração"""
        # Cria uma nova instância mock para evitar conflito
        new_instance = Mock()
        new_instance.invoke.return_value = "Test response"
        mock_langchain_ollama.return_value = new_instance
        
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        # Limpa kwargs antigos que podem causar conflito
        llm.kwargs.pop('temperature', None)
        
        llm.update_config(temperature=0.8, max_tokens=1024)
        
        assert llm.temperature == 0.8
        assert llm.kwargs["max_tokens"] == 1024
        
        # Verifica que reinicializou o modelo
        assert mock_langchain_ollama.call_count == 2
    
    @pytest.mark.unit
    def test_get_available_models(self, mock_ollama, mock_langchain_ollama):
        """Testa listagem de modelos disponíveis"""
        # Configura múltiplos modelos
        model1 = Mock()
        model1.model = "llama3.2:1b"
        model2 = Mock()
        model2.model = "gemma:2b"
        
        models_response = Mock()
        models_response.models = [model1, model2]
        mock_ollama.list.return_value = models_response
        
        llm = OllamaLLM(model_name="llama3.2:1b")
        models = llm.get_available_models()
        
        assert len(models) == 2
        assert "llama3.2:1b" in models
        assert "gemma:2b" in models
    
    @pytest.mark.unit
    def test_download_model(self, mock_ollama, mock_langchain_ollama):
        """Testa download de novo modelo"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        llm.download_model("new_model:latest")
        
        mock_ollama.pull.assert_called_with("new_model:latest")
    
    @pytest.mark.unit
    def test_switch_model(self, mock_ollama, mock_langchain_ollama):
        """Testa troca de modelo"""
        # Configura modelos disponíveis
        model1 = Mock()
        model1.model = "llama3.2:1b"
        model2 = Mock()
        model2.model = "gemma:2b"
        
        models_response = Mock()
        models_response.models = [model1, model2]
        mock_ollama.list.return_value = models_response
        
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        llm.switch_model("gemma:2b")
        
        assert llm.model_name == "gemma:2b"
        # Verifica que reinicializou
        assert mock_langchain_ollama.call_count == 2
    
    @pytest.mark.unit
    def test_switch_model_fails_reverts(self, mock_ollama, mock_langchain_ollama):
        """Testa que modelo volta ao anterior se troca falhar"""
        model1 = Mock()
        model1.model = "llama3.2:1b"
        
        models_response = Mock()
        models_response.models = [model1]
        mock_ollama.list.return_value = models_response
        
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        # Tenta trocar para modelo inexistente
        mock_ollama.pull.side_effect = Exception("Download failed")
        
        with pytest.raises(ValueError):
            llm.switch_model("unavailable_model")
        
        # Verifica que voltou ao modelo original
        assert llm.model_name == "llama3.2:1b"
    
    @pytest.mark.unit
    def test_build_rag_prompt(self, mock_ollama, mock_langchain_ollama):
        """Testa construção do prompt RAG"""
        llm = OllamaLLM(model_name="llama3.2:1b")
        
        prompt = llm._build_rag_prompt(
            "What is the purpose?",
            "def main(): print('Hello')"
        )
        
        assert "assistente especializado em programação" in prompt
        assert "CONTEXTO:" in prompt
        assert "def main(): print('Hello')" in prompt
        assert "PERGUNTA: What is the purpose?" in prompt
        assert "INSTRUÇÕES:" in prompt


class TestCreateOllamaLLM:
    """Testes para função utilitária create_ollama_llm"""
    
    @pytest.mark.unit
    def test_create_ollama_llm(self):
        """Testa criação via função utilitária"""
        with patch('src.llms.ollama_llm.OllamaLLM') as MockOllama:
            mock_instance = Mock()
            MockOllama.return_value = mock_instance
            
            llm = create_ollama_llm(
                model_name="test_model",
                temperature=0.5,
                custom_param="value"
            )
            
            MockOllama.assert_called_once_with(
                model_name="test_model",
                temperature=0.5,
                custom_param="value"
            )
            
            assert llm == mock_instance


@pytest.mark.requires_ollama
class TestOllamaIntegration:
    """Testes de integração que requerem Ollama rodando"""
    
    def test_real_ollama_connection(self):
        """Testa conexão real com Ollama (skip se não estiver rodando)"""
        try:
            import ollama
            ollama.list()
        except:
            pytest.skip("Ollama não está rodando")
        
        # Se chegou aqui, Ollama está rodando
        llm = OllamaLLM(model_name="llama3.2:1b")
        assert llm.llm is not None