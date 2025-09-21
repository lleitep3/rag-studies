"""
Implementação concreta do LLM usando Google Gemini
"""

import os
from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import BaseLLM


class GeminiLLM(BaseLLM):
    """
    Implementação do LLM usando Google Gemini
    
    Esta classe fornece uma interface para interagir com o modelo Gemini
    através do LangChain, com configurações otimizadas para RAG.
    """
    
    def __init__(self, 
                 model_name: str = "gemini-1.5-flash", 
                 temperature: float = 0.1,
                 max_tokens: Optional[int] = None,
                 **kwargs):
        """
        Inicializa o LLM Gemini
        
        Args:
            model_name: Nome do modelo Gemini (ex: "gemini-1.5-flash", "gemini-1.5-pro")
            temperature: Controla a criatividade das respostas (0.0 = determinístico, 1.0 = criativo)
            max_tokens: Número máximo de tokens na resposta (None = sem limite)
            **kwargs: Argumentos adicionais para o ChatGoogleGenerativeAI
        """
        super().__init__(model_name)
        
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Verifica se a API key está configurada
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY não encontrada nas variáveis de ambiente. "
                "Configure sua chave da API do Google no arquivo .env"
            )
        
        # Configurações específicas para RAG
        self.default_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            **kwargs
        }
        
        # Inicializa o modelo
        self._initialize_model()
        
    def _initialize_model(self):
        """Inicializa o modelo ChatGoogleGenerativeAI"""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                **self.default_config
            )
            print(f"✅ Modelo {self.model_name} inicializado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar modelo {self.model_name}: {str(e)}")
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
            
            # Extrai o conteúdo da resposta
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            error_msg = f"Erro ao consultar o modelo: {str(e)}"
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
1. Base sua resposta principalmente no contexto fornecido
2. Se o contexto não contém informação suficiente, indique isso claramente
3. Forneça exemplos de código quando relevante
4. Seja conciso mas completo
5. Use formatação markdown quando apropriado

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
            # Para Gemini, incorporamos o system prompt na mensagem
            full_prompt = f"{system_prompt}\n\nUsuário: {question}"
            
            response = self.llm.invoke(full_prompt)
            
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
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
            "provider": "Google Gemini",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "config": self.default_config
        }
    
    def update_config(self, **kwargs):
        """
        Atualiza configurações do modelo
        
        Args:
            **kwargs: Novas configurações
        """
        self.default_config.update(kwargs)
        
        # Atualiza campos específicos se fornecidos
        if 'temperature' in kwargs:
            self.temperature = kwargs['temperature']
        if 'max_output_tokens' in kwargs:
            self.max_tokens = kwargs['max_output_tokens']
            
        # Re-inicializa o modelo com as novas configurações
        self._initialize_model()
        
        print(f"✅ Configurações do modelo atualizadas: {kwargs}")


# Função utilitária para criar instâncias facilmente
def create_gemini_llm(model_name: str = "gemini-1.5-flash", 
                      temperature: float = 0.1,
                      **kwargs) -> GeminiLLM:
    """
    Função utilitária para criar uma instância do GeminiLLM
    
    Args:
        model_name: Nome do modelo
        temperature: Temperatura do modelo
        **kwargs: Argumentos adicionais
        
    Returns:
        GeminiLLM: Instância configurada
    """
    return GeminiLLM(
        model_name=model_name,
        temperature=temperature,
        **kwargs
    )