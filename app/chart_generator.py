"""
Módulo de geração de gráficos interativos e modernos.
Responsável por criar visualizações profissionais com matplotlib e plotly.
"""
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime
import seaborn as sns

# Configuração de logging
logger = logging.getLogger(__name__)

# Configurações visuais profissionais
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class ChartGenerator:
    """
    Gerador de gráficos profissionais para análise de dados do setor de petróleo e gás.
    """
    
    def __init__(self):
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        self.chart_configs = {
            'width': 800,
            'height': 500,
            'font_family': 'Arial, sans-serif',
            'background_color': '#ffffff',
            'grid_color': '#f0f0f0'
        }
    
    def create_pie_chart(self, data: Dict[str, float], title: str = "", 
                        subtitle: str = "") -> str:
        """
        Cria gráfico de pizza moderno e interativo.
        
        Args:
            data: Dicionário com labels e valores
            title: Título do gráfico
            subtitle: Subtítulo do gráfico
            
        Returns:
            String base64 da imagem do gráfico
        """
        try:
            # Usar matplotlib como fallback se plotly/kaleido falhar
            return self._create_pie_chart_matplotlib(data, title, subtitle)
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de pizza: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def _create_pie_chart_matplotlib(self, data: Dict[str, float], title: str = "", 
                                   subtitle: str = "") -> str:
        """
        Cria gráfico de pizza usando matplotlib (fallback).
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Configurar cores vibrantes
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            # Criar gráfico de pizza
            wedges, texts, autotexts = plt.pie(
                data.values(),
                labels=data.keys(),
                autopct='%1.1f%%',
                colors=colors[:len(data)],
                startangle=90,
                textprops={'fontsize': 10, 'color': '#333333'}
            )
            
            # Melhorar aparência dos textos
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Adicionar título
            full_title = f"{title}"
            if subtitle:
                full_title += f"\n{subtitle}"
            plt.title(full_title, fontsize=14, fontweight='bold', pad=20, color='#333333')
            
            # Ajustar layout
            plt.axis('equal')
            plt.tight_layout()
            
            # Salvar como imagem base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de pizza com matplotlib: {e}")
            raise e
    
    def create_bar_chart(self, data: Dict[str, float], title: str = "",
                        subtitle: str = "", orientation: str = "v") -> str:
        """
        Cria gráfico de barras moderno e interativo.
        
        Args:
            data: Dicionário com labels e valores
            title: Título do gráfico
            subtitle: Subtítulo do gráfico
            orientation: 'v' para vertical, 'h' para horizontal
            
        Returns:
            String base64 da imagem do gráfico
        """
        try:
            # Usar matplotlib como fallback
            return self._create_bar_chart_matplotlib(data, title, subtitle, orientation)
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de barras: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def _create_bar_chart_matplotlib(self, data: Dict[str, float], title: str = "",
                                   subtitle: str = "", orientation: str = "v") -> str:
        """
        Cria gráfico de barras usando matplotlib (fallback).
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Configurar cores vibrantes
            colors = ['#4ECDC4', '#45B7D1', '#FF6B6B', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            labels = list(data.keys())
            values = list(data.values())
            
            # Criar gráfico de barras
            if orientation == 'h':
                bars = plt.barh(labels, values, color=colors[0])
                plt.xlabel('Valor (USD)', fontsize=12, fontweight='bold')
                
                # Adicionar valores nas barras
                for i, (bar, value) in enumerate(zip(bars, values)):
                    plt.text(value + max(values) * 0.01, bar.get_y() + bar.get_height()/2, 
                            f'${value:,.0f}', va='center', fontsize=9, fontweight='bold')
            else:
                bars = plt.bar(labels, values, color=colors[0])
                plt.ylabel('Valor (USD)', fontsize=12, fontweight='bold')
                
                # Adicionar valores nas barras
                for i, (bar, value) in enumerate(zip(bars, values)):
                    plt.text(bar.get_x() + bar.get_width()/2, value + max(values) * 0.01, 
                            f'${value:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # Adicionar título
            full_title = f"{title}"
            if subtitle:
                full_title += f"\n{subtitle}"
            plt.title(full_title, fontsize=14, fontweight='bold', pad=20, color='#333333')
            
            # Melhorar aparência
            plt.grid(axis='y' if orientation == 'v' else 'x', alpha=0.3)
            plt.xticks(rotation=45 if orientation == 'v' else 0, ha='right')
            plt.tight_layout()
            
            # Salvar como imagem base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de barras com matplotlib: {e}")
            raise e
    
    def create_line_chart(self, data: Dict[str, Any], 
                         labels: List[str], title: str = "",
                         subtitle: str = "") -> str:
        """
        Cria gráfico de linhas moderno usando matplotlib.
        
        Args:
            data: Dicionário com séries de dados
            labels: Labels para o eixo X
            title: Título do gráfico
            subtitle: Subtítulo do gráfico
            
        Returns:
            String base64 da imagem do gráfico
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Adiciona cada série de dados
            for i, (series_name, values) in enumerate(data.items()):
                # Converte valores para lista se necessário
                if isinstance(values, (int, float)):
                    y_values = [values]
                else:
                    y_values = values
                
                # Ajusta os labels para o comprimento dos dados
                x_values = labels[:len(y_values)] if len(labels) != len(y_values) else labels
                
                plt.plot(x_values, y_values, 
                        marker='o', 
                        linewidth=2.5, 
                        markersize=6,
                        color=self.color_palette[i % len(self.color_palette)],
                        label=series_name)
            
            # Adiciona título
            full_title = f"{title}"
            if subtitle:
                full_title += f"\n{subtitle}"
            plt.title(full_title, fontsize=14, fontweight='bold', pad=20, color='#333333')
            
            # Configura os eixos
            plt.xlabel('Categoria', fontsize=12, fontweight='bold')
            plt.ylabel('Valor (USD)', fontsize=12, fontweight='bold')
            
            # Melhorar aparência
            plt.grid(True, alpha=0.3)
            plt.legend(loc='best', fontsize=10)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Salvar como imagem base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de linhas: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_donut_chart(self, data: Dict[str, float], title: str = "",
                          subtitle: str = "", center_text: str = "") -> str:
        """
        Cria gráfico de donut moderno e interativo.
        
        Args:
            data: Dicionário com labels e valores
            title: Título do gráfico
            subtitle: Subtítulo do gráfico
            center_text: Texto do centro do donut
            
        Returns:
            String base64 da imagem do gráfico
        """
        try:
            # Cria gráfico de donut
            fig = go.Figure(data=[go.Pie(
                labels=list(data.keys()),
                values=list(data.values()),
                hole=0.6,  # Donut mais fino
                marker=dict(
                    colors=self.color_palette[:len(data)],
                    line=dict(color='#ffffff', width=2)
                ),
                textinfo='label+percent',
                textposition='auto',
                textfont=dict(size=12, color='#333333'),
                hovertemplate='<b>%{label}</b><br>' +
                             'Valor: %{value:,.0f}<br>' +
                             'Percentual: %{percent}<br>' +
                             '<extra></extra>'
            )])
            
            # Adiciona texto no centro
            if center_text:
                fig.add_annotation(
                    text=f"<b>{center_text}</b>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=16, color='#333333'),
                    showarrow=False
                )
            
            # Configura layout
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b><br><span style='font-size: 14px; color: #666;'>{subtitle}</span>",
                    font=dict(size=18, color='#333333'),
                    x=0.5,
                    xanchor='center'
                ),
                width=self.chart_configs['width'],
                height=self.chart_configs['height'],
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(size=11)
                ),
                margin=dict(l=20, r=150, t=80, b=20)
            )
            
            # Salva como imagem base64
            img_bytes = fig.to_image(format="png", width=800, height=500)
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de donut: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def create_dashboard(self, charts_data: List[Dict[str, Any]], 
                        title: str = "Dashboard") -> str:
        """
        Cria dashboard com múltiplos gráficos.
        
        Args:
            charts_data: Lista com configurações dos gráficos
            title: Título do dashboard
            
        Returns:
            String base64 da imagem do dashboard
        """
        try:
            # Calcula layout de grid
            n_charts = len(charts_data)
            cols = min(2, n_charts)
            rows = (n_charts + cols - 1) // cols
            
            # Cria subplots
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=[chart['title'] for chart in charts_data],
                specs=[[{"type": "domain"} for _ in range(cols)] for _ in range(rows)]
            )
            
            # Adiciona cada gráfico
            for i, chart_data in enumerate(charts_data):
                row = i // cols + 1
                col = i % cols + 1
                
                if chart_data['type'] == 'pie':
                    fig.add_trace(
                        go.Pie(
                            labels=list(chart_data['data'].keys()),
                            values=list(chart_data['data'].values()),
                            hole=0.3,
                            marker=dict(
                                colors=self.color_palette[:len(chart_data['data'])],
                                line=dict(color='#ffffff', width=2)
                            ),
                            textinfo='label+percent',
                            textfont=dict(size=10, color='#333333')
                        ),
                        row=row, col=col
                    )
                elif chart_data['type'] == 'bar':
                    fig.add_trace(
                        go.Bar(
                            x=list(chart_data['data'].keys()),
                            y=list(chart_data['data'].values()),
                            marker=dict(
                                color=self.color_palette[0],
                                line=dict(color='#ffffff', width=1)
                            ),
                            text=[f"{v:,.0f}" for v in chart_data['data'].values()],
                            textfont=dict(size=9, color='#333333')
                        ),
                        row=row, col=col
                    )
            
            # Configura layout geral
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=20, color='#333333'),
                    x=0.5,
                    xanchor='center'
                ),
                width=1200,
                height=600 * rows,
                showlegend=True,
                paper_bgcolor=self.chart_configs['background_color'],
                plot_bgcolor=self.chart_configs['background_color']
            )
            
            # Salva como imagem base64
            img_bytes = fig.to_image(format="png", width=1200, height=600 * rows)
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar dashboard: {e}")
            return self._create_error_chart(f"Erro: {str(e)}")
    
    def _create_error_chart(self, error_message: str) -> str:
        """
        Cria gráfico de erro quando algo falha.
        
        Args:
            error_message: Mensagem de erro
            
        Returns:
            String base64 da imagem de erro
        """
        try:
            fig = go.Figure()
            fig.add_annotation(
                text=f"❌<br><b>Erro ao gerar gráfico</b><br>{error_message}",
                x=0.5,
                y=0.5,
                font=dict(size=14, color='#d62728'),
                showarrow=False,
                xanchor='center',
                yanchor='middle'
            )
            
            fig.update_layout(
                width=self.chart_configs['width'],
                height=self.chart_configs['height'],
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor='#fff5f5',
                paper_bgcolor='#fff5f5'
            )
            
            img_bytes = fig.to_image(format="png", width=800, height=500)
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de erro: {e}")
            # Retorna imagem de erro simples em base64
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


# Instância global do gerador de gráficos
chart_generator = ChartGenerator()

def generate_chart(chart_type: str, data: Dict[str, Any], title: str = "",
                  subtitle: str = "", **kwargs) -> str:
    """
    Função de conveniência para gerar gráficos.
    
    Args:
        chart_type: Tipo do gráfico ('pie', 'bar', 'line', 'donut', 'dashboard')
        data: Dados do gráfico
        title: Título do gráfico
        subtitle: Subtítulo do gráfico
        **kwargs: Parâmetros adicionais
        
    Returns:
        String base64 da imagem do gráfico
    """
    try:
        if chart_type == 'pie':
            return chart_generator.create_pie_chart(data, title, subtitle)
        elif chart_type == 'bar':
            orientation = kwargs.get('orientation', 'v')
            return chart_generator.create_bar_chart(data, title, subtitle, orientation)
        elif chart_type == 'line':
            # Verifica se os valores são listas ou números simples
            first_value = next(iter(data.values()))
            if isinstance(first_value, list):
                labels = kwargs.get('labels', list(range(len(first_value))))
            else:
                # Se forem números simples, usa os próprios labels dos dados
                labels = kwargs.get('labels', list(data.keys()))
            return chart_generator.create_line_chart(data, labels, title, subtitle)
        elif chart_type == 'donut':
            center_text = kwargs.get('center_text', '')
            return chart_generator.create_donut_chart(data, title, subtitle, center_text)
        elif chart_type == 'dashboard':
            return chart_generator.create_dashboard(data, title)
        else:
            logger.error(f"Tipo de gráfico não suportado: {chart_type}")
            return chart_generator._create_error_chart("Tipo de gráfico não suportado")
            
    except Exception as e:
        logger.error(f"Erro ao gerar gráfico: {e}")
        return chart_generator._create_error_chart(f"Erro: {str(e)}")