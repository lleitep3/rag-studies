"""
Implementação concreta do LLM usando Ollama (modelos locais)
"""

import ollama
from typing import Dict, Any, List
from langchain_ollama import OllamaLLM as LangChainOllamaLLM
from .base import BaseLLM


class OllamaLLM(BaseLLM):
    """
    Implementação do LLM usando Ollama (execução local)
    
    Esta classe fornece uma interface para interagir com modelos locais
    via Ollama, oferecendo uma alternativa sem limites de quota.
    """
    
    def __init__(self, 
                 model_name: str = "llama3.2:1b",
                 base_url: str = "http://localhost:11434",
                 temperature: float = 0.1,
                 **kwargs):
        """
        Inicializa o LLM Ollama
        
        Args:
            model_name: Nome do modelo Ollama (ex: "llama3.2:1b", "gemma3:4b")
            base_url: URL base do servidor Ollama
            temperature: Controla a criatividade das respostas
            **kwargs: Argumentos adicionais para o OllamaLLM
        """
        super().__init__(model_name)
        
        self.base_url = base_url
        self.temperature = temperature
        self.kwargs = kwargs
        
        # Verifica se o Ollama está rodando e o modelo existe
        self._check_ollama_availability()
        self._check_model_availability()
        
        # Inicializa o modelo
        self._initialize_model()
    
    def _check_ollama_availability(self):
        """Verifica se o servidor Ollama está rodando"""
        try:
            # Tenta fazer uma chamada simples para verificar se o servidor está up
            ollama.list()
            print("✅ Servidor Ollama está rodando")
        except Exception as e:
            raise ConnectionError(
                f"Ollama não está disponível. "
                f"Certifique-se de que o Ollama está rodando com: ollama serve\n"
                f"Erro: {str(e)}"
            )
    
    def _check_model_availability(self):
        """Verifica se o modelo está disponível localmente"""
        try:
            models = ollama.list()
            model_names = [model.model for model in models.models]
            
            if self.model_name not in model_names:
                print(f"⚠️ Modelo '{self.model_name}' não encontrado localmente.")
                print(f"📥 Tentando fazer download do modelo...")
                
                try:
                    # Tenta fazer pull do modelo
                    ollama.pull(self.model_name)
                    print(f"✅ Modelo '{self.model_name}' baixado com sucesso")
                except Exception as e:
                    available_models = ", ".join(model_names)
                    raise ValueError(
                        f"Não foi possível baixar o modelo '{self.model_name}'. "
                        f"Modelos disponíveis: {available_models}\n"
                        f"Erro: {str(e)}"
                    )
            else:
                print(f"✅ Modelo '{self.model_name}' encontrado localmente")
                
        except Exception as e:
            if "not found" not in str(e).lower():
                print(f"❌ Erro ao verificar modelos: {str(e)}")
                raise
    
    def _initialize_model(self):
        """Inicializa o modelo OllamaLLM"""
        try:
            self.llm = LangChainOllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=self.temperature,
                **self.kwargs
            )
            print(f"✅ Modelo Ollama '{self.model_name}' inicializado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar modelo Ollama: {str(e)}")
            raise
    
    def ask(self, question: str, context: str = "") -> str:
        """
        Faz uma pergunta ao modelo LLM
        
        Args:
            question: Pergunta a ser feita
            context: Contexto adicional (usado em RAG)
            
        Returns:
            str: Resposta do modelo
        """
        try:
            # Monta o prompt completo
            if context:
                prompt = self._build_rag_prompt(question, context)
            else:
                prompt = question
            
            # Faz a chamada para o modelo
            response = self.llm.invoke(prompt)
            
            return response
            
        except Exception as e:
            error_msg = f"Erro ao consultar o modelo Ollama: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def _build_rag_prompt(self, question: str, context: str) -> str:
        """
        Constrói um prompt otimizado para RAG
        
        Args:
            question: Pergunta do usuário
            context: Contexto recuperado do vector store
            
        Returns:
            str: Prompt formatado para RAG
        """
        prompt = f"""Você é um assistente especializado em programação e desenvolvimento de software.
Use o contexto fornecido abaixo para responder à pergunta do usuário de forma precisa e útil.

CONTEXTO:
{context}

PERGUNTA: {question}

INSTRUÇÕES:
- Base sua resposta principalmente no contexto fornecido
- Se o contexto não contém informação suficiente, indique isso claramente
- Forneça exemplos de código quando relevante
- Seja conciso mas completo
- Use formatação markdown quando apropriado

RESPOSTA:"""

        return prompt
    
    def ask_with_system_prompt(self, question: str, system_prompt: str) -> str:
        """
        Faz uma pergunta com um system prompt customizado
        
        Args:
            question: Pergunta do usuário
            system_prompt: Prompt de sistema personalizado
            
        Returns:
            str: Resposta do modelo
        """
        try:
            # Para Ollama, incorporamos o system prompt na mensagem
            full_prompt = f"{system_prompt}\n\nUsuário: {question}\n\nAssistente:"
            
            response = self.llm.invoke(full_prompt)
            return response
            
        except Exception as e:
            error_msg = f"Erro ao consultar o modelo com system prompt: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o modelo atual
        
        Returns:
            Dict com informações do modelo
        """
        return {
            "model_name": self.model_name,
            "provider": "Ollama (Local)",
            "base_url": self.base_url,
            "temperature": self.temperature,
            "kwargs": self.kwargs
        }
    
    def update_config(self, **kwargs):
        """
        Atualiza configurações do modelo
        
        Args:
            **kwargs: Novas configurações
        """
        # Atualiza campos específicos se fornecidos
        if 'temperature' in kwargs:
            self.temperature = kwargs.pop('temperature')
        if 'base_url' in kwargs:
            self.base_url = kwargs.pop('base_url')
            
        # Atualiza kwargs restantes (sem temperature e base_url)
        self.kwargs.update(kwargs)
        
        # Re-inicializa o modelo com as novas configurações
        self._initialize_model()
        
        print(f"✅ Configurações do modelo Ollama atualizadas")
    
    def get_available_models(self) -> List[str]:
        """
        Retorna lista de modelos disponíveis no Ollama
        
        Returns:
            List[str]: Nomes dos modelos disponíveis
        """
        try:
            models = ollama.list()
            return [model.model for model in models.models]
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {str(e)}")
            return []
    
    def download_model(self, model_name: str):
        """
        Baixa um modelo do repositório Ollama
        
        Args:
            model_name: Nome do modelo para baixar
        """
        try:
            print(f"📥 Baixando modelo '{model_name}'...")
            ollama.pull(model_name)
            print(f"✅ Modelo '{model_name}' baixado com sucesso")
        except Exception as e:
            error_msg = f"Erro ao baixar modelo '{model_name}': {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def switch_model(self, model_name: str):
        """
        Muda para outro modelo
        
        Args:
            model_name: Nome do novo modelo
        """
        old_model = self.model_name
        self.model_name = model_name
        
        try:
            self._check_model_availability()
            self._initialize_model()
            print(f"✅ Modelo mudou de '{old_model}' para '{model_name}'")
        except Exception as e:
            # Reverte para o modelo anterior em caso de erro
            self.model_name = old_model
            raise


# Função utilitária para criar instâncias facilmente
def create_ollama_llm(model_name: str = "llama3.2:1b", 
                      temperature: float = 0.1,
                      **kwargs) -> OllamaLLM:
    """
    Função utilitária para criar uma instância do OllamaLLM
    
    Args:
        model_name: Nome do modelo
        temperature: Temperatura do modelo
        **kwargs: Argumentos adicionais
        
    Returns:
        OllamaLLM: Instância configurada
    """
    return OllamaLLM(
        model_name=model_name,
        temperature=temperature,
        **kwargs
    )