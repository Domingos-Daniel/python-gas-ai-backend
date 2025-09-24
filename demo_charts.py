"""
Script de demonstração simplificado para a nova funcionalidade de análise com gráficos.
"""

import requests
import json

# Configurações da API
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def demo_analyze():
    """Demonstra a funcionalidade de análise com gráficos."""
    print("🎯 Demonstração de Análise com Gráficos")
    print("=" * 50)
    
    # Exemplo de análise
    test_case = {
        "question": "Analise a distribuição de investimentos das empresas de petróleo em Angola",
        "chart_types": ["pie", "bar"],
        "analysis_type": "financial"
    }
    
    print(f"📊 Enviando análise: {test_case['question']}")
    print(f"📈 Tipos de gráficos: {', '.join(test_case['chart_types'])}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            headers=HEADERS,
            json=test_case
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('answer', '')
            
            print(f"\n✅ Análise concluída com sucesso!")
            print(f"📄 Tamanho da resposta: {len(answer)} caracteres")
            
            # Mostra a resposta formatada
            print("\n" + "="*50)
            print("📊 RESPOSTA DA ANÁLISE:")
            print("="*50)
            print(answer)
            print("="*50)
            
            # Verifica se há gráficos
            if "base64" in answer:
                print("\n✅ Gráficos foram gerados e incluídos na resposta!")
            else:
                print("\nℹ️  Resposta textual (fallback)")
                
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def demo_chart_generation():
    """Demonstra geração individual de gráficos."""
    print("\n\n🎯 Demonstração de Geração de Gráficos")
    print("=" * 50)
    
    # Dados de exemplo
    chart_data = {
        "Total Energies": 35.2,
        "Sonangol": 28.7,
        "Azule Energy": 18.9,
        "Chevron": 10.3,
        "BP": 4.8,
        "Outras": 2.1
    }
    
    payload = {
        "chart_type": "pie",
        "data": chart_data,
        "title": "Participação de Mercado - Empresas de Petróleo em Angola",
        "subtitle": "Distribuição percentual das principais empresas"
    }
    
    print(f"📊 Gerando gráfico de pizza com dados de empresas")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-chart",
            headers=HEADERS,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            chart_base64 = result.get('chart_base64', '')
            
            print(f"✅ Gráfico gerado com sucesso!")
            print(f"📊 Tipo: {result.get('chart_type', 'unknown')}")
            print(f"📏 Tamanho do base64: {len(chart_base64)} caracteres")
            print(f"📋 Resumo: {result.get('data_summary', {})}")
            
            # Salva informações sobre o gráfico
            if chart_base64:
                print("✅ Imagem base64 gerada e pode ser renderizada no frontend!")
                
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def demo_traditional_chat():
    """Demonstra que o chat tradicional ainda funciona."""
    print("\n\n🎯 Demonstração de Chat Tradicional")
    print("=" * 50)
    
    question = "Quais são as principais empresas de petróleo em Angola?"
    
    print(f"💬 Pergunta: {question}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            headers=HEADERS,
            json={"question": question}
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('answer', '')
            
            print(f"✅ Resposta recebida ({len(answer)} caracteres)")
            print(f"📝 Preview: {answer[:200]}...")
            
            # Confirma que é texto puro
            if "base64" not in answer:
                print("✅ Confirmed: Resposta tradicional sem gráficos")
            else:
                print("⚠️  Unexpected: Gráficos encontrados na resposta tradicional")
                
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def main():
    """Executa todas as demonstrações."""
    print("🚀 Demonstração do Sistema com Análise e Gráficos")
    print("Servidor: http://localhost:8000")
    
    try:
        # Testa health check primeiro
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Servidor está rodando!")
        else:
            print("⚠️  Servidor pode não estar disponível")
            
        # Executa demonstrações
        demo_analyze()
        demo_chart_generation()
        demo_traditional_chat()
        
        print("\n\n🎉 Demonstração concluída!")
        print("\n📚 Endpoints disponíveis:")
        print("   • POST /chat - Chat tradicional")
        print("   • POST /analyze - Análise com gráficos")
        print("   • POST /generate-chart - Gerar gráfico individual")
        print("   • GET  /health - Status do sistema")
        print("   • GET  /docs - Documentação Swagger")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando em http://localhost:8000")
        print("   Por favor, inicie o servidor primeiro com: python run.py")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()