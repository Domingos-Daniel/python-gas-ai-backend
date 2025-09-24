"""
Teste para verificar se o advanced_data_analyzer_fixed está usando dados reais.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.advanced_data_analyzer_fixed import AdvancedDataAnalyzerFixed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_dados_reais():
    """Testa se o analisador está usando dados reais."""
    print("🧪 Iniciando teste de dados reais...")
    
    # Inicializa o analisador
    analyzer = AdvancedDataAnalyzerFixed()
    
    # Testes com diferentes contextos
    test_questions = [
        "Análise de investimentos da Total em Angola",
        "Performance financeira da Sonangol em 2024",
        "Produção de petróleo da Azule Energy",
        "Análise de mercado do setor petrolífero angolano",
        "KPIs de eficiência operacional da Chevron"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"Teste {i}: {question}")
        print(f"{'='*60}")
        
        try:
            result = analyzer.analyze_data(question)
            
            if result is None:
                print("❌ Análise retornou None - sem dados suficientes")
                continue
            
            # Verifica se há dados reais
            metadata = result.get('metadata', {})
            real_data_count = metadata.get('real_data_count', 0)
            data_source = metadata.get('data_source', 'unknown')
            
            print(f"✅ Análise concluída")
            print(f"📊 Fonte de dados: {data_source}")
            print(f"📈 Dados reais encontrados: {real_data_count}")
            
            # Mostra dados extraídos
            data = result.get('data', {})
            if data:
                print(f"\n📋 Dados extraídos ({len(data)} itens):")
                for key, value in list(data.items())[:5]:  # Mostra top 5
                    print(f"  • {key}: {value}")
                if len(data) > 5:
                    print(f"  ... e mais {len(data) - 5} itens")
            
            # Mostra KPIs
            kpis = result.get('kpis', {})
            if kpis:
                print(f"\n📊 KPIs calculados ({len(kpis)} métricas):")
                for kpi_name, kpi_data in list(kpis.items())[:3]:  # Mostra top 3
                    print(f"  • {kpi_name}: {kpi_data.get('value', 'N/A')} {kpi_data.get('unit', '')}")
            
            # Mostra insights
            insights = result.get('contextual_analysis', {}).get('key_insights', [])
            if insights:
                print(f"\n💡 Insights principais:")
                for insight in insights[:3]:  # Mostra top 3
                    print(f"  • {insight}")
            
            # Mostra recomendações
            recommendations = result.get('recommendations', [])
            if recommendations:
                print(f"\n🎯 Recomendações ({len(recommendations)}):")
                for rec in recommendations[:2]:  # Mostra top 2
                    print(f"  • {rec.get('category', '')}: {rec.get('recommendation', '')}")
            
            # Verifica se é baseado em dados reais
            if real_data_count > 0 and data_source == 'real_scraped_data':
                print(f"\n✅ SUCESSO: Análise baseada em dados reais!")
            else:
                print(f"\n⚠️ ATENÇÃO: Análise pode estar usando dados simulados")
            
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Teste concluído!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_dados_reais()