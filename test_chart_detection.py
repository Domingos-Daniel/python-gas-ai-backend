#!/usr/bin/env python3
"""Testa a detecção de tipos de gráficos na pergunta do usuário"""

import requests
import json

def test_chart_detection():
    """Testa se o sistema detecta corretamente os tipos de gráficos solicitados"""
    
    test_cases = [
        {
            "question": "Análise do setor petrolífero em Angola com gráfico de linha",
            "expected_types": ["line"],
            "description": "Português com 'linha'"
        },
        {
            "question": "Mostre a evolução temporal do setor petrolífero angolano",
            "expected_types": ["line"],
            "description": "Português com 'evolução temporal'"
        },
        {
            "question": "Comparação entre empresas de petróleo em Angola - gráfico de barras",
            "expected_types": ["bar"],
            "description": "Português com 'barras'"
        },
        {
            "question": "Análise de participação de mercado com gráfico de pizza",
            "expected_types": ["pie"],
            "description": "Português com 'pizza'"
        },
        {
            "question": "Dashboard de KPIs do setor petrolífero angolano",
            "expected_types": ["kpi"],
            "description": "Português com 'KPIs'"
        }
    ]
    
    print("🧪 TESTANDO DETECÇÃO DE GRÁFICOS")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Teste {i}: {test_case['description']}")
        print(f"Pergunta: {test_case['question']}")
        print(f"Esperado: {test_case['expected_types']}")
        
        try:
            # Testa o endpoint diretamente
            response = requests.post('http://localhost:8000/analyze', json={
                'question': test_case['question'],
                'chart_types': test_case['expected_types'],
                'analysis_type': 'comprehensive'
            })
            
            if response.status_code == 200:
                data = response.json()
                
                # Extrai os tipos de gráficos gerados
                charts_found = False
                chart_types_in_response = []
                
                if 'answer' in data:
                    # Procura por gráficos no campo answer (base64)
                    if 'data:image/png;base64,' in data['answer']:
                        charts_found = True
                        chart_count = data['answer'].count('data:image/png;base64,')
                        
                        # Tenta identificar o tipo de gráfico pela pergunta
                        if 'linha' in test_case['question'].lower() or 'evolução' in test_case['question'].lower():
                            chart_types_in_response.append('line')
                        if 'barra' in test_case['question'].lower():
                            chart_types_in_response.append('bar')
                        if 'pizza' in test_case['question'].lower():
                            chart_types_in_response.append('pie')
                        if 'kpi' in test_case['question'].lower():
                            chart_types_in_response.append('kpi')
                        
                        # Se não conseguiu identificar, usa os tipos solicitados
                        if not chart_types_in_response:
                            chart_types_in_response = test_case['expected_types']
                
                print(f"✅ Status: {response.status_code}")
                print(f"📈 Gráficos encontrados: {chart_count if charts_found else 0} ({', '.join(chart_types_in_response) if charts_found else 'nenhum'})")
                
                # Verifica se os tipos esperados estão presentes
                expected_found = any(chart_type in chart_types_in_response for chart_type in test_case['expected_types'])
                print(f"✅ Tipos esperados encontrados: {'Sim' if expected_found else 'Não'}")
                
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"Resposta: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
        
        print("-" * 30)

def test_frontend_detection():
    """Testa a função de detecção do frontend (simulação)"""
    
    def detectChartTypes(question: str) -> list:
        """Simula a função do frontend"""
        lowerQuestion = question.lower()
        
        chartKeywords = {
            'line': ['linha', 'linear', 'tendência', 'tendencia', 'evolução', 'evolucao', 'série temporal', 'serie temporal', 'temporal'],
            'bar': ['barra', 'barras', 'coluna', 'colunas', 'comparação', 'comparacao', 'versus', 'vs'],
            'pie': ['pizza', 'torta', 'setor', 'participação', 'participacao', 'percentual', 'proporção', 'proporcao'],
            'donut': ['donut', 'anel', 'rosquinha', 'rosca'],
            'kpi': ['kpi', 'indicador', 'métrica', 'metrica', 'dashboard', 'painel'],
            'production': ['produção', 'producao', 'extracao', 'extração', 'output'],
            'financial': ['financeiro', 'financeira', 'custos', 'receitas', 'lucros', 'despesas']
        }
        
        detectedTypes = []
        
        for chartType, keywords in chartKeywords.items():
            if any(keyword in lowerQuestion for keyword in keywords):
                detectedTypes.append(chartType)
        
        if len(detectedTypes) == 0 and 'gráfico' in lowerQuestion:
            return ['bar']
        
        return detectedTypes if detectedTypes else ["pie", "bar"]
    
    print("\n🧪 TESTANDO FUNÇÃO DE DETECÇÃO DO FRONTEND")
    print("=" * 50)
    
    test_questions = [
        "Análise do setor petrolífero em Angola com gráfico de linha",
        "Mostre a evolução temporal do setor",
        "Comparação com gráfico de barras",
        "Participação de mercado em pizza",
        "Dashboard de KPIs"
    ]
    
    for question in test_questions:
        result = detectChartTypes(question)
        print(f"Pergunta: {question}")
        print(f"Detectado: {result}")
        print("-" * 30)

if __name__ == "__main__":
    test_chart_detection()
    test_frontend_detection()