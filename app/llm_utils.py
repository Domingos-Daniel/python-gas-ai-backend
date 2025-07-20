"""
Módulo utilitário para LLM (Large Language Model).
Responsável por integrar LlamaIndex com Gemini SDK para consultas contextuais.
"""
from typing import Optional
import logging
from pathlib import Path
import time
import json
from functools import wraps

try:
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.llms.gemini import Gemini
    from llama_index.embeddings.gemini import GeminiEmbedding
    from llama_index.core.query_engine.base import BaseQueryEngine
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    # Fallback se LlamaIndex não estiver disponível
    LLAMAINDEX_AVAILABLE = False
    BaseQueryEngine = object

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
    Serviço para gerenciar consultas ao LLM usando LlamaIndex e Gemini.
    
    Responsabilidades:
    - Carregar índice previamente construído
    - Configurar LLM e embeddings
    - Processar consultas e retornar respostas
    """
    
    def __init__(self):
        self.query_engine: Optional[BaseQueryEngine] = None
        self.gemini_client = None
        self.use_llamaindex = LLAMAINDEX_AVAILABLE
        
        if GEMINI_AVAILABLE:
            self._initialize_gemini_direct()
        
        if LLAMAINDEX_AVAILABLE:
            self._initialize_llm()
            self._load_index()
        else:
            logger.warning("LlamaIndex não disponível - usando Gemini direto")
    
    def _initialize_gemini_direct(self) -> None:
        """Inicializa cliente Gemini direto como fallback."""
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            # Usa o modelo configurado no .env
            model_name = config.GEMINI_MODEL
            self.gemini_client = genai.GenerativeModel(model_name)
            logger.info(f"Cliente Gemini direto inicializado com {model_name} ✓")
        except Exception as e:
            logger.error(f"Erro ao inicializar Gemini direto: {e}")
            self.gemini_client = None
    
    def _initialize_llm(self) -> None:
        """Inicializa o modelo LLM e embeddings do Gemini."""
        try:
            # Configura LLM Gemini
            llm = Gemini(
                api_key=config.GEMINI_API_KEY,
                model=config.GEMINI_MODEL,
                temperature=0.1  # Para respostas mais consistentes
            )
            
            # Configura embeddings Gemini
            embed_model = GeminiEmbedding(
                api_key=config.GEMINI_API_KEY,
                model_name="models/embedding-001"
            )
            
            # Define configurações globais
            Settings.llm = llm
            Settings.embed_model = embed_model
            
            logger.info(f"LLM LlamaIndex inicializado: {config.GEMINI_MODEL}")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM: {e}")
            self.use_llamaindex = False
    
    def _load_index(self) -> None:
        """Carrega o índice previamente construído do diretório de storage."""
        try:
            index_path = Path(config.INDEX_DIR)
            
            if not index_path.exists():
                raise FileNotFoundError(
                    f"Diretório do índice não encontrado: {index_path}. "
                    "Execute 'python index_builder.py' primeiro."
                )
            
            # Carrega contexto de storage
            storage_context = StorageContext.from_defaults(
                persist_dir=str(index_path)
            )
            
            # Carrega índice
            index = load_index_from_storage(storage_context)
            
            # Cria query engine com configurações otimizadas
            self.query_engine = index.as_query_engine(
                similarity_top_k=5,  # Top 5 documentos mais similares
                response_mode="tree_summarize"  # Melhor para respostas longas
            )
            
            logger.info(f"Índice carregado com sucesso de: {index_path}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar índice: {e}")
            raise
    
    @rate_limit_decorator
    def query(self, question: str, history: list = None) -> str:
        """
        Processa uma pergunta e retorna uma resposta baseada no contexto.
        
        Args:
            question: Pergunta do usuário
            history: Histórico de mensagens da conversa
            
        Returns:
            Resposta gerada pelo LLM com base no contexto
            
        Raises:
            ValueError: Se a pergunta estiver vazia
            Exception: Para outros erros durante o processamento
        """
        if not question.strip():
            raise ValueError("Pergunta não pode estar vazia")
        
        if history is None:
            history = []
        
        try:
            logger.info(f"Processando pergunta: {question[:100]}...")
            logger.info(f"Histórico com {len(history)} mensagens")
            
            # Tenta usar LlamaIndex primeiro se disponível
            if self.use_llamaindex and self.query_engine:
                try:
                    response = self.query_engine.query(question)
                    answer = str(response).strip()
                    logger.info("Resposta gerada via LlamaIndex")
                    return answer
                except Exception as e:
                    logger.warning(f"Erro no LlamaIndex, usando fallback: {e}")
                    # Continua para o fallback
            
            # Fallback para Gemini direto
            if self.gemini_client:
                try:
                    # Carrega contexto dos arquivos se disponível
                    context, sources = self._load_context_files(question)
                    
                    # Constrói histórico da conversa
                    conversation_history = ""
                    if history:
                        conversation_history = "\n\nHISTÓRICO DA CONVERSA:\n"
                        for msg in history[-6:]:  # Últimas 6 mensagens para não exceder tokens
                            role = "USUÁRIO" if msg.get("role") == "user" else "ASSISTENTE"
                            content = msg.get("content", "")[:200]  # Limita tamanho
                            conversation_history += f"{role}: {content}\n"
                    
                    # Prompt melhorado para respostas mais profissionais com formatação markdown
                    prompt = f"""Você é um consultor especializado em energia e petróleo em Angola, com conhecimento detalhado sobre as principais empresas do setor. Baseie sua resposta exclusivamente nas informações do contexto fornecido.

