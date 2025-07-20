"""
Módulo de configuração do backend.
Responsável por carregar variáveis de ambiente e definir configurações globais.
"""
from dotenv import load_dotenv
import os
from typing import Optional

# Carrega variáveis do arquivo .env
load_dotenv()


class Config:
    """Classe para centralizar todas as configurações da aplicação."""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Diretórios
    INDEX_DIR: str = os.getenv("INDEX_DIR", "./storage")
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    
    # Configurações do servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Configurações do modelo
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    
    # Configurações de rate limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "10"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "60"))
    
    # Configurações de resposta
    MAX_OUTPUT_TOKENS: int = int(os.getenv("MAX_OUTPUT_TOKENS", "1200"))
    RESPONSE_TEMPERATURE: float = float(os.getenv("RESPONSE_TEMPERATURE", "0.3"))
    
    @classmethod
    def validate(cls) -> bool:
        """Valida se todas as configurações obrigatórias estão presentes."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY é obrigatória. Configure no arquivo .env")
        return True


# Instância global da configuração
config = Config()

# Valida configurações na importação
config.validate()
