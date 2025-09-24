import requests
import json
import re
import base64

def test_backend_direct():
    """Testar o backend diretamente para verificar geração de gráficos"""
    
    # Testes com diferentes tipos de perguntas
    test_cases = [
        {
            "question": "Mostre uma análise do setor petrolífero com gráfico",
            "chart_types": ["bar"],
            "expected": "bar"
        },
        {
            "question": "Análise com gráfico de linha da produção",
            "chart_types": ["line"],
            "expected": "line"
        },
        {
            "question": "Comparativo com gráfico de pizza",
            "chart_types": ["pie"],
            "expected": "pie"
        },
        {
            "question": "Tabela de comparação entre empresas",
            "chart_types": ["table"],
            "expected": "table"
        },
        {
            "question": "Análise geral do setor energético",
            "chart_types": ["bar", "pie"],
            "expected": "any"
        }
    ]
    
    api_url = "http://localhost:8000/analyze"
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🧪 Teste {i+1}: {test_case['question']}")
        print(f"📊 Tipos esperados: {test_case['chart_types']}")
        
        payload = {
            "question": test_case["question"],
            "chart_types": test_case["chart_types"],
            "analysis_type": "comprehensive"
        }
        
        try:
            response = requests.post(api_url, json=payload)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Analisar resposta
                has_answer = bool(data.get("answer"))
                answer_length = len(data.get("answer", ""))
                
                # Procurar gráficos
                base64_pattern = r'data:image/(png|jpeg|jpg|gif);base64,([A-Za-z0-9+/=]+)'
                charts = re.findall(base64_pattern, data.get("answer", ""))
                chart_count = len(charts)
                
                # Procurar menções a tipos de gráficos
                answer_lower = data.get("answer", "").lower()
                mentions = {
                    "bar": "bar" in answer_lower or "barras" in answer_lower,
                    "pie": "pie" in answer_lower or "pizza" in answer_lower,
                    "line": "line" in answer_lower or "linha" in answer_lower,
                    "table": "tabela" in answer_lower or "table" in answer_lower
                }
                
                print(f"📄 Tem resposta: {has_answer}")
                print(f"📏 Tamanho da resposta: {answer_length} caracteres")
                print(f"📊 Número de gráficos: {chart_count}")
                print(f"🔍 Menções a gráficos: {mentions}")
                
                if chart_count > 0:
                    print(f"✅ SUCESSO: {chart_count} gráfico(s) encontrado(s)")
                    
                    # Salvar gráfico para verificação
                    chart_data = charts[0][1]  # Pegar apenas o base64
                    chart_filename = f"debug_chart_{i+1}.png"
                    
                    with open(chart_filename, "wb") as f:
                        f.write(base64.b64decode(chart_data))
                    
                    print(f"💾 Gráfico salvo como: {chart_filename}")
                    
                else:
                    print(f"❌ NENHUM GRÁFICO ENCONTRADO")
                    
                    # Mostrar preview da resposta
                    preview = data.get("answer", "")[:300]
                    print(f"📝 Preview: {preview}...")
                
            else:
                print(f"❌ Erro: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exceção: {str(e)}")
    
    print("\n🎯 Resumo dos testes concluído!")

if __name__ == "__main__":
    test_backend_direct()