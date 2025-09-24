"""
Definição das rotas da API FastAPI.
Responsável por definir todos os endpoints disponíveis na aplicação.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging

from .llm_utils import query_llm, get_llm_health
from .chart_generator import generate_chart
from .advanced_chart_generator_fixed import AdvancedChartGeneratorFixed
from .data_analyzer import DataAnalyzer
from .advanced_data_analyzer_fixed import AdvancedDataAnalyzerFixed

# Configuração de logging
logger = logging.getLogger(__name__)

# Cria router para agrupar rotas
router = APIRouter()

# Inicializa analisador de dados
data_analyzer = DataAnalyzer()

# Inicializa gerador avançado de gráficos (versão melhorada)
advanced_chart_generator = AdvancedChartGeneratorFixed()

# Inicializa analisador avançado de dados com dados reais
advanced_data_analyzer = AdvancedDataAnalyzerFixed()


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


class AnalysisResponse(BaseModel):
    """Modelo para resposta de análise com gráficos."""
    analysis: str = Field(
        ...,
        description="Texto da análise gerada",
        example="Análise detalhada dos dados do setor petrolífero..."
    )
    charts: List[Dict[str, Any]] = Field(
        default=[],
        description="Lista de gráficos gerados com tipo e base64",
        example=[{"type": "line", "base64": "iVBORw0KGgoAAAANS...", "description": "Gráfico de linha"}]
    )
    data_summary: Dict[str, Any] = Field(
        default={},
        description="Resumo dos dados utilizados na análise"
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


class ChartResponse(BaseModel):
    """Modelo para resposta de geração de gráfico."""
    chart_base64: str = Field(
        ...,
        description="Imagem do gráfico em base64"
    )
    chart_type: str = Field(
        ...,
        description="Tipo do gráfico gerado"
    )
    data_summary: Dict[str, Any] = Field(
        ...,
        description="Resumo dos dados utilizados"
    )
    status: str = Field(
        default="success",
        description="Status da operação"
    )


class AnalysisRequest(BaseModel):
    """Modelo para requisição de análise com gráficos."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Pergunta do usuário para análise",
        example="Analise a distribuição de investimentos das empresas de petróleo em Angola"
    )
    chart_types: Optional[List[str]] = Field(
        default=["pie", "bar"],
        description="Tipos de gráficos desejados",
        example=["pie", "bar", "line"]
    )
    analysis_type: Optional[str] = Field(
        default="comprehensive",
        description="Tipo de análise: 'comprehensive', 'financial', 'operational', 'market'"
    )


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


