"""
Componente de dashboard del director
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils import format_currency
from config.settings import THEME_COLORS, GRADIENTS

def show_global_metrics(interactions, products, user_ids):
    """Muestra métricas globales del sistema"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Usuarios Totales", len(user_ids))
    
    with col2:
        st.metric("🛒 Transacciones", len(interactions))
    
    with col3:
        st.metric("📦 Productos", len(products))
    
    with col4:
        total_revenue = interactions['total_spent'].sum()
        st.metric("💰 Ingresos Totales", format_currency(total_revenue))

def show_top_products_chart(interactions):
    """Muestra gráfico de productos más vendidos"""
    st.markdown("#### 📊 Top 10 Productos Más Vendidos")
    
    top_products = interactions.groupby('product_name').agg({
        'purchase_count': 'sum',
        'total_spent': 'sum'
    }).sort_values('purchase_count', ascending=False).head(10)
    
    fig = px.bar(
        x=top_products['purchase_count'],
        y=top_products.index,
        orientation='h',
        labels={'x': 'Unidades Vendidas', 'y': 'Producto'},
        color=top_products['purchase_count'],
        color_continuous_scale='Viridis',
        text=top_products['purchase_count']
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        height=450,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_category_revenue_chart(interactions):
    """Muestra gráfico de ingresos por categoría"""
    st.markdown("#### 💰 Ingresos por Categoría")
    
    category_revenue = interactions.groupby('category')['total_spent'].sum().sort_values(ascending=False)
    
    fig = px.bar(
        x=category_revenue.index,
        y=category_revenue.values,
        labels={'x': 'Categoría', 'y': 'Ingresos ($)'},
        color=category_revenue.values,
        color_continuous_scale='Blues',
        text=category_revenue.values
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_sales_timeline(interactions):
    """Muestra evolución de ventas en el tiempo"""
    st.markdown("#### 📈 Evolución de Ventas Mensuales")
    
    interactions['purchase_date'] = pd.to_datetime(interactions['purchase_date'])
    
    monthly_sales = interactions.groupby(
        interactions['purchase_date'].dt.to_period('M')
    ).agg({
        'total_spent': 'sum',
        'product_id': 'count'
    })
    
    fig = go.Figure()
    
    # Línea de ingresos
    fig.add_trace(go.Scatter(
        x=monthly_sales.index.astype(str),
        y=monthly_sales['total_spent'],
        mode='lines+markers',
        name='Ingresos ($)',
        line=dict(color=THEME_COLORS['primary'], width=3),
        marker=dict(size=10),
        yaxis='y1'
    ))
    
    # Línea de transacciones
    fig.add_trace(go.Scatter(
        x=monthly_sales.index.astype(str),
        y=monthly_sales['product_id'],
        mode='lines+markers',
        name='Transacciones',
        line=dict(color=THEME_COLORS['success'], width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        yaxis=dict(title='Ingresos ($)', side='left'),
        yaxis2=dict(title='Transacciones', side='right', overlaying='y'),
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_user_activity_chart(user_stats):
    """Muestra distribución de actividad de usuarios"""
    st.markdown("#### 👥 Distribución de Actividad de Usuarios")
    
    # Categorizar usuarios por número de compras
    user_stats['activity_level'] = pd.cut(
        user_stats['num_interactions'],
        bins=[0, 5, 10, 20, float('inf')],
        labels=['Bajo (1-5)', 'Medio (6-10)', 'Alto (11-20)', 'Muy Alto (20+)']
    )
    
    activity_dist = user_stats['activity_level'].value_counts()
    
    fig = px.pie(
        values=activity_dist.values,
        names=activity_dist.index,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Usuarios: %{value}<br>Porcentaje: %{percent}'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_global_dashboard(interactions, products, user_stats):
    """
    Vista completa del dashboard global
    
    Args:
        interactions: DataFrame con transacciones
        products: DataFrame con productos
        user_stats: DataFrame con estadísticas de usuarios
    """
    st.markdown("### 🌍 Análisis Global del Sistema")
    
    user_ids = sorted(interactions['user_id'].unique())
    
    # Métricas principales
    show_global_metrics(interactions, products, user_ids)
    
    st.markdown("---")
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        show_top_products_chart(interactions)
        show_user_activity_chart(user_stats)
    
    with col2:
        show_category_revenue_chart(interactions)
        show_sales_timeline(interactions)