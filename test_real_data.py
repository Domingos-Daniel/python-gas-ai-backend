#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema está conseguindo extrair dados reais
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.data_analyzer import DataAnalyzer

def test_real_data_extraction():
    """Testa a extração de dados reais dos arquivos"""
    
    analyzer = DataAnalyzer()
    
    print("🔍 Testando extração de dados reais dos arquivos...\n")
    
    # Testa extração de um arquivo específico
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    if os.path.exists(data_dir):
        print(f"📁 Diretório de dados encontrado: {data_dir}")
        
        # Lista arquivos disponíveis
        files = [f for f in os.listdir(data_dir) if f.endswith('.txt') and not f.startswith('all_urls')]
        print(f"📄 Arquivos encontrados: {files}")
        
        # Testa extrair dados de um arquivo
        if files:
            test_file = os.path.join(data_dir, files[0])
            print(f"\n📖 Analisando arquivo: {files[0]}")
            
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"📊 Tamanho do conteúdo: {len(content)} caracteres")
                print(f"📝 Primeiras 500 caracteres:")
                print(content[:500])
                print("\n" + "="*60 + "\n")
                
                # Testa extração de dados
                extracted_data = analyzer.extract_numerical_data(content)
                print(f"📈 Dados extraídos: {len(extracted_data)} itens")
                
                if extracted_data:
                    print("✅ Dados encontrados:")
                    for key, value in extracted_data.items():
                        print(f"  • {key}: {value}")
                else:
                    print("⚠️ Nenhum dado numérico encontrado")
                
            except Exception as e:
                print(f"❌ Erro ao processar arquivo: {e}")
    
    # Testa o método de buscar dados reais do contexto
    print(f"\n{'='*60}\n")
    print("🔍 Testando método _get_real_data_from_context...")
    
    real_data = analyzer._get_real_data_from_context(
        "Análise do setor petrolífero em Angola", 
        "distribution"
    )
    
    if real_data:
        print(f"✅ Dados reais encontrados: {len(real_data)} itens")
        for key, value in real_data.items():
            print(f"  • {key}: {value}")
    else:
        print("⚠️ Nenhum dado real encontrado, usará dados mockados")

if __name__ == "__main__":
    test_real_data_extraction()