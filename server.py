#!/usr/bin/env python3
"""
Servidor de produção para o LLM Chatbot Backend.
Este arquivo é usado para iniciar a aplicação em ambientes de produção.
"""

import os
import uvicorn
from app.config import config

def main():
    """Inicia o servidor FastAPI usando uvicorn."""
    
    # Para produção, força algumas configurações
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    
    print(f"🚀 Iniciando servidor na porta {port}...")
    print(f"🔧 Host: {host}")
    print(f"🐞 Debug: {config.DEBUG}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # Desabilitado em produção
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
