"""
Script de inicialização do backend.
Facilita a configuração inicial e execução da aplicação.
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_python_version():
    """Verifica se a versão do Python é compatível."""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8+ é necessário")
        sys.exit(1)
    logger.info(f"Python {sys.version_info.major}.{sys.version_info.minor} ✓")


def install_dependencies():
    """Instala as dependências do projeto."""
    try:
        logger.info("Atualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        
        logger.info("Instalando dependências...")
        # Instala em modo mais tolerante
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt",
            "--prefer-binary",  # Prefere wheels binários
            "--no-cache-dir"    # Não usa cache para evitar problemas
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            logger.info("Dependências instaladas com sucesso ✓")
            return True
        else:
            logger.warning("Algumas dependências falharam, tentando instalação alternativa...")
            return install_dependencies_fallback()
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout na instalação (10 min) - tentando instalação alternativa...")
        return install_dependencies_fallback()
    except Exception as e:
        logger.error(f"Erro na instalação: {e}")
        return install_dependencies_fallback()


def install_dependencies_fallback():
    """Instala dependências essenciais como fallback."""
    essential_packages = [
        "fastapi",
        "uvicorn[standard]", 
        "python-dotenv",
        "pydantic",
        "aiofiles",
        "requests",
        "beautifulsoup4",
        "google-generativeai",
        "tiktoken",
        "tenacity"
    ]
    
    failed_packages = []
    
    for package in essential_packages:
        try:
            logger.info(f"Instalando {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                package, "--prefer-binary"
            ], check=True, capture_output=True, text=True, timeout=120)
            
        except Exception as e:
            logger.warning(f"Falha ao instalar {package}: {e}")
            failed_packages.append(package)
    
    if failed_packages:
        logger.warning(f"Pacotes que falharam: {', '.join(failed_packages)}")
        logger.info("Continuando com pacotes disponíveis...")
    
    # Tenta instalar LlamaIndex básico
    try:
        logger.info("Instalando LlamaIndex básico...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "llama-index-core", "--prefer-binary"
        ], check=True, capture_output=True, text=True, timeout=120)
    except Exception as e:
        logger.warning(f"LlamaIndex não instalado: {e}")
        logger.info("Sistema pode funcionar com limitações")
    
    logger.info("Instalação essencial concluída ✓")
    return True


def check_env_file():
    """Verifica se o arquivo .env existe e está configurado."""
    env_path = Path(".env")
    
    if not env_path.exists():
        logger.warning("Arquivo .env não encontrado")
        create_env = input("Deseja criar um arquivo .env de exemplo? (s/n): ")
        
        if create_env.lower() in ['s', 'sim', 'y', 'yes']:
            with open(".env", "w") as f:
                f.write("""# Configurações da API Gemini
GEMINI_API_KEY=coloca_aqui_a_sua_chave_gemini

# Diretório onde será armazenado o índice LlamaIndex
INDEX_DIR=./storage

# Configurações do servidor
HOST=0.0.0.0
PORT=8000

# Configurações de debug
DEBUG=True
""")
            logger.info("Arquivo .env criado. Configure sua GEMINI_API_KEY antes de continuar.")
            return False
    
    # Verifica se a chave está configurada
    with open(".env", "r") as f:
        content = f.read()
        if "coloca_aqui_a_sua_chave" in content:
            logger.warning("GEMINI_API_KEY não está configurada no arquivo .env")
            return False
    
    logger.info("Arquivo .env configurado ✓")
    return True


def check_data_directory():
    """Verifica se há dados na pasta data/."""
    data_path = Path("data")
    
    if not data_path.exists():
        data_path.mkdir()
        logger.info("Pasta data/ criada")
    
    # Verifica se há arquivos de dados
    data_files = list(data_path.glob("*.txt")) + list(data_path.glob("*.md"))
    
    if not data_files:
        logger.warning("Nenhum arquivo de dados encontrado em data/")
        print("\nOpções:")
        print("1. Adicionar arquivos .txt ou .md manualmente na pasta data/")
        print("2. Executar o scraper: python app/scraper.py")
        print("3. Usar dados de exemplo (já incluído)")
        
        return len(list(data_path.glob("*"))) > 1  # Verifica se há pelo menos o exemplo
    
    logger.info(f"Encontrados {len(data_files)} arquivos de dados ✓")
    return True


def build_index():
    """Constrói o índice LlamaIndex."""
    try:
        logger.info("Construindo índice LlamaIndex...")
        result = subprocess.run([sys.executable, "app/index_builder.py"], 
                               capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info("Índice construído com sucesso ✓")
            return True
        else:
            logger.error(f"Erro ao construir índice: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout ao construir índice (5 min)")
        return False
    except Exception as e:
        logger.error(f"Erro ao construir índice: {e}")
        return False


def start_server():
    """Inicia o servidor FastAPI."""
    try:
        logger.info("Iniciando servidor FastAPI...")
        logger.info("Servidor será executado em: http://localhost:8000")
        logger.info("Documentação API: http://localhost:8000/docs")
        logger.info("Pressione Ctrl+C para parar o servidor")
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--port", "8000",
            "--host", "0.0.0.0"
        ])
        
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")


def main():
    """Função principal de inicialização."""
    logger.info("=== Inicialização do LLM Chatbot Backend ===")
    
    # 1. Verifica versão do Python
    check_python_version()
    
    # 2. Instala dependências (não para se falhar)
    dependencies_ok = install_dependencies()
    if not dependencies_ok:
        logger.warning("Algumas dependências podem estar faltando")
        proceed = input("Deseja continuar mesmo assim? (s/n): ")
        if proceed.lower() not in ['s', 'sim', 'y', 'yes']:
            sys.exit(1)
    
    # 3. Verifica configuração
    if not check_env_file():
        logger.error("Configure o arquivo .env antes de continuar")
        sys.exit(1)
    
    # 4. Verifica dados
    has_data = check_data_directory()
    
    # 5. Constrói índice se necessário (opcional se LlamaIndex não funcionar)
    storage_path = Path("storage")
    if not storage_path.exists() or not list(storage_path.glob("*")):
        if has_data:
            if not build_index():
                logger.warning("Falha ao construir índice - continuando sem índice")
                logger.info("Você pode tentar construir o índice manualmente depois")
        else:
            logger.warning("Nenhum dado encontrado - continuando sem índice")
    else:
        logger.info("Índice já existe ✓")
    
    # 6. Inicia servidor
    start_server()


if __name__ == "__main__":
    main()
