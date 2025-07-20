"""
Construtor de índice LlamaIndex.
Script para criar e persistir o índice de documentos que será usado pelo chatbot.
Execute este script uma vez para preparar os dados.
"""
import logging
from pathlib import Path
from typing import List

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.schema import Document
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

from app.config import config

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexBuilder:
    """
    Responsável por construir e persistir o índice de documentos.
    
    Funcionalidades:
    - Lê documentos da pasta data/
    - Cria índice vetorial usando embeddings
    - Persiste índice para uso posterior
    """
    
    def __init__(self):
        self._setup_llm()
    
    def _setup_llm(self) -> None:
        """Configura LLM e embeddings para construção do índice."""
        try:
            # Configura LLM
            llm = Gemini(
                api_key=config.GEMINI_API_KEY,
                model=config.GEMINI_MODEL
            )
            
            # Configura embeddings
            embed_model = GeminiEmbedding(
                api_key=config.GEMINI_API_KEY,
                model_name="models/embedding-001"
            )
            
            # Define configurações globais
            Settings.llm = llm
            Settings.embed_model = embed_model
            
            logger.info("LLM e embeddings configurados para construção do índice")
            
        except Exception as e:
            logger.error(f"Erro ao configurar LLM: {e}")
            raise
    
    def _load_documents(self) -> List[Document]:
        """
        Carrega documentos da pasta data/.
        
        Returns:
            Lista de documentos carregados
            
        Raises:
            FileNotFoundError: Se a pasta data/ não existir
            ValueError: Se nenhum documento for encontrado
        """
        data_path = Path(config.DATA_DIR)
        
        if not data_path.exists():
            raise FileNotFoundError(
                f"Pasta de dados não encontrada: {data_path}. "
                "Crie a pasta 'data/' e adicione arquivos .txt ou .md"
            )
        
        try:
            # Carrega documentos de múltiplos formatos
            reader = SimpleDirectoryReader(
                input_dir=str(data_path),
                file_extractor={
                    ".txt": lambda file_path: [Document(text=file_path.read_text(encoding='utf-8'))],
                    ".md": lambda file_path: [Document(text=file_path.read_text(encoding='utf-8'))],
                },
                recursive=True  # Busca em subpastas também
            )
            
            documents = reader.load_data()
            
            if not documents:
                raise ValueError(
                    f"Nenhum documento encontrado em {data_path}. "
                    "Adicione arquivos .txt ou .md na pasta data/"
                )
            
            logger.info(f"Carregados {len(documents)} documentos de {data_path}")
            
            # Log detalhado dos documentos carregados
            for i, doc in enumerate(documents):
                doc_preview = doc.text[:100].replace('\n', ' ')
                logger.info(f"Documento {i+1}: {doc_preview}...")
            
            return documents
            
        except Exception as e:
            logger.error(f"Erro ao carregar documentos: {e}")
            raise
    
    def _create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Cria índice vetorial a partir dos documentos.
        
        Args:
            documents: Lista de documentos para indexar
            
        Returns:
            Índice vetorial criado
        """
        try:
            logger.info("Criando índice vetorial...")
            
            # Cria índice com configurações otimizadas
            index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True  # Mostra progresso da criação
            )
            
            logger.info("Índice vetorial criado com sucesso")
            return index
            
        except Exception as e:
            logger.error(f"Erro ao criar índice: {e}")
            raise
    
    def _persist_index(self, index: VectorStoreIndex) -> None:
        """
        Persiste o índice no diretório configurado.
        
        Args:
            index: Índice a ser persistido
        """
        try:
            storage_path = Path(config.INDEX_DIR)
            storage_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Persistindo índice em: {storage_path}")
            
            # Persiste o índice
            index.storage_context.persist(persist_dir=str(storage_path))
            
            logger.info("Índice persistido com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao persistir índice: {e}")
            raise
    
    def build_index(self) -> None:
        """
        Executa todo o processo de construção do índice.
        
        Passos:
        1. Carrega documentos
        2. Cria índice vetorial
        3. Persiste índice
        """
        try:
            logger.info("=== Iniciando construção do índice ===")
            
            # 1. Carrega documentos
            documents = self._load_documents()
            
            # 2. Cria índice
            index = self._create_index(documents)
            
            # 3. Persiste índice
            self._persist_index(index)
            
            logger.info("=== Construção do índice concluída com sucesso ===")
            logger.info(f"Índice salvo em: {config.INDEX_DIR}")
            logger.info("Agora você pode executar o servidor: uvicorn app.main:app --reload")
            
        except Exception as e:
            logger.error(f"Falha na construção do índice: {e}")
            raise


def main():
    """Função principal para execução do script."""
    try:
        builder = IndexBuilder()
        builder.build_index()
        
    except KeyboardInterrupt:
        logger.info("Operação cancelada pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        exit(1)


if __name__ == "__main__":
    main()