CONTEXTO EMPRESARIAL:
{context}{conversation_history}

DIRETRIZES PARA RESPOSTA:
• Responda de forma profissional, estruturada e completa usando formatação Markdown
• Use **negrito** para termos importantes e nomes de empresas
• Use *itálico* para destacar conceitos específicos
• Organize listas com • ou números quando apropriado
• Use cabeçalhos ## quando necessário para estruturar seções
• Inclua dados relevantes como números, projetos e atividades específicas
• Mantenha tom consultivo e informativo
• Se a informação for limitada, mencione isso claramente
• Conclua a resposta de forma natural, sem cortes abruptos
• Formate tabelas usando sintaxe markdown quando apropriado
• Use `código` para destacar valores específicos ou termos técnicos
• IMPORTANTE: Considere o histórico da conversa acima para manter contexto e coerência
• Se o usuário usar pronomes como "isso", "mesmo", "ele", etc., refira-se ao contexto anterior

PERGUNTA ATUAL DO CLIENTE: {question}

RESPOSTA DETALHADA (em Markdown):"""
                    
                    response = self.gemini_client.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=config.RESPONSE_TEMPERATURE,
                            max_output_tokens=config.MAX_OUTPUT_TOKENS,
                            top_p=0.8,
                            top_k=40
                        )
                    )
                    
                    answer = response.text.strip() if response.text else "Desculpe, não consegui gerar uma resposta adequada."
                    
                    # Adiciona seção de fontes se houver
                    if sources:
                        answer += "\n\n---\n\n### 📚 Fontes Consultadas\n\n"
                        for source in sources:
                            answer += f"• **[{source['name']}]({source['url']})** - {source['description']}\n"
                    
                    logger.info("Resposta gerada via Gemini direto")
                    return answer
                    
                except google_exceptions.ResourceExhausted as e:
                    logger.error("Quota da API excedida")
                    raise Exception("Quota da API do Gemini excedida. Tente novamente mais tarde.")
                    
                except google_exceptions.PermissionDenied as e:
                    logger.error("Erro de permissão na API")
                    raise Exception("Erro de autenticação. Verifique sua API key.")
                    
                except Exception as e:
                    logger.error(f"Erro no Gemini direto: {e}")
                    raise Exception(f"Erro ao processar pergunta: {str(e)}")
            
            else:
                raise Exception("Nenhum método de LLM disponível")
            
        except Exception as e:
            logger.error(f"Erro ao processar pergunta: {e}")
            # Re-levanta a exceção para que seja tratada pela API
            raise
    
    def _load_context_files(self, question: str = "") -> tuple[str, list]:
        """Carrega arquivos de contexto da pasta data de forma inteligente."""
        try:
            data_path = Path(config.DATA_DIR)
            if not data_path.exists():
                return "Contexto não disponível.", []
            
            # Mapeia arquivos para suas fontes/URLs
            source_mapping = {
                'total_': {
                    'name': 'Total Energies Angola',
                    'url': 'https://totalenergies.com/ao',
                    'description': 'Site oficial da Total Energies Angola'
                },
                'sonangol_': {
                    'name': 'Sonangol',
                    'url': 'https://sonangol.co.ao',
                    'description': 'Site oficial da Sonangol'
                },
                'azule_': {
                    'name': 'Azule Energy',
                    'url': 'https://azule-energy.com',
                    'description': 'Site oficial da Azule Energy'
                },
                'anpg_': {
                    'name': 'ANPG',
                    'url': 'https://anpg.ao',
                    'description': 'Site oficial da Agência Nacional de Petróleo, Gás e Biocombustíveis'
                }
            }
            
            # Carrega todos os arquivos de dados das empresas
            company_files = {}
            used_sources = []
            
            for file_path in data_path.glob("*.txt"):
                if any(prefix in file_path.name for prefix in ['total_', 'sonangol_', 'azule_', 'anpg_']):
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        # Remove metadados do cabeçalho
                        lines = content.split('\n')
                        content_start = 0
                        for i, line in enumerate(lines):
                            if '=' in line and len(line) > 10:
                                content_start = i + 2  # Pula linha separadora e linha vazia
                                break
                        
                        clean_content = '\n'.join(lines[content_start:]).strip()
                        if len(clean_content) > 100:  # Só inclui conteúdo substancial
                            company_files[file_path.name] = clean_content
                            
                            # Identifica a fonte
                            for prefix, source_info in source_mapping.items():
                                if file_path.name.startswith(prefix):
                                    if source_info not in used_sources:
                                        used_sources.append(source_info)
                                    break
                        
                    except Exception as e:
                        logger.warning(f"Erro ao ler {file_path}: {e}")
            
            if not company_files:
                return "Contexto empresarial não disponível.", []
            
            # Estratégia inteligente de seleção de contexto
            question_lower = question.lower()
            relevant_content = []
            relevant_sources = []
            
            # Mapeia palavras-chave para empresas
            keywords_map = {
                'total': ['total', 'totalenergies'],
                'sonangol': ['sonangol'],
                'azule': ['azule', 'azul'],
                'anpg': ['anpg', 'agência', 'agencia', 'nacional', 'petróleo', 'petroleo', 'regulador']
            }
            
            companies_mentioned = []
            for company, keywords in keywords_map.items():
                if any(keyword in question_lower for keyword in keywords):
                    companies_mentioned.append(company)
            
            # Se empresa específica mencionada, prioriza seu contexto
            if companies_mentioned:
                for company in companies_mentioned:
                    company_content = []
                    for filename, content in company_files.items():
                        if filename.startswith(f"{company}_"):
                            company_content.append(content[:2000])  # Mais conteúdo por empresa
                            
                            # Adiciona fonte correspondente
                            for prefix, source_info in source_mapping.items():
                                if filename.startswith(prefix) and source_info not in relevant_sources:
                                    relevant_sources.append(source_info)
                                    break
                    
                    if company_content:
                        relevant_content.append(f"=== {company.upper()} ===\n" + "\n\n".join(company_content))
                
                # Adiciona contexto resumido das outras empresas
                for company in ['total', 'sonangol', 'azule', 'anpg']:
                    if company not in companies_mentioned:
                        for filename, content in company_files.items():
                            if filename.startswith(f"{company}_") and filename.endswith("_01.txt"):  # Só primeira página
                                relevant_content.append(f"=== {company.upper()} (Resumo) ===\n" + content[:800])
                                
                                # Adiciona fonte correspondente
                                for prefix, source_info in source_mapping.items():
                                    if filename.startswith(prefix) and source_info not in relevant_sources:
                                        relevant_sources.append(source_info)
                                        break
                                break
            else:
                # Se nenhuma empresa específica, inclui resumo de todas
                for company in ['total', 'sonangol', 'azule', 'anpg']:
                    for filename, content in company_files.items():
                        if filename.startswith(f"{company}_") and filename.endswith("_01.txt"):
                            relevant_content.append(f"=== {company.upper()} ===\n" + content[:1200])
                            
                            # Adiciona fonte correspondente
                            for prefix, source_info in source_mapping.items():
                                if filename.startswith(prefix) and source_info not in relevant_sources:
                                    relevant_sources.append(source_info)
                                    break
                            break
            
            final_context = "\n\n".join(relevant_content)
            
            # Limita tamanho total para não exceder limites da API
            if len(final_context) > 8000:
                final_context = final_context[:8000] + "\n[...contexto truncado...]"
            
            return final_context if final_context else "Contexto limitado disponível.", relevant_sources
            
        except Exception as e:
            logger.warning(f"Erro ao carregar contexto: {e}")
            return "Erro ao acessar contexto empresarial.", []
    
    def health_check(self) -> dict:
        """
        Verifica se o serviço está funcionando corretamente.
        
        Returns:
            Dicionário com status do serviço
        """
        try:
            # Determina qual método está disponível
            if self.use_llamaindex and self.query_engine:
                test_response = self.query("Teste de conectividade")
                method = "llamaindex"
            elif self.gemini_client:
                # Testa o contexto disponível
                context, sources = self._load_context_files("teste")
                test_response = f"Gemini direto funcionando - Contexto: {len(context)} chars, Fontes: {len(sources)}"
                method = "gemini_direct"
            else:
                return {"status": "unhealthy", "error": "Nenhum método LLM disponível"}
            
            return {
                "status": "healthy",
                "method": method,
                "llamaindex_available": LLAMAINDEX_AVAILABLE,
                "gemini_available": GEMINI_AVAILABLE,
                "index_loaded": self.query_engine is not None,
                "test_response_length": len(test_response) if test_response else 0
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "llamaindex_available": LLAMAINDEX_AVAILABLE,
                "gemini_available": GEMINI_AVAILABLE,
                "index_loaded": self.query_engine is not None
            }


# Instância global do serviço LLM
# Será inicializada quando o módulo for importado
try:
    llm_service = LLMService()
    logger.info("Serviço LLM inicializado com sucesso")
except Exception as e:
    logger.error(f"Falha ao inicializar serviço LLM: {e}")
    # Permite que a aplicação continue, mas com funcionalidade limitada
    llm_service = None


def query_llm(question: str, history: list = None) -> str:
    """
    Função de conveniência para fazer consultas ao LLM.
    
    Args:
        question: Pergunta do usuário
        history: Histórico de mensagens da conversa
        
    Returns:
        Resposta do LLM
        
    Raises:
        Exception: Se o serviço não estiver disponível
    """
    if not llm_service:
        raise Exception("Serviço LLM não está disponível")
    
    return llm_service.query(question, history or [])


def get_llm_health() -> dict:
    """
    Retorna o status de saúde do serviço LLM.
    
    Returns:
        Dicionário com informações de saúde
    """
    if not llm_service:
        return {"status": "unavailable", "error": "Serviço não inicializado"}
    
    return llm_service.health_check()
