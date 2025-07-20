"""
Script simplificado para iniciar o servidor FastAPI.
Use este script como alternativa ao setup.py complexo.
"""
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_essential_imports():
    """Verifica se as importações essenciais funcionam."""
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        logger.info("✅ Importações essenciais OK")
        return True
    except ImportError as e:
        logger.error(f"❌ Falta dependência: {e}")
        logger.info("Execute: python install_essential.py")
        return False

def check_env():
    """Verifica arquivo .env básico."""
    env_path = Path(".env")
    if not env_path.exists():
        logger.info("Criando arquivo .env básico...")
        with open(".env", "w") as f:
            f.write("""# Configure sua chave API do Gemini
GEMINI_API_KEY=sua_chave_aqui
INDEX_DIR=./storage
HOST=0.0.0.0
PORT=8000
DEBUG=True
""")
        logger.warning("⚠️ Configure GEMINI_API_KEY no arquivo .env")
        return False
    
    # Verifica se está configurado
    content = env_path.read_text()
    if "sua_chave_aqui" in content:
        logger.warning("⚠️ Configure GEMINI_API_KEY no arquivo .env")
        return False
    
    logger.info("✅ Arquivo .env configurado")
    return True

def ensure_data():
    """Garante que existe pasta data com exemplo."""
    data_path = Path("data")
    data_path.mkdir(exist_ok=True)
    
    example_file = data_path / "exemplo.txt"
    if not example_file.exists():
        example_file.write_text("""
Informações sobre energia em Angola:

Angola é um importante produtor de petróleo em África, com várias empresas
internacionais operando no país, incluindo Total Energies, que tem
participação significativa no setor de exploração e produção.

A Total Energies Angola opera em diversos blocos offshore e onshore,
contribuindo para o desenvolvimento do setor energético do país.
""")
    
    logger.info("✅ Dados de exemplo disponíveis")

def start_simple_server():
    """Inicia servidor com configuração básica."""
    try:
        logger.info("🚀 Iniciando servidor FastAPI...")
        logger.info("📍 URL: http://localhost:8000")
        logger.info("📚 Docs: http://localhost:8000/docs")
        logger.info("⏹️ Pressione Ctrl+C para parar")
        
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
    except KeyboardInterrupt:
        logger.info("🛑 Servidor parado")
    except FileNotFoundError:
        logger.error("❌ uvicorn não encontrado - instale com: pip install uvicorn")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")

def main():
    logger.info("=== Inicialização Simplificada ===")
    
    # 1. Verifica importações
    if not check_essential_imports():
        return
    
    # 2. Verifica configuração
    if not check_env():
        logger.info("Configure o .env e execute novamente")
        return
    
    # 3. Garante dados
    ensure_data()
    
    # 4. Inicia servidor
    start_simple_server()

if __name__ == "__main__":
    main()
