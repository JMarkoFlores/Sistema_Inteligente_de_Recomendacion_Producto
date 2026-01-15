import streamlit as st
import pandas as pd
from src.model import ProductRecommendationANN
from src.utils import generate_user_names, load_data
from app.components.auth import show_login
from app.components.styles import get_custom_css
from app.components.recommendations import (
    display_recommendations_grid, 
    display_recommendations_table,
    show_purchase_modal
)
from app.components.balance import get_user_balance, deduct_balance
from app.components.profile import show_profile_view
from app.components.history import show_purchase_history
from app.components.balance import get_user_balance
from app.components.purchases import save_purchase
from app.components.dashboard import show_global_dashboard
from app.components.cart import (
    add_to_cart,
    show_cart_view,
    show_cart_badge,
    get_cart_count
)
from config.settings import APP_CONFIG, MODEL_CONFIG, GRADIENTS

# Configuración de la página
st.set_page_config(
    page_title=APP_CONFIG['page_title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
)

# Aplicar estilos CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA
# ============================================================================

@st.cache_resource
def load_model():
    """Carga el modelo de recomendación"""
    try:
        model = ProductRecommendationANN(n_users=1, n_products=1)
        model.load_model(MODEL_CONFIG['model_path'])
        return model
    except Exception as e:
        st.error(f"❌ Error al cargar modelo: {e}")
        st.info("💡 Ejecuta: `python scripts/train_model.py`")
        return None

def get_user_history(user_id, interactions, products):
    """Obtiene el historial de compras de un usuario"""
    user_purchases = interactions[interactions['user_id'] == user_id]
    
    if len(user_purchases) > 0:
        user_purchases = user_purchases.merge(
            products[['product_id', 'product_name', 'category']],
            on='product_id',
            how='left',
            suffixes=('', '_prod')
        )
    
    return user_purchases

# ============================================================================
# VISTA DE CLIENTE
# ============================================================================

def show_client_view():
    """Vista principal para clientes con tienda virtual completa"""
    from app.components.cart import initialize_cart
    initialize_cart()
    
    user_id = st.session_state['user_id']
    user_name = st.session_state['user_name']
    
    # Inicializar estado del modal
    if 'selected_product' not in st.session_state:
        st.session_state['selected_product'] = None
    
    # Cargar datos y modelo
    model = load_model()
    interactions, products, user_stats = load_data()
    
    if model is None or interactions is None:
        st.stop()
    
    # Header con información del usuario
    current_balance = get_user_balance(user_id)
    cart_count = get_cart_count()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {GRADIENTS['primary']};
            padding: 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        ">
            <h2 style="color: white; margin: 0; font-weight: 800;">
                🛒 Bienvenido, {user_name}
            </h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                💰 Saldo: ${current_balance:,.2f} | 🛒 Carrito: {cart_count} item(s) | ID: {user_id}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Salir", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Tienda", 
        show_cart_badge(),
        "👤 Mi Perfil", 
        "📜 Historial"
    ])
    
    # TAB 1: TIENDA
    with tab1:
        st.markdown("### 🎁 Productos Recomendados Para Ti")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info("💳 **Comprar**: Pago inmediato con descuento de saldo")
        with col_info2:
            st.info("🛒 **Carrito**: Añade productos y compra después")
        
        st.markdown("---")
        
        # Sidebar - Filtros
        with st.sidebar:
            st.markdown("### ⚙️ Configuración")
            
            n_recommendations = st.slider(
                "📊 Cantidad de productos",
                min_value=6,
                max_value=18,
                value=12,
                step=3
            )
            
            st.markdown("### 🏷️ Filtrar por Categoría")
            categories = ['Todas'] + sorted(products['category'].unique().tolist())
            selected_category = st.selectbox(
                "Categoría",
                options=categories,
                index=0
            )
        
        # Obtener productos ya comprados
        user_purchases = get_user_history(user_id, interactions, products)
        purchased_ids = user_purchases['product_id'].tolist() if len(user_purchases) > 0 else []
        
        # Filtrar por categoría
        if selected_category != 'Todas':
            products_filtered = products[products['category'] == selected_category]
        else:
            products_filtered = products
        
        # Generar recomendaciones
        with st.spinner('🤖 Generando recomendaciones personalizadas...'):
            recommendations = model.recommend_products(
                user_id=user_id,
                products_df=products_filtered,
                top_n=n_recommendations,
                exclude_purchased=purchased_ids
            )
        
        if len(recommendations) > 0:
            st.success(f"✨ Encontramos {len(recommendations)} productos perfectos para ti")
            
            # Callback para compra directa
            def handle_buy_click(product):
                st.session_state['selected_product'] = {
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'category': product['category'],
                    'price': product['price']
                }
            
            # Callback para añadir al carrito
            def handle_add_to_cart(product):
                success, message = add_to_cart({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'category': product['category'],
                    'price': product['price'],
                    'predicted_rating': product['predicted_rating']
                })
                if success:
                    st.toast(message, icon="✅")
                    st.rerun()
                else:
                    st.error(message)
            
            # Mostrar productos
            display_recommendations_grid(
                recommendations,
                show_buy_button=True,
                show_cart_button=True,
                on_buy_click=handle_buy_click,
                on_add_to_cart=handle_add_to_cart
            )
            
            # Tabla detallada
            display_recommendations_table(recommendations)
        else:
            st.warning("⚠️ No hay productos disponibles en este momento.")
        
        # Modal de compra directa
        if st.session_state.get('selected_product'):
            product = st.session_state['selected_product']
            quantity, confirmed, cancelled = show_purchase_modal(product, current_balance)
            
            if confirmed:
                # Usar save_purchase directamente (que ya maneja el descuento)
                success, message = save_purchase(
                    user_id,
                    product['product_id'],
                    product['product_name'],
                    product['category'],
                    product['price'],
                    quantity
                )
                
                if success:
                    st.success(f"🎉 {message}")
                    st.balloons()
                    st.session_state['selected_product'] = None
                    st.rerun()
                else:
                    st.error(message)
            
            if cancelled:
                st.session_state['selected_product'] = None
                st.rerun()
    
    # TAB 2: CARRITO
    with tab2:
        show_cart_view(user_id, current_balance)
    
    # TAB 3: PERFIL
    with tab3:
        user_purchases = get_user_history(user_id, interactions, products)
        show_profile_view(user_id, user_stats, user_purchases)
    
    # TAB 4: HISTORIAL
    with tab4:
        user_purchases = get_user_history(user_id, interactions, products)
        show_purchase_history(user_id, user_purchases)

