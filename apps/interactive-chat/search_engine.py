#!/usr/bin/env python3
"""
🔍 Search Engine
================

Motor de busca para encontrar contexto relevante nos documentos carregados.
Implementa busca por palavras-chave e pontuação por relevância.
"""

from typing import List, Dict, Any, Tuple
from langchain.schema import Document


class SimpleSearchEngine:
    """Motor de busca simples baseado em palavras-chave e pontuação"""
    
    def __init__(self, documents: List[Document]):
        """Inicializa com lista de documentos"""
        self.documents = documents
        
        # Palavras-chave para diferentes componentes
        self.keyword_mapping = {
            'loader': ['loader', 'load', 'document', 'python', 'carregar'],
            'llm': ['llm', 'model', 'gemini', 'ollama', 'pergunta', 'resposta', 'ask'],
            'vector': ['vector', 'store', 'chroma', 'embedding', 'retriever'],
            'engine': ['engine', 'rag', 'pipeline', 'setup'],
            'base': ['base', 'abstract', 'interface', 'herdar'],
            'config': ['config', 'configuration', 'yaml', 'settings'],
            'factory': ['factory', 'get_', 'create', 'build']
        }
    
    def find_relevant_context(self, question: str, max_docs: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Busca contexto relevante para a pergunta
        
        Args:
            question: Pergunta do usuário
            max_docs: Máximo de documentos a retornar
            
        Returns:
            Tupla com (contexto_concatenado, lista_de_fontes)
        """
        if not self.documents:
            return "", []
            
        question_lower = question.lower()
        doc_scores = []
        
        for doc in self.documents:
            score = self._calculate_relevance_score(question_lower, doc)
            file_path = doc.metadata.get('source', 'N/A')
            doc_scores.append((doc, score, file_path))
        
        # Ordena por pontuação e pega os top N
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        top_docs = doc_scores[:max_docs]
        
        # Prepara contexto e fontes
        context_parts = []
        sources = []
        
        for i, (doc, score, file_path) in enumerate(top_docs, 1):
            if score > 0:  # Só inclui documentos com alguma relevância
                context_parts.append(f"[ARQUIVO {i}: {file_path}]\n{doc.page_content}")
                sources.append({
                    'index': i,
                    'file': file_path,
                    'score': score,
                    'lines': len(doc.page_content.split('\n')),
                    'preview': self._get_preview(doc.page_content)
                })
        
        context = "\n\n".join(context_parts)
        return context, sources
    
    def _calculate_relevance_score(self, question_lower: str, doc: Document) -> int:
        """Calcula pontuação de relevância para um documento"""
        score = 0
        content_lower = doc.page_content.lower()
        file_path = doc.metadata.get('source', '').lower()
        
        # Pontuação por palavra-chave na pergunta
        for word in question_lower.split():
            if len(word) > 2:  # Ignora palavras muito pequenas
                word_count = content_lower.count(word)
                score += word_count * 2
        
        # Bonus por tipo de arquivo relevante
        for component, keywords in self.keyword_mapping.items():
            if any(kw in question_lower for kw in keywords):
                if component in file_path:
                    score += 15
        
        # Bonus por tamanho (arquivos maiores tendem a ser mais informativos)
        score += len(content_lower) // 1000
        
        # Bonus por presença de classes/funções importantes
        important_patterns = ['class ', 'def ', 'import ', 'from ']
        for pattern in important_patterns:
            score += content_lower.count(pattern)
        
        return score
    
    def _get_preview(self, content: str, max_chars: int = 150) -> str:
        """Gera preview do conteúdo"""
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "..."
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos documentos"""
        if not self.documents:
            return {
                'total_docs': 0,
                'total_lines': 0,
                'total_chars': 0,
                'files': []
            }
        
        total_lines = sum(len(doc.page_content.split('\n')) for doc in self.documents)
        total_chars = sum(len(doc.page_content) for doc in self.documents)
        
        files = []
        for doc in self.documents:
            files.append({
                'path': doc.metadata.get('source', 'N/A'),
                'lines': len(doc.page_content.split('\n')),
                'chars': len(doc.page_content),
                'size': doc.metadata.get('file_size', 0)
            })
        
        return {
            'total_docs': len(self.documents),
            'total_lines': total_lines,
            'total_chars': total_chars,
            'files': files
        }
    
    def search_by_keywords(self, keywords: List[str], max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Busca documentos que contenham palavras-chave específicas
        
        Args:
            keywords: Lista de palavras-chave
            max_results: Máximo de resultados
            
        Returns:
            Lista de documentos encontrados com metadados
        """
        results = []
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            file_path = doc.metadata.get('source', 'N/A')
            
            matches = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    matches += content_lower.count(keyword.lower())
                    matched_keywords.append(keyword)
            
            if matches > 0:
                results.append({
                    'file': file_path,
                    'matches': matches,
                    'matched_keywords': matched_keywords,
                    'lines': len(doc.page_content.split('\n')),
                    'preview': self._get_preview(doc.page_content)
                })
        
        # Ordena por número de matches
        results.sort(key=lambda x: x['matches'], reverse=True)
        return results[:max_results]


def demo():
    """Demonstração do motor de busca"""
    print("\n🔍 Demonstração do Search Engine")
    print("=" * 40)
    
    # Simula alguns documentos
    fake_docs = [
        Document(
            page_content="""
class PythonLoader(BaseLoader):
    def load(self, path: str) -> List[Document]:
        # Carrega arquivos Python
        pass
            """,
            metadata={'source': 'src/loaders/python_loader.py', 'file_size': 1024}
        ),
        Document(
            page_content="""
class GeminiLLM(BaseLLM):
    def ask(self, question: str) -> str:
        # Usa Google Gemini
        pass
            """,
            metadata={'source': 'src/llms/gemini_llm.py', 'file_size': 2048}
        )
    ]
    
    engine = SimpleSearchEngine(fake_docs)
    
    # Testa busca
    context, sources = engine.find_relevant_context("Como funciona o PythonLoader?")
    
    print(f"Contexto encontrado: {len(context)} caracteres")
    print(f"Fontes: {len(sources)}")
    
    for source in sources:
        print(f"  - {source['file']} (score: {source['score']})")
    
    # Estatísticas
    stats = engine.get_statistics()
    print(f"\nEstatísticas:")
    print(f"  Total de documentos: {stats['total_docs']}")
    print(f"  Total de linhas: {stats['total_lines']}")


if __name__ == "__main__":
    demo()