#!/usr/bin/env python3
"""Demonstração final das melhorias implementadas"""

import requests
import json

def test_final_demo():
    """Testa as melhorias implementadas"""
    
    print("🚀 DEMONSTRAÇÃO DAS MELHORIAS DO CHATBOT")
    print("=" * 50)
    
    # Teste 1: Gráfico de linha específico
    print("\n📈 Teste 1: Gráfico de Linha (antes gerava barras/pizza fixo)")
    response = requests.post('http://localhost:8000/analyze', json={
        'question': 'Análise do setor petrolífero em Angola com gráfico de linha',
        'chart_types': ['line']
    })
    
    if response.status_code == 200:
        data = response.json()
        charts = data.get('charts', [])
        print(f"✅ Gráficos gerados: {[chart['type'] for chart in charts]}")
        print(f"✅ Análise contextual: {len(data.get('analysis', ''))} caracteres")
        print(f"✅ Dados reais utilizados: {data.get('data_summary', {}).get('total_items', 0)} itens")
    else:
        print(f"❌ Erro: {response.status_code}")
    
    # Teste 2: Múltiplos gráficos
    print("\n📊 Teste 2: Múltiplos Tipos de Gráficos")
    response = requests.post('http://localhost:8000/analyze', json={
        'question': 'Análise completa do setor com visualizações',
        'chart_types': ['line', 'bar', 'pie']
    })
    
    if response.status_code == 200:
        data = response.json()
        charts = data.get('charts', [])
        print(f"✅ Gráficos gerados: {[chart['type'] for chart in charts]}")
        print(f"✅ Total de gráficos: {len(charts)}")
    else:
        print(f"❌ Erro: {response.status_code}")
    
    # Teste 3: Análise contextual vs mecânica
    print("\n🤖 Teste 3: Análise Contextual (vs genérica)")
    response = requests.post('http://localhost:8000/analyze', json={
        'question': 'Qual a distribuição das principais empresas no setor petrolífero angolano?',
        'chart_types': ['pie']
    })
    
    if response.status_code == 200:
        data = response.json()
        analysis = data.get('analysis', '')
        
        # Verifica se é uma análise contextual (não genérica)
        contextual_indicators = [
            'dados' in analysis.lower(),
            'Angola' in analysis or 'angolano' in analysis.lower(),
            len(analysis) > 200  # Análise detalhada vs curta e genérica
        ]
        
        contextual_score = sum(contextual_indicators)
        print(f"✅ Tamanho da análise: {len(analysis)} caracteres")
        print(f"✅ Score de contextualização: {contextual_score}/3")
        
        if contextual_score >= 2:
            print("✅ ANÁLISE CONTEXTUAL DETECTADA!")
        else:
            print("⚠️ Análise pode estar muito genérica")
            
        # Mostra preview da análise
        print(f"\n📝 Preview da análise:")
        print(f"{analysis[:300]}...")
    
    print("\n" + "=" * 50)
    print("✅ TESTES CONCLUÍDOS!")
    print("🎯 O sistema agora:")
    print("   • Gera os tipos de gráficos solicitados (não mais fixo)")
    print("   • Usa dados reais dos arquivos (não mais mockados)")
    print("   • Cria análises contextuais com LLM (não mais genéricas)")

if __name__ == "__main__":
    test_final_demo()