# ============================================================================
# VISTA DE DIRECTOR (SIN CAMBIOS)
# ============================================================================

def show_director_view():
    """Vista de dashboard para el director"""
    
    # Cargar datos y modelo
    model = load_model()
    interactions, products, user_stats = load_data()
    
    if model is None or interactions is None:
        st.stop()
    
    # Header con botón integrado
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {GRADIENTS['primary']};
            padding: 1.2rem 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        ">
            <h1 style="color: white; margin: 0; font-weight: 800; font-size: 1.8rem;">
                📊 Dashboard del Director
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 0.3rem 0 0 0; font-size: 0.95rem;">
                Sistema de Gestión y Análisis de Recomendaciones IA
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Salir", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar - Análisis de Usuario
    with st.sidebar:
        st.markdown("### 👤 Análisis Individual")
        
        user_ids = sorted(interactions['user_id'].unique())
        user_names = generate_user_names(user_ids)
        
        user_options = {f"{user_names[uid]} (ID: {uid})": uid for uid in user_ids}
        
        selected_user = st.selectbox(
            "Seleccionar usuario",
            options=list(user_options.keys()),
            index=0
        )
        
        user_id = user_options[selected_user]
        user_name = user_names[user_id]
        
        st.markdown("---")
        
        n_recommendations = st.slider(
            "📊 Recomendaciones",
            min_value=6,
            max_value=18,
            value=9,
            step=3
        )
        
        categories = ['Todas'] + sorted(products['category'].unique().tolist())
        selected_category = st.selectbox("🏷️ Categoría", options=categories)
        
        st.markdown("---")
        
        st.markdown("### 📈 Info del Sistema")
        st.info(f"""
        **Usuarios**: {len(user_ids)}  
        **Productos**: {len(products)}  
        **Transacciones**: {len(interactions)}  
        **Categorías**: {len(products['category'].unique())}
        """)
    
    # Usuario seleccionado
    st.markdown(f"""
    <div style="
        background: {GRADIENTS['info']};
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    ">
        <h3 style="color: white; margin: 0;">👤 Usuario Seleccionado</h3>
        <h2 style="color: white; margin: 0.5rem 0 0 0; font-weight: 800;">{user_name}</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0.3rem 0 0 0; font-size: 1.1rem;">
            ID: {user_id}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Recomendaciones", 
        "👤 Perfil Usuario", 
        "📜 Historial", 
        "🌍 Dashboard Global"
    ])
    
    # TAB 1: RECOMENDACIONES
    with tab1:
        st.markdown("### 🎁 Recomendaciones para Usuario Seleccionado")
        
        user_purchases = get_user_history(user_id, interactions, products)
        purchased_ids = user_purchases['product_id'].tolist() if len(user_purchases) > 0 else []
        
        if selected_category != 'Todas':
            products_filtered = products[products['category'] == selected_category]
        else:
            products_filtered = products
        
        recommendations = model.recommend_products(
            user_id=user_id,
            products_df=products_filtered,
            top_n=n_recommendations,
            exclude_purchased=purchased_ids
        )
        
        if len(recommendations) > 0:
            display_recommendations_grid(recommendations)
            display_recommendations_table(recommendations)
        else:
            st.warning("No hay recomendaciones disponibles")
    
    # TAB 2: PERFIL
    with tab2:
        user_purchases = get_user_history(user_id, interactions, products)
        show_profile_view(user_id, user_stats, user_purchases)
    
    # TAB 3: HISTORIAL
    with tab3:
        user_purchases = get_user_history(user_id, interactions, products)
        show_purchase_history(user_id, user_purchases)
    
    # TAB 4: DASHBOARD GLOBAL
    with tab4:
        show_global_dashboard(interactions, products, user_stats)

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Punto de entrada de la aplicación"""
    
    # Inicializar session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    # Mostrar vista según autenticación
    if not st.session_state['authenticated']:
        show_login()
    else:
        if st.session_state['role'] == 'director':
            show_director_view()
        else:
            show_client_view()
    
    # Footer
    if st.session_state.get('authenticated'):
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6b7280; padding: 2rem 0;">
            <p style="margin: 0;">🤖 Sistema de Recomendación con IA</p>
            <p style="margin: 0.5rem 0;">Desarrollado con TensorFlow + Streamlit</p>
            <p style="margin: 0; font-size: 0.9rem;">
                💡 Powered by Deep Learning & Neural Networks
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()