"""
Sistema de Tienda Virtual con Recomendaciones IA
Con autenticación y roles (Director / Cliente)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from model import ProductRecommendationANN
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Tienda Virtual IA",
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
    div[data-testid="column"] {
        padding: 0 0.75rem !important;
    }
    .element-container {
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE DATOS Y AUTENTICACIÓN
# ============================================================================

@st.cache_data
def generate_user_names(user_ids):
    """Genera nombres de usuario consistentes basados en IDs"""
    nombres = [
        "Juan", "María", "Carlos", "Ana", "Pedro", "Laura", "Miguel", "Carmen", "José", "Isabel",
        "Francisco", "Lucía", "Antonio", "Marta", "Manuel", "Elena", "David", "Patricia", "Javier", "Rosa",
        "Daniel", "Sofía", "Rafael", "Andrea", "Sergio", "Paula", "Jorge", "Beatriz", "Luis", "Clara",
        "Fernando", "Raquel", "Alberto", "Cristina", "Roberto", "Silvia", "Enrique", "Natalia", "Ricardo", "Teresa",
        "Pablo", "Mónica", "Ángel", "Diana", "Alejandro", "Victoria", "Raúl", "Sandra", "Adrián", "Eva"
    ]
    
    apellidos = [
        "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Martín", "Gómez",
        "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez",
        "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Suárez"
    ]
    
    user_names = {}
    for user_id in user_ids:
        np.random.seed(user_id)
        nombre = np.random.choice(nombres)
        apellido = np.random.choice(apellidos)
        user_names[user_id] = f"{nombre} {apellido}"
    
    return user_names

def load_model_and_data():
    """Carga el modelo y datos (sin caché para actualizaciones en tiempo real)"""
    try:
        model = ProductRecommendationANN(n_users=1, n_products=1)
        model.load_model('models/recommendation_model')
        
        interactions = pd.read_csv('data/interactions.csv')
        products = pd.read_csv('data/products.csv')
        user_stats = pd.read_csv('data/user_stats.csv')
        
        return model, interactions, products, user_stats
    except Exception as e:
        st.error(f"❌ Error al cargar modelo o datos: {e}")
        return None, None, None, None

def initialize_user_balance(user_id):
    """Inicializa el saldo de un usuario si no existe"""
    try:
        if os.path.exists('data/user_balances.csv'):
            balances = pd.read_csv('data/user_balances.csv')
        else:
            balances = pd.DataFrame(columns=['user_id', 'saldo_disponible'])
        
        if user_id not in balances['user_id'].values:
            new_balance = pd.DataFrame([{'user_id': user_id, 'saldo_disponible': 3000.0}])
            balances = pd.concat([balances, new_balance], ignore_index=True)
            balances.to_csv('data/user_balances.csv', index=False)
        
        return True
    except Exception as e:
        st.error(f"Error al inicializar saldo: {e}")
        return False

def get_user_balance(user_id):
    """Obtiene el saldo disponible de un usuario"""
    try:
        initialize_user_balance(user_id)
        balances = pd.read_csv('data/user_balances.csv')
        user_balance = balances[balances['user_id'] == user_id]
        
        if len(user_balance) > 0:
            return float(user_balance.iloc[0]['saldo_disponible'])
        return 3000.0
    except Exception as e:
        st.error(f"Error al obtener saldo: {e}")
        return 3000.0

def update_user_balance(user_id, amount_to_deduct):
    """Actualiza el saldo de un usuario después de una compra"""
    try:
        balances = pd.read_csv('data/user_balances.csv')
        balances.loc[balances['user_id'] == user_id, 'saldo_disponible'] -= amount_to_deduct
        balances.to_csv('data/user_balances.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Error al actualizar saldo: {e}")
        return False

def authenticate_user(username, password):
    """Autentica usuario y devuelve rol y user_id"""
    # Director
    if username.lower() == "director" and password == "12345":
        return "director", None, "Director del Sistema"
    
    # Cargar datos para verificar usuarios
    interactions = pd.read_csv('data/interactions.csv')
    user_ids = sorted(interactions['user_id'].unique())
    user_names = generate_user_names(user_ids)
    
    # Buscar usuario por nombre
    for user_id, name in user_names.items():
        if name.lower() == username.lower() and password == "12345":
            return "cliente", user_id, name
    
    return None, None, None

def save_purchase(user_id, product_id, product_name, category, price, quantity=1):
    """Guarda una nueva compra en el sistema"""
    try:
        # Calcular costo total
        total_cost = price * quantity
        
        # Verificar saldo disponible
        current_balance = get_user_balance(user_id)
        if current_balance < total_cost:
            return False, f"Saldo insuficiente. Necesitas ${total_cost:.2f} pero solo tienes ${current_balance:.2f}"
        
        # Cargar datos actuales
        interactions = pd.read_csv('data/interactions.csv')
        
        # Crear nueva compra
        new_purchase = {
            'user_id': user_id,
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'rating': 5,  # Rating por defecto
            'purchase_count': quantity,
            'price': price,
            'total_spent': total_cost,
            'purchase_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Agregar nueva compra
        interactions = pd.concat([interactions, pd.DataFrame([new_purchase])], ignore_index=True)
        interactions.to_csv('data/interactions.csv', index=False)
        
        # Actualizar saldo del usuario
        if not update_user_balance(user_id, total_cost):
            return False, "Error al actualizar saldo"
        
        # Actualizar estadísticas del usuario
        update_user_stats()
        
        new_balance = get_user_balance(user_id)
        return True, f"✅ Compra exitosa de {quantity} unidad(es) por ${total_cost:.2f}. Saldo restante: ${new_balance:.2f}"
        
    except Exception as e:
        return False, f"Error al guardar compra: {str(e)}"

def update_user_stats():
    """Actualiza las estadísticas de usuarios"""
    try:
        interactions = pd.read_csv('data/interactions.csv')
        
        user_stats = interactions.groupby('user_id').agg({
            'rating': 'mean',
            'purchase_count': 'sum',
            'total_spent': 'sum',
            'product_id': 'count'
        }).reset_index()
        
        user_stats.columns = ['user_id', 'avg_rating', 'total_purchases', 
                              'total_spent', 'num_interactions']
        
        user_stats.to_csv('data/user_stats.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Error al actualizar estadísticas: {e}")
        return False

# ============================================================================
# PANTALLA DE LOGIN
# ============================================================================

def show_login():
    """Muestra la pantalla de login"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: #667eea; font-size: 3rem;">🛒 Tienda Virtual IA</h1>
        <p style="font-size: 1.2rem; color: #666;">Sistema de Recomendaciones Inteligentes</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        ">
            <h2 style="color: white; text-align: center; margin-bottom: 1.5rem;">Iniciar Sesión</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Ingresa tu nombre completo o 'director'")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="12345")
            submit = st.form_submit_button("🚀 Ingresar", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Por favor completa todos los campos")
                else:
                    role, user_id, name = authenticate_user(username, password)
                    
                    if role:
                        st.session_state['authenticated'] = True
                        st.session_state['role'] = role
                        st.session_state['user_id'] = user_id
                        st.session_state['user_name'] = name
                        st.success(f"✅ Bienvenido, {name}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciales incorrectas")
        
        # Ayuda
        st.markdown("---")
        st.info("""
        **💡 Credenciales de Acceso:**
        
        **Director:**
        - Usuario: `director`
        - Contraseña: `12345`
        
        **Clientes:**
        - Usuario: Tu nombre completo (ej: Juan García)
        - Contraseña: `12345`
        """)

# ============================================================================
# VISTA DE CLIENTE (TIENDA VIRTUAL)
# ============================================================================

def show_client_view():
    """Vista de tienda virtual para clientes"""
    user_id = st.session_state['user_id']
    user_name = st.session_state['user_name']
    
    # Inicializar estado del modal
    if 'selected_product' not in st.session_state:
        st.session_state['selected_product'] = None
    
    # Cargar datos
    model, interactions, products, user_stats = load_model_and_data()
    
    if model is None:
        st.stop()
    
    # Header con usuario y saldo
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        current_balance = get_user_balance(user_id)
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        ">
            <h2 style="color: white; margin: 0;">🛒 Bienvenido, {user_name}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">ID: {user_id}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("💰 Saldo Disponible", f"${current_balance:.2f}")
    
    with col3:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Recomendaciones", "📊 Mi Perfil", "📜 Historial de Compras"])
    
    # TAB 1: RECOMENDACIONES (TIENDA)
    with tab1:
        st.markdown("### 🎁 Productos Recomendados Para Ti")
        st.markdown("Haz clic en **Comprar Ahora** para agregar productos a tu historial")
        st.markdown("---")
        
        # Obtener productos ya comprados
        user_purchases = interactions[interactions['user_id'] == user_id]
        purchased_ids = user_purchases['product_id'].tolist()
        
        # Generar recomendaciones
        recommendations = model.recommend_products(
            user_id=user_id,
            products_df=products,
            top_n=12,
            exclude_purchased=purchased_ids
        )
        
        if len(recommendations) == 0:
            st.warning("No hay más productos disponibles para recomendar en este momento.")
        else:
            # Mostrar productos en grid 3 columnas
            for i in range(0, len(recommendations), 3):
                cols = st.columns(3, gap="large")
                
                for j, col in enumerate(cols):
                    if i + j < len(recommendations):
                        rec = recommendations.iloc[i + j]
                        
                        with col:
                            rating_stars = "⭐" * int(rec['predicted_rating'])
                            
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1.5rem;
                                border-radius: 15px;
                                color: white;
                                height: 220px;
                                display: flex;
                                flex-direction: column;
                                justify-content: space-between;
                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                margin-bottom: 1rem;
                            ">
                                <div>
                                    <h4 style="margin: 0; color: white; font-size: 1.1rem;">{rec['product_name']}</h4>
                                    <p style="margin: 0.5rem 0; opacity: 0.9;">🏷️ {rec['category']}</p>
                                </div>
                                <div>
                                    <p style="margin: 0.5rem 0; font-size: 1.2rem;">{rating_stars}</p>
                                    <p style="margin: 0; font-size: 1.1rem; font-weight: bold;">
                                        Rating: {rec['predicted_rating']:.2f}/5
                                    </p>
                                    <p style="margin: 0.5rem 0; font-size: 1.4rem; font-weight: bold; color: #FFD700;">
                                        💰 ${rec['price']:.2f}
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Botón de compra
                            buy_key = f"buy_{rec['product_id']}_{i}_{j}"
                            if st.button(f"🛒 Comprar Ahora", key=buy_key, use_container_width=True):
                                st.session_state['selected_product'] = {
                                    'product_id': rec['product_id'],
                                    'product_name': rec['product_name'],
                                    'category': rec['category'],
                                    'price': rec['price']
                                }
                            
                            st.markdown("<br>", unsafe_allow_html=True)
        
        # Modal para seleccionar cantidad
        if 'selected_product' in st.session_state and st.session_state['selected_product'] is not None:
            product = st.session_state['selected_product']
            
            # Fondo oscuro del modal
            st.markdown("""
            <style>
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 999;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Contenido del modal
            with st.container():
                st.markdown("---")
                st.markdown(f"### 🛒 Comprar: {product['product_name']}")
                st.markdown(f"**Precio unitario:** ${product['price']:.2f}")
                st.markdown(f"**Categoría:** {product['category']}")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    quantity = st.number_input(
                        "Cantidad a comprar:",
                        min_value=1,
                        max_value=100,
                        value=1,
                        step=1,
                        key="quantity_input"
                    )
                    
                    total_price = product['price'] * quantity
                    current_balance = get_user_balance(user_id)
                    
                    st.markdown(f"**Total a pagar:** ${total_price:.2f}")
                    st.markdown(f"**Saldo actual:** ${current_balance:.2f}")
                    
                    if total_price > current_balance:
                        st.error(f"⚠️ Saldo insuficiente. Te faltan ${total_price - current_balance:.2f}")
                    else:
                        st.success(f"✅ Saldo suficiente. Quedará: ${current_balance - total_price:.2f}")
                    
                    st.markdown("---")
                    
                    col_confirm, col_cancel = st.columns(2)
                    
                    with col_confirm:
                        if st.button("✅ Confirmar Compra", use_container_width=True, type="primary"):
                            success, message = save_purchase(
                                user_id,
                                product['product_id'],
                                product['product_name'],
                                product['category'],
                                product['price'],
                                quantity
                            )
                            
                            if success:
                                st.success(message)
                                st.balloons()
                                st.session_state['selected_product'] = None
                                st.rerun()
                            else:
                                st.error(message)
                    
                    with col_cancel:
                        if st.button("❌ Cancelar", use_container_width=True):
                            st.session_state['selected_product'] = None
                            st.rerun()
                
                st.markdown("---")
    
    # TAB 2: PERFIL
    with tab2:
        st.markdown("### 📊 Estadísticas de tu Perfil")
        
        user_info = user_stats[user_stats['user_id'] == user_id]
        
        if len(user_info) > 0:
            user_info = user_info.iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🛍️ Compras", int(user_info['num_interactions']))
            with col2:
                st.metric("⭐ Rating Promedio", f"{user_info['avg_rating']:.2f}")
            with col3:
                st.metric("📦 Productos", int(user_info['total_purchases']))
            with col4:
                st.metric("💰 Total Gastado", f"${user_info['total_spent']:.2f}")
            
            st.markdown("---")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏷️ Tus Categorías Favoritas")
                category_counts = user_purchases['category'].value_counts()
                fig = px.bar(
                    x=category_counts.values,
                    y=category_counts.index,
                    orientation='h',
                    labels={'x': 'Compras', 'y': 'Categoría'},
                    color=category_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 💰 Gasto por Categoría")
                category_spending = user_purchases.groupby('category')['total_spent'].sum()
                fig = px.pie(
                    values=category_spending.values,
                    names=category_spending.index,
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aún no tienes compras registradas. ¡Ve a la pestaña Recomendaciones para comenzar!")
    
    # TAB 3: HISTORIAL
    with tab3:
        st.markdown("### 📜 Tu Historial de Compras")
        
        if len(user_purchases) > 0:
            user_purchases_sorted = user_purchases.sort_values('purchase_date', ascending=False)
            
            st.info(f"📦 Total de productos comprados: **{len(user_purchases_sorted)}**")
            
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
            
            csv = display_history.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Historial (CSV)",
                data=csv,
                file_name=f"historial_usuario_{user_id}.csv",
                mime="text/csv"
            )
        else:
            st.info("Aún no tienes compras registradas. ¡Visita la pestaña Recomendaciones!")

# ============================================================================
# VISTA DE DIRECTOR (DASHBOARD ADMINISTRATIVO)
# ============================================================================

def show_director_view():
    """Vista de dashboard para el director"""
    
    # Cargar datos
    model, interactions, products, user_stats = load_model_and_data()
    
    if model is None:
        st.stop()
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📊 Dashboard del Director")
        st.markdown("### Sistema de Gestión y Análisis")
    with col2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        st.subheader("👤 Análisis de Usuario")
        
        user_ids = sorted(interactions['user_id'].unique())
        user_names = generate_user_names(user_ids)
        
        user_options = {f"{user_names[uid]}": uid for uid in user_ids}
        
        selected_user = st.selectbox(
            "Seleccionar usuario",
            options=list(user_options.keys()),
            index=0
        )
        
        user_id = user_options[selected_user]
        user_name = user_names[user_id]
        
        n_recommendations = st.slider(
            "📊 Cantidad de recomendaciones",
            min_value=3,
            max_value=15,
            value=9,
            step=3
        )
        
        st.subheader("🏷️ Filtrar por Categoría")
        categories = ['Todas'] + sorted(products['category'].unique().tolist())
        selected_category = st.selectbox("Categoría", options=categories, index=0)
        
        st.markdown("---")
        
        st.subheader("📈 Info del Sistema")
        st.info(f"""
        **Usuarios**: {len(user_ids)}  
        **Productos**: {len(products)}  
        **Transacciones**: {len(interactions)}  
        **Categorías**: {len(products['category'].unique())}
        """)
    
    # Usuario seleccionado
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
    ">
        <h3 style="color: white; margin: 0;">👤 Usuario Seleccionado</h3>
        <h2 style="color: white; margin: 0.5rem 0 0 0;">{user_name}</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0;">ID: {user_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Recomendaciones", "📊 Perfil", "📜 Historial", "🌍 Global"])
    
    # TAB 1: RECOMENDACIONES
    with tab1:
        st.markdown("### 🎁 Productos Recomendados")
        
        user_purchases = interactions[interactions['user_id'] == user_id]
        purchased_ids = user_purchases['product_id'].tolist()
        
        if selected_category != 'Todas':
            category_products = products[products['category'] == selected_category]
            recommendations = model.recommend_products(
                user_id=user_id,
                products_df=category_products,
                top_n=n_recommendations,
                exclude_purchased=purchased_ids
            )
        else:
            recommendations = model.recommend_products(
                user_id=user_id,
                products_df=products,
                top_n=n_recommendations,
                exclude_purchased=purchased_ids
            )
        
        if len(recommendations) > 0:
            for i in range(0, len(recommendations), 3):
                cols = st.columns(3, gap="large")
                
                for j, col in enumerate(cols):
                    if i + j < len(recommendations):
                        rec = recommendations.iloc[i + j]
                        
                        with col:
                            rating_stars = "⭐" * int(rec['predicted_rating'])
                            
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1.5rem;
                                border-radius: 15px;
                                color: white;
                                height: 220px;
                            ">
                                <h4 style="margin: 0; color: white;">#{i+j+1} {rec['product_name']}</h4>
                                <p style="margin: 0.5rem 0; opacity: 0.9;">🏷️ {rec['category']}</p>
                                <p style="margin: 0.5rem 0;">{rating_stars}</p>
                                <p style="margin: 0; font-weight: bold;">Rating: {rec['predicted_rating']:.2f}/5</p>
                                <p style="margin: 0.5rem 0; font-size: 1.3rem; font-weight: bold;">💰 ${rec['price']:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("No hay recomendaciones disponibles")
    
    # TAB 2: PERFIL
    with tab2:
        st.markdown("### 📊 Estadísticas del Usuario")
        
        user_info = user_stats[user_stats['user_id'] == user_id]
        
        if len(user_info) > 0:
            user_info = user_info.iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🛍️ Compras", int(user_info['num_interactions']))
            with col2:
                st.metric("⭐ Rating", f"{user_info['avg_rating']:.2f}")
            with col3:
                st.metric("📦 Productos", int(user_info['total_purchases']))
            with col4:
                st.metric("💰 Gastado", f"${user_info['total_spent']:.2f}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏷️ Categorías Favoritas")
                category_counts = user_purchases['category'].value_counts()
                fig = px.bar(x=category_counts.values, y=category_counts.index, orientation='h')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 💰 Gasto por Categoría")
                category_spending = user_purchases.groupby('category')['total_spent'].sum()
                fig = px.pie(values=category_spending.values, names=category_spending.index, hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: HISTORIAL
    with tab3:
        st.markdown("### 📜 Historial de Compras")
        
        if len(user_purchases) > 0:
            user_purchases_sorted = user_purchases.sort_values('purchase_date', ascending=False)
            
            st.info(f"📦 Total: **{len(user_purchases_sorted)}** compras")
            
            st.dataframe(user_purchases_sorted[[
                'purchase_date', 'product_name', 'category', 'rating', 'total_spent'
            ]], use_container_width=True)
        else:
            st.info("Este usuario no tiene compras registradas")
    
    # TAB 4: VISTA GLOBAL
    with tab4:
        st.markdown("### 🌍 Análisis Global del Sistema")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Usuarios Totales", len(user_ids))
        with col2:
            st.metric("🛒 Transacciones", len(interactions))
        with col3:
            st.metric("💰 Ingresos Totales", f"${interactions['total_spent'].sum():.2f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Productos Más Vendidos")
            top_products = interactions.groupby('product_name').size().sort_values(ascending=False).head(10)
            fig = px.bar(x=top_products.values, y=top_products.index, orientation='h')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 💰 Categorías con Más Ingresos")
            category_revenue = interactions.groupby('category')['total_spent'].sum().sort_values(ascending=False)
            fig = px.bar(x=category_revenue.index, y=category_revenue.values)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    
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

if __name__ == "__main__":
    main()
