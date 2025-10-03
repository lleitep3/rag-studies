"""
Módulo de Capacidades do RAG
============================

Este módulo contém diferentes capacidades que podem ser aplicadas usando
a infraestrutura RAG. Cada capacidade é um componente especializado que:

1. Usa a infraestrutura RAG existente
2. Tem um propósito específico e bem definido
3. Implementa prompts e lógica especializados
4. Pode ser combinada com outras capacidades
"""

from .base import BaseCapacity

__all__ = ["BaseCapacity"]
