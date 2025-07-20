"""
Script para testar a configuração do Gemini com o novo modelo.
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent))

try:
    import google.generativeai as genai
    from app.config import config
    
    print("=== Teste de Configuração do Gemini ===")
    print(f"Modelo configurado: {config.GEMINI_MODEL}")
    print(f"API Key (primeiros 10 chars): {config.GEMINI_API_KEY[:10]}...")
    
    # Configura o cliente
    genai.configure(api_key=config.GEMINI_API_KEY)
    
    # Lista modelos disponíveis
    print("\nModelos disponíveis:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
    
    # Testa o modelo configurado
    print(f"\nTestando modelo: {config.GEMINI_MODEL}")
    model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    # Teste simples
    response = model.generate_content(
        "Diga 'olá' em uma frase curta",
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=50
        )
    )
    
    print(f"Resposta de teste: {response.text}")
    print("✅ Configuração funcionando corretamente!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Execute: pip install google-generativeai")
    
except Exception as e:
    print(f"❌ Erro na configuração: {e}")
    print("\nVerifique:")
    print("1. Se a GEMINI_API_KEY está correta no arquivo .env")
    print("2. Se você tem quota disponível na API")
    print("3. Se o modelo está disponível para sua conta")
