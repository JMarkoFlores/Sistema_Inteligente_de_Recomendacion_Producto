"""
Funciones utilitarias compartidas
"""
import pandas as pd
import numpy as np
import streamlit as st
from config.settings import DATA_CONFIG, USER_CONFIG

@st.cache_data
def generate_user_names(user_ids):
    """Genera nombres de usuario consistentes basados en IDs"""
    nombres = [
        "Juan", "María", "Carlos", "Ana", "Pedro", "Laura", "Miguel", "Carmen", 
        "José", "Isabel", "Francisco", "Lucía", "Antonio", "Marta", "Manuel", 
        "Elena", "David", "Patricia", "Javier", "Rosa", "Daniel", "Sofía", 
        "Rafael", "Andrea", "Sergio", "Paula", "Jorge", "Beatriz", "Luis", "Clara"
    ]
    
    apellidos = [
        "García", "Rodríguez", "González", "Fernández", "López", "Martínez", 
        "Sánchez", "Pérez", "Martín", "Gómez", "Jiménez", "Ruiz", "Hernández", 
        "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez"
    ]
    
    user_names = {}
    for user_id in user_ids:
        np.random.seed(user_id)
        nombre = np.random.choice(nombres)
        apellido = np.random.choice(apellidos)
        user_names[user_id] = f"{nombre} {apellido}"
    
    return user_names

def load_data():
    """Carga todos los datos del sistema"""
    try:
        interactions = pd.read_csv(DATA_CONFIG['interactions_path'])
        products = pd.read_csv(DATA_CONFIG['products_path'])
        user_stats = pd.read_csv(DATA_CONFIG['user_stats_path'])
        return interactions, products, user_stats
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return None, None, None

def format_currency(amount):
    """Formatea cantidad como moneda"""
    return f"${amount:,.2f}"

def get_rating_stars(rating):
    """Convierte rating numérico a estrellas"""
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "⭐" * full_stars + ("✨" * half_star) + ("☆" * empty_stars)