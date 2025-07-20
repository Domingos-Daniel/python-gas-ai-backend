"""
Script específico para fazer scraping dos sites das empresas angolanas de energia.
Sites alvo: Total Energies Angola, Sonangol, Azule Energies, ANPG
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

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnergySiteScraper:
    """Scraper especializado para sites de energia angolanos."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        # Sites com configurações específicas
        self.sites_config = {
            'total': {
                'url': 'https://totalenergies.com/angola',
                'name': 'Total Energies Angola',
                'selectors': {
                    'content': ['main', 'article', '.content', '.main-content', '#content'],
                    'remove': ['nav', 'footer', 'header', '.menu', '.navigation', 'script', 'style']
                },
                'max_pages': 5
            },
            'sonangol': {
                'url': 'https://www.sonangol.co.ao',
                'name': 'Sonangol',
                'selectors': {
                    'content': ['main', '.content', '#content', '.main-content', 'article'],
                    'remove': ['nav', 'footer', 'header', '.menu', '.sidebar', 'script', 'style']
                },
                'max_pages': 5
            },
            'azule': {
                'url': 'https://www.azule-energy.com',
                'name': 'Azule Energy',
                'selectors': {
                    'content': ['main', 'article', '.content', '.main-content'],
                    'remove': ['nav', 'footer', 'header', '.menu', 'script', 'style']
                },
                'max_pages': 5
            },
            'anpg': {
                'url': 'https://anpg.co.ao',
                'name': 'ANPG',
                'selectors': {
                    'content': ['main', '.content', '#content', '.main-content'],
                    'remove': ['nav', 'footer', 'header', '.menu', 'script', 'style']
                },
                'max_pages': 4
            }
        }
    
    def clean_text(self, text: str) -> str:
        """Limpa e formata texto extraído."""
        if not text:
            return ""
        
        # Remove espaços extras e quebras de linha
        text = re.sub(r'\s+', ' ', text)
        
        # Remove caracteres especiais problemáticos
        text = text.replace('\xa0', ' ')
        text = text.replace('\u200b', '')
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        
        # Remove múltiplos espaços
        text = re.sub(r'\s{2,}', ' ', text)
        
        return text.strip()
    
    def extract_page_content(self, url: str, site_key: str) -> dict:
        """Extrai conteúdo de uma página específica."""
        try:
            logger.info(f"Extraindo conteúdo de: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Detecta encoding
            if response.encoding == 'ISO-8859-1':
                response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            config = self.sites_config[site_key]
            
            # Remove elementos indesejados
            for selector in config['selectors']['remove']:
                for element in soup.select(selector):
                    element.decompose()
            
            # Extrai título
            title_elem = soup.find('title')
            if title_elem:
                title = self.clean_text(title_elem.get_text())
            else:
                title = f"Página - {config['name']}"
            
            # Extrai conteúdo principal
            content_text = ""
            for selector in config['selectors']['content']:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text()
                    break
            
            # Fallback para body se não encontrar conteúdo específico
            if not content_text:
                body = soup.find('body')
                if body:
                    content_text = body.get_text()
            
            content_text = self.clean_text(content_text)
            
            # Filtra conteúdo muito pequeno
            if len(content_text) < 200:
                logger.warning(f"Conteúdo muito pequeno em {url}: {len(content_text)} chars")
                return None
            
            return {
                'title': title,
                'content': content_text,
                'url': url,
                'site': config['name'],
                'extracted_at': datetime.now().isoformat(),
                'content_length': len(content_text)
            }
            
        except requests.RequestException as e:
            logger.error(f"Erro de rede ao acessar {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair conteúdo de {url}: {e}")
            return None
    
    def discover_pages(self, base_url: str, site_key: str) -> list:
        """Descobre páginas relevantes de um site."""
        try:
            logger.info(f"Descobrindo páginas em: {base_url}")
            
            response = self.session.get(base_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = set([base_url])  # Inclui a página principal
            base_domain = urlparse(base_url).netloc
            
            # Busca links internos
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                link_domain = urlparse(full_url).netloc
                
                # Filtra apenas links do mesmo domínio
                if link_domain == base_domain:
                    # Filtra links relevantes (evita downloads, imagens, etc.)
                    if not any(ext in full_url.lower() for ext in ['.pdf', '.jpg', '.png', '.zip', '.doc', '.xls']):
                        if '#' not in full_url:  # Remove âncoras
                            links.add(full_url)
            
            # Limita número de páginas
            max_pages = self.sites_config[site_key]['max_pages']
            links_list = list(links)[:max_pages]
            
            logger.info(f"Descobertas {len(links_list)} páginas em {base_url}")
            return links_list
            
        except Exception as e:
            logger.error(f"Erro ao descobrir páginas de {base_url}: {e}")
            return [base_url]  # Retorna pelo menos a URL base
    
    def scrape_site(self, site_key: str) -> list:
        """Faz scraping de um site específico."""
        if site_key not in self.sites_config:
            logger.error(f"Site não configurado: {site_key}")
            return []
        
        config = self.sites_config[site_key]
        base_url = config['url']
        
        logger.info(f"=== Iniciando scraping: {config['name']} ===")
        
        # Descobre páginas
        pages = self.discover_pages(base_url, site_key)
        
        # Extrai conteúdo de cada página
        contents = []
        for i, page_url in enumerate(pages, 1):
            logger.info(f"Processando página {i}/{len(pages)}: {page_url}")
            
            content = self.extract_page_content(page_url, site_key)
            if content:
                contents.append(content)
            
            # Pausa respeitosa entre requisições
            time.sleep(2)
        
        logger.info(f"=== Concluído {config['name']}: {len(contents)} páginas extraídas ===")
        return contents
    
    def save_content(self, contents: list, site_key: str) -> None:
        """Salva conteúdo extraído em arquivos."""
        if not contents:
            logger.warning(f"Nenhum conteúdo para salvar de {site_key}")
            return
        
        config = self.sites_config[site_key]
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Remove arquivos antigos deste site
        for old_file in data_dir.glob(f"{site_key}_*.txt"):
            old_file.unlink()
        
        # Salva novos conteúdos
        for i, content in enumerate(contents, 1):
            filename = f"{site_key}_{i:02d}.txt"
            filepath = data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Título: {content['title']}\n")
                f.write(f"Site: {content['site']}\n")
                f.write(f"URL: {content['url']}\n")
                f.write(f"Data de extração: {content['extracted_at']}\n")
                f.write(f"Tamanho do conteúdo: {content['content_length']} caracteres\n")
                f.write("=" * 80 + "\n\n")
                f.write(content['content'])
            
            logger.info(f"Salvo: {filepath} ({content['content_length']} chars)")
        
        # Salva também metadata em JSON
        metadata_file = data_dir / f"{site_key}_metadata.json"
        metadata = {
            'site': config['name'],
            'url': config['url'],
            'extracted_at': datetime.now().isoformat(),
            'pages_count': len(contents),
            'total_content_length': sum(c['content_length'] for c in contents),
            'pages': [{'title': c['title'], 'url': c['url'], 'length': c['content_length']} for c in contents]
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def scrape_all_sites(self) -> None:
        """Faz scraping de todos os sites configurados."""
        logger.info("=== INICIANDO SCRAPING DE TODOS OS SITES ===")
        
        total_contents = []
        
        for site_key in self.sites_config.keys():
            try:
                contents = self.scrape_site(site_key)
                if contents:
                    self.save_content(contents, site_key)
                    total_contents.extend(contents)
                else:
                    logger.warning(f"Nenhum conteúdo extraído de {site_key}")
                
                # Pausa entre sites
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Erro ao processar {site_key}: {e}")
        
        # Resumo final
        logger.info("=== RESUMO DO SCRAPING ===")
        logger.info(f"Total de páginas extraídas: {len(total_contents)}")
        logger.info(f"Total de caracteres: {sum(c.get('content_length', 0) for c in total_contents)}")
        
        if total_contents:
            logger.info("✅ Scraping concluído com sucesso!")
            logger.info("Execute 'python app/index_builder.py' para criar o índice.")
        else:
            logger.warning("⚠️ Nenhum conteúdo foi extraído.")


def main():
    """Função principal."""
    try:
        scraper = EnergySiteScraper()
        scraper.scrape_all_sites()
        
    except KeyboardInterrupt:
        logger.info("Scraping cancelado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")


if __name__ == "__main__":
    main()
