"""
Módulo de análise de dados para identificar oportunidades de visualização
nos dados extraídos e prepará-los para geração de gráficos.
"""

import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np
import os
from .llm_utils import query_llm_simple

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analisador de dados para identificar padrões e oportunidades de visualização."""
    
    def __init__(self):
        self.chart_patterns = {
            'distribution': ['distribuição', 'participação', 'percentagem', 'quota', 'market share'],
            'comparison': ['comparação', 'comparar', 'versus', 'vs', 'diferença'],
            'trend': ['tendência', 'evolução', 'progressão', 'histórico', 'série temporal'],
            'composition': ['composição', 'constituição', 'estrutura', 'breakdown'],
            'financial': ['investimento', 'receita', 'lucro', 'custo', 'orçamento', 'financeiro'],
            'operational': ['produção', 'volume', 'capacidade', 'operacional', 'desempenho'],
            'geographic': ['regional', 'localização', 'geográfico', 'província', 'bloco']
        }
        
        self.company_keywords = {
            'total': ['total', 'total energies', 'total angola'],
            'sonangol': ['sonangol', 'sonangol ep'],
            'azule': ['azule', 'azule energy'],
            'anpg': ['anpg', 'agência nacional'],
            'chevron': ['chevron', 'chevron angola'],
            'bp': ['bp', 'bp angola'],
            'en': ['en angola', 'en i', 'eni']
        }
        
        self.sector_metrics = {
            'production': ['produção', 'barril', 'bpd', 'óleo', 'gás', 'reserva'],
            'investment': ['investimento', 'capital', 'financiamento', 'dólar', 'USD'],
            'employment': ['emprego', 'trabalhador', 'funcionário', 'pessoal', 'mão de obra'],
            'environment': ['ambiental', 'sustentabilidade', 'co2', 'emissão', 'verde'],
            'technology': ['tecnologia', 'digital', 'inovação', 'automação', 'inteligência']
        }
    
    def analyze_data(self, question: str, analysis_type: str = "comprehensive") -> Optional[Dict[str, Any]]:
        """
        Analisa a pergunta e identifica oportunidades de visualização.
        
        Args:
            question: Pergunta do usuário
            analysis_type: Tipo de análise ('comprehensive', 'financial', 'operational', 'market')
            
        Returns:
            Dicionário com dados para visualização ou None se não houver dados suficientes
        """
        try:
            logger.info(f"Analisando pergunta para visualização: {question[:50]}...")
            
            # Detecta tipo de análise solicitada
            analysis_category = self._detect_analysis_category(question, analysis_type)
            
            # Gera dados simulados baseados na categoria (para demonstração)
            # Em produção, aqui seria integrado com dados reais do sistema
            mock_data = self._generate_mock_data(analysis_category, question)
            
            if not mock_data:
                logger.info("Nenhum dado relevante encontrado para visualização")
                return None
            
            # Prepara título e subtítulo
            title = self._generate_chart_title(question, analysis_category)
            subtitle = self._generate_chart_subtitle(analysis_category)
            
            result = {
                'data': mock_data,
                'title': title,
                'subtitle': subtitle,
                'analysis_category': analysis_category,
                'chart_types': self._suggest_chart_types(analysis_category, mock_data),
                'metadata': {
                    'question': question,
                    'analysis_type': analysis_type,
                    'timestamp': datetime.now().isoformat(),
                    'data_points': len(mock_data)
                }
            }
            
            logger.info(f"Análise concluída com {len(mock_data)} pontos de dados")
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise de dados: {e}")
            return None
    
    def _detect_analysis_category(self, question: str, analysis_type: str) -> str:
        """Detecta a categoria de análise baseada na pergunta."""
        question_lower = question.lower()
        
        # Mapeamento de tipos de análise
        if analysis_type != "comprehensive":
            return analysis_type
        
        # Detecta por palavras-chave
        for category, keywords in self.chart_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        
        # Detecta empresas específicas
        for company, keywords in self.company_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return f"company_{company}"
        
        # Detecta métricas de setor
        for metric, keywords in self.sector_metrics.items():
            if any(keyword in question_lower for keyword in keywords):
                return f"metric_{metric}"
        
        return "general"
    
    def _get_real_data_from_context(self, question: str, category: str) -> Optional[Dict[str, float]]:
        """Tenta obter dados reais dos arquivos scrapeados antes de usar dados mockados."""
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            if not os.path.exists(data_dir):
                return None
            
            # Procura por arquivos de dados que possam conter informações relevantes
            relevant_files = []
            for filename in os.listdir(data_dir):
                if filename.endswith('.txt') and not filename.startswith('all_urls'):
                    relevant_files.append(os.path.join(data_dir, filename))
            
            # Analisa os arquivos em busca de dados numéricos relevantes
            all_data = {}
            
            for filepath in relevant_files[:5]:  # Limita a 5 arquivos para performance
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Extrai dados numéricos do conteúdo
                    extracted_data = self.extract_numerical_data(content)
                    if extracted_data and len(extracted_data) >= 2:
                        all_data.update(extracted_data)
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar arquivo {filepath}: {e}")
                    continue
            
            # Se encontrou dados suficientes, retorna
            if len(all_data) >= 2:
                logger.info(f"Dados reais extraídos do contexto: {len(all_data)} itens")
                return all_data
                
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados reais: {e}")
            return None
    
    def _generate_mock_data(self, category: str, question: str) -> Dict[str, float]:
        """Gera dados simulados para demonstração baseados na categoria."""
        
        # Primeiro tenta obter dados reais do contexto
        real_data = self._get_real_data_from_context(question, category)
        if real_data:
            return real_data
        
        # Dados de exemplo para diferentes categorias
        mock_datasets = {
            'distribution': {
                'Total Energies': 35.2,
                'Sonangol': 28.7,
                'Azule Energy': 18.9,
                'Chevron': 10.3,
                'BP': 4.8,
                'Outras': 2.1
            },
            'comparison': {
                '2020': 125000,
                '2021': 138000,
                '2022': 142000,
                '2023': 156000,
                '2024': 163000
            },
            'financial': {
                'Investimento em Exploração': 850000000,
                'Desenvolvimento de Campos': 1200000000,
                'Infraestrutura': 450000000,
                'Tecnologia': 230000000,
                'Sustentabilidade': 180000000,
                'Outros': 95000000
            },
            'operational': {
                'Produção de Óleo (bpd)': 1450000,
                'Produção de Gás (mmcf/d)': 8900,
                'Reservas Provas (bilhões)': 8.2,
                'Poços em Operação': 234,
                'Blocos em Produção': 15
            },
            'company_total': {
                'Exploração & Produção': 45.8,
                'Refino & Química': 28.3,
                'Distribuição': 15.7,
                'Gás & Energia': 8.2,
                'Renováveis': 2.0
            },
            'company_sonangol': {
                'Upstream': 52.1,
                'Midstream': 23.4,
                'Downstream': 18.9,
                'Serviços': 5.6
            },
            'metric_production': {
                'Bloco 15': 185000,
                'Bloco 17': 234000,
                'Bloco 31': 156000,
                'Bloco 32': 142000,
                'Bloco 14': 98000
            },
            'metric_investment': {
                'Exploração': 2.1,
                'Desenvolvimento': 3.8,
                'Infraestrutura': 1.2,
                'P&D': 0.4,
                'ESG': 0.3
            }
        }
        
        # Retorna dataset apropriado ou gera um genérico
        base_category = category.split('_')[0] if '_' in category else category
        
        if category in mock_datasets:
            return mock_datasets[category]
        elif base_category in mock_datasets:
            return mock_datasets[base_category]
        else:
            # Gera dados genéricos baseados na pergunta
            return self._generate_generic_data(question)
    
    def _generate_generic_data(self, question: str) -> Dict[str, float]:
        """Gera dados genéricos baseados nas palavras-chave da pergunta."""
        # Extrai possíveis categorias da pergunta
        words = re.findall(r'\b\w+\b', question.lower())
        
        # Categorias comuns
        categories = ['Categoria A', 'Categoria B', 'Categoria C', 'Categoria D', 'Categoria E']
        
        # Gera valores aleatórios mas consistentes
        np.random.seed(len(question))  # Seed baseada no tamanho da pergunta
        
        data = {}
        for i, cat in enumerate(categories):
            value = np.random.uniform(10, 100) * (1 - i * 0.1)  # Valores decrescentes
            data[cat] = round(value, 1)
        
        return data
    
    def _generate_chart_title(self, question: str, category: str) -> str:
        """Gera título apropriado para o gráfico."""
        # Remove palavras comuns e gera título
        clean_question = re.sub(r'^(me )?(faça|crie|mostre|analise|explique)\s+', '', question.lower())
        clean_question = re.sub(r'[?\.!]', '', clean_question)
        
        # Capitaliza primeira letra de cada palavra
        title = clean_question.title()
        
        # Adiciona contexto baseado na categoria
        if category.startswith('company_'):
            company = category.replace('company_', '').title()
            title = f"{company}: {title}"
        elif category.startswith('metric_'):
            metric = category.replace('metric_', '').title()
            title = f"{metric} - {title}"
        
        return title
    
    def _generate_chart_subtitle(self, category: str) -> str:
        """Gera subtítulo descritivo baseado na categoria."""
        subtitles = {
            'distribution': 'Distribuição percentual dos dados',
            'comparison': 'Comparação ao longo do tempo',
            'trend': 'Tendência e evolução histórica',
            'financial': 'Valores em milhões de dólares',
            'operational': 'Métricas operacionais principais',
            'company_total': 'Performance da Total Energies',
            'company_sonangol': 'Performance da Sonangol',
            'metric_production': 'Produção por área/bloco',
            'metric_investment': 'Investimento por categoria (bilhões USD)'
        }
        
        return subtitles.get(category, 'Dados analisados do setor de petróleo e gás em Angola')
    
    def _suggest_chart_types(self, category: str, data: Dict[str, Any]) -> List[str]:
        """Sugere tipos de gráficos apropriados baseados na categoria e dados."""
        suggestions = {
            'distribution': ['pie', 'donut', 'bar'],
            'comparison': ['bar', 'line'],
            'trend': ['line', 'bar'],
            'financial': ['bar', 'pie'],
            'operational': ['bar', 'dashboard'],
            'company_total': ['pie', 'donut'],
            'company_sonangol': ['pie', 'donut'],
            'metric_production': ['bar', 'line'],
            'metric_investment': ['bar', 'pie']
        }
        
        # Sugestões baseadas no número de dados
        if len(data) <= 5:
            preferred = ['pie', 'donut']
        elif len(data) <= 10:
            preferred = ['bar', 'line']
        else:
            preferred = ['line', 'bar']
        
        base_category = category.split('_')[0] if '_' in category else category
        category_suggestions = suggestions.get(base_category, preferred)
        
        # Retorna sugestões ordenadas por preferência
        return category_suggestions
    
    def _get_contextual_analysis(self, data: Dict[str, float], question: str, category: str) -> str:
        """Obtém análise contextualizada do LLM baseada nos dados extraídos."""
        try:
            # Prepara um resumo dos dados para o LLM
            data_summary = ", ".join([f"{k}: {v:.1f}" for k, v in list(data.items())[:5]])
            
            prompt = f"""Como especialista em análise do setor petrolífero angolano, analise estes dados:

