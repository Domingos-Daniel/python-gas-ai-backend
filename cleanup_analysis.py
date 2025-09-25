#!/usr/bin/env python3
"""
Script para analisar e identificar arquivos desnecessários no projeto.
"""

import os
import re
from pathlib import Path

def find_unused_files():
    """Identifica arquivos que podem ser desnecessários."""
    
    backend_dir = Path("c:/Projectos/conferencia/backend")
    app_dir = backend_dir / "app"
    
    # Arquivos suspeitos de serem desnecessários
    suspicious_files = [
        "scraped_data_manager_backup.py",
        "advanced_chart_generator_fixed.py", 
        "advanced_data_analyzer_fixed.py",
        "simple_llm.py",
        "angola_energy_scraper.py",  # Versão antiga do scraper
        "chart_generator.py",  # Pode ser substituído pelo avançado
        "data_analyzer.py",  # Pode ser substituído pelo avançado
    ]
    
    # Arquivos de teste/backup na raiz
    root_suspicious = [
        "backend_response.txt",
        "requirements-new.txt",
        "scraper_energia.py",
        "scraper_simples.py",
        "simple_start.py",
        "start_production.py",
        "build_index_simples.py",
        "fix_file.py",
        "install_essential.py",
        "setup.py",
        "server.py",
        "run.py",  # Duplicado do main.py?
    ]
    
    print("🔍 ANÁLISE DE ARQUIVOS DESNECESSÁRIOS")
    print("=" * 50)
    
    # Verificar arquivos suspeitos no app/
    print("\n📁 Arquivos suspeitos em app/:")
    for filename in suspicious_files:
        filepath = app_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  ⚠️  {filename} ({size} bytes)")
            
            # Verificar se é importado em algum lugar
            imported = False
            for py_file in app_dir.glob("*.py"):
                if py_file.name == filename:
                    continue
                try:
                    content = py_file.read_text(encoding='utf-8')
                    if filename.replace('.py', '') in content:
                        imported = True
                        print(f"     📋 Importado em: {py_file.name}")
                        break
                except:
                    pass
            
            if not imported:
                print(f"     ❌ Não parece ser importado")
    
    # Verificar arquivos suspeitos na raiz
    print("\n📁 Arquivos suspeitos na raiz:")
    for filename in root_suspicious:
        filepath = backend_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  ⚠️  {filename} ({size} bytes)")
    
    # Verificar arquivos de dados antigos
    print("\n📁 Arquivos de dados antigos:")
    data_dir = backend_dir / "data"
    txt_files = list(data_dir.glob("*.txt"))
    scraped_files = list((data_dir / "scraped").glob("*.json"))
    
    print(f"  📄 Arquivos .txt em data/: {len(txt_files)}")
    for f in txt_files[:5]:  # Mostrar primeiros 5
        print(f"     - {f.name}")
    if len(txt_files) > 5:
        print(f"     ... e mais {len(txt_files) - 5} arquivos")
    
    print(f"  📊 Arquivos scraped em data/scraped/: {len(scraped_files)}")
    for f in scraped_files[:5]:  # Mostrar primeiros 5
        print(f"     - {f.name}")
    if len(scraped_files) > 5:
        print(f"     ... e mais {len(scraped_files) - 5} arquivos")
    
    # Verificar arquivos duplicados
    print("\n📁 Possíveis duplicações:")
    pairs = [
        ("chart_generator.py", "advanced_chart_generator_fixed.py"),
        ("data_analyzer.py", "advanced_data_analyzer_fixed.py"),
        ("main.py", "run.py"),
        ("angola_energy_scraper.py", "firecrawl_scraper.py"),
    ]
    
    for original, duplicate in pairs:
        orig_path = app_dir / original
        dup_path = app_dir / duplicate
        
        if orig_path.exists() and dup_path.exists():
            print(f"  ⚠️  Possível duplicação: {original} ↔ {duplicate}")
    
    print("\n" + "=" * 50)
    print("✅ Análise concluída!")
    print("\n💡 Recomendações:")
    print("   1. Remover arquivos de backup (_backup, _fixed)")
    print("   2. Consolidar versões duplicadas")
    print("   3. Limpar arquivos de dados antigos")
    print("   4. Manter apenas scrapers ativos (firecrawl_scraper.py)")

if __name__ == "__main__":
    find_unused_files()