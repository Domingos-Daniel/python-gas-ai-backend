#!/usr/bin/env python3
"""Testa os diferentes tipos de gráficos disponíveis"""

import requests
import json

def test_chart_types():
    """Testa diferentes tipos de gráficos"""
    
    # Testa com gráfico de linha
    print("=== Testando Gráfico de Linha ===")
    try:
        response = requests.post('http://localhost:8000/analyze', json={
            'question': 'Análise do setor petrolífero em Angola com gráfico de linha',
            'chart_types': ['line']
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Tipos de gráficos gerados: {[chart['type'] for chart in data.get('charts', [])]}")
            print(f"Primeiros 200 chars da análise: {data.get('analysis', '')[:200]}...")
        else:
            print(f"Erro: {response.text[:200]}")
            
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    
    # Testa com múltiplos tipos de gráficos
    print("\n=== Testando Múltiplos Gráficos ===")
    try:
        response = requests.post('http://localhost:8000/analyze', json={
            'question': 'Análise do setor petrolífero em Angola com diferentes visualizações',
            'chart_types': ['line', 'bar', 'pie']
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Tipos de gráficos gerados: {[chart['type'] for chart in data.get('charts', [])]}")
            print(f"Número de gráficos: {len(data.get('charts', []))}")
        else:
            print(f"Erro: {response.text[:200]}")
            
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    test_chart_types()