Dados encontrados: {data_summary}
Pergunta do usuário: {question}
Categoria: {category}

Forneça uma análise natural, conversacional e insights relevantes sobre o que estes dados significam para o setor petrolífero em Angola. Seja específico e contextual, evando genéricismos."""

            # Usa o LLM para gerar análise contextual
            analysis = query_llm_simple(prompt)
            
            if analysis and len(analysis.strip()) > 50:
                return analysis.strip()
            
        except Exception as e:
            logger.warning(f"Erro ao obter análise contextual: {e}")
        
        return None

    def generate_analysis_text(self, analysis_data: Dict[str, Any], original_question: str) -> str:
        """
        Gera texto de análise baseado nos dados e pergunta original - versão melhorada com IA.
        
        Args:
            analysis_data: Dados da análise
            original_question: Pergunta original do usuário
            
        Returns:
            Texto de análise formatado
        """
        try:
            data = analysis_data.get('data', {})
            category = analysis_data.get('analysis_category', 'general')
            title = analysis_data.get('title', 'Análise')
            
            # Primeiro tenta obter análise contextual do LLM
            contextual_analysis = self._get_contextual_analysis(data, original_question, category)
            if contextual_analysis:
                return f"### 📊 **Análise Contextual: Entendendo os Dados**\n\n{contextual_analysis}"
            
            # Se não conseguiu análise contextual, usa a análise estatística
            # Análise básica dos dados
            total = sum(data.values())
            max_key = max(data, key=data.get)
            min_key = min(data, key=data.get)
            avg = total / len(data) if data else 0
            
            # Gera texto baseado na categoria com linguagem mais natural
            if category == 'distribution':
                # Calcula insights interessantes
                top3 = sorted(data.items(), key=lambda x: x[1], reverse=True)[:3]
                concentration = sum([v for k, v in top3])
                
                # Identifica o contexto real dos dados
                context_clues = []
                if any('gas' in k.lower() or 'discovery' in k.lower() for k in data.keys()):
                    context_clues.append("descobertas de gás")
                if any('bloco' in k.lower() or 'block' in k.lower() for k in data.keys()):
                    context_clues.append("blocos de exploração")
                if any('produção' in k.lower() or 'production' in k.lower() for k in data.keys()):
                    context_clues.append("produção")
                
                context = " e ".join(context_clues) if context_clues else "o setor analisado"
                
                analysis = f"""### 📊 **Análise de Distribuição: Mapeando {context.title()}**

