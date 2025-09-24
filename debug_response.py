"""
Script para debugar a resposta completa do endpoint /analyze
"""
import requests
import json

def debug_response():
    """Debuga a resposta completa do endpoint."""
    
    print("🔍 Debugando resposta do endpoint /analyze...")
    
    # Teste com gráfico de linha
    payload = {
        'question': 'Análise do setor petrolífero em Angola com gráfico de linha',
        'chart_types': ['line'],
        'analysis_type': 'comprehensive'
    }
    
    try:
        response = requests.post('http://localhost:8000/analyze', json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Estrutura da resposta:")
            
            # Verificar campos principais
            print(f"Campos disponíveis: {list(data.keys())}")
            
            if 'answer' in data:
                print(f"\n📄 Campo 'answer' tem {len(data['answer'])} caracteres")
                print("Primeiros 500 caracteres do 'answer':")
                print(data['answer'][:500])
                print("...")
                
                # Procurar por gráficos no answer
                if 'data:image/png;base64,' in data['answer']:
                    chart_count = data['answer'].count('data:image/png;base64,')
                    print(f"✅ Encontrados {chart_count} gráficos no campo 'answer'")
                else:
                    print("❌ Nenhum gráfico encontrado no campo 'answer'")
            
            # Verificar se há outros campos
            for key, value in data.items():
                if key != 'answer':
                    if isinstance(value, list):
                        print(f"\n📋 Campo '{key}' é uma lista com {len(value)} itens")
                        for i, item in enumerate(value):
                            if isinstance(item, dict):
                                print(f"  Item {i}: {list(item.keys())}")
                    elif isinstance(value, dict):
                        print(f"\n📋 Campo '{key}' é um dict com chaves: {list(value.keys())}")
                    else:
                        print(f"\n📋 Campo '{key}' tem tipo: {type(value)}")
                        
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_response()