import requests

# Testar pergunta genérica sobre o setor
payload = {
    'question': 'quais são as principais empresas de petróleo em angola?',
    'history': []
}

try:
    response = requests.post('http://localhost:8000/chat', json=payload)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        result = response.json()
        print('\n=== RESPOSTA ===')
        print(result.get('answer', 'No answer'))
        # print(result.get('answer', 'No answer')[:500] + '...')
        # print('\n=== FONTES CONSULTADAS ===')
        # for source in result.get('sources', []):
        #     print(f'• {source}')
        # print(f'\nTotal de fontes: {len(result.get("sources", []))}')
    else:
        print(f'Erro: {response.text}')
except Exception as e:
    print(f'Erro: {e}')