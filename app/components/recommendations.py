"""
Componentes para mostrar recomendaciones de productos
"""
import streamlit as st
import pandas as pd
from config.settings import GRADIENTS
from src.utils import get_rating_stars, format_currency


def display_product_card(rec, index, show_buy_button=False, show_cart_button=False, 
                        on_buy_click=None, on_add_to_cart=None):
    """
    Muestra una tarjeta de producto individual con botones
    """
    rating_stars = get_rating_stars(rec['predicted_rating'])
    
    # INFO DEL PRODUCTO
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #1f2937; font-size: 1.05rem;">
            #{index + 1} {rec['product_name']}
        </h4>
        <p style="margin: 0.3rem 0; color: #667eea; font-weight: 600; font-size: 0.9rem;">
            🏷️ {rec['category']}
        </p>
        <p style="margin: 0.4rem 0; font-size: 1.1rem;">
            {rating_stars}
        </p>
        <p style="margin: 0.2rem 0; font-size: 0.85rem; color: #6b7280;">
            Rating: {rec['predicted_rating']:.2f}/5.0
        </p>
        <p style="margin: 0.6rem 0 0.2rem 0; font-size: 1.4rem; color: #059669; font-weight: 700;">
            {format_currency(rec['price'])}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # BOTONES - SIEMPRE MOSTRAR PARA DEBUG
    col1, col2 = st.columns(2)
    
    with col1:
        buy_clicked = st.button(
            "💳 Comprar", 
            key=f"buy_{rec['product_id']}_{index}",
            use_container_width=True,
            type="primary"
        )
        if buy_clicked and on_buy_click:
            on_buy_click(rec)
    
    with col2:
        cart_clicked = st.button(
            "🛒 Carrito", 
            key=f"cart_{rec['product_id']}_{index}",
            use_container_width=True,
            type="secondary"
        )
        if cart_clicked and on_add_to_cart:
            on_add_to_cart(rec)
    
    st.markdown("<br>", unsafe_allow_html=True)


def display_recommendations_grid(recommendations, show_buy_button=True, 
                                show_cart_button=True, on_buy_click=None, 
                                on_add_to_cart=None):
    """
    Muestra recomendaciones en grid de 3 columnas
    """
    if len(recommendations) == 0:
        st.warning("⚠️ No hay productos disponibles")
        return
    
    # Grid de 3 columnas
    for i in range(0, len(recommendations), 3):
        cols = st.columns(3, gap="medium")
        
        for j, col in enumerate(cols):
            if i + j < len(recommendations):
                rec = recommendations.iloc[i + j]
                
                with col:
                    display_product_card(
                        rec, 
                        i + j, 
                        show_buy_button=show_buy_button,
                        show_cart_button=show_cart_button,
                        on_buy_click=on_buy_click,
                        on_add_to_cart=on_add_to_cart
                    )


def display_recommendations_table(recommendations):
    """Muestra tabla detallada de recomendaciones"""
    with st.expander("📋 Ver tabla detallada de productos", expanded=False):
        display_df = recommendations.copy()
        display_df['predicted_rating'] = display_df['predicted_rating'].round(2)
        display_df['price'] = display_df['price'].apply(format_currency)
        
        display_df = display_df.rename(columns={
            'product_name': 'Producto',
            'category': 'Categoría',
            'predicted_rating': 'Rating Estimado',
            'price': 'Precio'
        })
        
        st.dataframe(
            display_df[['Producto', 'Categoría', 'Rating Estimado', 'Precio']],
            use_container_width=True,
            height=400
        )


def show_purchase_modal(product, user_balance):
    """
    Muestra modal para confirmar compra directa
    """
    st.markdown("---")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    ">
        <h2 style="margin: 0 0 1rem 0; color: white;">💳 Compra Directa</h2>
        <h3 style="margin: 0; color: white;">{product['product_name']}</h3>
        <p style="margin: 0.5rem 0; opacity: 0.9;">Categoría: {product['category']}</p>
        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">
            Precio: {format_currency(product['price'])}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    quantity = st.number_input(
        "Cantidad a comprar:",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        key="modal_quantity"
    )
    
    total_price = product['price'] * quantity
    
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
    ">
        <h4 style="margin: 0 0 1rem 0; color: #1f2937;">📊 Resumen de Compra</h4>
        <p style="margin: 0.5rem 0; font-size: 1.1rem;">
            <strong>Precio unitario:</strong> {format_currency(product['price'])}
        </p>
        <p style="margin: 0.5rem 0; font-size: 1.1rem;">
            <strong>Cantidad:</strong> {quantity}
        </p>
        <p style="margin: 0.5rem 0; font-size: 1.3rem; color: #667eea;">
            <strong>Total a pagar:</strong> {format_currency(total_price)}
        </p>
        <hr style="margin: 1rem 0; border: none; border-top: 2px solid #e5e7eb;">
        <p style="margin: 0.5rem 0; font-size: 1.1rem;">
            <strong>Saldo actual:</strong> {format_currency(user_balance)}
        </p>
        <p style="margin: 0.5rem 0; font-size: 1.1rem; color: {'#059669' if user_balance >= total_price else '#dc2626'};">
            <strong>Saldo después:</strong> {format_currency(user_balance - total_price)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    insufficient = total_price > user_balance
    
    if insufficient:
        st.error(f"❌ Saldo insuficiente. Te faltan {format_currency(total_price - user_balance)}")
    else:
        st.success(f"✅ Saldo suficiente para realizar la compra")
    
    st.markdown("---")
    
    col_confirm, col_cancel = st.columns(2)
    
    with col_confirm:
        confirmed = st.button(
            "✅ Confirmar Compra", 
            use_container_width=True, 
            type="primary",
            key="confirm_purchase",
            disabled=insufficient
        )
    
    with col_cancel:
        cancelled = st.button(
            "❌ Cancelar", 
            use_container_width=True,
            key="cancel_purchase"
        )
    
    return quantity, confirmed, cancelled
