"""
Sistema de Carrito de Compras
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from config.settings import GRADIENTS
from src.utils import format_currency, get_rating_stars
from app.components.balance import get_user_balance, deduct_balance
from app.components.purchases import save_purchase


# ============================================================================
# FUNCIONES DE GESTIÓN DEL CARRITO
# ============================================================================

def initialize_cart():
    """Inicializa el carrito en session state"""
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []


def add_to_cart(product):
    """
    Añade un producto al carrito
    
    Args:
        product: Diccionario con datos del producto
        
    Returns:
        tuple: (success, message)
    """
    initialize_cart()
    
    # Verificar si el producto ya está en el carrito
    for item in st.session_state['cart']:
        if item['product_id'] == product['product_id']:
            item['quantity'] += 1
            return True, f"✅ Cantidad actualizada: {item['quantity']} unidad(es)"
    
    # Agregar nuevo producto
    cart_item = {
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'category': product['category'],
        'price': product['price'],
        'predicted_rating': product.get('predicted_rating', 5.0),
        'quantity': 1
    }
    
    st.session_state['cart'].append(cart_item)
    return True, f"✅ '{product['product_name']}' añadido al carrito"


def remove_from_cart(product_id):
    """Elimina un producto del carrito"""
    initialize_cart()
    st.session_state['cart'] = [
        item for item in st.session_state['cart'] 
        if item['product_id'] != product_id
    ]


def update_cart_quantity(product_id, quantity):
    """Actualiza la cantidad de un producto en el carrito"""
    initialize_cart()
    for item in st.session_state['cart']:
        if item['product_id'] == product_id:
            if quantity <= 0:
                remove_from_cart(product_id)
            else:
                item['quantity'] = quantity
            break


def clear_cart():
    """Vacía el carrito"""
    st.session_state['cart'] = []


def get_cart_total():
    """Calcula el total del carrito"""
    initialize_cart()
    total = sum(item['price'] * item['quantity'] for item in st.session_state['cart'])
    return total


def get_cart_count():
    """Obtiene la cantidad total de items en el carrito"""
    initialize_cart()
    return sum(item['quantity'] for item in st.session_state['cart'])


# ============================================================================
# COMPONENTES VISUALES DEL CARRITO
# ============================================================================

def show_cart_badge():
    """Muestra badge con cantidad de items en el carrito"""
    count = get_cart_count()
    if count > 0:
        return f"🛒 Carrito ({count})"
    return "🛒 Carrito"


def show_cart_item(item, index):
    """
    Muestra un item del carrito con controles de cantidad y eliminación
    
    Args:
        item: Diccionario con datos del producto
        index: Índice del item
    """
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 2px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    ">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="padding: 0.5rem 0;">
            <h4 style="margin: 0; color: #1f2937; font-size: 1.1rem;">{item['product_name']}</h4>
            <p style="margin: 0.3rem 0; color: #6b7280; font-size: 0.9rem;">
                🏷️ {item['category']}
            </p>
            <p style="margin: 0.2rem 0; color: #9ca3af; font-size: 0.85rem;">
                {get_rating_stars(item['predicted_rating'])} {item['predicted_rating']:.1f}/5
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="padding: 1rem 0; text-align: center;">
            <p style="margin: 0; font-size: 1.2rem; color: #667eea; font-weight: 700;">
                {format_currency(item['price'])}
            </p>
            <p style="margin: 0.2rem 0; color: #9ca3af; font-size: 0.85rem;">
                precio unitario
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Control de cantidad
        col_minus, col_qty, col_plus = st.columns([1, 2, 1])
        
        with col_minus:
            if st.button("➖", key=f"minus_{item['product_id']}_{index}", 
                        help="Reducir cantidad"):
                new_qty = max(1, item['quantity'] - 1)
                update_cart_quantity(item['product_id'], new_qty)
                st.rerun()
        
        with col_qty:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem 0;">
                <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #1f2937;">
                    {item['quantity']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_plus:
            if st.button("➕", key=f"plus_{item['product_id']}_{index}", 
                        help="Aumentar cantidad"):
                update_cart_quantity(item['product_id'], item['quantity'] + 1)
                st.rerun()
        
        # Subtotal
        subtotal = item['price'] * item['quantity']
        st.markdown(f"""
        <div style="text-align: center; margin-top: 0.5rem;">
            <p style="margin: 0; font-weight: 700; color: #059669; font-size: 1.15rem;">
                {format_currency(subtotal)}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div style='padding: 1rem 0;'></div>", unsafe_allow_html=True)
        if st.button("🗑️", key=f"remove_{item['product_id']}_{index}", 
                     help="Eliminar del carrito", use_container_width=True,
                     type="secondary"):
            remove_from_cart(item['product_id'])
            st.toast(f"'{item['product_name']}' eliminado del carrito", icon="🗑️")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def show_cart_summary(user_balance):
    """
    Muestra resumen del carrito con detalles de pago
    
    Args:
        user_balance: Saldo disponible del usuario
        
    Returns:
        float: Total del carrito
    """
    cart_total = get_cart_total()
    cart_count = get_cart_count()
    
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        border: 3px solid #667eea;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
    ">
        <h3 style="margin: 0 0 1.2rem 0; color: #1f2937; font-size: 1.4rem;">
            📊 Resumen de Compra
        </h3>
        
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.6rem 0;">
                <span style="color: #6b7280;">Productos:</span>
                <strong style="color: #1f2937;">{cart_count} item(s)</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.6rem 0;">
                <span style="color: #6b7280;">Subtotal:</span>
                <strong style="color: #1f2937;">{format_currency(cart_total)}</strong>
            </div>
        </div>
        
        <hr style="margin: 1.2rem 0; border: none; border-top: 2px solid #e5e7eb;">
        
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.8rem 0;">
                <span style="font-size: 1.2rem; color: #1f2937; font-weight: 600;">Total a pagar:</span>
                <strong style="font-size: 1.4rem; color: #667eea;">{format_currency(cart_total)}</strong>
            </div>
        </div>
        
        <hr style="margin: 1.2rem 0; border: none; border-top: 2px solid #e5e7eb;">
        
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <div style="display: flex; justify-content: space-between; margin: 0.4rem 0;">
                <span style="color: white; opacity: 0.9;">Tu saldo actual:</span>
                <strong style="color: white; font-size: 1.1rem;">{format_currency(user_balance)}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 0.4rem 0;">
                <span style="color: white; opacity: 0.9;">Saldo después:</span>
                <strong style="color: white; font-size: 1.2rem;">
                    {format_currency(user_balance - cart_total)}
                </strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return cart_total


