"""
Módulo utilitário para LLM (Large Language Model).
Integração com Angola Energy Prompt System para consultas especializadas.
"""
from typing import Optional
import logging
from pathlib import Path
import time
import json
from functools import wraps
from .angola_energy_prompts import angola_energy_prompts

try:
    import google.generativeai as genai
    from google.api_core import exceptions as google_exceptions
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    google_exceptions = None

from .config import config

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting global
last_request_time = 0
request_count = 0
request_times = []


def rate_limit_decorator(func):
    """Decorator para implementar rate limiting."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_request_time, request_count, request_times
        
        current_time = time.time()
        
        # Remove requisições antigas (mais de 1 minuto)
        request_times = [t for t in request_times if current_time - t < 60]
        
        # Verifica se excedeu o limite
        if len(request_times) >= config.MAX_REQUESTS_PER_MINUTE:
            wait_time = 60 - (current_time - request_times[0])
            logger.warning(f"Rate limit atingido. Aguardando {wait_time:.1f} segundos...")
            raise Exception(f"Rate limit atingido. Tente novamente em {wait_time:.1f} segundos.")
        
        # Adiciona timestamp da requisição atual
        request_times.append(current_time)
        
        return func(*args, **kwargs)
    
    return wrapper


class LLMService:
    """
    Serviço para gerenciar consultas ao LLM usando Angola Energy Prompt System.
    """
    
    def __init__(self):
        self.gemini_client = None
        
        if GEMINI_AVAILABLE:
            self._initialize_gemini_direct()
        else:
            logger.error("Gemini não disponível")
    
    def _initialize_gemini_direct(self) -> None:
        """Inicializa cliente Gemini direto."""
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.gemini_client = genai.GenerativeModel(config.GEMINI_MODEL)
            logger.info(f"Cliente Gemini inicializado com {config.GEMINI_MODEL} ✓")
        except Exception as e:
            logger.error(f"Erro ao inicializar Gemini: {e}")
            self.gemini_client = None
    
    def process_query_with_llm(self, question: str, conversation_history: list = None, 
                              context_data: dict = None) -> dict:
        """
        Process query using Angola Energy Prompt System
        """
        try:
            logger.info(f"🤖 Processing query: {question[:100]}...")
            
            # Check for simple greetings
            if self._is_simple_greeting(question):
                logger.info("✅ Simple greeting detected")
                greeting_response = self._generate_greeting_response(conversation_history)
                return {
                    "response": greeting_response,
                    "source": "greeting_system",
                    "confidence": 0.95,
                    "metadata": {
                        "type": "greeting",
                        "timestamp": time.time()
                    }
                }
            
            # Create system prompt with context
            system_prompt = angola_energy_prompts.create_system_prompt(
                context_data=context_data,
                user_info=None
            )
            
            # Create query-specific prompt
            query_prompt = angola_energy_prompts.create_query_prompt(
                question=question,
                context="",
                conversation_history=conversation_history
            )
            
            # Determine if this is a generic question
            is_generic = self._is_generic_question(question)
            
            # Load context for detailed questions
            context, sources = "", []
            if not is_generic:
                context, sources = self._load_context_files(question)
            
            # Build appropriate prompt
            if is_generic:
                prompt = f"""{system_prompt}

{query_prompt}

📋 **RESPOSTA CONCISA:**
Forneça uma resposta direta e objetiva."""
            else:
                prompt = f"""{system_prompt}

{query_prompt}

🔍 **ANÁLISE DETALHADA:**
Forneça uma análise abrangente com:
• Dados específicos e numéricos
• Contexto temporal atualizado
• Análise estratégica e insights
• Formatação clara com Markdown

