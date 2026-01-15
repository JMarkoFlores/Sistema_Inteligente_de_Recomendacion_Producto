"""
Componente de autenticación
"""
import streamlit as st
import pandas as pd
from src.utils import generate_user_names
from config.settings import USER_CONFIG, GRADIENTS

def authenticate_user(username, password):
    """Autentica usuario y devuelve rol y user_id"""
    # Director
    if (username.lower() == USER_CONFIG['director_username'] and 
        password == USER_CONFIG['director_password']):
        return "director", None, "Director del Sistema"
    
    # Clientes
    interactions = pd.read_csv('data/interactions.csv')
    user_ids = sorted(interactions['user_id'].unique())
    user_names = generate_user_names(user_ids)
    
    for user_id, name in user_names.items():
        if (name.lower() == username.lower() and 
            password == USER_CONFIG['default_password']):
            return "cliente", user_id, name
    
    return None, None, None

def show_login():
    """Muestra la pantalla de login mejorada"""
    
    # Hero section
    st.markdown(f"""
    <div style="
        background: {GRADIENTS['primary']};
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    ">
        <h1 style="
            color: white; 
            font-size: 3.5rem; 
            margin: 0;
            font-weight: 800;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        ">🛒 Tienda Virtual IA</h1>
        <p style="
            font-size: 1.4rem; 
            color: rgba(255,255,255,0.95);
            margin: 1rem 0 0 0;
            font-weight: 300;
        ">Sistema de Recomendaciones Inteligentes con Deep Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border: 1px solid #e5e7eb;
        ">
            <h2 style="
                color: #1f2937; 
                text-align: center; 
                margin-bottom: 2rem;
                font-weight: 700;
            ">Iniciar Sesión</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("##### 👤 Usuario")
            username = st.text_input(
                "Usuario", 
                placeholder="Ingresa tu nombre completo o 'director'",
                label_visibility="collapsed"
            )
            
            st.markdown("##### 🔒 Contraseña")
            password = st.text_input(
                "Contraseña", 
                type="password", 
                placeholder="Ingresa tu contraseña",
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit = st.form_submit_button(
                "🚀 Ingresar al Sistema", 
                use_container_width=True,
                type="primary"
            )
            
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
                        st.success(f"✅ ¡Bienvenido, {name}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciales incorrectas. Verifica tu usuario y contraseña.")
        
        # Información de credenciales
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("💡 Credenciales de Acceso", expanded=False):
            st.markdown("""
            <div style="padding: 1rem;">
                <h4 style="color: #667eea; margin-top: 0;">👔 Director del Sistema</h4>
                <p style="margin: 0.5rem 0;">
                    <strong>Usuario:</strong> <code>director</code><br>
                    <strong>Contraseña:</strong> <code>12345</code>
                </p>
                
                <h4 style="color: #667eea; margin-top: 1.5rem;">👥 Clientes</h4>
                <p style="margin: 0.5rem 0;">
                    <strong>Usuario:</strong> Tu nombre completo (ej: Juan García)<br>
                    <strong>Contraseña:</strong> <code>12345</code>
                </p>
                
                <p style="margin-top: 1.5rem; font-size: 0.9rem; color: #6b7280;">
                    💡 <em>Todos los usuarios inician con $3,000 de saldo</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Features
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### ✨ Características del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {GRADIENTS['info']};
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="margin: 0; color: white;">Inteligencia Artificial</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Recomendaciones personalizadas con Deep Learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {GRADIENTS['success']};
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="margin: 0; color: white;">Analytics Avanzado</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Dashboard completo con métricas en tiempo real</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: {GRADIENTS['warm']};
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
            <h3 style="margin: 0; color: white;">Sistema Seguro</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Autenticación y gestión de roles</p>
        </div>
        """, unsafe_allow_html=True)