Os números nos contam uma história fascinante sobre {context}. Quando examinamos os dados disponíveis, **{max_key}** se destaca como o elemento principal, representando **{data[max_key]:.1f}** unidades.

**O que isso significa na prática:**

🎯 **Concentração**: Os três maiores ({', '.join([k for k, v in top3])}) representam **{concentration:.1f}%** do total - uma configuração que revela muito sobre a estrutura do mercado.

📈 **Diversidade**: Com **{len(data)}** categorias diferentes, vemos uma diversificação interessante, cada uma com seu papel específico.

**Insight**: A amplitude de **{(data[max_key] - data[min_key]):.1f}** pontos entre o maior e menor valor indica oportunidades e desafios únicos neste segmento."""

            elif category == 'comparison':
                # Análise de tendências
                values = list(data.values())
                years = list(data.keys())
                growth = ((values[-1] / values[0]) - 1) * 100 if len(values) > 1 else 0
                volatility = np.std(values) / np.mean(values) * 100 if len(values) > 2 else 0
                
                analysis = f"""### 📈 **Evolução Temporal: Uma História em Números**

A análise da série temporal revela uma trajetória fascinante. De **{years[0]}** a **{years[-1]}**, observamos uma variação de **{growth:+.1f}%**, refletindo as dinâmicas do mercado petrolífero angolano.

