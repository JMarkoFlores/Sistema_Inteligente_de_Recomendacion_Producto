"""
Componente de historial de compras
"""
import streamlit as st
import pandas as pd
from src.utils import format_currency

def show_purchase_history(user_id, user_purchases):
    """
    Muestra el historial de compras del usuario
    
    Args:
        user_id: ID del usuario
        user_purchases: DataFrame con historial de compras
    """
    st.markdown("## 📜 Tu Historial de Compras")
    
    if len(user_purchases) > 0:
        # Ordenar por fecha
        user_purchases_sorted = user_purchases.sort_values('purchase_date', ascending=False)
        
        # Estadísticas rápidas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📦 Total de Compras",
                len(user_purchases_sorted)
            )
        
        with col2:
            st.metric(
                "💰 Gasto Total",
                format_currency(user_purchases_sorted['total_spent'].sum())
            )
        
        with col3:
            st.metric(
                "⭐ Rating Promedio",
                f"{user_purchases_sorted['rating'].mean():.2f}"
            )
        
        st.markdown("---")
        
        # Tabla de historial
        display_history = user_purchases_sorted[[
            'purchase_date', 'product_name', 'category', 'rating', 
            'purchase_count', 'total_spent'
        ]].copy()
        
        display_history['total_spent'] = display_history['total_spent'].apply(format_currency)
        
        display_history = display_history.rename(columns={
            'purchase_date': 'Fecha',
            'product_name': 'Producto',
            'category': 'Categoría',
            'rating': 'Rating',
            'purchase_count': 'Cantidad',
            'total_spent': 'Total'
        })
        
        st.dataframe(
            display_history,
            use_container_width=True,
            height=500
        )
        
        # Botón de descarga
        csv = display_history.to_csv(index=False)
        st.download_button(
            label="📥 Descargar Historial Completo (CSV)",
            data=csv,
            file_name=f"historial_usuario_{user_id}.csv",
            mime="text/csv",
            type="primary"
        )
        
    else:
        st.info("📭 No tienes compras registradas aún.")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        ">
            <h3 style="color: white; margin: 0 0 1rem 0;">🎁 ¡Descubre productos increíbles!</h3>
            <p style="margin: 0; opacity: 0.9;">
                Ve a la pestaña de Recomendaciones para encontrar productos 
                perfectos para ti, seleccionados por nuestra IA.
            </p>
        </div>
        """, unsafe_allow_html=True)