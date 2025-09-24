"""
Gerador avançado de gráficos e KPIs para o setor de petróleo e gás.
Inclui métricas especializadas, análises contextuais e visualizações profissionais.
"""
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logger = logging.getLogger(__name__)

class AdvancedChartGenerator:
    """
    Gerador avançado com KPIs e métricas especializadas para o setor petrolífero.
    """
    
    def __init__(self):
        # Paleta de cores profissional para petróleo e gás
        self.oil_gas_palette = {
            'primary': ['#1f4e79', '#2e75b6', '#5b9bd5', '#a5d6ff', '#e1f0ff'],
            'secondary': ['#c5504b', '#d6604d', '#f2a1a1', '#ffe6e6'],
            'tertiary': ['#70ad47', '#9bc53f', '#c6e377', '#e8f5d6'],
            'neutral': ['#404040', '#737373', '#aeaeae', '#e6e6e6']
        }
        
        # Configurações de estilo
        self.style_config = {
            'font_family': 'Arial, sans-serif',
            'title_size': 16,
            'label_size': 12,
            'tick_size': 10,
            'dpi': 300,
            'figsize': (12, 8),
            'grid_alpha': 0.3
        }
        
        # KPIs específicos do setor
        self.oil_gas_kpis = {
            'production_efficiency': 'Eficiência de Produção',
            'operational_cost_ratio': 'Custo Operacional/Receita',
            'safety_incident_rate': 'Taxa de Incidentes de Segurança',
            'environmental_compliance': 'Conformidade Ambiental',
            'equipment_availability': 'Disponibilidade de Equipamentos',
            'reserves_replacement_ratio': 'Taxa de Substituição de Reservas'
        }
        
        # Configurar estilo seaborn
        sns.set_theme(style="whitegrid", palette="husl")
        plt.style.use('seaborn-v0_8')
    
    def create_advanced_line_chart(self, data: Dict[str, List[float]], 
                                  dates: List[str], title: str = "",
                                  subtitle: str = "", y_label: str = "Valor (USD)",
                                  show_trend: bool = True, show_forecast: bool = True) -> str:
        """
        Cria gráfico de linhas avançado com análise de tendência e projeção.
        """
        try:
            fig, ax = plt.subplots(figsize=self.style_config['figsize'], dpi=self.style_config['dpi'])
            
            colors = self.oil_gas_palette['primary']
            
            for i, (series_name, values) in enumerate(data.items()):
                # Converter valores para float
                numeric_values = [float(v) for v in values]
                
                # Plotar linha principal
                ax.plot(dates, numeric_values, 
                       color=colors[i % len(colors)],
                       linewidth=3, marker='o', markersize=8,
                       label=series_name, alpha=0.8)
                
                # Adicionar tendência se solicitado
                if show_trend and len(numeric_values) > 3:
                    x_numeric = range(len(numeric_values))
                    z = np.polyfit(x_numeric, numeric_values, 1)
                    p = np.poly1d(z)
                    trend_values = p(x_numeric)
                    
                    ax.plot(dates, trend_values, 
                           color=colors[i % len(colors)],
                           linewidth=2, linestyle='--', alpha=0.6,
                           label=f'{series_name} (Tendência)')
                
                # Adicionar projeção se solicitado
                if show_forecast and len(numeric_values) > 5:
                    forecast_dates, forecast_values = self._generate_forecast(dates, numeric_values)
                    if forecast_dates:
                        ax.plot(forecast_dates, forecast_values,
                               color=colors[i % len(colors)],
                               linewidth=2, linestyle=':', alpha=0.7,
                               label=f'{series_name} (Projeção)')
                        
                        # Adicionar área de confiança
                        confidence_interval = self._calculate_confidence_interval(numeric_values, forecast_values)
                        ax.fill_between(forecast_dates, 
                                      [f - ci for f, ci in zip(forecast_values, confidence_interval)],
                                      [f + ci for f, ci in zip(forecast_values, confidence_interval)],
                                      alpha=0.2, color=colors[i % len(colors)])
            
            # Configurar eixos e títulos
            ax.set_title(f"{title}\n{subtitle}" if subtitle else title, 
                        fontsize=self.style_config['title_size'], 
                        fontweight='bold', pad=20)
            ax.set_xlabel('Período', fontsize=self.style_config['label_size'], fontweight='bold')
            ax.set_ylabel(y_label, fontsize=self.style_config['label_size'], fontweight='bold')
            
            # Melhorar aparência
            ax.grid(True, alpha=self.style_config['grid_alpha'], linestyle='-', linewidth=0.5)
            ax.legend(loc='best', fontsize=self.style_config['tick_size'], frameon=True, shadow=True)
            
            # Formatar eixo Y para valores monetários
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Rotacionar labels do eixo X
            plt.xticks(rotation=45, ha='right')
            
            # Adicionar anotações de valores máximos e mínimos
            self._add_value_annotations(ax, data, dates)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'], 
                       bbox_inches='tight', facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de linhas avançado: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_kpi_dashboard(self, kpis: Dict[str, Dict[str, float]], 
                           title: str = "Painel de KPIs - Petróleo e Gás") -> str:
        """
        Cria dashboard profissional com KPIs do setor petrolífero.
        """
        try:
            fig = plt.figure(figsize=(16, 10), dpi=self.style_config['dpi'])
            
            # Layout 2x3 para KPIs
            n_kpis = len(kpis)
            cols = 3
            rows = (n_kpis + cols - 1) // cols
            
            for i, (kpi_key, kpi_data) in enumerate(kpis.items()):
                ax = plt.subplot(rows, cols, i + 1)
                
                # Obter configuração do KPI
                kpi_config = self._get_kpi_config(kpi_key)
                
                # Criar gráfico de gauge
                self._create_gauge_chart(ax, kpi_data, kpi_config)
                
                ax.set_title(kpi_config['name'], fontsize=14, fontweight='bold', pad=20)
            
            # Adicionar título geral
            fig.suptitle(title, fontsize=20, fontweight='bold', y=0.95)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none')
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
        Cria análise detalhada de produção com múltiplas métricas.
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=self.style_config['dpi'])
            
            colors = self.oil_gas_palette['primary']
            
            # Gráfico 1: Produção total
            total_production = [sum(values) for values in zip(*production_data.values())]
            ax1.plot(time_periods, total_production, color=colors[0], linewidth=3, marker='o')
            ax1.set_title('Produção Total', fontweight='bold')
            ax1.set_ylabel('Barris/Dia')
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Produção por campo
            for i, (field, values) in enumerate(production_data.items()):
                ax2.plot(time_periods, values, label=field, color=colors[i % len(colors)], linewidth=2)
            ax2.set_title('Produção por Campo', fontweight='bold')
            ax2.set_ylabel('Barris/Dia')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Gráfico 3: Eficiência de produção
            efficiency = self._calculate_production_efficiency(production_data)
            ax3.bar(time_periods, efficiency, color=colors[2], alpha=0.7)
            ax3.set_title('Eficiência de Produção (%)', fontweight='bold')
            ax3.set_ylabel('Percentual')
            ax3.grid(True, alpha=0.3)
            
            # Gráfico 4: Análise de tendência
            trend_data = self._calculate_trend_analysis(production_data, time_periods)
            ax4.plot(time_periods, trend_data['growth_rate'], color=colors[3], linewidth=2, marker='s')
            ax4.axhline(y=0, color='red', linestyle='--', alpha=0.7)
            ax4.set_title('Taxa de Crescimento (%)', fontweight='bold')
            ax4.set_ylabel('Percentual')
            ax4.grid(True, alpha=0.3)
            
            # Título geral
            fig.suptitle(title, fontsize=18, fontweight='bold')
            
            # Rotacionar labels do eixo X
            for ax in [ax1, ax2, ax3, ax4]:
                ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none')
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
        Cria análise financeira detalhada com múltiplas métricas.
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=self.style_config['dpi'])
            axes = axes.flatten()
            
            # Métricas financeiras
            metrics = [
                ('Receita', 'revenue', 'Revenue (USD M)'),
                ('EBITDA', 'ebitda', 'EBITDA (USD M)'),
                ('Margem EBITDA', 'ebitda_margin', 'Margem (%)'),
                ('CAPEX', 'capex', 'CAPEX (USD M)')
            ]
            
            colors = self.oil_gas_palette['primary']
            
            for i, (display_name, key, y_label) in enumerate(metrics):
                ax = axes[i]
                
                if key in financial_data:
                    values = financial_data[key]
                    
                    # Plotar linha principal
                    ax.plot(periods, values, color=colors[i], linewidth=3, marker='o', markersize=8)
                    
                    # Adicionar área colorida
                    ax.fill_between(periods, values, alpha=0.3, color=colors[i])
                    
                    # Adicionar valores nos pontos
                    for j, (period, value) in enumerate(zip(periods, values)):
                        ax.annotate(f'${value:,.0f}M' if 'USD' in y_label else f'{value:.1f}%',
                                  (j, value), textcoords="offset points", 
                                  xytext=(0,10), ha='center', fontweight='bold')
                    
                    ax.set_title(display_name, fontsize=14, fontweight='bold')
                    ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    ax.tick_params(axis='x', rotation=45)
            
            # Título geral
            fig.suptitle('Performance Financeira - Análise Trimestral', fontsize=18, fontweight='bold')
            
            plt.tight_layout()
            
            # Salvar como base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=self.style_config['dpi'],
                       bbox_inches='tight', facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar análise financeira: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def _generate_forecast(self, dates: List[str], values: List[float]) -> Tuple[List[str], List[float]]:
        """Gera projeção baseada em tendência linear."""
        try:
            if len(values) < 3:
                return [], []
            
            # Simples projeção linear
            x = np.arange(len(values))
            z = np.polyfit(x, values, 1)
            p = np.poly1d(z)
            
            # Gerar 3 pontos de projeção
            future_x = np.arange(len(values), len(values) + 3)
            forecast_values = p(future_x)
            
            # Gerar datas futuras
            last_date = datetime.strptime(dates[-1], '%Y-%m')
            forecast_dates = []
            for i in range(1, 4):
                future_date = last_date + timedelta(days=30*i)
                forecast_dates.append(future_date.strftime('%Y-%m'))
            
            return forecast_dates, forecast_values.tolist()
            
        except Exception:
            return [], []
    
    def _calculate_confidence_interval(self, historical: List[float], forecast: List[float]) -> List[float]:
        """Calcula intervalo de confiança simples."""
        try:
            std_dev = np.std(historical)
            return [std_dev * 0.5] * len(forecast)  # Simplificado
        except Exception:
            return [0] * len(forecast)
    
    def _add_value_annotations(self, ax, data: Dict[str, List[float]], dates: List[str]):
        """Adiciona anotações de valores máximos e mínimos."""
        try:
            for series_name, values in data.items():
                numeric_values = [float(v) for v in values]
                max_idx = np.argmax(numeric_values)
                min_idx = np.argmin(numeric_values)
                
                # Anotação máxima
                ax.annotate(f'MÁX: ${numeric_values[max_idx]:,.0f}',
                          xy=(dates[max_idx], numeric_values[max_idx]),
                          xytext=(10, 10), textcoords='offset points',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='green', alpha=0.7),
                          fontsize=9, fontweight='bold')
                
                # Anotação mínima
                ax.annotate(f'MÍN: ${numeric_values[min_idx]:,.0f}',
                          xy=(dates[min_idx], numeric_values[min_idx]),
                          xytext=(10, -15), textcoords='offset points',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7),
                          fontsize=9, fontweight='bold')
                
                break  # Apenas para a primeira série
                
        except Exception:
            pass  # Ignorar erros de anotação
    
    def _get_kpi_config(self, kpi_key: str) -> Dict[str, Any]:
        """Obtém configuração de KPI."""
        configs = {
            'production_efficiency': {
                'name': 'Eficiência de Produção',
                'unit': '%',
                'target': 85,
                'min_good': 75,
                'color_scale': 'RdYlGn'
            },
            'operational_cost_ratio': {
                'name': 'Custo Operacional/Receita',
                'unit': '%',
                'target': 30,
                'max_good': 35,
                'color_scale': 'RdYlGn_r'
            },
            'safety_incident_rate': {
                'name': 'Taxa de Incidentes',
                'unit': 'incidentes/1M horas',
                'target': 0.5,
                'max_good': 1.0,
                'color_scale': 'RdYlGn_r'
            }
        }
        return configs.get(kpi_key, configs['production_efficiency'])
    
    def _create_gauge_chart(self, ax, kpi_data: Dict[str, float], config: Dict[str, Any]):
        """Cria gráfico de gauge para KPI."""
        try:
            value = kpi_data.get('current', 0)
            target = config['target']
            
            # Criar semicírculo
            theta = np.linspace(0, np.pi, 100)
            r = np.ones_like(theta)
            
            # Cores baseadas no valor
            if config['unit'] == '%':
                if value >= config['min_good']:
                    color = 'green'
                elif value >= target * 0.8:
                    color = 'orange'
                else:
                    color = 'red'
            else:
                if value <= config.get('max_good', target * 1.2):
                    color = 'green'
                elif value <= target * 1.5:
                    color = 'orange'
                else:
                    color = 'red'
            
            # Plotar gauge
            ax.plot(theta, r, color='lightgray', linewidth=10)
            ax.fill_between(theta[:int(len(theta) * value/target)], 
                          r[:int(len(theta) * value/target)], 
                          color=color, alpha=0.8)
            
            # Adicionar valor e rótulos
            ax.text(np.pi/2, 0.5, f'{value}{config["unit"]}', 
                   ha='center', va='center', fontsize=16, fontweight='bold')
            ax.text(np.pi/2, 0.2, f'Meta: {target}{config["unit"]}', 
                   ha='center', va='center', fontsize=10, alpha=0.7)
            
            ax.set_xlim(0, np.pi)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
        except Exception:
            ax.text(0.5, 0.5, f'{config["name"]}\nDados Indisponíveis', 
                   ha='center', va='center', fontsize=12)
            ax.axis('off')
    
    def _calculate_production_efficiency(self, production_data: Dict[str, List[float]]) -> List[float]:
        """Calcula eficiência de produção."""
        try:
            # Simplificado: eficiência baseada na variação
            total_production = [sum(values) for values in zip(*production_data.values())]
            max_production = max(total_production)
            efficiency = [(p/max_production)*100 for p in total_production]
            return efficiency
        except Exception:
            return [80] * len(list(production_data.values())[0])  # Valor padrão
    
    def _calculate_trend_analysis(self, production_data: Dict[str, List[float]], 
                                time_periods: List[str]) -> Dict[str, List[float]]:
        """Calcula análise de tendência."""
        try:
            total_production = [sum(values) for values in zip(*production_data.values())]
            
            # Calcular taxa de crescimento mês a mês
            growth_rate = []
            for i in range(1, len(total_production)):
                if total_production[i-1] > 0:
                    growth = ((total_production[i] - total_production[i-1]) / total_production[i-1]) * 100
                    growth_rate.append(growth)
                else:
                    growth_rate.append(0)
            
            # Adicionar primeiro valor como 0
            growth_rate.insert(0, 0)
            
            return {'growth_rate': growth_rate}
        except Exception:
            return {'growth_rate': [0] * len(time_periods)}
    
    def _create_error_chart(self, error_message: str) -> str:
        """Cria gráfico de erro."""
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            ax.text(0.5, 0.5, f'Erro ao Gerar Gráfico\n\n{error_message}', 
                   ha='center', va='center', fontsize=14, 
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='red', alpha=0.1))
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception:
            return ""