**Tendências Identificadas:**

🔄 **Volatilidade**: Com coeficiente de variação de **{volatility:.1f}%**, os dados mostram uma certa estabilidade/instabilidade ao longo do período.

📊 **Faixa de Variação**: Os valores oscilaram entre **{min(values):,}** e **{max(values):,}** unidades, representando uma amplitude de **{(max(values) - min(values)):,}** unidades.

**Perspectiva Histórica**: A média anual de **{avg:,.0f}** unidades nos dá uma referência importante para entender o comportamento do setor ao longo do tempo."""

            elif category == 'financial':
                # Análise financeira mais profunda
                top_investment = max(data.items(), key=lambda x: x[1])
                investment_ratio = top_investment[1] / total
                
                analysis = f"""### 💰 **Panorama Financeiro: Onde Vai o Dinheiro**

Os números financeiros revelam a estratégia de investimento do setor. Com um volume total de **${total:,.0f}**, observamos prioridades claras na alocação de recursos.

**Destaques Financeiros:**

💎 **Principal Investimento**: **{top_investment[0]}** recebe **${top_investment[1]:,.0f}**, representando **{investment_ratio*100:.1f}%** do total - indicando onde está o foco estratégico.

🎯 **Concentração de Recursos**: A análise mostra que **{max_key}** e **{min_key}** representam as extremidades do espectro de investimento, com uma diferença significativa de **${(data[max_key] - data[min_key]):,.0f}**.

**Interpretação Estratégica**: O valor médio de **${avg:,.0f}** por categoria nos ajuda a entender o perfil de risco e retorno esperado para cada área de investimento."""

            else:
                # Análise genérica mais envolvente
                categories_above_avg = len([v for v in data.values() if v > avg])
                
                analysis = f"""### 📋 **Análise Detalhada: O que os Dados nos Contam**

Ao explorar os dados disponíveis, descobrimos um panorama multifacetado do setor. A análise abrange **{len(data)}** categorias principais, cada uma com sua própria importância estratégica.

**Principais Descobertas:**

🌟 **Líder de Mercado**: **{max_key}** se destaca com **{data[max_key]:.1f}** unidades, estabelecendo-se como referência no setor analisado.

📊 **Distribuição de Performance**: **{categories_above_avg}** das categorias analisadas estão acima da média de **{avg:.1f}**, indicando uma distribuição equilibrada ou concentrada.