@router.post(
    "/analyze",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Pergunta inválida"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
    summary="Análise com Gráficos",
    description="Realiza análise completa com geração de gráficos baseados nos dados disponíveis."
)
async def analyze_endpoint(payload: AnalysisRequest) -> ChatResponse:
    """
    Endpoint para análise com geração de gráficos.
    
    Args:
        payload: Dados da requisição contendo a pergunta e tipos de gráficos
        
    Returns:
        Resposta com análise e gráficos em base64
        
    Raises:
        HTTPException: Para erros de validação ou processamento
    """
    try:
        logger.info(f"Nova análise recebida: {payload.question[:50]}...")
        
        # Valida se a pergunta não está vazia após strip
        question = payload.question.strip()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pergunta não pode estar vazia"
            )
        
        # Analisa os dados disponíveis usando o analisador avançado
        analysis_data = advanced_data_analyzer.analyze_data(question, payload.analysis_type)
        
        if not analysis_data:
            # Fallback para resposta normal se não houver dados suficientes
            answer = query_llm(question, [])
            return ChatResponse(answer=answer)
        
        # Gera gráficos solicitados - usando gerador avançado para tipos específicos
        charts = []
        requested_chart_types = payload.chart_types or ['bar']
        
        for chart_type in requested_chart_types:
            try:
                chart_data = analysis_data.get('data', {})
                chart_title = analysis_data.get('title', 'Análise de Dados')
                chart_subtitle = analysis_data.get('subtitle', '')
                
                # Usar gerador avançado para tipos específicos
                if chart_type == 'line':
                    # Para gráficos de linha com análise de tendência
                    dates = analysis_data.get('dates', list(chart_data.keys()) if chart_data else [])
                    chart_base64 = advanced_chart_generator.create_advanced_line_chart(
                        data={'Série Principal': list(chart_data.values())},
                        dates=dates,
                        title=chart_title,
                        subtitle=chart_subtitle,
                        show_trend=True,
                        show_forecast=True
                    )
                elif chart_type == 'kpi':
                    # Para dashboard de KPIs
                    kpis = analysis_data.get('kpis', {
                        'Produção': {'current': 85.5, 'target': 90.0, 'status': 'good'},
                        'Eficiência': {'current': 78.2, 'target': 80.0, 'status': 'moderate'},
                        'Investimento': {'current': 92.1, 'target': 85.0, 'status': 'excellent'}
                    })
                    chart_base64 = advanced_chart_generator.create_kpi_dashboard(
                        kpis=kpis,
                        title=f"KPIs - {chart_title}"
                    )
                elif chart_type == 'production':
                    # Para análise de produção
                    production_data = analysis_data.get('production_data', chart_data)
                    dates = analysis_data.get('dates', list(chart_data.keys()) if chart_data else [])
                    chart_base64 = advanced_chart_generator.create_production_analysis_chart(
                        production_data=production_data,
                        time_periods=dates,
                        title=f"Análise de Produção - {chart_title}"
                    )
                elif chart_type == 'financial':
                    # Para análise financeira
                    financial_data = analysis_data.get('financial_data', chart_data)
                    periods = analysis_data.get('dates', list(chart_data.keys()) if chart_data else [])
                    chart_base64 = advanced_chart_generator.create_financial_performance_chart(
                        financial_data=financial_data,
                        periods=periods
                    )
                else:
                    # Usar gerador padrão para outros tipos
                    chart_base64 = generate_chart(
                        chart_type=chart_type,
                        data=chart_data,
                        title=chart_title,
                        subtitle=chart_subtitle
                    )
                
                charts.append({
                    'type': chart_type,
                    'base64': chart_base64,
                    'description': f"Gráfico {chart_type} gerado com análise avançada"
                })
                
            except Exception as e:
                logger.warning(f"Erro ao gerar gráfico {chart_type}: {e}")
                charts.append({
                    'type': chart_type,
                    'base64': None,
                    'description': f"Erro ao gerar gráfico {chart_type}: {str(e)}"
                })
        
        # Gera análise textual contextual profunda
        contextual_analysis = analysis_data.get('contextual_analysis', {})
        kpis = analysis_data.get('kpis', {})
        trends = analysis_data.get('trends', {})
        recommendations = analysis_data.get('recommendations', [])
        
        # Constrói análise textual com insights profundos
        analysis_text = f"""
## {contextual_analysis.get('title', 'Análise de Dados')}

{contextual_analysis.get('subtitle', '')}

### 📋 Resumo Executivo
{contextual_analysis.get('executive_summary', 'Análise indisponível.')}

### 🔍 Principais Insights
"""
        
        # Adiciona insights principais
        key_insights = contextual_analysis.get('key_insights', [])
        for insight in key_insights:
            analysis_text += f"- {insight}\n"
        
        # Adiciona análise competitiva se disponível
        competitive_analysis = contextual_analysis.get('competitive_analysis', '')
        if competitive_analysis:
            analysis_text += f"\n### 🏆 Análise Competitiva\n{competitive_analysis}\n"
        
        # Adiciona análise de riscos se disponível
        risk_assessment = contextual_analysis.get('risk_assessment', '')
        if risk_assessment:
            analysis_text += f"\n### ⚠️ Análise de Riscos\n{risk_assessment}\n"
        
        # Adiciona KPIs
        if kpis:
            analysis_text += "\n### 📊 KPIs Principais\n"
            for kpi_name, kpi_data in kpis.items():
                status_emoji = {
                    'excellent': '🟢',
                    'good': '🟡',
                    'moderate': '🟠',
                    'needs_improvement': '🔴',
                    'high': '🔵',
                    'low': '⚫'
                }.get(kpi_data.get('status', ''), '⚪')
                
                analysis_text += f"- **{kpi_name.replace('_', ' ').title()}:** "
                analysis_text += f"{kpi_data.get('current', 0):.1f}"
                if 'target' in kpi_data:
                    analysis_text += f" (meta: {kpi_data['target']:.1f})"
                analysis_text += f" {status_emoji}\n"
        
        # Adiciona tendências
        if any(trends.values()):
            analysis_text += "\n### 📈 Tendências Identificadas\n"
            
            if trends.get('short_term'):
                analysis_text += "**Curto Prazo:**\n"
                for trend in trends['short_term']:
                    analysis_text += f"- {trend}\n"
            
            if trends.get('medium_term'):
                analysis_text += "**Médio Prazo:**\n"
                for trend in trends['medium_term']:
                    analysis_text += f"- {trend}\n"
            
            if trends.get('long_term'):
                analysis_text += "**Longo Prazo:**\n"
                for trend in trends['long_term']:
                    analysis_text += f"- {trend}\n"
        
        # Adiciona recomendações
        if recommendations:
            analysis_text += "\n### 💡 Recomendações Estratégicas\n"
            for rec in recommendations:
                analysis_text += f"- **{rec.get('category', 'Geral')}** (Prioridade: {rec.get('priority', 'Média')}): "
                analysis_text += f"{rec.get('recommendation', '')}\n"
                if 'impact' in rec:
                    analysis_text += f"  Impacto: {rec['impact']}\n"
        
        # Adiciona rodapé com confiança
        confidence = contextual_analysis.get('confidence', 0.8)
        analysis_text += f"\n---\n*Confiança da análise: {confidence*100:.0f}%*"
        
        analysis_text = analysis_text.strip()
        
        # Prepara resumo dos dados com informações completas
        data_summary = {
            "total_items": len(analysis_data.get('data', {})),
            "category": analysis_data.get('analysis_category', 'general'),
            "title": analysis_data.get('title', ''),
            "subtitle": analysis_data.get('subtitle', ''),
            "context": analysis_data.get('contextual_analysis', {}),
            "kpis": analysis_data.get('kpis', {}),
            "trends": analysis_data.get('trends', {}),
            "recommendations": len(analysis_data.get('recommendations', [])),
            "confidence": analysis_data.get('contextual_analysis', {}).get('confidence', 0.8),
            "metadata": analysis_data.get('metadata', {})
        }
        
        logger.info("Análise com gráficos gerada com sucesso")
        
        # Formata a resposta para compatibilidade com o frontend
        # O frontend espera o campo 'answer' com a análise e gráficos combinados
        formatted_answer = analysis_text
        
        # Adiciona os gráficos à resposta se houverem
        if charts:
            formatted_answer += "\n\n### 📊 Visualizações:\n"
            for i, chart in enumerate(charts, 1):
                if chart.get('base64'):
                    formatted_answer += f"\n**Gráfico {i}:** {chart['description']}\n"
                    formatted_answer += f"![Gráfico {chart['type']}](data:image/png;base64,{chart['base64']})\n"
        
        # Retorna no formato compatível com o frontend (usando ChatResponse)
        return ChatResponse(answer=formatted_answer)
        
    except HTTPException:
        # Re-raise HTTPExceptions
        raise
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Erro no endpoint de análise: {error_message}")
        
        # Fallback para resposta normal
        try:
            answer = query_llm(payload.question, [])
            return ChatResponse(answer=answer)
        except Exception as fallback_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro na análise: {error_message}"
            )

    def _generate_default_kpis(self, data: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Gera KPIs padrão com base nos dados disponíveis."""
        try:
            values = list(data.values())
            total = sum(values)
            
            # KPIs padrão do setor petrolífero
            kpis = {
                'production_efficiency': {
                    'current': 82.5,
                    'target': 85.0,
                    'trend': 'up'
                },
                'operational_cost_ratio': {
                    'current': 28.3,
                    'target': 30.0,
                    'trend': 'down'
                },
                'safety_incident_rate': {
                    'current': 0.8,
                    'target': 0.5,
                    'trend': 'stable'
                },
                'environmental_compliance': {
                    'current': 96.2,
                    'target': 95.0,
                    'trend': 'up'
                },
                'equipment_availability': {
                    'current': 89.7,
                    'target': 90.0,
                    'trend': 'up'
                }
            }
            
            # Ajustar KPIs baseados nos dados
            if total > 0:
                # Adicionar métrica de distribuição
                kpis['revenue_distribution'] = {
                    'current': max(values) / total * 100,
                    'target': 25.0,
                    'trend': 'up' if max(values) / total > 0.3 else 'down'
                }
            
            return kpis
            
        except Exception:
            return {
                'production_efficiency': {'current': 80.0, 'target': 85.0, 'trend': 'stable'},
                'operational_cost_ratio': {'current': 30.0, 'target': 30.0, 'trend': 'stable'}
            }


@router.post(
    "/generate-chart",
    response_model=ChartResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Dados inválidos"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"},
    },
    summary="Gerar Gráfico",
    description="Gera um gráfico específico com base nos dados fornecidos."
)
async def generate_chart_endpoint(
    payload: Dict[str, Any]
) -> ChartResponse:
    """
    Endpoint para geração de gráficos individuais.
    
    Args:
        payload: Dicionário com chart_type, data, title, subtitle e outros parâmetros
        
    Returns:
        Gráfico gerado em base64
        
    Raises:
        HTTPException: Para erros de validação ou processamento
    """
    try:
        # Extrai parâmetros do payload
        chart_type = payload.get('chart_type', 'bar')
        data = payload.get('data', {})
        title = payload.get('title', 'Gráfico de Dados')
        subtitle = payload.get('subtitle', '')
        
        logger.info(f"Gerando gráfico do tipo: {chart_type}")
        
        # Valida dados
        if not data or not isinstance(data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados inválidos fornecidos"
            )
        
        # Valida tipo de gráfico
        valid_chart_types = ['pie', 'bar', 'line', 'donut', 'dashboard']
        if chart_type not in valid_chart_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de gráfico inválido. Use: {', '.join(valid_chart_types)}"
            )
        
        # Gera gráfico
        chart_base64 = generate_chart(
            chart_type=chart_type,
            data=data,
            title=title,
            subtitle=subtitle
        )
        
        logger.info("Gráfico gerado com sucesso")
        
        return ChartResponse(
            chart_base64=chart_base64,
            chart_type=chart_type,
            data_summary={
                "labels": list(data.keys()),
                "values": list(data.values()),
                "count": len(data)
            },
            status="success"
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions
        raise
        
    except Exception as e:
        error_message = str(e)
        logger.error(f"Erro ao gerar gráfico: {error_message}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar gráfico: {error_message}"
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
        "message": "LLM Chatbot Backend API com Análise e Gráficos",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "chat": "/chat",
        "analyze": "/analyze",
        "generate-chart": "/generate-chart",
        "features": [
            "Chat com contexto empresarial",
            "Análise com gráficos interativos",
            "Geração de visualizações profissionais",
            "Suporte para múltiplos tipos de gráficos"
        ]
    }
