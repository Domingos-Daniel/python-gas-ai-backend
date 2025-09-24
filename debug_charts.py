#!/usr/bin/env python3
"""Debug dos gráficos"""

import requests
import json

def debug_charts():
    """Debug da geração de gráficos"""
    
    # Testa com dados simples
    print("=== Debug Gráficos ===")
    try:
        response = requests.post('http://localhost:8000/analyze', json={
            'question': 'Análise do setor petrolífero em Angola com gráfico de linha',
            'chart_types': ['line']
        })
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Chaves disponíveis: {list(data.keys())}")
            print(f"Número de gráficos: {len(data.get('charts', []))}")
            
            if data.get('charts'):
                for i, chart in enumerate(data['charts']):
                    print(f"Gráfico {i+1}: tipo={chart.get('type')}, data_keys={list(chart.get('data', {}).keys())}")
            else:
                print("Nenhum gráfico gerado!")
                
            # Verifica análise
            analysis = data.get('analysis', '')
            print(f"\nAnálise (primeiros 300 chars): {analysis[:300]}...")
            
            # Verifica se há erro
            if data.get('error'):
                print(f"Erro detectado: {data.get('error')}")
        else:
            print(f"Erro completo: {response.text[:500]}")
            
    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    debug_charts()