Contexto:
{context}"""
            
            # Generate response with Gemini
            response = self.gemini_client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.RESPONSE_TEMPERATURE,
                    max_output_tokens=config.MAX_OUTPUT_TOKENS,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            if response and response.text:
                final_response = response.text.strip()
                
                # Add source attribution with links
                if sources:
                    source_links = []
                    for source in sources:
                        if isinstance(source, dict) and 'name' in source and 'url' in source:
                            source_links.append(f"[{source['name']}]({source['url']})")
                        else:
                            source_links.append(str(source))
                    
                    if source_links:
                        final_response += f"\n\n---\n*Fontes: {', '.join(source_links)}*"
                
                return {
                    "response": final_response,
                    "source": "angola_energy_prompts",
                    "confidence": 0.85,
                    "metadata": {
                        "type": "detailed_analysis" if not is_generic else "generic_response",
                        "prompt_version": "angola_energy_v1",
                        "timestamp": time.time(),
                        "context_used": bool(context)
                    }
                }
            else:
                return {
                    "response": "Desculpe, não consegui processar sua pergunta. Por favor, tente novamente.",
                    "source": "error_fallback",
                    "confidence": 0.0,
                    "metadata": {
                        "error": "Empty response",
                        "timestamp": time.time()
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            return {
                "response": "Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.",
                "source": "error_fallback",
                "confidence": 0.0,
                "metadata": {
                    "error": str(e),
                    "timestamp": time.time()
                }
            }
    
    def _is_simple_greeting(self, question: str) -> bool:
        """Check if the question is a simple greeting"""
        greetings = ['olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'oi', 'hello', 'hi']
        question_lower = question.lower().strip()
        return any(greeting in question_lower for greeting in greetings) and len(question.split()) <= 3
    
    def _generate_greeting_response(self, conversation_history: list = None) -> str:
        """Generate greeting response with concrete examples"""
        greetings = [
            "Olá! 👋 Sou seu consultor especializado em energia e petróleo em Angola. Posso ajudá-lo com:\n\n• Análises das principais empresas (Sonangol, Total, Azule Energy)\n• Tendências do mercado energético angolano\n• Dados de produção e investimentos\n• Projetos e desenvolvimentos do setor\n\nO que gostaria de saber?",
            "Bom dia! 💡 Estou aqui para fornecer informações estratégicas sobre o setor de energia angolano. Posso ajudar com:\n\n• Análises de desempenho das empresas\n• Dados de produção e exportação\n• Tendências de mercado e oportunidades\n• Contexto regulatório e investimentos\n\nQual sua pergunta específica?",
            "Oi! 🛢️ Seja bem-vindo ao consultor especializado em energia de Angola. Minhas principais capacidades incluem:\n\n• Análises detalhadas das empresas petrolíferas\n• Dados atualizados do setor energético\n• Insights sobre projetos e investimentos\n• Informações sobre regulamentações e mercado\n\nComo posso ser útil para você hoje?"
        ]
        import random
        return random.choice(greetings)
    
    def _is_generic_question(self, question: str) -> bool:
        """Determine if this is a generic question"""
        generic_keywords = ['quem é', 'o que é', 'definir', 'definição', 'significado']
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in generic_keywords) or len(question.split()) <= 5
    
    def _load_context_files(self, question: str = "") -> tuple[str, list]:
        """Carrega arquivos de contexto da pasta data."""
        try:
            data_path = Path(config.DATA_DIR)
            if not data_path.exists():
                return "Contexto não disponível.", []
            
            # Mapeia arquivos para suas fontes com URLs base
            source_mapping = {
                'total_': ('Total Energies Angola', 'https://www.totalenergies.com'),
                'sonangol_': ('Sonangol', 'https://www.sonangol.co.ao'),
                'azule_': ('Azule Energy', 'https://www.azuleenergy.com'),
                'anpg_': ('ANPG', 'https://www.anpg.ao'),
                'petroangola_': ('Petroangola', 'https://www.petroangola.ao')
            }
            
            # Carrega arquivos relevantes
            company_files = {}
            used_sources = []
            
            for file_path in data_path.glob("*.txt"):
                for prefix, (source_name, base_url) in source_mapping.items():
                    if file_path.name.startswith(prefix):
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            # Remove metadados do cabeçalho
                            lines = content.split('\n')
                            content_start = 0
                            for i, line in enumerate(lines):
                                if '=' in line and len(line) > 10:
                                    content_start = i + 2
                                    break
                            
                            clean_content = '\n'.join(lines[content_start:]).strip()
                            if len(clean_content) > 100:
                                company_files[source_name] = {
                                    'content': clean_content[:2000],  # Limita tamanho
                                    'url': base_url
                                }
                                if source_name not in used_sources:
                                    used_sources.append(source_name)
                            
                        except Exception as e:
                            logger.warning(f"Erro ao ler {file_path}: {e}")
                        break
            
            if not company_files:
                return "Contexto empresarial não disponível.", []
            
            # Seleciona contexto baseado na pergunta
            question_lower = question.lower()
            relevant_content = []
            final_sources = []
            
            # Verifica empresas mencionadas
            companies_mentioned = []
            for company in [info[0] for info in source_mapping.values()]:
                if company.lower() in question_lower:
                    companies_mentioned.append(company)
            
            # Se empresas específicas mencionadas, prioriza elas
            if companies_mentioned:
                for company in companies_mentioned:
                    if company in company_files:
                        relevant_content.append(f"=== {company.upper()} ===\n{company_files[company]['content']}")
                        final_sources.append({
                            'name': company,
                            'url': company_files[company]['url']
                        })
                
                # Adiciona resumo das outras empresas
                for company, data in company_files.items():
                    if company not in companies_mentioned:
                        relevant_content.append(f"=== {company.upper()} (Visão Geral) ===\n{data['content'][:800]}")
            else:
                # Inclui todas as empresas
                for company, data in company_files.items():
                    relevant_content.append(f"=== {company.upper()} ===\n{data['content'][:1200]}")
                    final_sources.append({
                        'name': company,
                        'url': data['url']
                    })
            
            final_context = "\n\n".join(relevant_content)
            
            # Limita tamanho total
            if len(final_context) > 6000:
                final_context = final_context[:6000] + "\n[...contexto continua...]"
            
            return final_context, final_sources
            
        except Exception as e:
            logger.warning(f"Erro ao carregar contexto: {e}")
            return "Erro ao acessar contexto empresarial.", []
    
    def health_check(self) -> dict:
        """Verifica se o serviço está funcionando."""
        try:
            if not self.gemini_client:
                return {"status": "unhealthy", "error": "Gemini não inicializado"}
            
            # Testa com uma pergunta simples
            test_response = self.process_query_with_llm("teste", [])
            
            return {
                "status": "healthy",
                "method": "angola_energy_prompts",
                "gemini_available": GEMINI_AVAILABLE,
                "test_response": bool(test_response.get("response"))
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "gemini_available": GEMINI_AVAILABLE
            }


# Instância global do serviço LLM
try:
    llm_service = LLMService()
    logger.info("Serviço LLM inicializado com sucesso")
except Exception as e:
    logger.error(f"Falha ao inicializar serviço LLM: {e}")
    llm_service = None


def query_llm(question: str, history: list = None) -> str:
    """
    Função principal para consultas ao LLM usando Angola Energy Prompt System.
    
    Args:
        question: Pergunta do usuário
        history: Histórico de mensagens da conversa
        
    Returns:
        Resposta do LLM usando Angola Energy Prompts
        
    Raises:
        Exception: Se o serviço não estiver disponível
    """
    if not llm_service:
        raise Exception("Serviço LLM não está disponível")
    
    result = llm_service.process_query_with_llm(question, history or [])
    return result.get("response", "Desculpe, não consegui gerar uma resposta.")


def query_llm_simple(prompt: str) -> str:
    """
    Função simples para consultar o LLM sem contexto de índice.
    
    Args:
        prompt: Texto da pergunta/prompt
        
    Returns:
        Resposta do LLM
    """
    try:
        if not GEMINI_AVAILABLE:
            return None
            
        # Configura Gemini se ainda não estiver configurado
        if not hasattr(query_llm_simple, '_gemini_client'):
            genai.configure(api_key=config.GEMINI_API_KEY)
            query_llm_simple._gemini_client = genai.GenerativeModel(config.GEMINI_MODEL)
        
        # Gera resposta
        response = query_llm_simple._gemini_client.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Erro em query_llm_simple: {e}")
        return None


def get_llm_health() -> dict:
    """
    Retorna o status de saúde do serviço LLM.
    
    Returns:
        Dicionário com informações de saúde
    """
    if not llm_service:
        return {"status": "unavailable", "error": "Serviço não inicializado"}
    
    return llm_service.health_check()
