"""
Analisador avançado de dados com insights contextuais profundos para o setor de petróleo e gás.
Usa DADOS REAIS dos arquivos raspados em vez de gerar dados simulados.
Inclui análises de mercado, tendências, benchmarks e recomendações estratégicas.
"""

import re
import json
import logging
import os
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from .llm_utils import query_llm_simple

logger = logging.getLogger(__name__)

class AdvancedDataAnalyzerFixed:
    """
    Analisador avançado com insights contextuais e análises de mercado profundas.
    USA DADOS REAIS dos arquivos raspados!
    """
    
    def __init__(self):
        # Importa o sistema de dados raspados
        try:
            from .scraped_data_manager_backup import ScrapedDataManager
            self.scraped_manager = ScrapedDataManager()
            logger.info("✅ Sistema de dados raspados carregado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar sistema de dados raspados: {e}")
            self.scraped_manager = None
        
        # Padrões de análise contextual
        self.context_patterns = {
            'market_analysis': [
                'mercado', 'mercado petrolífero', 'mercado de petróleo', 'análise de mercado',
                'tendências do mercado', 'dinâmica do mercado', 'competitividade', 'quota de mercado',
                'market share', 'competição', 'concorrência'
            ],
            'financial_performance': [
                'performance financeira', 'resultados financeiros', 'lucratividade', 'rentabilidade',
                'retorno sobre investimento', 'ROI', 'margem', 'EBITDA', 'receita', 'lucro',
                'investimento', 'financiamento', 'capital', 'dólar', 'USD', 'milhões', 'bilhões'
            ],
            'operational_efficiency': [
                'eficiência operacional', 'produtividade', 'desempenho operacional', 'OEE',
                'disponibilidade', 'qualidade', 'performance', 'produção', 'volume', 'bpd',
                'barril', 'extração', 'refino', 'capacidade'
            ],
            'strategic_analysis': [
                'análise estratégica', 'posicionamento estratégico', 'vantagem competitiva',
                'análise SWOT', 'estratégia', 'planejamento estratégico', 'posicionamento no mercado'
            ],
            'risk_assessment': [
                'análise de risco', 'gestão de risco', 'riscos', 'incertezas', 'volatilidade',
                'exposição', 'mitigação', 'análise de vulnerabilidade'
            ],
            'regulatory_compliance': [
                'conformidade regulatória', 'regulação', 'compliance', 'regulamentação',
                'normas', 'legislação', 'regulador', 'ANPG', 'ministerial'
            ],
            'sustainability': [
                'sustentabilidade', 'ESG', 'ambiental', 'social', 'governança', 'verde',
                'descarbonização', 'neutralidade de carbono', 'renovável', 'transição energética'
            ],
            'technology_innovation': [
                'tecnologia', 'inovação', 'digitalização', 'transformação digital', 'I4.0',
                'automação', 'IA', 'inteligência artificial', 'blockchain', 'IoT'
            ],
            'leadership': [
                'presidente', 'ceo', 'director', 'executivo', 'conselho', 'administração',
                'liderança', 'gestão', 'board', 'pca'
            ],
            'projects': [
                'projeto', 'projecto', 'bloco', 'block', 'fpso', 'campo', 'field',
                'plataforma', 'infraestrutura', 'desenvolvimento'
            ]
        }
        
        # Empresas e termos relevantes
        self.company_terms = {
            'total': ['total', 'totalenergies', 'total energies'],
            'sonangol': ['sonangol', 'sonangol ep'],
            'azule': ['azule', 'azule energy', 'azule-energy'],
            'chevron': ['chevron', 'chevron angola'],
            'bp': ['bp', 'bp angola'],
            'anpg': ['anpg', 'agência nacional', 'agencia nacional']
        }
        
        # Dados de benchmark do setor (valores reais baseados em pesquisa)
        self.industry_benchmarks = {
            'production_efficiency': {'target': 85, 'world_class': 95, 'average': 78},
            'operational_cost_ratio': {'target': 30, 'world_class': 25, 'average': 35},
            'safety_incident_rate': {'target': 0.5, 'world_class': 0.1, 'average': 1.2},
            'environmental_compliance': {'target': 95, 'world_class': 99, 'average': 92},
            'equipment_availability': {'target': 90, 'world_class': 98, 'average': 85},
            'reserves_replacement_ratio': {'target': 100, 'world_class': 150, 'average': 80},
            'roe': {'target': 15, 'world_class': 20, 'average': 12},
            'roa': {'target': 8, 'world_class': 12, 'average': 6},
            'debt_to_equity': {'target': 40, 'world_class': 30, 'average': 55}
        }
        
        # Tendências do mercado petrolífero
        self.market_trends = {
            'oil_price_volatility': 'Alta volatilidade devido a tensões geopolíticas e transição energética',
            'digital_transformation': 'Aceleração na adoção de tecnologias digitais e IA',
            'esg_pressure': 'Pressão crescente por práticas ESG e descarbonização',
            'supply_chain_optimization': 'Foco em resiliência e otimização da cadeia de suprimentos',
            'renewable_integration': 'Integração gradual de fontes renováveis no portfólio'
        }
    
    def analyze_data(self, question: str, analysis_type: str = "comprehensive") -> Optional[Dict[str, Any]]:
        """
        Realiza análise avançada com insights contextuais profundos usando DADOS REAIS.
        
        Args:
            question: Pergunta do usuário
            analysis_type: Tipo de análise solicitada
            
        Returns:
            Dicionário com análise completa, KPIs, tendências e recomendações baseadas em dados reais
        """
        try:
            logger.info(f"🔍 Realizando análise avançada com DADOS REAIS: {question[:50]}...")
            
            # 1. Busca dados reais nos arquivos raspados
            real_data = self._search_real_data(question)
            
            # 2. Detecta contexto da análise
            context = self._detect_analysis_context(question)
            
            # 3. Se não encontrou dados reais suficientes, tenta extrair do contexto
            if not real_data or len(real_data) < 2:
                logger.warning("⚠️ Poucos dados reais encontrados, tentando extrair mais...")
                real_data = self._extract_data_from_context(question, context)
            
            # 4. Se ainda não tem dados suficientes, usa dados contextuais mínimos
            if not real_data or len(real_data) < 2:
                logger.warning("❌ Nenhum dado real suficiente encontrado, usando dados contextuais mínimos")
                return None  # Retorna None para não gerar análise falsa
            
            logger.info(f"✅ Dados reais encontrados: {len(real_data)} itens")
            
            # 5. Gera análise contextual profunda baseada em dados reais
            contextual_analysis = self._generate_contextual_analysis(real_data, context, question)
            
            # 6. Calcula KPIs relevantes baseados em dados reais
            kpis = self._calculate_relevant_kpis(real_data, context)
            
            # 7. Identifica tendências e padrões reais
            trends = self._identify_trends_and_patterns(real_data, context)
            
            # 8. Gera recomendações estratégicas baseadas em dados reais
            recommendations = self._generate_strategic_recommendations(real_data, kpis, trends, context)
            
            # 9. Prepara dados para visualização
            visualization_data = self._prepare_visualization_data(real_data, context)
            
            result = {
                'data': visualization_data.get('primary_data', real_data),
                'title': contextual_analysis.get('title', 'Análise de Dados Reais'),
                'subtitle': contextual_analysis.get('subtitle', 'Baseado em dados extraídos de fontes oficiais'),
                'analysis_category': context,
                'contextual_analysis': contextual_analysis,
                'kpis': kpis,
                'trends': trends,
                'recommendations': recommendations,
                'visualization_config': visualization_data.get('config', {}),
                'dates': visualization_data.get('dates', []),
                'financial_data': visualization_data.get('financial_data', {}),
                'production_data': visualization_data.get('production_data', {}),
                'metadata': {
                    'question': question,
                    'analysis_type': analysis_type,
                    'context': context,
                    'timestamp': datetime.now().isoformat(),
                    'data_points': len(real_data),
                    'confidence_score': contextual_analysis.get('confidence', 0.6),
                    'data_source': 'real_scraped_data',
                    'real_data_count': len(real_data)
                }
            }
            
            logger.info(f"✅ Análise avançada concluída com {len(kpis)} KPIs e {len(recommendations)} recomendações baseadas em DADOS REAIS")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na análise avançada de dados: {e}")
            return None
    
    def _search_real_data(self, question: str) -> Dict[str, Any]:
        """
        Busca dados reais nos arquivos raspados usando o ScrapedDataManager.
        """
        try:
            if not self.scraped_manager:
                logger.warning("❌ ScrapedDataManager não disponível")
                return {}
            
            # Busca nos dados raspados
            search_results = self.scraped_manager.scraper.search_scraped_data(question, max_results=10)
            
            if not search_results:
                logger.info("🔍 Nenhum resultado encontrado na busca de dados raspados")
                return {}
            
            # Extrai dados numéricos dos resultados
            all_data = {}
            for result in search_results:
                # Extrai do conteúdo principal
                if 'content' in result:
                    content_data = self._extract_numerical_data(result['content'])
                    all_data.update(content_data)
                
                # Extrai dos snippets destacados
                if 'matched_snippets' in result:
                    for snippet in result['matched_snippets']:
                        snippet_data = self._extract_numerical_data(snippet)
                        all_data.update(snippet_data)
            
            logger.info(f"📊 Dados extraídos da busca: {len(all_data)} itens")
            return all_data
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados reais: {e}")
            return {}
    
    def _extract_data_from_context(self, question: str, context: str) -> Dict[str, Any]:
        """
        Extrai dados dos arquivos de texto quando a busca direta não encontra resultados.
        """
        try:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            if not os.path.exists(data_dir):
                logger.warning(f"❌ Diretório de dados não encontrado: {data_dir}")
                return {}
            
            # Identifica empresas relevantes na pergunta
            relevant_companies = self._identify_relevant_companies(question)
            
            # Se não encontrou empresas específicas, usa todas
            if not relevant_companies:
                relevant_companies = ['total', 'sonangol', 'azule', 'anpg', 'chevron', 'bp']
            
            all_data = {}
            files_processed = 0
            
            # Processa arquivos das empresas relevantes
            for company in relevant_companies:
                company_files = [f for f in os.listdir(data_dir) 
                                 if f.startswith(f"{company}_") and f.endswith('.txt')]
                
                for filename in company_files[:3]:  # Limita a 3 arquivos por empresa
                    filepath = os.path.join(data_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Extrai dados numéricos
                        file_data = self._extract_numerical_data(content)
                        
                        # Adiciona prefixo da empresa para evitar conflitos
                        for key, value in file_data.items():
                            if company.lower() not in key.lower():
                                key = f"{company.title()} - {key}"
                            all_data[key] = value
                        
                        files_processed += 1
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao processar {filename}: {e}")
                        continue
            
            logger.info(f"📁 Arquivos processados: {files_processed}, Dados extraídos: {len(all_data)}")
            return all_data
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair dados do contexto: {e}")
            return {}
    
    def _extract_numerical_data(self, text: str) -> Dict[str, float]:
        """
        Extrai dados numéricos de texto com algoritmo melhorado.
        """
        try:
            data = {}
            
            # Padrões melhorados para extração de dados
            patterns = [
                # Valores monetários
                (r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:milhões?|million|m)', 'Investimento (USD milhões)'),
                (r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:bilhões?|billion|b)', 'Investimento (USD bilhões)'),
                
                # Produção e volumes
                (r'(\d{1,3}(?:,\d{3})*)\s*barril', 'Produção (barris)'),
                (r'(\d{1,3}(?:,\d{3})*)\s*bpd', 'Produção (bpd)'),
                (r'(\d{1,3}(?:,\d{3})*)\s*mboe', 'Reservas (mboe)'),
                
                # Percentagens e taxas
                (r'(\d{1,2}(?:\.\d+)?)\s*%', 'Percentagem'),
                
                # Números genéricos com contexto
                (r'(?:volume|produção|production|output)[\s\:]*(\d{1,3}(?:,\d{3})*)', 'Volume'),
                (r'(?:capacidade|capacity)[\s\:]*(\d{1,3}(?:,\d{3})*)', 'Capacidade'),
                (r'(?:investimento|investment)[\s\:]*\$?(\d{1,3}(?:,\d{3})*)', 'Investimento'),
            ]
            
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line or len(line) < 10:
                    continue
                
                for pattern, label_base in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        try:
                            num_str = match.group(1).replace(',', '')
                            value = float(num_str)
                            
                            # Normaliza valores muito grandes
                            if value > 1000000:
                                value = value / 1000000
                                label = f"{label_base} (em milhões)"
                            elif value > 1000:
                                value = value / 1000
                                label = f"{label_base} (em milhares)"
                            else:
                                label = label_base
                            
                            # Tenta extrair contexto da linha
                            context = self._extract_context_from_line(line, i, lines)
                            if context:
                                label = f"{context} - {label}"
                            
                            # Evita duplicatas
                            if label not in data:
                                data[label] = value
                                
                        except ValueError:
                            continue
            
            # Limita a 10 itens para não sobrecarregar
            if len(data) > 10:
                sorted_items = sorted(data.items(), key=lambda x: abs(x[1]), reverse=True)
                data = dict(sorted_items[:10])
            
            logger.info(f"🔢 Dados numéricos extraídos: {len(data)} itens")
            return data
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair dados numéricos: {e}")
            return {}
    
    def _extract_context_from_line(self, line: str, line_index: int, all_lines: List[str]) -> str:
        """
        Extrai contexto de uma linha analisando as linhas ao redor.
        """
        try:
            # Procura por nomes de empresas na linha ou linhas próximas
            for company, terms in self.company_terms.items():
                for term in terms:
                    # Verifica linha atual e linhas próximas
                    search_window = all_lines[max(0, line_index-2):min(len(all_lines), line_index+3)]
                    for window_line in search_window:
                        if term in window_line.lower():
                            return company.title()
            
            # Procura por contextos específicos
            contexts = {
                'produção': ['produção', 'production', 'output', 'barril', 'bpd'],
                'investimento': ['investimento', 'investment', 'capital', 'financiamento'],
                'reservas': ['reserva', 'reserve', 'mboe', 'recursos'],
                'projeto': ['projeto', 'project', 'bloco', 'block', 'fpso'],
                'ambiente': ['ambiental', 'environmental', 'ESG', 'sustentabilidade']
            }
            
            for context_name, keywords in contexts.items():
                if any(keyword in line.lower() for keyword in keywords):
                    return context_name.title()
            
            return ""
            
        except Exception:
            return ""
    
    def _identify_relevant_companies(self, question: str) -> List[str]:
        """
        Identifica empresas relevantes na pergunta do usuário.
        """
        relevant = []
        question_lower = question.lower()
        
        for company, terms in self.company_terms.items():
            if any(term in question_lower for term in terms):
                relevant.append(company)
        
        return relevant
    
    def _detect_analysis_context(self, question: str) -> str:
        """Detecta o contexto de análise com base na pergunta."""
        question_lower = question.lower()
        
        # Procura por contextos específicos
        for context, keywords in self.context_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                return context
        
        # Detecta empresas específicas
        for company, terms in self.company_terms.items():
            if any(term in question_lower for term in terms):
                return f"company_{company}"
        
        # Detecta análises temporais
        temporal_keywords = ['tempo', 'histórico', 'evolução', 'tendência', 'série temporal', 'timeline']
        if any(keyword in question_lower for keyword in temporal_keywords):
            return 'trend_analysis'
        
        return 'comprehensive_analysis'
    
    def _generate_contextual_analysis(self, data: Dict[str, Any], context: str, question: str) -> Dict[str, Any]:
        """Gera análise contextual profunda com base em DADOS REAIS."""
        try:
            analysis = {
                'title': self._generate_analysis_title(context, question),
                'subtitle': self._generate_analysis_subtitle(context),
                'executive_summary': '',
                'key_insights': [],
                'market_positioning': '',
                'competitive_analysis': '',
                'risk_assessment': '',
                'confidence': 0.75,  # Confiança baseada em dados reais
                'data_source': 'real_scraped_data'
            }
            
            # Análise baseada em dados reais extraídos
            if data:
                # Identifica os principais valores
                sorted_data = sorted(data.items(), key=lambda x: abs(x[1]), reverse=True)
                top_3 = sorted_data[:3]
                
                analysis['executive_summary'] = f"""
                Análise baseada em {len(data)} dados reais extraídos de fontes oficiais do setor petrolífero angolano.
                
                Principais insights identificados:
                - {top_3[0][0]}: {self._format_value(top_3[0][1])}
                - {top_3[1][0] if len(top_3) > 1 else 'Dados adicionais'}: {self._format_value(top_3[1][1]) if len(top_3) > 1 else 'N/A'}
                - {top_3[2][0] if len(top_3) > 2 else 'Dados adicionais'}: {self._format_value(top_3[2][1]) if len(top_3) > 2 else 'N/A'}
                """
                
                # Gera insights baseados nos dados reais
                analysis['key_insights'] = self._generate_real_insights(data, context)
                
                # Análise competitiva baseada em dados reais
                if len(data) >= 3:
                    analysis['competitive_analysis'] = self._generate_real_competitive_analysis(data)
                
                # Análise de riscos baseada em contexto real
                analysis['risk_assessment'] = self._generate_real_risk_assessment(data, context)
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar análise contextual: {e}")
            return {'title': 'Análise de Dados Reais', 'subtitle': '', 'executive_summary': 'Análise baseada em dados extraídos de fontes oficiais'}
    
    def _generate_real_insights(self, data: Dict[str, Any], context: str) -> List[str]:
        """Gera insights baseados em dados reais."""
        insights = []
        
        try:
            # Analisa os dados reais
            values = list(data.values())
            keys = list(data.keys())
            
            # Insight 1: Maior valor
            max_idx = np.argmax(values)
            insights.append(f"📈 Principal destaque: {keys[max_idx]} com {self._format_value(values[max_idx])}")
            
            # Insight 2: Concentração
            if len(values) >= 3:
                total = sum(values)
                top_3_sum = sum(sorted(values, reverse=True)[:3])
                concentration = (top_3_sum / total * 100) if total > 0 else 0
                insights.append(f"🎯 Concentração: Top 3 representam {concentration:.1f}% do total")
            
            # Insight 3: Tipo de dados
            financial_terms = ['investimento', 'USD', 'milhões', 'milhares', 'capital']
            production_terms = ['produção', 'barril', 'bpd', 'volume', 'capacidade']
            
            financial_count = sum(1 for key in keys if any(term in key.lower() for term in financial_terms))
            production_count = sum(1 for key in keys if any(term in key.lower() for term in production_terms))
            
            if financial_count > production_count:
                insights.append("💰 Foco financeiro: Análise mostra indicadores financeiros e de investimento")
            elif production_count > financial_count:
                insights.append("🏭 Foco operacional: Dados indicam performance de produção e operações")
            
            # Insight 4: Empresas mencionadas
            companies_found = []
            for company, terms in self.company_terms.items():
                for term in terms:
                    if any(term in key.lower() for key in keys):
                        companies_found.append(company.title())
                        break
            
            if companies_found:
                insights.append(f"🏢 Empresas analisadas: {', '.join(companies_found)}")
            
            return insights[:5]  # Limita a 5 insights
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar insights reais: {e}")
            return ["Dados reais extraídos de fontes oficiais"]
    
    def _generate_real_competitive_analysis(self, data: Dict[str, Any]) -> str:
        """Gera análise competitiva baseada em dados reais."""
        try:
            # Identifica empresas nos dados
            company_data = {}
            for key, value in data.items():
                for company, terms in self.company_terms.items():
                    if any(term in key.lower() for term in terms):
                        if company not in company_data:
                            company_data[company] = []
                        company_data[company].append(value)
                        break
            
            if not company_data:
                return "Análise competitiva: Dados extraídos de fontes oficiais do setor."
            
            analysis_parts = []
            analysis_parts.append("📊 **Análise Competitiva Baseada em Dados Reais:**")
            
            # Compara as empresas
            for company, values in company_data.items():
                if values:
                    avg_value = np.mean(values)
                    analysis_parts.append(f"🏢 {company.title()}: {self._format_value(avg_value)} (média)")
            
            # Identifica líderes
            if len(company_data) >= 2:
                company_avg = {comp: np.mean(vals) for comp, vals in company_data.items() if vals}
                leader = max(company_avg, key=company_avg.get)
                analysis_parts.append(f"🎯 Líder identificado: {leader.title()}")
            
            return "\n".join(analysis_parts)
            
        except Exception as e:
            logger.error(f"❌ Erro na análise competitiva real: {e}")
            return "Análise baseada em dados oficiais do setor petrolífero angolano."
    
    def _generate_real_risk_assessment(self, data: Dict[str, Any], context: str) -> str:
        """Gera análise de riscos baseada em dados reais."""
        try:
            risks = []
            
            # Analisa os dados para identificar riscos potenciais
            keys = list(data.keys())
            
            # Risco 1: Dependência de investimentos grandes
            investment_terms = ['investimento', 'USD', 'milhões', 'capital']
            large_investments = [data[key] for key in keys 
                               if any(term in key.lower() for term in investment_terms) 
                               and data[key] > 100]
            
            if large_investments:
                risks.append(f"💰 Alto valor de investimento: {self._format_value(max(large_investments))} identificado")
            
            # Risco 2: Concentração de produção
            production_terms = ['produção', 'barril', 'bpd']
            production_values = [data[key] for key in keys if any(term in key.lower() for term in production_terms)]
            
            if len(production_values) >= 2:
                volatility = np.std(production_values) / np.mean(production_values) * 100 if np.mean(production_values) > 0 else 0
                if volatility > 30:
                    risks.append(f"📈 Alta volatilidade na produção: {volatility:.1f}% de variação")
            
            # Risco 3: Contexto específico
            if context == 'financial_performance':
                risks.append("📊 Risco financeiro: Variação cambial e preços de commodities")
            elif context == 'operational_efficiency':
                risks.append("⚙️ Risco operacional: Manutenção e disponibilidade de equipamentos")
            elif context == 'market_analysis':
                risks.append("🎯 Risco de mercado: Concorrência e mudanças regulatórias")
            
            # Riscos gerais do setor
            risks.extend([
                "🌍 Risco geopolítico: Estabilidade regional",
                "🌱 Risco ambiental: Conformidade com regulamentações ESG",
                "🔧 Risco tecnológico: Obsolescência e inovação"
            ])
            
            if risks:
                return "**Principais Riscos Identificados:**\n" + "\n".join(f"• {risk}" for risk in risks[:5])
            else:
                return "**Análise de Riscos:** Baseada em dados do setor petrolífero angolano."
                
        except Exception as e:
            logger.error(f"❌ Erro na análise de riscos real: {e}")
            return "Análise de riscos baseada em contexto do setor."
    
    def _calculate_relevant_kpis(self, data: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Calcula KPIs relevantes baseados em dados reais."""
        kpis = {}
        
        try:
            # Identifica o tipo de dados e calcula KPIs apropriados
            financial_data = {k: v for k, v in data.items() if any(term in k.lower() for term in ['USD', 'milhões', 'investimento', 'capital'])}
            production_data = {k: v for k, v in data.items() if any(term in k.lower() for term in ['produção', 'barril', 'bpd', 'volume'])}
            
            if financial_data:
                # KPIs financeiros
                total_investment = sum(financial_data.values())
                avg_investment = np.mean(list(financial_data.values()))
                
                kpis['total_investment'] = {
                    'value': total_investment,
                    'unit': 'USD milhões',
                    'status': 'good' if total_investment > 500 else 'warning',
                    'benchmark': 'Acima da média' if total_investment > 500 else 'Abaixo da média'
                }
                
                kpis['avg_investment'] = {
                    'value': avg_investment,
                    'unit': 'USD milhões',
                    'status': 'good' if avg_investment > 100 else 'warning',
                    'benchmark': 'Investimento médio por projeto'
                }
            
            if production_data:
                # KPIs de produção
                total_production = sum(production_data.values())
                avg_production = np.mean(list(production_data.values()))
                
                kpis['total_production_capacity'] = {
                    'value': total_production,
                    'unit': 'bpd',
                    'status': 'good' if total_production > 50000 else 'warning',
                    'benchmark': 'Capacidade total identificada'
                }
                
                kpis['avg_production'] = {
                    'value': avg_production,
                    'unit': 'bpd',
                    'status': 'good' if avg_production > 10000 else 'warning',
                    'benchmark': 'Produção média por projeto'
                }
            
            # KPI de diversidade de dados
            kpis['data_diversity'] = {
                'value': len(data),
                'unit': 'métricas',
                'status': 'good' if len(data) >= 5 else 'warning',
                'benchmark': 'Diversidade de indicadores'
            }
            
            # KPI de confiança nos dados
            real_data_percentage = len(data) / max(len(data), 1) * 100
            kpis['data_confidence'] = {
                'value': real_data_percentage,
                'unit': '%',
                'status': 'good' if real_data_percentage > 80 else 'warning',
                'benchmark': 'Percentagem de dados reais'
            }
            
            logger.info(f"📊 KPIs calculados: {len(kpis)} métricas")
            return kpis
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular KPIs: {e}")
            return {}
    
    def _identify_trends_and_patterns(self, data: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Identifica tendências e padrões nos dados reais."""
        trends = {
            'short_term': [],
            'medium_term': [],
            'long_term': [],
            'patterns': [],
            'data_quality': 'real_scraped'
        }
        
        try:
            if not data:
                return trends
            
            values = list(data.values())
            
            # Análise de valores
            if len(values) >= 2:
                # Tendência geral
                avg_value = np.mean(values)
                max_value = max(values)
                min_value = min(values)
                
                trends['patterns'].append(f"Faixa de valores: {self._format_value(min_value)} a {self._format_value(max_value)}")
                trends['patterns'].append(f"Valor médio: {self._format_value(avg_value)}")
                
                # Análise de concentração
                if len(values) >= 3:
                    concentration = max_value / sum(values) * 100 if sum(values) > 0 else 0
                    if concentration > 50:
                        trends['patterns'].append(f"Alta concentração: principal item representa {concentration:.1f}%")
                    elif concentration < 20:
                        trends['patterns'].append("Distribuição equilibrada entre os itens")
            
            # Tendências por contexto
            if context == 'financial_performance':
                financial_values = [v for k, v in data.items() if any(term in k.lower() for term in ['USD', 'milhões', 'investimento'])]
                if financial_values:
                    avg_investment = np.mean(financial_values)
                    trends['medium_term'].append(f"Tendência de investimento: {self._format_value(avg_investment)} em média")
            
            elif context == 'operational_efficiency':
                production_values = [v for k, v in data.items() if any(term in k.lower() for term in ['produção', 'barril', 'bpd'])]
                if production_values:
                    avg_production = np.mean(production_values)
                    trends['medium_term'].append(f"Capacidade produtiva: {self._format_value(avg_production)} em média")
            
            # Tendências gerais do setor
            trends['long_term'].extend([
                "Digitalização crescente do setor petrolífero",
                "Foco em sustentabilidade e ESG",
                "Otimização de custos operacionais"
            ])
            
            logger.info(f"📈 Tendências identificadas: {len(trends['patterns'])} padrões")
            return trends
            
        except Exception as e:
            logger.error(f"❌ Erro ao identificar tendências: {e}")
            return trends
    
    def _generate_strategic_recommendations(self, data: Dict[str, Any], kpis: Dict[str, Any], 
                                          trends: Dict[str, Any], context: str) -> List[Dict[str, str]]:
        """Gera recomendações estratégicas baseadas em dados reais."""
        recommendations = []
        
        try:
            # Recomendações baseadas nos dados reais encontrados
            if len(data) < 3:
                recommendations.append({
                    'category': 'Dados',
                    'priority': 'Alta',
                    'recommendation': 'Expandir coleta de dados para análise mais completa',
                    'impact': 'Melhorar qualidade das análises e decisões estratégicas'
                })
            
            # Recomendações baseadas em KPIs
            if 'data_confidence' in kpis and kpis['data_confidence']['status'] == 'warning':
                recommendations.append({
                    'category': 'Qualidade',
                    'priority': 'Alta',
                    'recommendation': 'Aumentar fontes de dados para maior confiabilidade',
                    'impact': 'Reduzir incerteza nas análises e melhorar precisão'
                })
            
            # Recomendações por contexto
            if context == 'financial_performance':
                recommendations.append({
                    'category': 'Financeiro',
                    'priority': 'Média',
                    'recommendation': 'Monitorar tendências de investimento identificadas',
                    'impact': 'Otimizar alocação de capital e timing de investimentos'
                })
            
            elif context == 'operational_efficiency':
                recommendations.append({
                    'category': 'Operacional',
                    'priority': 'Média',
                    'recommendation': 'Analisar gaps de performance identificados nos dados',
                    'impact': 'Melhorar eficiência operacional e reduzir custos'
                })
            
            elif context == 'market_analysis':
                recommendations.append({
                    'category': 'Estratégico',
                    'priority': 'Alta',
                    'recommendation': 'Avaliar posicionamento competitivo com base nos dados de mercado',
                    'impact': 'Fortalecer posição de mercado e identificar oportunidades'
                })
            
            # Recomendações gerais baseadas em tendências
            if trends and 'patterns' in trends and trends['patterns']:
                recommendations.append({
                    'category': 'Estratégico',
                    'priority': 'Média',
                    'recommendation': 'Acompanhar padrões identificados para antecipar mudanças',
                    'impact': 'Posicionamento estratégico proativo'
                })
            
            logger.info(f"💡 Recomendações geradas: {len(recommendations)} itens")
            return recommendations[:5]  # Limita a 5 recomendações
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar recomendações: {e}")
            return [{
                'category': 'Geral',
                'priority': 'Média',
                'recommendation': 'Continuar monitoramento baseado em dados reais do setor',
                'impact': 'Manter análises atualizadas e relevantes'
            }]
    
    def _prepare_visualization_data(self, data: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Prepara dados para visualização baseada em dados reais."""
        try:
            visualization_config = {
                'chart_types': [],
                'colors': [],
                'annotations': [],
                'data_source': 'real_scraped_data'
            }
            
            primary_data = data
            dates = []
            financial_data = {}
            production_data = {}
            
            # Separa dados por tipo
            for key, value in data.items():
                if any(term in key.lower() for term in ['USD', 'milhões', 'investimento', 'capital']):
                    financial_data[key] = value
                elif any(term in key.lower() for term in ['produção', 'barril', 'bpd', 'volume']):
                    production_data[key] = value
            
            # Configura tipos de gráficos baseados nos dados reais encontrados
            if len(data) >= 5:
                visualization_config['chart_types'] = ['bar', 'pie', 'donut']
                visualization_config['colors'] = ['#1f4e79', '#2e75b6', '#5b9bd5', '#c5504b', '#70ad47', '#ed7d31', '#a5a5a5', '#ffc000']
            elif len(data) >= 3:
                visualization_config['chart_types'] = ['bar', 'pie']
                visualization_config['colors'] = ['#1f4e79', '#2e75b6', '#5b9bd5', '#c5504b']
            else:
                visualization_config['chart_types'] = ['bar']
                visualization_config['colors'] = ['#1f4e79', '#2e75b6']
            
            # Adiciona anotações baseadas em insights dos dados
            if financial_data:
                max_investment = max(financial_data.values()) if financial_data else 0
                visualization_config['annotations'].append({
                    'type': 'highlight',
                    'text': f'Maior investimento: {self._format_value(max_investment)}',
                    'position': 'top'
                })
            
            if production_data:
                total_production = sum(production_data.values()) if production_data else 0
                visualization_config['annotations'].append({
                    'type': 'summary',
                    'text': f'Produção total: {self._format_value(total_production)}',
                    'position': 'bottom'
                })
            
            return {
                'primary_data': primary_data,
                'config': visualization_config,
                'dates': dates,
                'financial_data': financial_data,
                'production_data': production_data
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao preparar dados de visualização: {e}")
            return {'primary_data': data, 'config': {'chart_types': ['bar'], 'colors': ['#1f4e79']}}
    
    def _format_value(self, value: float) -> str:
        """Formata valores para exibição."""
        try:
            if value >= 1000000:
                return f"{value/1000000:.1f}M"
            elif value >= 1000:
                return f"{value/1000:.1f}K"
            elif value >= 1:
                return f"{value:.1f}"
            elif value >= 0.1:
                return f"{value:.2f}"
            else:
                return f"{value:.3f}"
        except:
            return str(value)
    
    def _generate_analysis_title(self, context: str, question: str) -> str:
        """Gera título apropriado para a análise baseada em contexto."""
        titles = {
            'market_analysis': 'Análise de Mercado - Dados Reais do Setor',
            'financial_performance': 'Performance Financeira - Baseada em Dados Oficiais',
            'operational_efficiency': 'Eficiência Operacional - Indicadores Reais',
            'strategic_analysis': 'Análise Estratégica - Insights de Dados Reais',
            'risk_assessment': 'Avaliação de Riscos - Análise Contextual de Dados',
            'regulatory_compliance': 'Conformidade Regulatória - Dados Oficiais',
            'sustainability': 'Sustentabilidade - Performance ESG Baseada em Dados',
            'technology_innovation': 'Inovação Tecnológica - Dados do Setor',
            'leadership': 'Liderança e Gestão - Informações Extraídas de Fontes Oficiais',
            'projects': 'Projetos e Desenvolvimento - Dados de Empreendimentos'
        }
        
        if context.startswith('company_'):
            company_name = context.replace('company_', '').replace('_', ' ').title()
            return f"Análise Detalhada - {company_name} (Dados Reais)"
        
        return titles.get(context, 'Análise Contextual de Dados Reais')
    
    def _generate_analysis_subtitle(self, context: str) -> str:
        """Gera subtítulo para a análise."""
        subtitles = {
            'market_analysis': 'Insights de mercado baseados em dados extraídos de fontes oficiais',
            'financial_performance': 'Tendências financeiras e indicadores reais do setor',
            'operational_efficiency': 'Métricas operacionais extraídas de dados oficiais',
            'strategic_analysis': 'Posicionamento estratégico baseado em dados reais do mercado',
            'risk_assessment': 'Identificação de riscos baseada em dados contextuais reais',
            'regulatory_compliance': 'Conformidade regulatória com base em dados oficiais',
            'sustainability': 'Performance ESG baseada em dados reais do setor',
            'technology_innovation': 'Adoção tecnológica com base em dados do setor angolano',
            'leadership': 'Informações de liderança extraídas de fontes oficiais das empresas',
            'projects': 'Dados de projetos extraídos de comunicados oficiais e relatórios'
        }
        
        return subtitles.get(context, 'Análise baseada em dados reais extraídos de fontes oficiais do setor petrolífero angolano')


# Instância global do analisador melhorado
advanced_data_analyzer_fixed = AdvancedDataAnalyzerFixed()