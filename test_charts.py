"""
Script de teste para demonstrar a funcionalidade de análise com gráficos.
Testa os novos endpoints de análise e geração de gráficos.
"""

import requests
import json
import base64
from datetime import datetime

# Configurações da API
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_analyze_endpoint():
    """Testa o endpoint de análise com gráficos."""
    print("🧪 Testando endpoint de análise com gráficos...")
    
    # Testes de diferentes tipos de análise
    test_cases = [
        {
            "question": "Analise a distribuição de investimentos das empresas de petróleo em Angola",
            "chart_types": ["pie", "donut", "bar"],
            "analysis_type": "financial"
        },
        {
            "question": "Mostre a comparação da produção entre os principais blocos de petróleo",
            "chart_types": ["bar", "line"],
            "analysis_type": "operational"
        },
        {
            "question": "Qual é a participação de mercado das empresas no setor de petróleo angolano?",
            "chart_types": ["pie", "donut"],
            "analysis_type": "market"
        },
        {
            "question": "Analise a estrutura organizacional da Sonangol",
            "chart_types": ["pie", "bar"],
            "analysis_type": "comprehensive"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Teste {i}: {test_case['question'][:50]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/analyze",
                headers=HEADERS,
                json=test_case
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Sucesso! Resposta recebida com {len(result.get('answer', ''))} caracteres")
                
                # Verifica se há gráficos na resposta
                if "base64" in result.get('answer', ''):
                    print("📈 Gráficos detectados na resposta!")
                else:
                    print("⚠️  Nenhum gráfico detectado - fallback para resposta normal")
                
                # Mostra preview da resposta
                preview = result.get('answer', '')[:200].replace('\n', ' ')
                print(f"📝 Preview: {preview}...")
                
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro no teste {i}: {str(e)}")

def test_generate_chart_endpoint():
    """Testa o endpoint de geração individual de gráficos."""
    print("\n🧪 Testando endpoint de geração de gráficos individuais...")
    
    # Dados de teste
    test_data = {
        "pie": {
            "Total Energies": 35.2,
            "Sonangol": 28.7,
            "Azule Energy": 18.9,
            "Chevron": 10.3,
            "BP": 4.8,
            "Outras": 2.1
        },
        "bar": {
            "2020": 125000,
            "2021": 138000,
            "2022": 142000,
            "2023": 156000,
            "2024": 163000
        },
        "line": {
            "Janeiro": 45000,
            "Fevereiro": 52000,
            "Março": 48000,
            "Abril": 61000,
            "Maio": 58000,
            "Junho": 67000
        },
        "donut": {
            "Exploração": 45.8,
            "Produção": 28.3,
            "Refino": 15.7,
            "Distribuição": 10.2
        }
    }
    
    for chart_type, data in test_data.items():
        print(f"\n📈 Testando gráfico {chart_type.upper()}...")
        
        payload = {
            "chart_type": chart_type,
            "data": data,
            "title": f"Gráfico de {chart_type.title()} - Teste",
            "subtitle": f"Dados de demonstração para {chart_type}"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/generate-chart",
                headers=HEADERS,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                chart_base64 = result.get('chart_base64', '')
                
                print(f"✅ Gráfico {chart_type} gerado com sucesso!")
                print(f"📊 Tamanho do base64: {len(chart_base64)} caracteres")
                print(f"📋 Resumo dos dados: {result.get('data_summary', {})}")
                
                # Salva imagem em arquivo para visualização
                if chart_base64:
                    try:
                        image_data = base64.b64decode(chart_base64)
                        filename = f"chart_{chart_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        
                        with open(filename, 'wb') as f:
                            f.write(image_data)
                        
                        print(f"💾 Imagem salva como: {filename}")
                    except Exception as e:
                        print(f"⚠️  Erro ao salvar imagem: {e}")
                
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro ao gerar gráfico {chart_type}: {str(e)}")

def test_traditional_chat():
    """Testa o endpoint tradicional de chat para garantir retrocompatibilidade."""
    print("\n🧪 Testando endpoint tradicional de chat...")
    
    test_questions = [
        "Quais são as principais empresas de petróleo em Angola?",
        "Me fale sobre o projeto do Bloco 17",
        "Quais serviços a Total oferece?"
    ]
    
    for question in test_questions:
        print(f"\n💬 Pergunta: {question}")
        
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
                
                # Verifica se não há gráficos (deve ser texto puro)
                if "base64" not in answer:
                    print("✅ Resposta tradicional confirmada (sem gráficos)")
                else:
                    print("⚠️  Resposta contém gráficos - inesperado para chat tradicional")
                
                # Mostra preview
                preview = answer[:150].replace('\n', ' ')
                print(f"📝 Preview: {preview}...")
                
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro no chat: {str(e)}")

def test_health_check():
    """Testa o health check da API."""
    print("\n🧪 Testando health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check: {result.get('status', 'unknown')}")
            print(f"ℹ️  Mensagem: {result.get('message', '')}")
            print(f"🔧 LLM Service: {result.get('llm_service', {}).get('status', 'unknown')}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no health check: {str(e)}")

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes do sistema com análise e gráficos")
    print(f"📍 URL base: {BASE_URL}")
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Aguarda confirmação do usuário
    input("\n⚠️  Certifique-se de que o servidor está rodando e pressione Enter para continuar...")
    
    try:
        # Executa testes
        test_health_check()
        test_traditional_chat()
        test_analyze_endpoint()
        test_generate_chart_endpoint()
        
        print(f"\n✅ Todos os testes concluídos!")
        print(f"⏰ Término: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}")

if __name__ == "__main__":
    main()