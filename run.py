#!/usr/bin/env python3
"""
Script de execução simples para o LLM Chatbot Backend.
Usado para iniciar a aplicação localmente ou em produção.
"""

if __name__ == "__main__":
    from app.main import run_server
    run_server()