"""
Teste para verificar o tipo específico de gráfico gerado
"""
import requests
import base64
import re

def test_specific_chart_type():
    """Testa e verifica o tipo específico de gráfico gerado."""
    
    # Teste específico para gráfico de linha
    user_question = "Análise do setor petrolífero em Angola com gráfico de linha"
    
    print(f"🧪 Testando geração de gráfico de linha...")
    print(f"Pergunta: {user_question}")
    
    payload = {
        'question': user_question,
        'chart_types': ['line'],
        'analysis_type': 'comprehensive'
    }
    
    try:
        response = requests.post('http://localhost:8000/analyze', json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extrair o conteúdo da resposta
            answer = data.get('answer', '')
            
            # Procurar por padrões que indicam o tipo de gráfico
            patterns = {
                'line': ['gráfico de linha', 'evolução temporal', 'série temporal', 'tendência', 'linha'],
                'bar': ['gráfico de barras', 'comparação', 'barras', 'bar'],
                'pie': ['gráfico de pizza', 'participação', 'pizza', 'pie'],
                'kpi': ['kpi', 'indicador', 'dashboard', 'painel']
            }
            
            detected_type = None
            for chart_type, keywords in patterns.items():
                if any(keyword in answer.lower() for keyword in keywords):
                    detected_type = chart_type
                    break
            
            # Contar gráficos base64
            base64_count = answer.count('data:image/png;base64,')
            
            print(f"\n📊 Resultados:")
            print(f"Tamanho da resposta: {len(answer)} caracteres")
            print(f"Número de gráficos base64: {base64_count}")
            print(f"Tipo de gráfico detectado: {detected_type}")
            
            # Extrair e salvar o gráfico se existir
            if base64_count > 0:
                # Encontrar o primeiro gráfico base64
                base64_pattern = r'data:image/png;base64,([A-Za-z0-9+/=]+)'
                matches = re.findall(base64_pattern, answer)
                
                if matches:
                    print(f"Encontrados {len(matches)} gráficos base64")
                    
                    # Salvar o primeiro gráfico
                    try:
                        image_data = base64.b64decode(matches[0])
                        filename = f"teste_verificado_{detected_type or 'unknown'}.png"
                        
                        with open(filename, 'wb') as f:
                            f.write(image_data)
                        
                        print(f"✅ Gráfico salvo como: {filename}")
                        
                        # Analisar o conteúdo da análise
                        print(f"\n📄 Preview da análise:")
                        # Pegar texto antes do primeiro gráfico
                        text_before_chart = answer.split('data:image/png;base64,')[0]
                        # Pegar últimas linhas significativas
                        lines = text_before_chart.strip().split('\n')
                        if len(lines) > 10:
                            print('\n'.join(lines[-10:]))
                        else:
                            print(text_before_chart[-500:])
                            
                    except Exception as e:
                        print(f"❌ Erro ao salvar gráfico: {e}")
            
            # Verificar se é uma análise contextual ou genérica
            if any(word in answer.lower() for word in ['dados reais', 'fontes oficiais', 'análise baseada']):
                print("✅ Análise usa dados reais")
            else:
                print("⚠️  Análise pode ser genérica")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_specific_chart_type()