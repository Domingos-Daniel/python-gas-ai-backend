"""
Módulo scraper (opcional).
Utilitário para coletar dados dos sites mencionados para alimentar o chatbot.
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

from .config import config

logger = logging.getLogger(__name__)


class WebScraper:
    """
    Scraper para coletar dados de sites específicos.
    
    Sites alvo:
    - Total
    - Sonangol Refinação  
    - Azule Energies
    - ANPG
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # URLs dos sites alvo (atualizadas)
        self.target_sites = {
            'total': 'https://totalenergies.com/angola',
            'sonangol': 'https://www.sonangol.co.ao',
            'azule': 'https://www.azule-energy.com',
            'anpg': 'https://anpg.co.ao'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Limpa e formata texto extraído.
        
        Args:
            text: Texto bruto
            
        Returns:
            Texto limpo
        """
        if not text:
            return ""
        
        # Remove espaços extras e quebras de linha
        text = re.sub(r'\s+', ' ', text)
        
        # Remove caracteres especiais problemáticos
        text = text.replace('\xa0', ' ')
        text = text.replace('\u200b', '')
        
        return text.strip()
    
    def extract_page_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extrai conteúdo de uma página específica.
        
        Args:
            url: URL da página
            
        Returns:
            Dicionário com título e conteúdo ou None se houver erro
        """
        try:
            logger.info(f"Extraindo conteúdo de: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts e estilos
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extrai título
            title = soup.find('title')
            title_text = title.get_text() if title else urlparse(url).path
            
            # Extrai conteúdo principal
            # Tenta diferentes seletores comuns para conteúdo principal
            content_selectors = [
                'main',
                'article',
                '.content',
                '.main-content',
                '#content',
                'body'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content_text = content_element.get_text()
                    break
            
            if not content_text:
                content_text = soup.get_text()
            
            return {
                'title': self.clean_text(title_text),
                'content': self.clean_text(content_text),
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo de {url}: {e}")
            return None
    
    def discover_pages(self, base_url: str, max_pages: int = 10) -> List[str]:
        """
        Descobre páginas relevantes de um site.
        
        Args:
            base_url: URL base do site
            max_pages: Número máximo de páginas a descobrir
            
        Returns:
            Lista de URLs descobertas
        """
        try:
            response = self.session.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Busca links internos
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Filtra apenas links do mesmo domínio
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    links.append(full_url)
            
            # Remove duplicatas e limita
            unique_links = list(set(links))[:max_pages]
            
            logger.info(f"Descobertas {len(unique_links)} páginas em {base_url}")
            return unique_links
            
        except Exception as e:
            logger.error(f"Erro ao descobrir páginas de {base_url}: {e}")
            return [base_url]  # Retorna pelo menos a URL base
    
    def scrape_site(self, site_name: str, max_pages: int = 5) -> List[Dict[str, str]]:
        """
        Faz scraping de um site específico.
        
        Args:
            site_name: Nome do site (chave em target_sites)
            max_pages: Número máximo de páginas
            
        Returns:
            Lista de conteúdos extraídos
        """
        if site_name not in self.target_sites:
            logger.error(f"Site não reconhecido: {site_name}")
            return []
        
        base_url = self.target_sites[site_name]
        logger.info(f"Iniciando scraping de {site_name}: {base_url}")
        
        # Descobre páginas
        pages = self.discover_pages(base_url, max_pages)
        
        # Extrai conteúdo de cada página
        contents = []
        for page_url in pages:
            content = self.extract_page_content(page_url)
            if content and len(content['content']) > 100:  # Ignora páginas muito pequenas
                contents.append(content)
            
            # Pausa entre requisições para ser respeitoso
            time.sleep(1)
        
        logger.info(f"Extraído conteúdo de {len(contents)} páginas de {site_name}")
        return contents
    
    def save_content(self, contents: List[Dict[str, str]], site_name: str) -> None:
        """
        Salva conteúdo extraído em arquivos.
        
        Args:
            contents: Lista de conteúdos
            site_name: Nome do site
        """
        data_dir = Path(config.DATA_DIR)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        for i, content in enumerate(contents):
            filename = f"{site_name}_{i+1}.txt"
            filepath = data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Título: {content['title']}\n")
                f.write(f"URL: {content['url']}\n")
                f.write(f"{'='*50}\n\n")
                f.write(content['content'])
            
            logger.info(f"Conteúdo salvo: {filepath}")
    
    def scrape_all_sites(self, max_pages_per_site: int = 3) -> None:
        """
        Faz scraping de todos os sites configurados.
        
        Args:
            max_pages_per_site: Páginas máximas por site
        """
        logger.info("=== Iniciando scraping de todos os sites ===")
        
        for site_name in self.target_sites:
            try:
                logger.info(f"Processando site: {site_name}")
                
                contents = self.scrape_site(site_name, max_pages_per_site)
                
                if contents:
                    self.save_content(contents, site_name)
                else:
                    logger.warning(f"Nenhum conteúdo extraído de {site_name}")
                
            except Exception as e:
                logger.error(f"Erro ao processar {site_name}: {e}")
        
        logger.info("=== Scraping concluído ===")


def main():
    """Função principal para executar o scraper."""
    try:
        scraper = WebScraper()
        scraper.scrape_all_sites(max_pages_per_site=3)
        
        logger.info("Scraping concluído! Execute 'python app/index_builder.py' para criar o índice.")
        
    except KeyboardInterrupt:
        logger.info("Scraping cancelado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal no scraping: {e}")


if __name__ == "__main__":
    main()
