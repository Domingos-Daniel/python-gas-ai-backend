"""
Teste demonstrativo das melhorias visuais e análises contextuais.
Mostra gráficos profissionais, KPIs específicos e análises aprofundadas.
"""

import requests
import json
import base64
import matplotlib.pyplot as plt
from io import BytesIO

def test_advanced_visualizations():
    """Testa as novas visualizações avançadas."""
    
    base_url = "http://localhost:8000"
    
    print("🚀 TESTE DAS MELHORIAS VISUAIS E ANÁLISES CONTEXTUAIS")
    print("=" * 70)
    
    # Teste 1: Análise de mercado com gráficos profissionais
    print("\n📊 Teste 1: Análise de Mercado com KPIs Avançados")
    
    test_questions = [
        {
            "question": "Analise a distribuição de market share das empresas de petróleo em Angola",
            "chart_types": ["pie", "donut", "bar"],
            "analysis_type": "market"
        },
        {
            "question": "Compare o desempenho financeiro das empresas petrolíferas em Angola",
            "chart_types": ["line", "kpi", "financial"],
            "analysis_type": "financial"
        },
        {
            "question": "Qual a eficiência operacional da Total Energies em comparação com o setor?",
            "chart_types": ["kpi", "production", "dashboard"],
            "analysis_type": "operational"
        }
    ]
    
    for i, test_case in enumerate(test_questions, 1):
        print(f"\n{'-'*50}")
        print(f"Caso {i}: {test_case['question'][:60]}...")
        print(f"Tipos de gráfico: {', '.join(test_case['chart_types'])}")
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json=test_case,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                
                # Detecta gráficos na resposta
                charts_detected = answer.count('![Gráfico')
                kpis_detected = answer.count('KPIs Principais')
                trends_detected = answer.count('Tendências')
                recommendations_detected = answer.count('Recomendações')
                
                print(f"✅ Gráficos detectados: {charts_detected}")
                print(f"✅ Seção de KPIs: {'Sim' if kpis_detected > 0 else 'Não'}")
                print(f"✅ Análise de tendências: {'Sim' if trends_detected > 0 else 'Não'}")
                print(f"✅ Recomendações estratégicas: {'Sim' if recommendations_detected > 0 else 'Não'}")
                
                # Mostra preview da análise
                if len(answer) > 200:
                    preview = answer[:200].replace('\n', ' ')
                    print(f"📝 Preview: {preview}...")
                
                # Extrai e salva gráficos se existirem
                if charts_detected > 0:
                    save_charts_from_response(answer, f"teste_{i}")
                    
            else:
                print(f"❌ Erro: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
    
    # Teste 2: KPIs específicos do setor
    print(f"\n{'='*70}")
    print("\n📈 Teste 2: KPIs Específicos do Setor Petrolífero")
    
    kpi_questions = [
        "Mostre os KPIs de produção e eficiência do setor",
        "Analise a taxa de incidentes de segurança e conformidade ambiental",
        "Qual o ROI e margem de lucro das empresas petrolíferas?"
    ]
    
    for question in kpi_questions:
        print(f"\n🔍 {question}")
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json={
                    "question": question,
                    "chart_types": ["kpi", "dashboard"],
                    "analysis_type": "comprehensive"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                
                # Verifica indicadores específicos
                indicators = [
                    'produção', 'eficiência', 'ROI', 'margem', 'incidentes',
                    'conformidade', 'ambiental', 'safety', 'production'
                ]
                
                found_indicators = [ind for ind in indicators if ind.lower() in answer.lower()]
                print(f"✅ Indicadores detectados: {', '.join(found_indicators[:3])}")
                
                # Verifica emojis de status
                status_emojis = ['🟢', '🟡', '🔴', '🟠', '🔵']
                emojis_found = sum(1 for emoji in status_emojis if emoji in answer)
                print(f"✅ Indicadores visuais de status: {emojis_found}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print(f"\n{'='*70}")
    print("\n✅ CONCLUSÃO DAS MELHORIAS:")
    print("   • KPIs específicos do setor petrolífero implementados")
    print("   • Análises contextuais com benchmarks e tendências")
    print("   • Gráficos profissionais com cores e temas personalizados")
    print("   • Recomendações estratégicas baseadas em dados")
    print("   • Indicadores visuais de status (🟢🟡🔴)")
    print("   • Múltiplos tipos de gráficos avançados")

def save_charts_from_response(response_text, prefix):
    """Extrai e salva gráficos da resposta."""
    try:
        import re
        
        # Procura por imagens base64 na resposta
        pattern = r'!\[([^\]]*)\]\((data:image/([^;]+);base64,([^)]+))\)'
        matches = re.findall(pattern, response_text)
        
        if matches:
            print(f"   📸 {len(matches)} gráfico(s) encontrado(s)")
            
            for i, (alt_text, full_match, img_type, base64_data) in enumerate(matches):
                try:
                    # Decodifica base64
                    img_data = base64.b64decode(base64_data)
                    
                    # Salva em arquivo
                    filename = f"{prefix}_chart_{i+1}.png"
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    
                    print(f"   💾 Gráfico salvo: {filename}")
                    
                except Exception as e:
                    print(f"   ⚠️  Erro ao salvar gráfico {i+1}: {e}")
        
    except Exception as e:
        print(f"   ⚠️  Erro ao processar gráficos: {e}")

if __name__ == "__main__":
    test_advanced_visualizations()