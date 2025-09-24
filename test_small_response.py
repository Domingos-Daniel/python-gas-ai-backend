import requests
import json

def test_small_response():
    """Testar se o problema é tamanho da resposta"""
    
    api_url = "http://localhost:8000/analyze"
    
    # Testar com uma pergunta simples que deve gerar resposta pequena
    payload = {
        "question": "Qual é a produção da Sonangol?",
        "chart_types": ["bar"],
        "analysis_type": "simple"
    }
    
    try:
        response = requests.post(api_url, json=payload)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"📄 Tamanho da resposta: {len(data.get('answer', ''))} caracteres")
            print(f"📝 Preview: {data.get('answer', '')[:200]}...")
            
            # Verificar se tem gráfico
            has_chart = "data:image" in data.get("answer", "")
            print(f"📊 Tem gráfico: {has_chart}")
            
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")

if __name__ == "__main__":
    test_small_response()