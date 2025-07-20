# -*- coding: utf-8 -*-
"""
Script para fazer scraping dos sites de energia angolanos.
Sites: Total Energies Angola, Sonangol, Azule Energies, ANPG
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
from pathlib import Path
import json
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime

# Configuracao de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnergyScraper:
    """Scraper para sites de energia angolanos."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        })
        
        self.sites = {
            'total': 'https://totalenergies.com/angola',
            'sonangol': 'https://www.sonangol.co.ao',
            'azule': 'https://www.azule-energy.com',
            'anpg': 'https://anpg.co.ao'
        }
    
    def clean_text(self, text):
        """Limpa texto extraido."""
        if not text:
            return ""
        
        # Remove espacos extras
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\xa0', ' ')
        text = text.replace('\u200b', '')
        
        return text.strip()
    
    def extract_content(self, url):
        """Extrai conteudo de uma pagina."""
        try:
            logger.info(f"Extraindo: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove elementos indesejaveis
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # Titulo
            title_elem = soup.find('title')
            title = self.clean_text(title_elem.get_text()) if title_elem else "Sem titulo"
            
            # Conteudo principal
            content = ""
            for selector in ['main', 'article', '.content', '.main-content', '#content']:
                elem = soup.select_one(selector)
                if elem:
                    content = elem.get_text()
                    break
            
            if not content:
                body = soup.find('body')
                content = body.get_text() if body else ""
            
            content = self.clean_text(content)
            
            if len(content) < 100:
                return None
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'length': len(content),
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair {url}: {e}")
            return None
    
    def scrape_site(self, site_key):
        """Faz scraping de um site."""
        base_url = self.sites.get(site_key)
        if not base_url:
            logger.error(f"Site nao encontrado: {site_key}")
            return []
        
        logger.info(f"Scraping {site_key}: {base_url}")
        
        # Extrai pagina principal
        contents = []
        main_content = self.extract_content(base_url)
        if main_content:
            contents.append(main_content)
        
        # Tenta encontrar links adicionais
        try:
            response = self.session.get(base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            base_domain = urlparse(base_url).netloc
            links = set()
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(base_url, href)
                
                if urlparse(full_url).netloc == base_domain:
                    if not any(ext in full_url.lower() for ext in ['.pdf', '.jpg', '.png', '.zip']):
                        links.add(full_url)
            
            # Limita a 3 paginas adicionais
            for url in list(links)[:3]:
                if url != base_url:
                    content = self.extract_content(url)
                    if content:
                        contents.append(content)
                    time.sleep(2)  # Pausa respeitosa
                        
        except Exception as e:
            logger.warning(f"Erro ao buscar links em {base_url}: {e}")
        
        logger.info(f"Extraidas {len(contents)} paginas de {site_key}")
        return contents
    
    def save_contents(self, contents, site_key):
        """Salva conteudos em arquivos."""
        if not contents:
            return
        
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Remove arquivos antigos
        for old_file in data_dir.glob(f"{site_key}_*.txt"):
            old_file.unlink()
        
        # Salva novos conteudos
        for i, content in enumerate(contents, 1):
            filename = f"{site_key}_{i:02d}.txt"
            filepath = data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Titulo: {content['title']}\n")
                f.write(f"URL: {content['url']}\n")
                f.write(f"Extraido em: {content['extracted_at']}\n")
                f.write(f"Tamanho: {content['length']} caracteres\n")
                f.write("=" * 60 + "\n\n")
                f.write(content['content'])
            
            logger.info(f"Salvo: {filepath}")
    
    def scrape_all(self):
        """Faz scraping de todos os sites."""
        logger.info("=== INICIANDO SCRAPING ===")
        
        all_contents = []
        
        for site_key in self.sites.keys():
            try:
                contents = self.scrape_site(site_key)
                if contents:
                    self.save_contents(contents, site_key)
                    all_contents.extend(contents)
                
                time.sleep(3)  # Pausa entre sites
                
            except Exception as e:
                logger.error(f"Erro ao processar {site_key}: {e}")
        
        logger.info(f"=== CONCLUIDO: {len(all_contents)} paginas extraidas ===")
        return all_contents


def main():
    """Funcao principal."""
    try:
        scraper = EnergyScraper()
        scraper.scrape_all()
        
        print("\nScraping concluido!")
        print("Execute: python app/index_builder.py")
        
    except KeyboardInterrupt:
        print("\nScraping cancelado.")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
