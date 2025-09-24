#!/usr/bin/env python3
"""
Teste para verificar a geração de gráficos com cores apropriadas.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.chart_generator import chart_generator
import base64

def test_chart_colors():
    """Testa a geração de gráficos com diferentes tipos de dados."""
    
    # Dados de exemplo
    sample_data = {
        'Desenvolvimento de Campos': 1200000000,
        'Exploração': 850000000,
        'Produção': 750000000,
        'Refino': 210000000,
        'Distribuição': 100000000,
        'Outros': 95000000
    }
    
    print("🎨 Testando geração de gráficos com cores...")
    
    # Testar gráfico de pizza
    print("📊 Gerando gráfico de pizza...")
    pie_chart = chart_generator.create_pie_chart(
        sample_data, 
        "📊 Distribuição de Investimentos",
        "Análise do setor de petróleo em Angola"
    )
    
    # Salvar imagem para verificação
    if pie_chart:
        with open("test_pie_chart.png", "wb") as f:
            f.write(base64.b64decode(pie_chart))
        print("✅ Gráfico de pizza salvo como 'test_pie_chart.png'")
    else:
        print("❌ Erro ao gerar gráfico de pizza")
    
    # Testar gráfico de barras
    print("📈 Gerando gráfico de barras...")
    bar_chart = chart_generator.create_bar_chart(
        sample_data,
        "📈 Investimentos por Categoria",
        "Valores em milhões de USD"
    )
    
    if bar_chart:
        with open("test_bar_chart.png", "wb") as f:
            f.write(base64.b64decode(bar_chart))
        print("✅ Gráfico de barras salvo como 'test_bar_chart.png'")
    else:
        print("❌ Erro ao gerar gráfico de barras")
    
    # Testar cores da paleta
    print("🎨 Paleta de cores atual:")
    for i, color in enumerate(chart_generator.color_palette):
        print(f"  Cor {i+1}: {color}")
    
    # Testar configurações
    print("⚙️  Configurações atuais:")
    for key, value in chart_generator.chart_configs.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_chart_colors()