"""
Aplicação principal FastAPI.
Ponto de entrada da aplicação que configura e inicia o servidor.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from .routes import router
from .config import config

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Executa código de inicialização e limpeza.
    """
    # Startup
    logger.info("=== Iniciando LLM Chatbot Backend ===")
    logger.info(f"Modo debug: {config.DEBUG}")
    logger.info(f"Modelo LLM: {config.GEMINI_MODEL}")
    
    try:
        # Verifica se o serviço LLM está funcionando
        from .llm_utils import get_llm_health
        health = get_llm_health()
        
        if health.get("status") == "healthy":
            logger.info("✅ Serviço LLM inicializado com sucesso")
        else:
            logger.warning("⚠️ Serviço LLM com problemas - verifique configurações")
            
    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
    
    yield
    
    # Shutdown
    logger.info("=== Finalizando aplicação ===")


# Cria instância do FastAPI
app = FastAPI(
    title="LLM Chatbot Backend",
    description="""
    Backend para chatbot usando LlamaIndex e Gemini SDK.
    
    ## Funcionalidades
    
    * **Chat**: Endpoint para conversar com o chatbot
    * **Health Check**: Verificação de status dos serviços
    * **Documentação**: Interface Swagger automática
    
    ## Como usar
    
    1. Configure sua API key do Gemini no arquivo `.env`
    2. Execute `python app/index_builder.py` para criar o índice
    3. Inicie o servidor com `uvicorn app.main:app --reload`
    4. Acesse `/docs` para testar a API
    """,
    version="1.0.0",
    contact={
        "name": "Equipe de Desenvolvimento",
        "url": "https://github.com/seu-usuario/seu-repo",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://localhost:8080",  # Vue development server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:3001",  # Porta alternativa Next.js
        "*",  # Permite todas as origens em desenvolvimento
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas da aplicação
app.include_router(router, prefix="/api/v1")

# Adiciona rotas diretamente no app para compatibilidade
app.include_router(router)


# Handler global para exceções não tratadas
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global para capturar exceções não tratadas.
    
    Args:
        request: Requisição HTTP
        exc: Exceção capturada
        
    Returns:
        Resposta JSON com erro
    """
    logger.error(f"Exceção não tratada: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "detail": "Ocorreu um erro inesperado. Tente novamente." if not config.DEBUG else str(exc),
            "status": "error"
        }
    )


# Função para executar a aplicação
def run_server():
    """Função para executar o servidor programaticamente."""
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    run_server()