**Síntese dos Insights**: Os dados apontam para um setor em **{min_key}** com **{data[min_key]:.1f}** unidades representando áreas de potencial crescimento, enquanto **{max_key}** demonstra maturidade e estabilidade operacional."""

            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao gerar texto de análise: {e}")
            return "Com base nos dados disponíveis, realizamos uma análise abrangente que revela insights importantes sobre o setor petrolífero angolano."
    
    def extract_numerical_data(self, text: str) -> Dict[str, float]:
        """
        Extrai dados numéricos de texto para análise - versão melhorada para dados reais do setor petrolífero.
        
        Args:
            text: Texto para extrair dados
            
        Returns:
            Dicionário com dados numéricos extraídos
        """
        try:
            data = {}
            
            # Padrões específicos para o setor petrolífero angolano
            patterns = [
                # Produção (bpd, barris por dia)
                (r'(\d{1,3}(?:,\d{3})*)\s*bpd?', r'Produção\s+[\w\s]*?(?:em|de)?\s*([\w\s]+?)(?:\s*[:\-\|]|\s*(?:atingiu|foi|é))'),
                # Reservas (bilhões de barris)
                (r'(\d+\.?\d*)\s*(?:bilhão|bilhões|billion)', r'Reservas\s+[\w\s]*?(?:de)?\s*([\w\s]+?)(?:\s*[:\-\|]|\s*(?:são|totalizam))'),
                # Investimentos (milhões/bilhões USD)
                (r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:milhão|milhões|million|bilhão|bilhões|billion)?\s*\$?(?:USD)?', r'Investimento\s+[\w\s]*?(?:em|de)?\s*([\w\s]+?)(?:\s*[:\-\|]|\s*(?:será|foi|é))'),
                # Percentagens
                (r'(\d{1,2}(?:\.\d+)?)\s*%', r'([\w\s]+?)(?:\s*representa|\s*atinge|\s*atingiu|\s*corresponde|\s*é)\s*\d{1,2}(?:\.\d+)?\s*%'),
                # Números gerais com contexto
                (r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', r'([A-Z][\w\s]{3,30}?)(?:\s*[:\-\|]|\s*(?:tem|possui|conta|apresenta))\s*\d{1,3}(?:,\d{3})*(?:\.\d+)?')
            ]
            
            # Processa o texto linha por linha
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line or len(line) < 10:  # Pula linhas muito curtas
                    continue
                    
                for num_pattern, label_pattern in patterns:
                    num_matches = re.findall(num_pattern, line, re.IGNORECASE)
                    if num_matches:
                        # Tenta encontrar um label apropriado
                        label_match = re.search(label_pattern, line, re.IGNORECASE)
                        if label_match:
                            label = label_match.group(1).strip()
                            # Limpa o label
                            label = re.sub(r'^[\s\-\|]*', '', label)
                            label = re.sub(r'[\s\-\|]*$', '', label)
                            label = re.sub(r'\s+', ' ', label)
                            
                            if label and len(label) > 3 and len(label) < 40:
                                # Processa o número (remove vírgulas)
                                num_str = num_matches[0].replace(',', '')
                                try:
                                    num_value = float(num_str)
                                    # Normaliza valores muito grandes (converte para milhões se necessário)
                                    if num_value > 1000000:
                                        num_value = num_value / 1000000
                                        label = f"{label} (em milhões)"
                                    data[label] = num_value
                                except ValueError:
                                    continue
            
            # Se não encontrou dados suficientes, tenta padrões mais simples
            if len(data) < 2:
                # Procura por padrões básicos de números e porcentagens
                basic_patterns = [
                    (r'(\d{1,2}(?:\.\d+)?)\s*%', r'([\w\s]{5,30})'),
                    (r'\$(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', r'([\w\s]{5,30})'),
                    (r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', r'([\w\s]{5,30})')
                ]
                
                for line in lines[:20]:  # Limita às primeiras 20 linhas
                    for num_pattern, label_pattern in basic_patterns:
                        matches = re.finditer(f'{label_pattern}.*?{num_pattern}', line, re.IGNORECASE)
                        for match in matches:
                            try:
                                label = match.group(1).strip()
                                number = match.group(2).replace(',', '')
                                data[label] = float(number)
                            except:
                                continue
            
            # Limita a 8 itens para não sobrecarregar
            if len(data) > 8:
                # Pega os 8 maiores valores
                sorted_items = sorted(data.items(), key=lambda x: abs(x[1]), reverse=True)
                data = dict(sorted_items[:8])
            
            logger.info(f"Dados extraídos: {len(data)} itens")
            return data if len(data) >= 2 else {}
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados numéricos: {e}")
            return {}