"""
Test script for document upload functionality.
Tests various document types and processing capabilities.
"""
import os
import sys
import requests
import json
from pathlib import Path

def test_document_upload():
    """Test document upload functionality with sample files."""
    
    # API endpoint
    base_url = "http://localhost:8002"
    upload_endpoint = f"{base_url}/upload-document"
    
    print("🧪 Testing Document Upload Functionality")
    print("=" * 50)
    
    # Test different file types
    test_files = [
        {
            "name": "sample_excel.xlsx",
            "content": "Sample Excel data for oil sector analysis",
            "type": "excel"
        },
        {
            "name": "sample_pdf.pdf", 
            "content": "Sample PDF document about Angolan oil industry",
            "type": "pdf"
        },
        {
            "name": "sample_text.txt",
            "content": "Sample text file with oil sector information",
            "type": "txt"
        },
        {
            "name": "sample_word.docx",
            "content": "Sample Word document about petroleum operations",
            "type": "word"
        }
    ]
    
    # Create test files
    test_dir = Path("test_documents")
    test_dir.mkdir(exist_ok=True)
    
    for test_file in test_files:
        file_path = test_dir / test_file["name"]
        
        if test_file["type"] == "excel":
            # Create a simple Excel file
            try:
                import pandas as pd
                data = {
                    'Company': ['Total', 'Sonangol', 'Chevron', 'ExxonMobil'],
                    'Production_2023': [150000, 200000, 120000, 180000],
                    'Investment_2023': [500, 700, 400, 600],
                    'Country': ['Angola', 'Angola', 'Angola', 'Angola']
                }
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, sheet_name='Oil_Data')
                print(f"✅ Created Excel test file: {test_file['name']}")
            except ImportError:
                print(f"⚠️  Skipping Excel test - pandas not available")
                continue
                
        elif test_file["type"] == "pdf":
            # Create a simple text file for PDF (we'll treat it as PDF for testing)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"""Relatório do Setor Petrolífero Angolano

Este é um documento de teste sobre o setor petrolífero em Angola.

Principais Empresas:
- TotalEnergies: Operações em blocos offshore
- Sonangol: Empresa nacional de petróleos
- Chevron: Investimentos em exploração
- ExxonMobil: Produção e desenvolvimento

Dados de Produção:
- Produção média diária: 1.2 milhões de barris
- Reservas provadas: 8.2 bilhões de barris
- Investimentos anuais: $8.5 bilhões

Este documento serve como contexto para testes do sistema.
""")
            print(f"✅ Created PDF test file: {test_file['name']}")
            
        elif test_file["type"] == "txt":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"""Informações sobre o Setor de Petróleo e Gás em Angola

Angola é um dos maiores produtores de petróleo da África subsaariana.
As principais empresas operadoras incluem TotalEnergies, Sonangol, Chevron e ExxonMobil.

Produção:
- Angola produz aproximadamente 1.2 milhões de barris por dia
- Os principais campos estão localizados no offshore
- A indústria representa cerca de 90% das exportações do país

Investimentos:
- Investimentos anuais na indústria petrolífera angolana ultrapassam $8 bilhões
- Novos projetos estão em desenvolvimento nos blocos 14, 15 e 17
- O governo está promovendo projetos de gás natural

Este arquivo de texto serve como contexto para o chatbot.
""")
            print(f"✅ Created TXT test file: {test_file['name']}")
            
        elif test_file["type"] == "word":
            # Create a simple text file for Word (we'll treat it as Word for testing)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"""Documento Word - Análise do Setor Petrolífero Angolano

INTRODUÇÃO
Este documento apresenta uma análise detalhada do setor petrolífero em Angola.

EMPRESAS OPERADORAS
As principais empresas operando em Angola incluem:
1. TotalEnergies - Blocos 14, 17
2. Sonangol - Operações nacionais  
3. Chevron - Blocos 0, 2
4. ExxonMobil - Bloco 15

DADOS ECONÔMICOS
- Produção diária: 1.2MM bpd
- Reservas: 8.2 bilhões barris
- Investimentos: $8.5B anuais

CONCLUSÃO
O setor continua sendo o motor da economia angolana.

Tabela de Produção:
Ano | Produção (bpd)
2020 | 1,180,000
2021 | 1,150,000  
2022 | 1,200,000
2023 | 1,220,000
""")
            print(f"✅ Created Word test file: {test_file['name']}")
    
    # Test each file type
    print(f"\n📤 Testing document uploads...")
    print("-" * 30)
    
    for test_file in test_files:
        file_path = test_dir / test_file["name"]
        
        if not file_path.exists():
            print(f"⚠️  Skipping {test_file['name']} - file not created")
            continue
            
        try:
            print(f"\n📄 Testing {test_file['name']} ({test_file['type']})...")
            
            # Prepare file for upload
            with open(file_path, 'rb') as f:
                files = {'file': (test_file['name'], f, 'application/octet-stream')}
                
                # Make upload request
                response = requests.post(upload_endpoint, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Upload successful!")
                    print(f"   File: {result['filename']}")
                    print(f"   Type: {result['file_type']}")
                    print(f"   Status: {result['status']}")
                    print(f"   Content preview: {result['text_content'][:100]}...")
                    print(f"   Metadata: {json.dumps(result['metadata'], indent=2)}")
                else:
                    print(f"❌ Upload failed!")
                    print(f"   Status: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error - Backend server not running")
            print(f"   Please start the backend server first: python server.py")
            break
        except Exception as e:
            print(f"❌ Error testing {test_file['name']}: {str(e)}")
    
    # Test chat with document context
    print(f"\n💬 Testing chat with document context...")
    print("-" * 35)
    
    try:
        # First upload a document
        txt_file = test_dir / "sample_text.txt"
        if txt_file.exists():
            print(f"📤 Uploading text document for context test...")
            
            with open(txt_file, 'rb') as f:
                files = {'file': ('oil_context.txt', f, 'text/plain')}
                upload_response = requests.post(upload_endpoint, files=files, timeout=30)
                
                if upload_response.status_code == 200:
                    upload_data = upload_response.json()
                    document_context = upload_data['text_content']
                    
                    print(f"✅ Document uploaded successfully")
                    print(f"📝 Testing chat with document context...")
                    
                    # Test chat with document context
                    chat_endpoint = f"{base_url}/chat"
                    chat_payload = {
                        "question": "Quais são as principais empresas operando em Angola?",
                        "history": [],
                        "document_context": document_context
                    }
                    
                    chat_response = requests.post(chat_endpoint, json=chat_payload, timeout=30)
                    
                    if chat_response.status_code == 200:
                        chat_data = chat_response.json()
                        print(f"✅ Chat with context successful!")
                        print(f"🤖 Response: {chat_data['answer']}")
                    else:
                        print(f"❌ Chat with context failed!")
                        print(f"   Status: {chat_response.status_code}")
                        print(f"   Error: {chat_response.text}")
                else:
                    print(f"❌ Document upload failed for context test")
                    
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error - Backend server not running")
    except Exception as e:
        print(f"❌ Error testing chat with context: {str(e)}")
    
    print(f"\n🎉 Document upload tests completed!")
    print("=" * 50)
    
    # Cleanup
    try:
        import shutil
        shutil.rmtree(test_dir)
        print(f"🧹 Cleaned up test files")
    except:
        pass

if __name__ == "__main__":
    test_document_upload()