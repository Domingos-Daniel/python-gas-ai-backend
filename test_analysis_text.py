#!/usr/bin/env python3
"""
Script de teste para verificar a melhoria na geração de texto de análise
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.data_analyzer import DataAnalyzer

def test_analysis_text():
    """Testa a geração de texto de análise melhorada"""
    
    analyzer = DataAnalyzer()
    
    # Dados de teste para diferentes categorias
    test_cases = [
        {
            'name': 'Distribuição',
            'data': {
                'Total Energies': 35.2,
                'Sonangol': 28.7,
                'Azule Energy': 18.9,
                'Chevron': 10.3,
                'BP': 4.8,
                'Outras': 2.1
            },
            'category': 'distribution',
            'title': 'Distribuição de Participação no Setor Petrolífero'
        },
        {
            'name': 'Financeiro',
            'data': {
                'Investimento em Exploração': 850000000,
                'Desenvolvimento de Campos': 1200000000,
                'Infraestrutura': 450000000,
                'Tecnologia': 230000000,
                'Sustentabilidade': 180000000,
                'Outros': 95000000
            },
            'category': 'financial',
            'title': 'Investimentos no Setor Petrolífero'
        },
        {
            'name': 'Comparação Temporal',
            'data': {
                '2020': 125000,
                '2021': 138000,
                '2022': 142000,
                '2023': 156000,
                '2024': 163000
            },
            'category': 'comparison',
            'title': 'Evolução da Produção de Petróleo'
        }
    ]
    
    print("🧪 Testando a nova geração de texto de análise...\n")
    
    for test_case in test_cases:
        print(f"📊 Teste: {test_case['name']}")
        print("=" * 60)
        
        # Prepara dados de análise
        analysis_data = {
            'data': test_case['data'],
            'analysis_category': test_case['category'],
            'title': test_case['title'],
            'subtitle': 'Análise detalhada'
        }
        
        # Gera texto de análise
        analysis_text = analyzer.generate_analysis_text(analysis_data, f"Análise de {test_case['name']}")
        
        print(analysis_text)
        print("\n" + "=" * 80 + "\n")
    
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    test_analysis_text()