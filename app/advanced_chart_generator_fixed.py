"""
Gerador avançado de gráficos e KPIs para o setor de petróleo e gás.
VERSÃO MELHORADA - Corrige problemas visuais.
"""

import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logger = logging.getLogger(__name__)

class AdvancedChartGeneratorFixed:
    """
    Gerador avançado com KPIs e métricas especializadas para o setor petrolífero.
    VERSÃO MELHORADA com gráficos profissionais e sem sobreposições.
    """
    
    def __init__(self):
        # Paleta de cores profissional para petróleo e gás
        self.oil_gas_palette = {
            'primary': ['#1f4e79', '#2e75b6', '#5b9bd5', '#a5d6ff', '#e1f0ff'],
            'secondary': ['#c5504b', '#d6604d', '#f2a1a1', '#ffe6e6'],
            'tertiary': ['#70ad47', '#9bc53f', '#c6e377', '#e8f5d6'],
            'neutral': ['#404040', '#737373', '#aeaeae', '#e6e6e6'],
            'accent': ['#ff6b35', '#f7931e', '#ffd23f', '#06d6a0', '#118ab2']
        }
        
        # Configurações de estilo melhoradas
        self.style_config = {
            'font_family': 'Arial, sans-serif',
            'title_size': 16,
            'subtitle_size': 12,
            'label_size': 11,
            'tick_size': 9,
            'dpi': 300,
            'figsize': (14, 8),
            'grid_alpha': 0.2,
            'legend_fontsize': 10,
            'annotation_fontsize': 9
        }
        
        # Configurar estilo seaborn com melhorias
        sns.set_theme(style="whitegrid", palette="husl")
        plt.style.use('seaborn-v0_8')
        
        # Configurações para evitar sobreposições
        plt.rcParams.update({
            'figure.constrained_layout.use': True,
            'figure.autolayout': False,
            'legend.frameon': True,
            'legend.shadow': True,
            'legend.framealpha': 0.8,
            'axes.titlepad': 20,
            'axes.labelpad': 10,
            'xtick.major.pad': 8,
            'ytick.major.pad': 8
        })
    
    def create_advanced_line_chart(self, data: Dict[str, List[float]], 
                                  dates: List[str], title: str = "",
                                  subtitle: str = "", y_label: str = "Valor (USD)",
                                  show_trend: bool = True, show_forecast: bool = True) -> str:
        """
        Cria gráfico de linhas avançado COM MELHORIAS VISUAIS.
        """
        try:
            fig, ax = plt.subplots(figsize=self.style_config['figsize'], dpi=self.style_config['dpi'])
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.1, right=0.85, top=0.85, bottom=0.15)
            
            colors = self.oil_gas_palette['primary']
            
            for i, (series_name, values) in enumerate(data.items()):
                numeric_values = [float(v) for v in values]
                
                # Plotar linha principal com estilo melhorado
                ax.plot(dates, numeric_values, 
                       color=colors[i % len(colors)],
                       linewidth=3, marker='o', markersize=6,
                       label=series_name, alpha=0.9)
            
            # Configurar eixos e títulos com melhor espaçamento
            full_title = f"{title}\n{subtitle}" if subtitle else title
            ax.set_title(full_title, 
                        fontsize=self.style_config['title_size'], 
                        fontweight='bold', 
                        pad=25)
            
            ax.set_xlabel('Período', 
                         fontsize=self.style_config['label_size'], 
                         fontweight='bold',
                         labelpad=15)
            
            ax.set_ylabel(y_label, 
                         fontsize=self.style_config['label_size'], 
                         fontweight='bold',
                         labelpad=15)
            
            # LEGENDA FORA DO GRÁFICO para evitar sobreposição
            ax.legend(bbox_to_anchor=(1.05, 1), 
                     loc='upper left',
                     fontsize=self.style_config['legend_fontsize'],
                     frameon=True, 
                     shadow=True,
                     facecolor='white',
                     edgecolor='gray',
                     framealpha=0.9)
            
            # Rotacionar labels do eixo X com melhor espaçamento
            ax.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            ax.tick_params(axis='y', labelsize=self.style_config['tick_size'])
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'], 
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de linhas: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_kpi_dashboard(self, kpis: Dict[str, Dict[str, float]], 
                           title: str = "Painel de KPIs - Petróleo e Gás") -> str:
        """
        Cria dashboard profissional com KPIs do setor petrolífero.
        """
        try:
            n_kpis = len(kpis)
            if n_kpis <= 2:
                cols, rows = 2, 1
                figsize = (14, 6)
            elif n_kpis <= 4:
                cols, rows = 2, 2
                figsize = (14, 10)
            else:
                cols, rows = 3, 2
                figsize = (16, 10)
            
            fig = plt.figure(figsize=figsize, dpi=self.style_config['dpi'])
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15, 
                               wspace=0.3, hspace=0.4)
            
            for i, (kpi_key, kpi_data) in enumerate(kpis.items()):
                ax = plt.subplot(rows, cols, i + 1)
                
                # Criar gráfico de gauge simples
                value = kpi_data.get('current', 0)
                
                # Criar semicírculo
                theta = np.linspace(0, np.pi, 100)
                r = np.ones_like(theta) * 0.8
                
                ax.plot(theta, r, color='lightgray', linewidth=12, alpha=0.5)
                
                # Adicionar valor
                ax.text(np.pi/2, 0.4, f'{value:.1f}%', 
                       ha='center', va='center', fontsize=18, fontweight='bold')
                
                ax.set_title(kpi_key.replace('_', ' ').title(), 
                           fontsize=13, fontweight='bold', pad=20)
                
                ax.set_xlim(0, np.pi)
                ax.set_ylim(0, 1)
                ax.set_aspect('equal')
                ax.axis('off')
            
            # Adicionar título geral
            fig.suptitle(title, fontsize=18, fontweight='bold', y=0.92)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar dashboard de KPIs: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_production_analysis_chart(self, production_data: Dict[str, List[float]],
                                       time_periods: List[str], 
                                       title: str = "Análise de Produção") -> str:
        """
        Cria análise detalhada de produção com MELHORIAS VISUAIS.
        """
        try:
            # Criar layout 2x2 com mais espaço
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=self.style_config['dpi'])
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.08, right=0.92, top=0.85, bottom=0.12, 
                               wspace=0.25, hspace=0.35)
            
            colors = self.oil_gas_palette['primary']
            
            # Gráfico 1: Produção total
            total_production = [sum(values) for values in zip(*production_data.values())]
            ax1.plot(time_periods, total_production, color=colors[0], linewidth=3, 
                    marker='o', markersize=6)
            ax1.set_title('Produção Total', fontweight='bold', fontsize=14, pad=15)
            ax1.set_ylabel('Barris/Dia', fontweight='bold', fontsize=12)
            ax1.grid(True, alpha=0.2)
            ax1.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            
            # Gráfico 2: Produção por campo
            for i, (field, values) in enumerate(production_data.items()):
                ax2.plot(time_periods, values, label=field, color=colors[i % len(colors)], 
                        linewidth=2.5, marker='s', markersize=5)
            
            ax2.set_title('Produção por Campo', fontweight='bold', fontsize=14, pad=15)
            ax2.set_ylabel('Barris/Dia', fontweight='bold', fontsize=12)
            ax2.grid(True, alpha=0.2)
            ax2.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            
            # LEGENDA FORA DO GRÁFICO
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                      fontsize=self.style_config['legend_fontsize'],
                      frameon=True, shadow=True, facecolor='white')
            
            # Gráfico 3: Eficiência de produção
            # Calcular eficiência simplificada
            efficiency = []
            for values in zip(*production_data.values()):
                total = sum(values)
                efficiency.append(min(100, (total / 1000) * 100))  # Normalizar
            
            bars = ax3.bar(time_periods, efficiency, color=colors[2], alpha=0.7, 
                          edgecolor='black', linewidth=0.5)
            ax3.set_title('Eficiência de Produção (%)', fontweight='bold', fontsize=14, pad=15)
            ax3.set_ylabel('Percentual (%)', fontweight='bold', fontsize=12)
            ax3.grid(True, alpha=0.2)
            ax3.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            ax3.set_ylim(0, 100)
            
            # Gráfico 4: Análise de tendência
            # Calcular crescimento simples
            growth_rate = []
            for i in range(1, len(total_production)):
                if total_production[i-1] > 0:
                    growth = ((total_production[i] - total_production[i-1]) / total_production[i-1]) * 100
                    growth_rate.append(growth)
                else:
                    growth_rate.append(0)
            growth_rate.insert(0, 0)  # Primeiro valor como 0
            
            ax4.plot(time_periods, growth_rate, color=colors[3], linewidth=2.5, 
                    marker='s', markersize=6, label='Crescimento')
            ax4.axhline(y=0, color='red', linestyle='--', alpha=0.7, linewidth=2)
            ax4.set_title('Taxa de Crescimento (%)', fontweight='bold', fontsize=14, pad=15)
            ax4.set_ylabel('Percentual (%)', fontweight='bold', fontsize=12)
            ax4.grid(True, alpha=0.2)
            ax4.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            
            # Título geral
            fig.suptitle(title, fontsize=18, fontweight='bold', y=0.92)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar análise de produção: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_financial_performance_chart(self, financial_data: Dict[str, List[float]],
                                        periods: List[str]) -> str:
        """
        Cria análise financeira detalhada com MELHORIAS VISUAIS.
        """
        try:
            # Layout 2x2 com mais espaço
            fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=self.style_config['dpi'])
            axes = axes.flatten()
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.08, right=0.92, top=0.85, bottom=0.12, 
                               wspace=0.25, hspace=0.35)
            
            # Métricas financeiras
            metrics = [
                ('Receita Total', 'revenue', 'Receita (USD M)'),
                ('EBITDA', 'ebitda', 'EBITDA (USD M)'),
                ('Margem EBITDA', 'ebitda_margin', 'Margem (%)'),
                ('CAPEX', 'capex', 'CAPEX (USD M)')
            ]
            
            colors = self.oil_gas_palette['primary']
            
            for i, (display_name, key, y_label) in enumerate(metrics):
                ax = axes[i]
                
                if key in financial_data:
                    values = financial_data[key]
                    
                    # Plotar linha principal com estilo melhorado
                    ax.plot(periods, values, color=colors[i], linewidth=3, 
                           marker='o', markersize=7)
                    
                    # Adicionar área colorida sutil
                    ax.fill_between(periods, values, alpha=0.2, color=colors[i])
                    
                    # Configurações do gráfico com mais espaço
                    ax.set_title(display_name, fontsize=14, fontweight='bold', pad=15)
                    ax.set_ylabel(y_label, fontsize=12, fontweight='bold', labelpad=10)
                    ax.grid(True, alpha=0.2)
                    ax.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
                    ax.tick_params(axis='y', labelsize=self.style_config['tick_size'])
            
            # Título geral
            fig.suptitle('Performance Financeira - Análise Trimestral', 
                        fontsize=18, fontweight='bold', y=0.92)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar análise financeira: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_advanced_bar_chart(self, data: Dict[str, float], title: str = "Comparação de Valores",
                                 subtitle: str = "", x_label: str = "Categorias", 
                                 y_label: str = "Valores") -> str:
        """
        Cria gráfico de barras avançado com estilo profissional.
        """
        try:
            fig, ax = plt.subplots(figsize=(12, 8), dpi=self.style_config['dpi'])
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
            
            categories = list(data.keys())
            values = list(data.values())
            colors = self.oil_gas_palette['primary'][:len(categories)]
            
            # Criar barras
            bars = ax.bar(categories, values, color=colors, alpha=0.8, 
                         edgecolor='black', linewidth=0.5)
            
            # Adicionar valores nas barras (com posição inteligente)
            for bar, value in zip(bars, values):
                height = bar.get_height()
                # Posicionar valor dentro da barra se for alta, fora se for baixa
                if height > max(values) * 0.8:
                    y_pos = height * 0.9
                    color = 'white'
                else:
                    y_pos = height + max(values) * 0.02
                    color = 'black'
                
                ax.text(bar.get_x() + bar.get_width()/2., y_pos,
                       f'{value:,.0f}', ha='center', va='center' if height > max(values) * 0.8 else 'bottom',
                       fontsize=self.style_config['annotation_fontsize'],
                       fontweight='bold', color=color)
            
            # Configurações do gráfico
            full_title = f"{title}\n{subtitle}" if subtitle else title
            ax.set_title(full_title, fontsize=self.style_config['title_size'], 
                        fontweight='bold', pad=20)
            ax.set_xlabel(x_label, fontsize=self.style_config['label_size'], 
                         fontweight='bold', labelpad=10)
            ax.set_ylabel(y_label, fontsize=self.style_config['label_size'], 
                         fontweight='bold', labelpad=10)
            
            # Melhorar aparência
            ax.grid(True, alpha=0.2, axis='y', linestyle='-', linewidth=0.5)
            ax.tick_params(axis='x', rotation=45, labelsize=self.style_config['tick_size'])
            ax.tick_params(axis='y', labelsize=self.style_config['tick_size'])
            
            plt.tight_layout()
            
            # Salvar
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de barras: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_pie_chart_advanced(self, data: Dict[str, float], title: str = "Distribuição") -> str:
        """
        Cria gráfico de pizza avançado com estilo profissional.
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 8), dpi=self.style_config['dpi'])
            
            # Adicionar margens extras
            fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
            
            labels = list(data.keys())
            values = list(data.values())
            colors = self.oil_gas_palette['primary'][:len(labels)]
            
            # Criar gráfico de pizza com estilo melhorado
            wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors,
                                              autopct='%1.1f%%', startangle=90,
                                              textprops={'fontsize': self.style_config['label_size'],
                                                       'fontweight': 'bold'})
            
            # Melhorar aparência dos textos
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(self.style_config['annotation_fontsize'])
            
            # Configurações
            ax.set_title(title, fontsize=self.style_config['title_size'], 
                        fontweight='bold', pad=20)
            
            # Adicionar legenda fora do gráfico
            ax.legend(wedges, [f'{label}: {value:,.0f}' for label, value in zip(labels, values)],
                     title="Valores", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=self.style_config['legend_fontsize'])
            
            plt.tight_layout()
            
            # Salvar
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none',
                       pad_inches=0.2)
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de pizza: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def _create_error_chart(self, error_message: str) -> str:
        """Cria gráfico de erro (melhorado)."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Mensagem de erro mais profissional
            ax.text(0.5, 0.6, '⚠️ Erro ao Gerar Gráfico', 
                   ha='center', va='center', fontsize=16, fontweight='bold',
                   color='darkred')
            
            ax.text(0.5, 0.4, error_message, 
                   ha='center', va='center', fontsize=12, 
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='mistyrose', 
                           alpha=0.7, edgecolor='red', linewidth=2))
            
            ax.text(0.5, 0.2, 'Por favor, verifique os dados e tente novamente.', 
                   ha='center', va='center', fontsize=10, style='italic')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception:
            return ""


# Instância global do gerador melhorado
advanced_chart_generator_fixed = AdvancedChartGeneratorFixed()