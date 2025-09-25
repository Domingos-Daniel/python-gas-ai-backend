"""
Firecrawl-based intelligent web scraper for Angola energy sector companies.
Extracts clean, structured content optimized for LLM context.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from firecrawl import FirecrawlApp
import html2text
import markdown
from readability import Document
import requests
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedContent:
    """Structured content from scraped pages"""
    url: str
    title: str
    content: str
    summary: str
    keywords: List[str]
    company: str
    scraped_at: datetime
    content_type: str  # 'about', 'projects', 'news', 'services', 'contact'
    relevance_score: float

class AngolaEnergyScraper:
    """
    Intelligent scraper for Angola energy sector using Firecrawl
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize scraper with Firecrawl API"""
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("Firecrawl API key is required")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # No line wrapping
        
        # Company configurations with optimized scraping strategies
        self.companies = {
            'total': {
                'base_url': 'https://totalenergies.com',
                'angola_path': '/angola',
                'scrape_urls': [
                    'https://totalenergies.com/angola',
                    'https://totalenergies.com/angola/about-us',
                    'https://totalenergies.com/angola/our-activities',
                    'https://totalenergies.com/angola/our-projects',
                    'https://totalenergies.com/angola/sustainability'
                ],
                'keywords': ['TotalEnergies', 'petróleo', 'gás', 'Angola', 'blocos', 'exploração', 'produção'],
                'content_filters': ['about', 'activities', 'projects', 'sustainability', 'news']
            },
            'sonangol': {
                'base_url': 'https://www.sonangol.co.ao',
                'scrape_urls': [
                    'https://www.sonangol.co.ao',
                    'https://www.sonangol.co.ao/about-us',
                    'https://www.sonangol.co.ao/business-areas',
                    'https://www.sonangol.co.ao/projects',
                    'https://www.sonangol.co.ao/news'
                ],
                'keywords': ['Sonangol', 'petróleo', 'Angola', 'exploração', 'produção', 'refinação'],
                'content_filters': ['about', 'business', 'projects', 'news']
            },
            'azule': {
                'base_url': 'https://www.azule-energy.com',
                'scrape_urls': [
                    'https://www.azule-energy.com',
                    'https://www.azule-energy.com/about',
                    'https://www.azule-energy.com/what-we-do',
                    'https://www.azule-energy.com/our-assets',
                    'https://www.azule-energy.com/angola'
                ],
                'keywords': ['Azule Energy', 'Angola', 'petróleo', 'gás', 'PLS', 'exploração'],
                'content_filters': ['about', 'what-we-do', 'assets', 'angola']
            },
            'anpg': {
                'base_url': 'https://anpg.co.ao',
                'scrape_urls': [
                    'https://anpg.co.ao',
                    'https://anpg.co.ao/quem-somos',
                    'https://anpg.co.ao/areas-de-atuacao',
                    'https://anpg.co.ao/concessoes',
                    'https://anpg.co.ao/noticias'
                ],
                'keywords': ['ANPG', 'Agência Nacional', 'Petróleo', 'Gás', 'Angola', 'concessões'],
                'content_filters': ['quem-somos', 'areas', 'concessoes', 'noticias']
            },
            'petroangola': {
                'base_url': 'https://petroangola.com',
                'scrape_urls': [
                    'https://petroangola.com',
                    'https://petroangola.com/category/noticias/',
                    'https://petroangola.com/category/empresas/',
                    'https://petroangola.com/category/petroleo/',
                    'https://petroangola.com/category/gas/'
                ],
                'keywords': ['Petroangola', 'notícias', 'petróleo', 'gás', 'Angola', 'empresas'],
                'content_filters': ['noticias', 'empresas', 'petroleo', 'gas']
            }
        }
    
    def scrape_company(self, company_name: str) -> List[ScrapedContent]:
        """
        Scrape all relevant pages for a specific company
        """
        if company_name not in self.companies:
            raise ValueError(f"Company {company_name} not configured")
        
        company_config = self.companies[company_name]
        scraped_contents = []
        
        logger.info(f"🔍 Starting scrape for {company_name}")
        
        for url in company_config['scrape_urls']:
            try:
                content = self._scrape_page(url, company_name, company_config)
                if content and content.relevance_score > 0.3:  # Only keep relevant content
                    scraped_contents.append(content)
                    logger.info(f"✅ Scraped: {url} (relevance: {content.relevance_score:.2f})")
                else:
                    logger.info(f"⚠️  Low relevance content from: {url}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to scrape {url}: {e}")
                continue
        
        logger.info(f"📊 Total pages scraped for {company_name}: {len(scraped_contents)}")
        return scraped_contents
    
    def _scrape_page(self, url: str, company_name: str, company_config: Dict) -> Optional[ScrapedContent]:
        """
        Scrape a single page with intelligent content extraction
        """
        try:
            # Use Firecrawl to scrape the page
            scrape_result = self.app.scrape_url(
                url,
                params={
                    'formats': ['markdown', 'html'],
                    'includeTags': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'section', 'div'],
                    'excludeTags': ['nav', 'footer', 'header', 'aside', 'script', 'style'],
                    'timeout': 30000,  # 30 seconds timeout
                    'waitFor': 2000,   # Wait 2 seconds for dynamic content
                }
            )
            
            if not scrape_result or 'markdown' not in scrape_result:
                logger.warning(f"No content extracted from {url}")
                return None
            
            # Extract and clean content
            markdown_content = scrape_result.get('markdown', '')
            html_content = scrape_result.get('html', '')
            title = scrape_result.get('metadata', {}).get('title', '')
            
            # Clean and structure the content
            cleaned_content = self._clean_content(markdown_content, html_content)
            summary = self._generate_summary(cleaned_content)
            keywords = self._extract_keywords(cleaned_content, company_config['keywords'])
            relevance_score = self._calculate_relevance(cleaned_content, company_config['keywords'])
            content_type = self._classify_content(url, cleaned_content)
            
            return ScrapedContent(
                url=url,
                title=title or f"{company_name.title()} - {content_type.title()}",
                content=cleaned_content,
                summary=summary,
                keywords=keywords,
                company=company_name,
                scraped_at=datetime.now(),
                content_type=content_type,
                relevance_score=relevance_score
            )
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _clean_content(self, markdown_content: str, html_content: str) -> str:
        """
        Clean and structure content for LLM consumption
        """
        # Use readability to extract main content
        if html_content:
            doc = Document(html_content)
            clean_html = doc.summary()
            # Convert to markdown
            markdown_from_html = self.html_converter.handle(clean_html)
            content = markdown_from_html
        else:
            content = markdown_content
        
        # Clean up the content
        content = self._remove_noise(content)
        content = self._structure_content(content)
        
        return content
    
    def _remove_noise(self, content: str) -> str:
        """
        Remove navigation, ads, and other noise from content
        """
        # Remove common noise patterns
        noise_patterns = [
            r'\n\s*\n\s*\n+',  # Multiple blank lines
            r'\[.*?\]\(.*?\)',  # Markdown links that might be navigation
            r'facebook|twitter|linkedin|instagram',  # Social media
            r'cookie|privacy policy|terms of service',  # Legal text
            r'© \d{4}|copyright|all rights reserved',  # Copyright
        ]
        
        import re
        for pattern in noise_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Remove very short lines (likely navigation or formatting)
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 10 or line.endswith('.'):  # Keep meaningful lines
                clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
    def _structure_content(self, content: str) -> str:
        """
        Structure content with clear sections for LLM processing
        """
        lines = content.split('\n')
        structured_lines = []
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect headers
            if len(line) < 100 and (line.isupper() or line.endswith(':') or line.startswith('#')):
                if current_section:
                    structured_lines.append(f"\n## {current_section}\n")
                current_section = line.strip('#:')
                continue
            
            # Structure paragraphs
            if len(line) > 50:
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)
    
    def _generate_summary(self, content: str) -> str:
        """
        Generate a concise summary of the content
        """
        sentences = content.split('.')
        if len(sentences) > 3:
            summary = '. '.join(sentences[:3]) + '.'
        else:
            summary = content[:300] + '...' if len(content) > 300 else content
        
        return summary.strip()
    
    def _extract_keywords(self, content: str, base_keywords: List[str]) -> List[str]:
        """
        Extract relevant keywords from content
        """
        # Combine base keywords with content-specific keywords
        content_lower = content.lower()
        keywords = base_keywords.copy()
        
        # Add energy sector specific keywords found in content
        energy_terms = [
            'petróleo', 'petroleo', 'óleo', 'oleo', 'gás', 'gas', 'lng',
            'exploração', 'exploracao', 'produção', 'producao', 'refinação', 'refinacao',
            'bloco', 'poço', 'poco', 'offshore', 'onshore', 'submarino',
            'reservas', 'reservatórios', 'reservatorios', 'camadas', 'jazidas',
            'perfuração', 'perfuracao', 'sondagens', 'sísmica', 'sismica',
            'ambiental', 'sustentabilidade', 'renovável', 'renovavel',
            'angola', 'africa', 'atlântico', 'atlantico', 'cabinda'
        ]
        
        for term in energy_terms:
            if term in content_lower and term not in keywords:
                keywords.append(term)
        
        return keywords[:15]  # Limit to top 15 keywords
    
    def _calculate_relevance(self, content: str, keywords: List[str]) -> float:
        """
        Calculate relevance score based on keyword density and content quality
        """
        if not content or not keywords:
            return 0.0
        
        content_lower = content.lower()
        keyword_matches = 0
        total_keywords = len(keywords)
        
        for keyword in keywords:
            if keyword.lower() in content_lower:
                keyword_matches += 1
        
        # Base relevance from keywords
        keyword_relevance = keyword_matches / total_keywords if total_keywords > 0 else 0
        
        # Quality factors
        content_length = len(content)
        has_structure = '#' in content or len(content.split('\n')) > 5
        has_sentences = content.count('.') > 2
        
        quality_score = 0.0
        if content_length > 500:
            quality_score += 0.3
        if has_structure:
            quality_score += 0.2
        if has_sentences:
            quality_score += 0.2
        
        # Combined score
        final_score = (keyword_relevance * 0.6) + (quality_score * 0.4)
        return min(final_score, 1.0)
    
    def _classify_content(self, url: str, content: str) -> str:
        """
        Classify content type based on URL and content analysis
        """
        url_lower = url.lower()
        content_lower = content.lower()
        
        # URL-based classification
        if any(term in url_lower for term in ['about', 'quem-somos', 'sobre']):
            return 'about'
        elif any(term in url_lower for term in ['project', 'projeto', 'atividade', 'activity']):
            return 'projects'
        elif any(term in url_lower for term in ['news', 'noticia', 'blog']):
            return 'news'
        elif any(term in url_lower for term in ['service', 'servico', 'what-we-do']):
            return 'services'
        elif any(term in url_lower for term in ['contact', 'contato']):
            return 'contact'
        
        # Content-based classification
        if any(term in content_lower for term in ['sobre nós', 'quem somos', 'about us', 'nossa empresa']):
            return 'about'
        elif any(term in content_lower for term in ['projeto', 'project', 'atividade', 'exploração', 'produção']):
            return 'projects'
        elif any(term in content_lower for term in ['notícia', 'news', 'recente', 'última']):
            return 'news'
        
        return 'general'
    
    def save_to_file(self, scraped_contents: List[ScrapedContent], output_dir: str = "data"):
        """
        Save scraped content to structured files for LLM consumption
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for content in scraped_contents:
            # Create filename with company and content type
            timestamp = content.scraped_at.strftime("%Y%m%d_%H%M%S")
            filename = f"{content.company}_{content.content_type}_{timestamp}.txt"
            filepath = output_path / filename
            
            # Format content for LLM consumption
            formatted_content = self._format_for_llm(content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            logger.info(f"💾 Saved: {filename}")
    
    def _format_for_llm(self, content: ScrapedContent) -> str:
        """
        Format content specifically for LLM context consumption
        """
        formatted = f"""# {content.title}

**Fonte:** {content.url}
**Empresa:** {content.company.title()}
**Tipo:** {content.content_type.title()}
**Data:** {content.scraped_at.strftime('%Y-%m-%d %H:%M:%S')}
**Relevância:** {content.relevance_score:.2f}
**Keywords:** {', '.join(content.keywords[:10])}

## Resumo
{content.summary}

## Conteúdo Principal
{content.content}

---
"""
        return formatted
    
    def scrape_all_companies(self, output_dir: str = "data") -> Dict[str, List[ScrapedContent]]:
        """
        Scrape all configured companies and save results
        """
        all_results = {}
        
        for company_name in self.companies.keys():
            try:
                logger.info(f"\n🚀 Starting scrape for {company_name}")
                company_contents = self.scrape_company(company_name)
                all_results[company_name] = company_contents
                
                # Save to files
                self.save_to_file(company_contents, output_dir)
                
                logger.info(f"✅ Completed {company_name}: {len(company_contents)} pages scraped")
                
            except Exception as e:
                logger.error(f"❌ Failed to scrape {company_name}: {e}")
                all_results[company_name] = []
        
        return all_results

# Usage example and testing
if __name__ == "__main__":
    # Initialize scraper
    scraper = AngolaEnergyScraper()
    
    # Scrape all companies
    results = scraper.scrape_all_companies()
    
    # Print summary
    for company, contents in results.items():
        print(f"\n{company.upper()}: {len(contents)} pages scraped")
        for content in contents:
            print(f"  - {content.title} ({content.content_type}) - Relevance: {content.relevance_score:.2f}")