#!/usr/bin/env python3
"""
Módulo de integração do scraper com o sistema LLM.
Permite buscas inteligentes nos dados scraped e citações de fontes.
"""

import logging
from typing import List, Dict, Optional, Tuple
from .scraper import AngolaEnergyScraper

logger = logging.getLogger(__name__)


class ScrapedDataManager:
    """
    Gerenciador de dados scraped para integração com LLM.
    Fornece busca inteligente e formatação de respostas com citações.
    """

    def __init__(self):
        self.scraper = AngolaEnergyScraper()

    def search_and_format_response(self, question: str, max_results: int = 5) -> Tuple[str, List[Dict]]:
        """
        Busca nos dados scraped e formata resposta inteligente com citações.

        Args:
            question: Pergunta do usuário
            max_results: Número máximo de resultados

        Returns:
            Tupla com (resposta_formatada, lista_de_fontes)
        """
        try:
            # Busca nos dados scraped
            search_results = self.scraper.search_scraped_data(question, max_results=max_results)

            if not search_results:
                return "Não encontrei informações específicas sobre esta pergunta nos dados disponíveis.", []

            # Análise inteligente da pergunta
            question_lower = question.lower()
            is_general_company_question = self._is_general_company_question(question_lower)
            is_leadership_question = self._is_leadership_question(question_lower)
            target_company = self._extract_target_company(question_lower)

            # Formata resposta baseada no tipo de pergunta
            response_parts = []
            sources = []

            if is_general_company_question and target_company:
                # Resposta estruturada para pergunta geral sobre empresa
                response_parts.append(f"🏢 **{target_company.upper()} - Agência Nacional de Petróleo, Gás e Biocombustíveis**\n")
                response_parts.append("A ANPG é a entidade reguladora do setor petrolífero angolano, responsável por:\n")
                response_parts.append("• **Regulação** do setor upstream e downstream")
                response_parts.append("• **Fiscalização** de concessões e contratos")
                response_parts.append("• **Promoção** de investimentos no setor energético")
                response_parts.append("• **Monitoramento** da produção petrolífera nacional\n")

                # Adiciona informações específicas encontradas
                leadership_info = []
                general_info = []

                for result in search_results:
                    if result['found_in_leadership']:
                        leadership_info.append(result)
                    else:
                        general_info.append(result)

                # Seção de liderança
                if leadership_info:
                    response_parts.append("� **Estrutura Executiva:**")
                    for result in leadership_info[:3]:  # Máximo 3 itens de liderança
                        executives = self._extract_executive_names(result.get('leadership_content', ''))
                        if executives:
                            response_parts.append(f"• **Executivos identificados:** {', '.join(executives[:3])}")
                        else:
                            # Extrai informações relevantes do título
                            title_info = self._extract_title_info(result['title'])
                            if title_info:
                                response_parts.append(f"• {title_info}")
                        sources.append({
                            'name': 'ANPG',
                            'url': result['url'],
                            'description': f"Página: {result['title'][:50]}...",
                            'relevance_score': result['relevance_score']
                        })

                # Seção de informações gerais
                if general_info:
                    response_parts.append("\n� **Atividades Recentes:**")
                    for result in general_info[:2]:  # Máximo 2 itens gerais
                        # Extrai informações-chave do snippet
                        key_info = self._extract_key_info(result.get('matched_snippets', []))
                        if key_info:
                            response_parts.append(f"• {key_info}")
                        sources.append({
                            'name': 'ANPG',
                            'url': result['url'],
                            'description': f"Página: {result['title'][:50]}...",
                            'relevance_score': result['relevance_score']
                        })

            elif is_leadership_question:
                # Resposta focada em liderança
                response_parts.append("📊 **Informações Executivas Encontradas:**\n")

                for result in search_results[:3]:
                    if result['found_in_leadership']:
                        executives = self._extract_executive_names(result.get('leadership_content', ''))
                        if executives:
                            response_parts.append(f"👤 **Executivos identificados:** {', '.join(executives[:5])}")
                        else:
                            response_parts.append(f"📄 **{result['title']}**")

                        # Adiciona contexto relevante
                        if result['matched_snippets']:
                            for snippet in result['matched_snippets'][:1]:
                                clean_snippet = snippet.replace('...', '').strip()
                                if len(clean_snippet) > 20:
                                    response_parts.append(f"   💡 {clean_snippet[:200]}...")

                        response_parts.append(f"   🔗 Fonte: [{result['site'].title()}]({result['url']})\n")

                        sources.append({
                            'name': result['site'].title(),
                            'url': result['url'],
                            'description': f"Página: {result['title']}",
                            'relevance_score': result['relevance_score']
                        })

            else:
                # Resposta genérica
                response_parts.append("📋 **Informações Encontradas:**\n")

                for result in search_results[:3]:
                    response_parts.append(f"📄 **{result['title']}**")

                    if result['matched_snippets']:
                        for snippet in result['matched_snippets'][:1]:
                            clean_snippet = snippet.replace('...', '').strip()
                            if len(clean_snippet) > 20:
                                response_parts.append(f"   💡 {clean_snippet[:150]}...")

                    response_parts.append(f"   🔗 [{result['site'].title()}]({result['url']})\n")

                    sources.append({
                        'name': result['site'].title(),
                        'url': result['url'],
                        'description': f"Página: {result['title']}",
                        'relevance_score': result['relevance_score']
                    })

            # Junta tudo
            final_response = '\n'.join(response_parts)

            # Adiciona nota sobre atualização dos dados
            final_response += "\n---\n*Dados atualizados automaticamente dos sites oficiais das empresas angolanas*"

            return final_response, sources

        except Exception as e:
            logger.error(f"Erro na busca de dados scraped: {e}")
            return f"Erro ao consultar dados: {str(e)}", []

    def get_leadership_info_formatted(self, company: Optional[str] = None) -> str:
        """
        Retorna informações de liderança formatadas.

        Args:
            company: Empresa específica (opcional)

        Returns:
            Informações formatadas sobre liderança
        """
        try:
            leadership_data = self.scraper.get_leadership_info(company)

            if not leadership_data:
                if company:
                    return f"Não encontrei informações de liderança para {company}."
                else:
                    return "Não encontrei informações de liderança disponíveis."

            response_parts = ["👥 **Informações Executivas:**\n"]

            for info in leadership_data:
                response_parts.append(f"🏢 **{info['company'].upper()}**")
                response_parts.append(f"📋 {info['title']}")

                if info['leadership_content']:
                    # Extrai nomes de executivos do conteúdo
                    executives = self._extract_executive_names(info['leadership_content'])
                    if executives:
                        response_parts.append("👤 **Executivos identificados:**")
                        for exec_name in executives[:5]:  # Máximo 5 por empresa
                            response_parts.append(f"   • {exec_name}")
                    else:
                        # Mostra conteúdo bruto se não conseguir extrair nomes
                        content_preview = info['leadership_content'][:300]
                        response_parts.append(f"   💡 {content_preview}...")

                response_parts.append(f"   🔗 {info['citation']}\n")

            return '\n'.join(response_parts)

        except Exception as e:
            logger.error(f"Erro ao obter informações de liderança: {e}")
            return f"Erro ao consultar informações de liderança: {str(e)}"

    def _is_leadership_question(self, question: str) -> bool:
        """Verifica se a pergunta é sobre liderança/executivos."""
        leadership_keywords = [
            'pca', 'presidente', 'ceo', 'director', 'executivo', 'conselho',
            'board', 'administração', 'management', 'quem é', 'quem está',
            'quem comanda', 'quem dirige', 'líder', 'liderança'
        ]
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in leadership_keywords)

    def _is_company_question(self, question: str) -> bool:
        """Verifica se a pergunta é sobre uma empresa específica."""
        company_keywords = [
            'sonangol', 'total', 'azule', 'anpg', 'petroangola',
            'empresa', 'companhia', 'sobre a', 'sobre o', 'me fale sobre',
            'fale sobre', 'o que é', 'quem é'
        ]
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in company_keywords)

    def _is_general_company_question(self, question: str) -> bool:
        """Verifica se é uma pergunta geral sobre uma empresa (não específica sobre liderança)."""
        general_keywords = [
            'me fale sobre', 'fale sobre', 'sobre a', 'sobre o', 'o que é',
            'quem é', 'empresa', 'companhia', 'organização', 'entidade'
        ]
        leadership_keywords = [
            'pca', 'presidente', 'ceo', 'director', 'executivo', 'conselho',
            'quem comanda', 'quem dirige', 'líder', 'liderança'
        ]

        has_general = any(keyword in question for keyword in general_keywords)
        has_leadership = any(keyword in question for keyword in leadership_keywords)

        return has_general and not has_leadership

    def _extract_target_company(self, question: str) -> Optional[str]:
        """Extrai o nome da empresa alvo da pergunta."""
        companies = {
            'anpg': ['anpg', 'agência nacional', 'agencia nacional', 'petróleo', 'petroleo'],
            'sonangol': ['sonangol'],
            'total': ['total', 'totalenergies'],
            'azule': ['azule', 'azul'],
            'petroangola': ['petroangola', 'petro angola']
        }

        for company, keywords in companies.items():
            if any(keyword in question for keyword in keywords):
                return company

        return None

    def _extract_title_info(self, title: str) -> Optional[str]:
        """Extrai informações relevantes do título."""
        title_lower = title.lower()

        # Padrões comuns em títulos da ANPG
        if 'visita' in title_lower:
            return "Realização de visitas técnicas e institucionais"
        elif 'entrega' in title_lower or 'entregam' in title_lower:
            return "Entrega de projetos sociais e infraestrutura"
        elif 'assinatura' in title_lower or 'contrato' in title_lower:
            return "Formalização de contratos e acordos"
        elif 'descoberta' in title_lower:
            return "Descobertas de novos reservatórios"
        elif 'produção' in title_lower or 'inicio' in title_lower:
            return "Inícios de produção e desenvolvimento de campos"
        elif 'forum' in title_lower or 'conferência' in title_lower:
            return "Participação em eventos e fóruns do setor"

        return None

    def _extract_key_info(self, snippets: List[str]) -> Optional[str]:
        """Extrai informações-chave dos snippets."""
        if not snippets:
            return None

        # Junta todos os snippets e procura por informações relevantes
        combined_text = ' '.join(snippets).lower()

        # Procura por números e estatísticas
        import re
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', combined_text)

        if numbers:
            # Se há números, pode ser produção, valores, etc.
            return f"Dados quantitativos identificados: {', '.join(numbers[:3])}"

        # Procura por nomes de projetos ou blocos
        project_patterns = [
            r'bloco \d+', r'bloco [IVX]+', r'fpso \w+', r'clov', r'egina',
            r'pazflor', r'dalia', r'girassol', r'jasmim', r'rosa', r'orchid'
        ]

        for pattern in project_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            if matches:
                return f"Projetos mencionados: {', '.join(set(matches[:3]))}"

        # Procura por ações ou atividades
        actions = []
        if 'entrega' in combined_text or 'entregam' in combined_text:
            actions.append("entrega de infraestrutura")
        if 'visita' in combined_text:
            actions.append("visitas técnicas")
        if 'contrato' in combined_text or 'assinatura' in combined_text:
            actions.append("formalização de contratos")
        if 'produção' in combined_text or 'produzir' in combined_text:
            actions.append("atividades de produção")

        if actions:
            return f"Atividades: {', '.join(actions)}"

        return None

    def _extract_executive_names(self, text: str) -> List[str]:
        """
        Extrai nomes de executivos do texto usando padrões comuns.

        Args:
            text: Texto para analisar

        Returns:
            Lista de nomes encontrados
        """
        import re

        # Padrões para nomes de executivos em português
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',  # Nomes próprios (2+ palavras)
            r'PCA[^a-zA-Z]*([A-Z][a-z]+\s+[A-Z][a-z]+)',  # PCA Nome Sobrenome
            r'Presidente[^a-zA-Z]*([A-Z][a-z]+\s+[A-Z][a-z]+)',  # Presidente Nome Sobrenome
            r'Director[^a-zA-Z]*([A-Z][a-z]+\s+[A-Z][a-z]+)',  # Director Nome Sobrenome
            r'CEO[^a-zA-Z]*([A-Z][a-z]+\s+[A-Z][a-z]+)',  # CEO Nome Sobrenome
        ]

        names = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            names.extend(matches)

        # Remove duplicatas e filtra nomes válidos (pelo menos 2 palavras)
        unique_names = list(set(names))
        valid_names = [name.strip() for name in unique_names if len(name.split()) >= 2]

        return valid_names[:10]  # Máximo 10 nomes


# Instância global do gerenciador
scraped_data_manager = ScrapedDataManager()


def search_scraped_data_for_llm(question: str) -> Tuple[str, List[Dict]]:
    """
    Função de conveniência para buscar dados scraped e formatar para LLM.

    Args:
        question: Pergunta do usuário

    Returns:
        Tupla com (resposta_formatada, fontes)
    """
    return scraped_data_manager.search_and_format_response(question)


def get_leadership_info_for_llm(company: Optional[str] = None) -> str:
    """
    Função de conveniência para obter informações de liderança formatadas.

    Args:
        company: Empresa específica (opcional)

    Returns:
        Informações formatadas
    """
    return scraped_data_manager.get_leadership_info_formatted(company)