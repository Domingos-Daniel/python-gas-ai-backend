"""
Debugar o conteúdo real da resposta do backend
"""
import requests
import json

def debug_response_content():
    """Debuga o conteúdo real da resposta."""
    
    user_question = "Análise do setor petrolífero em Angola com gráfico de linha"
    
    print(f"🧪 Debugando resposta para: {user_question}")
    
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
            answer = data.get('answer', '')
            
            print(f"\n📊 Estatísticas da resposta:")
            print(f"Tamanho total: {len(answer)} caracteres")
            print(f"Contém 'line': {'line' in answer.lower()}")
            print(f"Contém 'linha': {'linha' in answer.lower()}")
            print(f"Contém 'gráfico': {'gráfico' in answer.lower()}")
            print(f"Contém 'evolução': {'evolução' in answer.lower()}")
            
            # Procurar por padrões específicos
            import re
            
            # Procurar por menções de tipo de gráfico
            chart_mentions = re.findall(r'gráfico\s+de\s+(\w+)', answer.lower())
            print(f"Menções a 'gráfico de X': {chart_mentions}")
            
            # Procurar por padrão de imagem
            img_pattern = r'!\[([^\]]*)\]\((data:image/[^;]+;base64,[^)]+)\)'
            img_matches = re.findall(img_pattern, answer)
            print(f"Imagens markdown: {len(img_matches)}")
            
            # Procurar por base64 direto
            base64_pattern = r'data:image/(png|jpeg|jpg|gif);base64,([A-Za-z0-9+/=]+)'
            base64_matches = re.findall(base64_pattern, answer)
            print(f"Imagens base64 encontradas: {len(base64_matches)}")
            
            # Extrair parte da resposta antes da imagem
            if base64_matches:
                parts = answer.split('data:image')
                if len(parts) > 0:
                    text_before = parts[0][-500:]  # Últimos 500 chars antes da imagem
                    print(f"\n📝 Texto antes da imagem (últimos 500 chars):")
                    print(text_before)
            
            # Salvar resposta completa para análise
            with open('debug_resposta_completa.txt', 'w', encoding='utf-8') as f:
                f.write(answer)
            print(f"\n💾 Resposta completa salva em: debug_resposta_completa.txt")
            
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_response_content()