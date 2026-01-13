"""
Aplicación Streamlit para Sistema de Recomendación de Productos
Interfaz interactiva para obtener recomendaciones personalizadas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from model import ProductRecommendationANN
import os

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Recomendación IA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model_and_data():
    """
    Carga el modelo y datos (con caché para optimizar)
    """
    try:
        # Cargar modelo
        model = ProductRecommendationANN(n_users=1, n_products=1)
        model.load_model('models/recommendation_model')
        
        # Cargar datos
        interactions = pd.read_csv('data/interactions.csv')
        products = pd.read_csv('data/products.csv')
        user_stats = pd.read_csv('data/user_stats.csv')
        
        return model, interactions, products, user_stats
    except Exception as e:
        st.error(f"❌ Error al cargar modelo o datos: {e}")
        st.info("💡 Ejecuta primero: python generate_data.py && python model.py")
        return None, None, None, None

def display_header():
    """
    Muestra el encabezado de la aplicación
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("🛒 Sistema Inteligente de Recomendación")
        st.markdown("### Powered by Redes Neuronales Artificiales (ANN)")
    
    with col2:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)

def display_how_it_works():
    """
    Muestra explicación del funcionamiento del sistema
    """
    with st.expander("🤖 ¿Cómo funciona este sistema?", expanded=False):
        st.markdown("""
        ### Tecnología de Recomendación Inteligente
        
        Este sistema utiliza **Redes Neuronales Artificiales** con una técnica llamada 
        **Collaborative Filtering** (Filtrado Colaborativo) para predecir qué productos 
        te gustarán más.
        
        #### 🧠 Proceso:
        
        1. **Aprendizaje de Patrones**: El modelo analiza miles de interacciones previas 
           (compras y ratings) de usuarios similares a ti.
        
        2. **Embeddings**: Convierte usuarios y productos en vectores numéricos que capturan 
           sus características y preferencias de forma matemática.
        
        3. **Red Neuronal Profunda**: Procesa estos vectores a través de múltiples capas 
           de neuronas artificiales (128 → 64 → 32) para encontrar patrones complejos.
        
        4. **Predicción Personalizada**: Estima qué tan probable es que te guste cada producto 
           (rating de 0 a 5) y te muestra los mejores candidatos.
        
        #### 📊 Arquitectura del Modelo:
        - **Embeddings**: 50 dimensiones para usuarios y productos
        - **Capas ocultas**: 3 capas densas con activación ReLU
        - **Dropout**: Previene sobreajuste (30%, 20%)
        - **Métricas**: MAE y RMSE para evaluar precisión
        
        #### ✨ Ventajas:
        - Personalización basada en tu historial
        - Descubre productos que otros usuarios similares disfrutaron
        - Mejora continuamente con más datos
        """)

def get_user_history(user_id, interactions_df, products_df):
    """
    Obtiene el historial de compras de un usuario
    """
    user_purchases = interactions_df[interactions_df['user_id'] == user_id]
    
    if len(user_purchases) > 0:
        user_purchases = user_purchases.merge(
            products_df[['product_id', 'product_name', 'category']],
            on='product_id',
            how='left',
            suffixes=('', '_prod')
        )
    
    return user_purchases

def display_user_stats(user_id, user_stats_df, interactions_df):
    """
    Muestra estadísticas del usuario
    """
    st.markdown("### 📊 Tu Perfil de Compras")
    
    user_info = user_stats_df[user_stats_df['user_id'] == user_id]
    
    if len(user_info) > 0:
        user_info = user_info.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🛍️ Compras Realizadas", int(user_info['num_interactions']))
        
        with col2:
            st.metric("⭐ Rating Promedio", f"{user_info['avg_rating']:.2f}")
        
        with col3:
            st.metric("📦 Productos Totales", int(user_info['total_purchases']))
        
        with col4:
            st.metric("💰 Total Gastado", f"${user_info['total_spent']:.2f}")
        
        # Categorías favoritas
        user_purchases = interactions_df[interactions_df['user_id'] == user_id]
        if len(user_purchases) > 0:
            category_counts = user_purchases['category'].value_counts()
            
            st.markdown("#### 🏷️ Tus Categorías Favoritas")
            
            fig = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                labels={'x': 'Número de compras', 'y': 'Categoría'},
                color=category_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Usuario nuevo sin historial previo")

