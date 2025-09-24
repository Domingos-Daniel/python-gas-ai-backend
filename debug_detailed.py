#!/usr/bin/env python3
"""
Script de debug detalhado para verificar a resposta completa do endpoint /analyze
"""

import requests
import json
import base64

def debug_analyze_endpoint():
    """Testa o endpoint /analyze com debug detalhado"""
    
    url = "http://localhost:8000/analyze"
    
    # Teste com análise e gráfico de linha
    payload = {
        "question": "Análise do setor petrolífero em Angola com gráfico de linha",
        "chart_types": ["line"]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("=== Debug Detalhado do Endpoint /analyze ===")
        print(f"Enviando requisição para: {url}")
        print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\nResposta JSON completa:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Análise detalhada
                print(f"\n=== Análise Detalhada ===")
                print(f"Chaves disponíveis: {list(data.keys())}")
                
                if 'answer' in data:
                    answer = data['answer']
                    print(f"Tamanho do campo 'answer': {len(answer)} caracteres")
                    print(f"Primeiros 500 caracteres do 'answer': {answer[:500]}")
                    
                    # Verifica se há gráficos no answer
                    if 'data:image/png;base64,' in answer:
                        print("✅ Gráficos detectados no campo 'answer'")
                        # Conta quantos gráficos
                        chart_count = answer.count('data:image/png;base64,')
                        print(f"Número de gráficos: {chart_count}")
                    else:
                        print("❌ Nenhum gráfico detectado no campo 'answer'")
                else:
                    print("❌ Campo 'answer' não encontrado na resposta")
                    
                if 'status' in data:
                    print(f"Status: {data['status']}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao decodificar JSON: {e}")
                print(f"Resposta raw: {response.text[:500]}")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    debug_analyze_endpoint()