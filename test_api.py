"""
Script de teste para a API do chatbot.
Demonstra como usar os endpoints da API.
"""
import requests
import json
import time


def test_api():
    """Testa os endpoints da API."""
    base_url = "http://localhost:8000"
    
    print("=== Teste da API LLM Chatbot ===\n")
    
    # 1. Teste health check
    print("1. Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except requests.RequestException as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o servidor está rodando: uvicorn app.main:app --reload")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. Teste endpoint raiz
    print("2. Testando endpoint raiz...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except requests.RequestException as e:
        print(f"Erro: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Teste chat endpoint
    print("3. Testando Chat Endpoint...")
    
    perguntas_teste = [
        "Quais são os principais serviços da Total?",
        "O que você sabe sobre energia em Angola?",
        "Conte-me sobre a Total Energies"
    ]
    
    for i, pergunta in enumerate(perguntas_teste, 1):
        print(f"\n3.{i}. Pergunta: {pergunta}")
        
        try:
            payload = {"question": pergunta}
            response = requests.post(
                f"{base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Resposta: {data['answer'][:200]}...")
                print(f"Status: {data['status']}")
            else:
                print(f"Erro: {response.text}")
                
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
        
        # Pausa entre requisições
        time.sleep(1)
    
    print("\n" + "="*50 + "\n")
    
    # 4. Teste com pergunta vazia (deve dar erro)
    print("4. Testando pergunta vazia (deve retornar erro)...")
    try:
        payload = {"question": ""}
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
    except requests.RequestException as e:
        print(f"Erro: {e}")
    
    print("\n=== Teste concluído ===")


def interactive_chat():
    """Modo de chat interativo."""
    base_url = "http://localhost:8000"
    
    print("=== Chat Interativo ===")
    print("Digite suas perguntas (digite 'sair' para terminar)\n")
    
    while True:
        pergunta = input("Você: ").strip()
        
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            break
        
        if not pergunta:
            continue
        
        try:
            payload = {"question": pergunta}
            response = requests.post(
                f"{base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Bot: {data['answer']}\n")
            else:
                print(f"Erro {response.status_code}: {response.text}\n")
                
        except requests.RequestException as e:
            print(f"Erro na conexão: {e}\n")
    
    print("Chat finalizado!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "chat":
        interactive_chat()
    else:
        test_api()
        
        # Oferece modo interativo
        print("\nDeseja testar o chat interativo? (s/n): ", end="")
        if input().lower() in ['s', 'sim', 'y', 'yes']:
            print()
            interactive_chat()
