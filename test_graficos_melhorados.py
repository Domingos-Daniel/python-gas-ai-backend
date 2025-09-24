"""
Teste dos gráficos melhorados para verificar correções visuais.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.advanced_chart_generator_fixed import advanced_chart_generator_fixed
from datetime import datetime, timedelta
import json

def test_graficos_melhorados():
    """Testa os gráficos melhorados com dados de exemplo."""
    print("🎨 Iniciando teste dos gráficos melhorados...")
    
    # Criar gerador melhorado
    generator = advanced_chart_generator_fixed
    
    # Dados de exemplo mais realistas
    dates = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
    
    # Testar gráfico de linhas avançado
    print("\n📈 Testando gráfico de linhas avançado...")
    line_data = {
        'Produção Total': [85000, 88000, 92000, 89000, 95000, 98000],
        'Produção Prevista': [86000, 89000, 90000, 92000, 94000, 96000],
        'Custo Operacional': [45000, 47000, 49000, 48000, 50000, 52000]
    }
    
    try:
        line_chart = generator.create_advanced_line_chart(
            data=line_data,
            dates=dates,
            title="Análise de Produção e Custos Operacionais",
            subtitle="Comparação entre produção real vs prevista e custos",
            y_label="Valor (USD)",
            show_trend=True,
            show_forecast=True
        )
        
        if line_chart:
            print("✅ Gráfico de linhas criado com sucesso!")
            print(f"   📊 Tamanho do gráfico: {len(line_chart)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_linhas_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(line_chart))
            print("   💾 Gráfico salvo como 'teste_linhas_melhorado.png'")
        else:
            print("❌ Erro: Gráfico de linhas vazio")
            
    except Exception as e:
        print(f"❌ Erro ao criar gráfico de linhas: {e}")
    
    # Testar dashboard de KPIs
    print("\n📊 Testando dashboard de KPIs...")
    kpis = {
        'production_efficiency': {
            'current': 87.5,
            'target': 85.0,
            'trend': 'up'
        },
        'operational_cost_ratio': {
            'current': 32.1,
            'target': 30.0,
            'trend': 'stable'
        },
        'safety_incident_rate': {
            'current': 0.8,
            'target': 0.5,
            'trend': 'down'
        },
        'environmental_compliance': {
            'current': 96.2,
            'target': 95.0,
            'trend': 'up'
        },
        'equipment_availability': {
            'current': 91.3,
            'target': 90.0,
            'trend': 'up'
        },
        'reserves_replacement_ratio': {
            'current': 78.5,
            'target': 100.0,
            'trend': 'down'
        }
    }
    
    try:
        kpi_dashboard = generator.create_kpi_dashboard(
            kpis=kpis,
            title="Painel de KPIs - Setor Petrolífero Angolano"
        )
        
        if kpi_dashboard:
            print("✅ Dashboard de KPIs criado com sucesso!")
            print(f"   📊 Tamanho do dashboard: {len(kpi_dashboard)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_kpi_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(kpi_dashboard))
            print("   💾 Dashboard salvo como 'teste_kpi_melhorado.png'")
        else:
            print("❌ Erro: Dashboard de KPIs vazio")
            
    except Exception as e:
        print(f"❌ Erro ao criar dashboard de KPIs: {e}")
    
    # Testar análise de produção
    print("\n🏭 Testando análise de produção...")
    production_data = {
        'Campo A': [25000, 26000, 27000, 26500, 28000, 29000],
        'Campo B': [18000, 18500, 19000, 18800, 19500, 20000],
        'Campo C': [15000, 15500, 16000, 15800, 16500, 17000],
        'Campo D': [12000, 12500, 13000, 12800, 13500, 14000]
    }
    
    try:
        production_chart = generator.create_production_analysis_chart(
            production_data=production_data,
            time_periods=dates,
            title="Análise Detalhada de Produção por Campo"
        )
        
        if production_chart:
            print("✅ Análise de produção criada com sucesso!")
            print(f"   📊 Tamanho do gráfico: {len(production_chart)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_producao_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(production_chart))
            print("   💾 Gráfico salvo como 'teste_producao_melhorado.png'")
        else:
            print("❌ Erro: Análise de produção vazia")
            
    except Exception as e:
        print(f"❌ Erro ao criar análise de produção: {e}")
    
    # Testar análise financeira
    print("\n💰 Testando análise financeira...")
    financial_data = {
        'revenue': [850, 880, 920, 890, 950, 980],
        'ebitda': [340, 352, 368, 356, 380, 392],
        'ebitda_margin': [40.0, 40.0, 40.0, 40.0, 40.0, 40.0],
        'capex': [120, 125, 130, 128, 135, 140]
    }
    
    try:
        financial_chart = generator.create_financial_performance_chart(
            financial_data=financial_data,
            periods=dates
        )
        
        if financial_chart:
            print("✅ Análise financeira criada com sucesso!")
            print(f"   📊 Tamanho do gráfico: {len(financial_chart)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_financeiro_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(financial_chart))
            print("   💾 Gráfico salvo como 'teste_financeiro_melhorado.png'")
        else:
            print("❌ Erro: Análise financeira vazia")
            
    except Exception as e:
        print(f"❌ Erro ao criar análise financeira: {e}")
    
    # Testar gráfico de barras
    print("\n📊 Testando gráfico de barras...")
    bar_data = {
        'TotalEnergies': 450000,
        'Sonangol': 380000,
        'Chevron': 320000,
        'Azule Energy': 280000,
        'ENI': 250000,
        'BP': 220000
    }
    
    try:
        bar_chart = generator.create_advanced_bar_chart(
            data=bar_data,
            title="Investimentos por Empresa em Angola",
            subtitle="Análise comparativa dos investimentos (USD milhões)",
            x_label="Empresas",
            y_label="Investimentos (USD milhões)"
        )
        
        if bar_chart:
            print("✅ Gráfico de barras criado com sucesso!")
            print(f"   📊 Tamanho do gráfico: {len(bar_chart)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_barras_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(bar_chart))
            print("   💾 Gráfico salvo como 'teste_barras_melhorado.png'")
        else:
            print("❌ Erro: Gráfico de barras vazio")
            
    except Exception as e:
        print(f"❌ Erro ao criar gráfico de barras: {e}")
    
    # Testar gráfico de pizza
    print("\n🥧 Testando gráfico de pizza...")
    pie_data = {
        'Exploração': 45.2,
        'Refino': 28.7,
        'Distribuição': 15.3,
        'Petróquímica': 10.8
    }
    
    try:
        pie_chart = generator.create_pie_chart_advanced(
            data=pie_data,
            title="Distribuição das Atividades do Setor Petrolífero"
        )
        
        if pie_chart:
            print("✅ Gráfico de pizza criado com sucesso!")
            print(f"   📊 Tamanho do gráfico: {len(pie_chart)} caracteres base64")
            
            # Salvar para visualização
            with open('teste_pizza_melhorado.png', 'wb') as f:
                import base64
                f.write(base64.b64decode(pie_chart))
            print("   💾 Gráfico salvo como 'teste_pizza_melhorado.png'")
        else:
            print("❌ Erro: Gráfico de pizza vazio")
            
    except Exception as e:
        print(f"❌ Erro ao criar gráfico de pizza: {e}")
    
    print("\n🎉 Teste concluído! Verifique os arquivos PNG gerados.")
    print("\n🔍 Principais melhorias implementadas:")
    print("   ✅ Legendas e labels fora dos gráficos para evitar sobreposição")
    print("   ✅ Mais espaçamento entre elementos visuais")
    print("   ✅ Cores mais harmoniosas e profissionais")
    print("   ✅ Anotações inteligentes que evitam sobreposição")
    print("   ✅ Layout automático melhorado")
    print("   ✅ Fontes e tamanhos otimizados")
    print("   ✅ Grades mais sutis e elegantes")

if __name__ == "__main__":
    test_graficos_melhorados()