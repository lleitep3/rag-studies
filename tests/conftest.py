"""
Configuração global para os testes pytest
==========================================

Define fixtures e configurações compartilhadas entre todos os testes.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
from typing import List

# Adiciona o diretório src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain.docstore.document import Document


@pytest.fixture
def mock_loader():
    """Mock para BaseLoader"""
    loader = Mock()
    loader.load.return_value = [
        Document(
            page_content="def test_function():\n    return 'test'",
            metadata={"source": "test.py", "file_type": "python", "file_size": 100}
        ),
        Document(
            page_content="class TestClass:\n    pass",
            metadata={"source": "class.py", "file_type": "python", "file_size": 50}
        )
    ]
    return loader


@pytest.fixture
def mock_vector_store():
    """Mock para BaseVectorStore"""
    store = Mock()
    store.add_documents.return_value = ["doc_1", "doc_2"]
    
    # Mock do retriever
    retriever = Mock()
    retriever.invoke.return_value = [
        Document(
            page_content="Relevant context for the query",
            metadata={"source": "doc1.py"}
        )
    ]
    store.get_retriever.return_value = retriever
    store.get_collection_stats.return_value = {
        "total_documents": 2,
        "collection_name": "test_collection",
        "status": "active"
    }
    
    return store


@pytest.fixture
def mock_llm():
    """Mock para BaseLLM"""
    llm = Mock()
    llm.model_name = "test_model"
    llm.ask.return_value = "This is a test response from the LLM."
    llm.ask_with_system_prompt.return_value = "Response with system prompt."
    llm.get_model_info.return_value = {
        "model_name": "test_model",
        "provider": "test_provider",
        "temperature": 0.1
    }
    return llm


@pytest.fixture
def mock_ollama_response():
    """Mock para resposta do Ollama"""
    return {
        "model": "llama3.2:1b",
        "created_at": "2024-01-01T00:00:00Z",
        "response": "Test response from Ollama",
        "done": True
    }


@pytest.fixture
def sample_code():
    """Código Python de exemplo para testes"""
    return '''
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        # Armazena senha em texto plano (problema de segurança)
        self.users[username] = password
    
    def authenticate(self, username, password):
        return self.users.get(username) == password
'''


@pytest.fixture
def sample_review_response():
    """Resposta simulada de code review"""
    return """
PROBLEMAS ENCONTRADOS:
- [Segurança] Armazenamento de senha em texto plano (linha 11)
- [Documentação] Falta de type hints nas funções (linha 2)
- [Validação] Ausência de validação de entrada (linha 10)

SUGESTÕES DE MELHORIA:
- [Segurança] Use hash bcrypt ou similar para senhas (linha 11)
- [Documentação] Adicione type hints para melhor clareza
- [Performance] Considere usar cache para autenticação frequente

PONTOS POSITIVOS:
- Estrutura de classe bem organizada
- Nomes de variáveis descritivos
- Separação clara de responsabilidades

RESUMO:
O código apresenta problemas críticos de segurança com o armazenamento de senhas em texto plano. 
Recomenda-se implementar hashing de senhas e adicionar validação de entrada.
"""


@pytest.fixture
def test_documents():
    """Lista de documentos de teste"""
    return [
        Document(
            page_content="Python best practices guide",
            metadata={"source": "guide.md", "file_type": "markdown"}
        ),
        Document(
            page_content="Security guidelines for web applications",
            metadata={"source": "security.md", "file_type": "markdown"}
        ),
        Document(
            page_content="Performance optimization techniques",
            metadata={"source": "performance.py", "file_type": "python"}
        )
    ]


# Configuração de logging para os testes
@pytest.fixture(autouse=True)
def configure_test_logging():
    """Configura logging para os testes"""
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Marca para testes que requerem Ollama
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "requires_ollama: mark test as requiring Ollama server"
    )
    config.addinivalue_line(
        "markers", "requires_chroma: mark test as requiring ChromaDB"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )