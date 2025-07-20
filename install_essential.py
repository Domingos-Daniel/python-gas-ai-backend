"""
Script simplificado de instalação das dependências essenciais.
Use este script se o setup.py falhar.
"""
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dependências essenciais que geralmente funcionam
ESSENTIAL_PACKAGES = [
    "fastapi",
    "uvicorn[standard]",
    "python-dotenv", 
    "pydantic",
    "aiofiles",
    "requests",
    "beautifulsoup4",
    "google-generativeai"
]

def install_package(package):
    """Instala um pacote individual."""
    try:
        logger.info(f"Instalando {package}...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            package, "--prefer-binary", "--no-cache-dir"
        ], check=True, capture_output=True, text=True, timeout=120)
        logger.info(f"{package} ✓")
        return True
    except Exception as e:
        logger.error(f"Falha em {package}: {e}")
        return False

def main():
    logger.info("=== Instalação Essencial ===")
    
    # Atualiza pip primeiro
    try:
        logger.info("Atualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
    except Exception as e:
        logger.warning(f"Falha ao atualizar pip: {e}")
    
    # Instala pacotes essenciais
    success_count = 0
    for package in ESSENTIAL_PACKAGES:
        if install_package(package):
            success_count += 1
    
    logger.info(f"=== Instalação concluída: {success_count}/{len(ESSENTIAL_PACKAGES)} pacotes ===")
    
    if success_count >= 6:  # Pelo menos os básicos
        logger.info("✅ Dependências essenciais instaladas com sucesso!")
        logger.info("Você pode prosseguir com: python simple_start.py")
    else:
        logger.error("❌ Muitas falhas na instalação")
        logger.info("Tente instalar manualmente: pip install fastapi uvicorn python-dotenv google-generativeai")

if __name__ == "__main__":
    main()
