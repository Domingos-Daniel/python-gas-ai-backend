"""
Definição das rotas da API FastAPI.
Responsável por definir todos os endpoints disponíveis na aplicação.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import logging

from .llm_utils import query_llm, get_llm_health

# Configuração de logging
logger = logging.getLogger(__name__)

# Cria router para agrupar rotas
router = APIRouter()


# ===== MODELOS PYDANTIC =====

class ChatRequest(BaseModel):
    """Modelo para requisição de chat."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Pergunta do usuário para o chatbot",
        example="Quais são os principais serviços da Total?"
    )
    history: Optional[list] = Field(
        default=[],
        description="Histórico de mensagens da conversa",
        example=[
            {"role": "user", "content": "Me fale sobre o ANPG"},
            {"role": "assistant", "content": "O ANPG é a Agência Nacional..."}
        ]
    )


class ChatResponse(BaseModel):
    """Modelo para resposta de chat."""
    answer: str = Field(
        ...,
        description="Resposta gerada pelo chatbot",
        example="A Total oferece diversos serviços na área de energia..."
    )
    status: str = Field(
        default="success",
        description="Status da operação",
        example="success"
    )


class HealthResponse(BaseModel):
    """Modelo para resposta de health check."""
    status: str = Field(..., description="Status geral da aplicação")
    llm_service: dict = Field(..., description="Status do serviço LLM")
    message: str = Field(..., description="Mensagem descritiva")


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro."""
    error: str = Field(..., description="Descrição do erro")
    status: str = Field(default="error", description="Status da operação")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")


# ===== ENDPOINTS =====

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Pergunta inválida"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
    summary="Consulta ao Chatbot",
    description="Envia uma pergunta para o chatbot e recebe uma resposta baseada no conhecimento indexado."
)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Endpoint principal para interação com o chatbot.
    
    Args:
        payload: Dados da requisição contendo a pergunta e histórico
        
    Returns:
        Resposta do chatbot
        
    Raises:
        HTTPException: Para erros de validação ou processamento
    """
    try:
        logger.info(f"Nova pergunta recebida: {payload.question[:50]}...")
        
        # Valida se a pergunta não está vazia após strip
        question = payload.question.strip()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pergunta não pode estar vazia"
            )
        
        # Processa pergunta usando LLM com histórico
        answer = query_llm(question, payload.history)
        
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Não foi possível gerar uma resposta"
            )
        
        logger.info("Resposta gerada com sucesso")
        
        return ChatResponse(
            answer=answer,
            status="success"
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions
        raise
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Erro no endpoint de chat: {error_message}")
        
        # Tratamento específico para diferentes tipos de erro
        if "quota" in error_message.lower() or "rate limit" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisições excedido. Tente novamente em alguns minutos."
            )
        elif "autenticação" in error_message.lower() or "api key" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Erro de autenticação. Verifique a configuração da API."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno: {error_message}"
            )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica o status de saúde da aplicação e seus componentes."
)
async def health_check() -> HealthResponse:
    """
    Endpoint para verificação de saúde da aplicação.
    
    Returns:
        Status detalhado da aplicação
    """
    try:
        # Verifica status do serviço LLM
        llm_health = get_llm_health()
        
        # Determina status geral
        overall_status = "healthy" if llm_health.get("status") == "healthy" else "degraded"
        
        # Mensagem baseada no status
        if overall_status == "healthy":
            message = "Todos os serviços estão funcionando normalmente"
        else:
            message = "Alguns serviços podem estar com problemas"
        
        logger.info(f"Health check executado: {overall_status}")
        
        return HealthResponse(
            status=overall_status,
            llm_service=llm_health,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return HealthResponse(
            status="unhealthy",
            llm_service={"status": "error", "error": str(e)},
            message="Erro ao verificar status da aplicação"
        )


@router.get(
    "/",
    summary="Root Endpoint",
    description="Endpoint raiz da API com informações básicas."
)
async def root():
    """
    Endpoint raiz da API.
    
    Returns:
        Informações básicas sobre a API
    """
    return {
        "message": "LLM Chatbot Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "chat": "/chat"
    }