def display_recommendations(recommendations):
    """
    Muestra las recomendaciones de forma visual
    """
    st.markdown("### 🎯 Productos Recomendados Para Ti")
    
    if len(recommendations) == 0:
        st.warning("No se encontraron recomendaciones disponibles.")
        return
    
    # Mostrar en tarjetas
    for i in range(0, len(recommendations), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                rec = recommendations.iloc[i + j]
                
                with col:
                    # Tarjeta de producto
                    rating_stars = "⭐" * int(rec['predicted_rating'])
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem;
                        border-radius: 10px;
                        color: white;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    ">
                        <div>
                            <h4 style="margin: 0; color: white;">#{i+j+1} {rec['product_name']}</h4>
                            <p style="margin: 0.5rem 0; opacity: 0.9;">🏷️ {rec['category']}</p>
                        </div>
                        <div>
                            <p style="margin: 0.5rem 0; font-size: 1.2rem;">{rating_stars}</p>
                            <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                                Rating estimado: {rec['predicted_rating']:.2f}/5
                            </p>
                            <p style="margin: 0.5rem 0; font-size: 1.3rem; font-weight: bold;">
                                💰 ${rec['price']:.2f}
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Tabla detallada
    with st.expander("📋 Ver tabla detallada"):
        display_df = recommendations.copy()
        display_df['predicted_rating'] = display_df['predicted_rating'].round(2)
        display_df['price'] = display_df['price'].round(2)
        display_df = display_df.rename(columns={
            'product_name': 'Producto',
            'category': 'Categoría',
            'predicted_rating': 'Rating Estimado',
            'price': 'Precio ($)'
        })
        st.dataframe(
            display_df[['Producto', 'Categoría', 'Rating Estimado', 'Precio ($)']],
            use_container_width=True
        )

def display_category_filter(model, user_id, products_df, interactions_df, selected_category):
    """
    Muestra recomendaciones filtradas por categoría
    """
    st.markdown("### 🔍 Explorar por Categoría")
    
    # Filtrar productos por categoría
    category_products = products_df[products_df['category'] == selected_category]
    
    # Obtener productos ya comprados
    user_purchases = get_user_history(user_id, interactions_df, products_df)
    purchased_ids = user_purchases['product_id'].tolist() if len(user_purchases) > 0 else []
    
    # Obtener recomendaciones
    recommendations = model.recommend_products(
        user_id=user_id,
        products_df=category_products,
        top_n=6,
        exclude_purchased=purchased_ids
    )
    
    if len(recommendations) > 0:
        st.success(f"✨ Encontramos {len(recommendations)} productos de **{selected_category}** para ti")
        display_recommendations(recommendations)
    else:
        st.info(f"No hay más productos de {selected_category} para recomendar en este momento.")

def main():
    """
    Función principal de la aplicación
    """
    
    # Cargar recursos
    model, interactions, products, user_stats = load_model_and_data()
    
    if model is None:
        st.stop()
    
    # Encabezado
    display_header()
    
    # Explicación del sistema
    display_how_it_works()
    
    st.markdown("---")
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Selector de usuario
        st.subheader("👤 Selecciona tu Usuario")
        
        user_ids = sorted(interactions['user_id'].unique())
        user_id = st.selectbox(
            "ID de Usuario",
            options=user_ids,
            index=0,
            help="Selecciona tu ID de usuario para obtener recomendaciones personalizadas"
        )
        
        # Número de recomendaciones
        n_recommendations = st.slider(
            "📊 Cantidad de recomendaciones",
            min_value=3,
            max_value=15,
            value=9,
            step=3
        )
        
        # Filtro de categoría
        st.subheader("🏷️ Filtrar por Categoría")
        categories = ['Todas'] + sorted(products['category'].unique().tolist())
        selected_category = st.selectbox(
            "Categoría",
            options=categories,
            index=0
        )
        
        st.markdown("---")
        
        # Información del modelo
        st.subheader("📈 Info del Modelo")
        st.info(f"""
        **Usuarios**: {model.n_users}  
        **Productos**: {model.n_products}  
        **Embedding**: {model.embedding_dim}D  
        **Interacciones**: {len(interactions)}
        """)
    
    # Contenido principal
    tab1, tab2, tab3 = st.tabs(["🎯 Recomendaciones", "📊 Mi Perfil", "📜 Historial"])
    
    with tab1:
        # Mostrar estadísticas rápidas
        display_user_stats(user_id, user_stats, interactions)
        
        st.markdown("---")
        
        # Obtener historial del usuario
        user_purchases = get_user_history(user_id, interactions, products)
        purchased_ids = user_purchases['product_id'].tolist() if len(user_purchases) > 0 else []
        
        # Filtrar por categoría si se seleccionó
        if selected_category != 'Todas':
            display_category_filter(model, user_id, products, interactions, selected_category)
        else:
            # Generar recomendaciones
            with st.spinner('🤖 Generando recomendaciones personalizadas...'):
                recommendations = model.recommend_products(
                    user_id=user_id,
                    products_df=products,
                    top_n=n_recommendations,
                    exclude_purchased=purchased_ids
                )
            
            if len(recommendations) > 0:
                st.success(f"✨ Hemos encontrado {len(recommendations)} productos perfectos para ti")
                display_recommendations(recommendations)
            else:
                st.warning("No se pudieron generar recomendaciones en este momento.")
    
    with tab2:
        st.markdown("## 👤 Análisis de tu Perfil")
        
        user_purchases = get_user_history(user_id, interactions, products)
        
        if len(user_purchases) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribución de ratings
                st.markdown("#### ⭐ Distribución de tus Ratings")
                rating_dist = user_purchases['rating'].value_counts().sort_index()
                
                fig = px.bar(
                    x=rating_dist.index,
                    y=rating_dist.values,
                    labels={'x': 'Rating', 'y': 'Cantidad'},
                    color=rating_dist.values,
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gasto por categoría
                st.markdown("#### 💰 Gasto por Categoría")
                category_spending = user_purchases.groupby('category')['total_spent'].sum().sort_values(ascending=False)
                
                fig = px.pie(
                    values=category_spending.values,
                    names=category_spending.index,
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Evolución temporal
            st.markdown("#### 📅 Evolución de Compras")
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
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👋 ¡Bienvenido! Aún no tienes historial de compras.")
    
    with tab3:
        st.markdown("## 📜 Tu Historial de Compras")
        
        user_purchases = get_user_history(user_id, interactions, products)
        
        if len(user_purchases) > 0:
            # Ordenar por fecha
            user_purchases_sorted = user_purchases.sort_values('purchase_date', ascending=False)
            
            # Mostrar estadística
            st.info(f"📦 Total de productos comprados: **{len(user_purchases_sorted)}**")
            
            # Tabla con historial
            display_history = user_purchases_sorted[[
                'purchase_date', 'product_name', 'category', 'rating', 
                'purchase_count', 'total_spent'
            ]].copy()
            
            display_history = display_history.rename(columns={
                'purchase_date': 'Fecha',
                'product_name': 'Producto',
                'category': 'Categoría',
                'rating': 'Rating',
                'purchase_count': 'Cantidad',
                'total_spent': 'Total ($)'
            })
            
            st.dataframe(display_history, use_container_width=True, height=400)
            
            # Descargar CSV
            csv = display_history.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Historial (CSV)",
                data=csv,
                file_name=f"historial_usuario_{user_id}.csv",
                mime="text/csv"
            )
        else:
            st.info("No tienes compras registradas aún.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>🤖 Sistema de Recomendación con IA | Desarrollado con TensorFlow + Streamlit</p>
        <p>📚 Proyecto de Inteligencia Artificial Aplicada al Comercio Electrónico</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