def process_cart_checkout(user_id, user_balance):
    """
    Procesa la compra del carrito completo
    
    Args:
        user_id: ID del usuario
        user_balance: Saldo disponible
        
    Returns:
        tuple: (success, message, new_balance)
    """
    initialize_cart()
    cart = st.session_state['cart']
    
    if len(cart) == 0:
        return False, "❌ El carrito está vacío", user_balance
    
    cart_total = get_cart_total()
    
    # Verificar saldo
    if user_balance < cart_total:
        deficit = cart_total - user_balance
        return False, f"❌ Saldo insuficiente. Te faltan {format_currency(deficit)}", user_balance
    
    # Descontar saldo
    success, new_balance, message = deduct_balance(user_id, cart_total)
    
    if not success:
        return False, message, user_balance
    
    # Procesar cada producto del carrito
    failed_items = []
    success_count = 0
    
    for item in cart:
        purchase_success, purchase_message = save_purchase(
            user_id,
            item['product_id'],
            item['product_name'],
            item['category'],
            item['price'],
            item['quantity']
        )
        
        if purchase_success:
            success_count += 1
        else:
            failed_items.append(item['product_name'])
    
    # Limpiar carrito si todo fue exitoso
    if success_count == len(cart):
        clear_cart()
        return True, f"🎉 ¡Compra exitosa! {success_count} producto(s) por {format_currency(cart_total)}. Saldo: {format_currency(new_balance)}", new_balance
    elif success_count > 0:
        clear_cart()
        return True, f"⚠️ Compra parcial: {success_count} de {len(cart)} productos. Saldo: {format_currency(new_balance)}", new_balance
    else:
        return False, f"❌ Error al procesar la compra. Tu saldo no se descontó.", new_balance


# ============================================================================
# VISTA PRINCIPAL DEL CARRITO
# ============================================================================

def show_cart_view(user_id, user_balance):
    """
    Muestra la vista completa del carrito con opciones de gestión
    
    Args:
        user_id: ID del usuario
        user_balance: Saldo disponible
    """
    initialize_cart()
    cart = st.session_state['cart']
    
    # Header del carrito
    st.markdown(f"""
    <div style="
        background: {GRADIENTS['success']};
        padding: 1.8rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    ">
        <h2 style="color: white; margin: 0; font-weight: 800; font-size: 1.8rem;">
            🛒 Mi Carrito de Compras
        </h2>
        <p style="color: rgba(255,255,255,0.95); margin: 0.5rem 0 0 0; font-size: 1.15rem;">
            {get_cart_count()} producto(s) | Total: {format_currency(get_cart_total())}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carrito vacío
    if len(cart) == 0:
        st.info("🛒 Tu carrito está vacío")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 2rem 0;
        ">
            <h2 style="color: white; margin: 0 0 1rem 0; font-size: 2rem;">
                🎁 ¡Descubre productos increíbles!
            </h2>
            <p style="margin: 0; opacity: 0.95; font-size: 1.1rem;">
                Ve a la pestaña <strong>🎯 Tienda</strong> para añadir productos a tu carrito
            </p>
            <p style="margin: 1rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                💡 Añade productos al carrito y compra todo junto cuando estés listo
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Layout principal: Productos + Resumen
    col_left, col_right = st.columns([2.5, 1.5])
    
    with col_left:
        st.markdown("### 📦 Productos en tu Carrito")
        
        # Mostrar items del carrito
        for index, item in enumerate(cart):
            show_cart_item(item, index)
        
        # Botones de acción
        st.markdown("<br>", unsafe_allow_html=True)
        col_clear, col_continue = st.columns(2)
        
        with col_clear:
            if st.button("🗑️ Vaciar Carrito", type="secondary", use_container_width=True):
                clear_cart()
                st.toast("Carrito vaciado", icon="🗑️")
                st.rerun()
        
        with col_continue:
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem; color: #6b7280;">
                <small>👈 Continúa editando o procede al pago →</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("### 💳 Checkout")
        
        # Resumen del carrito
        cart_total = show_cart_summary(user_balance)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Verificar saldo
        insufficient_balance = user_balance < cart_total
        
        if insufficient_balance:
            deficit = cart_total - user_balance
            st.error(f"❌ Saldo insuficiente")
            st.warning(f"Te faltan {format_currency(deficit)}")
        else:
            st.success("✅ Saldo suficiente")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de compra
        if st.button(
            "💳 Procesar Compra Completa", 
            use_container_width=True, 
            type="primary",
            disabled=insufficient_balance,
            help="Comprar todos los productos del carrito"
        ):
            with st.spinner("Procesando compra..."):
                success, message, new_balance = process_cart_checkout(user_id, user_balance)
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)
