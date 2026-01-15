"""
Componente de perfil de usuario
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils import format_currency
from config.settings import THEME_COLORS

def display_user_stats_cards(user_info):
    """Muestra tarjetas con estadísticas del usuario"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🛍️ Compras Realizadas", 
            int(user_info['num_interactions'])
        )
    
    with col2:
        st.metric(
            "⭐ Rating Promedio", 
            f"{user_info['avg_rating']:.2f}"
        )
    
    with col3:
        st.metric(
            "📦 Productos Totales", 
            int(user_info['total_purchases'])
        )
    
    with col4:
        st.metric(
            "💰 Total Gastado", 
            format_currency(user_info['total_spent'])
        )

def display_category_chart(user_purchases):
    """Muestra gráfico de categorías favoritas"""
    st.markdown("#### 🏷️ Tus Categorías Favoritas")
    
    category_counts = user_purchases['category'].value_counts()
    
    fig = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation='h',
        labels={'x': 'Número de compras', 'y': 'Categoría'},
        color=category_counts.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=350,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_spending_pie(user_purchases):
    """Muestra gráfico circular de gasto por categoría"""
    st.markdown("#### 💰 Distribución de Gastos")
    
    category_spending = user_purchases.groupby('category')['total_spent'].sum()
    
    fig = px.pie(
        values=category_spending.values,
        names=category_spending.index,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Gastado: $%{value:.2f}<br>Porcentaje: %{percent}'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_rating_distribution(user_purchases):
    """Muestra distribución de ratings del usuario"""
    st.markdown("#### ⭐ Distribución de Ratings")
    
    rating_dist = user_purchases['rating'].value_counts().sort_index()
    
    fig = px.bar(
        x=rating_dist.index,
        y=rating_dist.values,
        labels={'x': 'Rating', 'y': 'Cantidad'},
        color=rating_dist.values,
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(dtick=1),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_timeline_chart(user_purchases):
    """Muestra evolución temporal de compras"""
    st.markdown("#### 📅 Evolución de Compras en el Tiempo")
    
    user_purchases['purchase_date'] = pd.to_datetime(user_purchases['purchase_date'])
    monthly_purchases = user_purchases.groupby(
        user_purchases['purchase_date'].dt.to_period('M')
    ).size()
    
    fig = px.line(
        x=monthly_purchases.index.astype(str),
        y=monthly_purchases.values,
        labels={'x': 'Mes', 'y': 'Número de compras'},
        markers=True
    )
    
    fig.update_traces(
        line_color=THEME_COLORS['primary'],
        line_width=3,
        marker=dict(size=10, color=THEME_COLORS['secondary'])
    )
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_profile_view(user_id, user_stats, user_purchases):
    """
    Vista completa del perfil de usuario
    
    Args:
        user_id: ID del usuario
        user_stats: DataFrame con estadísticas
        user_purchases: DataFrame con historial de compras
    """
    st.markdown("## 👤 Análisis de tu Perfil")
    
    user_info = user_stats[user_stats['user_id'] == user_id]
    
    if len(user_info) > 0:
        user_info = user_info.iloc[0]
        
        # Estadísticas principales
        display_user_stats_cards(user_info)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            display_category_chart(user_purchases)
            display_rating_distribution(user_purchases)
        
        with col2:
            display_spending_pie(user_purchases)
            display_timeline_chart(user_purchases)
        
    else:
        st.info("👋 ¡Bienvenido! Aún no tienes historial de compras.")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        ">
            <h3 style="color: white; margin: 0 0 1rem 0;">🚀 Comienza tu experiencia de compra</h3>
            <p style="margin: 0; opacity: 0.9;">
                Dirígete a la pestaña de Recomendaciones para descubrir productos 
                personalizados especialmente para ti.
            </p>
        </div>
        """, unsafe_allow_html=True)