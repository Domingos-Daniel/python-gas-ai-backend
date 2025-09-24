"""
Teste de integração com o frontend - simulando a requisição real
"""
import requests
import json

def detect_chart_types(question):
    """Simula a função do frontend que detecta tipos de gráficos."""
    lower_question = question.lower()
    detected_types = []
    
    # Mapeamento de palavras-chave para tipos de gráficos
    chart_keywords = {
        'line': ['linha', 'evolução', 'temporal', 'série temporal', 'tendência', 'progressão'],
        'bar': ['barra', 'comparação', 'comparar', 'versus', 'ranking', 'histograma'],
        'pie': ['pizza', 'participação', 'percentual', 'proporção', 'distribuição', 'quota'],
        'donut': ['donut', 'rosquinha', 'anel'],
        'kpi': ['kpi', 'indicador', 'métrica', 'dashboard', 'painel', 'desempenho'],
        'production': ['produção', 'produzir', 'extrair', 'barris', 'óleo', 'gás'],
        'financial': ['financeiro', 'financeira', 'dinheiro', 'investimento', 'receita', 'lucro', 'custo']
    }
    
    # Verificar cada tipo de gráfico
    for chart_type, keywords in chart_keywords.items():
        if any(keyword in lower_question for keyword in keywords):
            detected_types.append(chart_type)
    
    # Se nenhum tipo foi detectado, usar padrões
    if not detected_types:
        if 'gráfico' in lower_question or 'gráfica' in lower_question:
            detected_types = ['pie', 'bar']  # Padrão
        else:
            detected_types = ['pie', 'bar']  # Padrão absoluto
    
    return detected_types

def test_frontend_request():
    """Testa uma requisição simulando o frontend com detecção de gráficos."""
    
    # Pergunta do usuário
    user_question = "Análise do setor petrolífero em Angola com gráfico de linha"
    
    print(f"🧪 Simulando requisição do frontend...")
    print(f"Pergunta do usuário: {user_question}")
    
    # Detectar tipos de gráficos (como o frontend faz)
    detected_chart_types = detect_chart_types(user_question)
    print(f"Tipos de gráficos detectados: {detected_chart_types}")
    
    # Preparar payload como o frontend faria
    payload = {
        'question': user_question,
        'chart_types': detected_chart_types,
        'analysis_type': 'comprehensive'
    }
    
    print(f"Payload enviado: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    # Enviar requisição
    try:
        response = requests.post('http://localhost:8000/analyze', json=payload)
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"Resposta tem {len(data.get('answer', ''))} caracteres")
            
            # Verificar se há gráficos
            chart_count = data.get('answer', '').count('data:image/png;base64,')
            print(f"Número de gráficos gerados: {chart_count}")
            
            # Verificar tipos de gráficos detectados na resposta
            answer_lower = data.get('answer', '').lower()
            detected_in_response = []
            
            if 'linha' in answer_lower or 'evolução' in answer_lower:
                detected_in_response.append('line')
            if 'barra' in answer_lower:
                detected_in_response.append('bar')
            if 'pizza' in answer_lower:
                detected_in_response.append('pie')
            if 'kpi' in answer_lower or 'indicador' in answer_lower:
                detected_in_response.append('kpi')
            
            print(f"Tipos detectados na resposta: {detected_in_response}")
            
            # Mostrar parte da análise
            if len(data.get('answer', '')) > 1000:
                print(f"\n📊 Preview da análise:")
                print(data['answer'][:1000] + "...")
            else:
                print(f"\n📊 Análise completa:")
                print(data.get('answer', ''))
                
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_frontend_request()