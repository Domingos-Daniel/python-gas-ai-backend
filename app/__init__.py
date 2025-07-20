"""
LLM Chatbot Backend Package
===========================

Backend modular para chatbot usando FastAPI, LlamaIndex e Gemini SDK.

Módulos principais:
- main: Aplicação FastAPI principal
- routes: Definição de endpoints
- llm_utils: Integração LLM e processamento
- config: Configurações da aplicação
- index_builder: Construção do índice de documentos
- scraper: Coleta automática de dados (opcional)
"""

__version__ = "1.0.0"
__author__ = "Equipe de Desenvolvimento"

# Permite execução direta do módulo
if __name__ == "__main__":
    from .main import run_server
    run_server()
