"""
Configuración centralizada del sistema
"""

# Configuración de la aplicación
APP_CONFIG = {
    'page_title': 'Tienda Virtual IA',
    'page_icon': '🛒',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Configuración del modelo
MODEL_CONFIG = {
    'embedding_dim': 50,
    'model_path': 'models/recommendation_model',
    'epochs': 30,
    'batch_size': 64
}

# Configuración de datos
DATA_CONFIG = {
    'interactions_path': 'data/interactions.csv',
    'products_path': 'data/products.csv',
    'user_stats_path': 'data/user_stats.csv',
    'user_balances_path': 'data/user_balances.csv'
}

# Configuración de usuarios
USER_CONFIG = {
    'default_balance': 3000.0,
    'director_username': 'director',
    'director_password': '12345',
    'default_password': '12345'
}

# Colores del tema
THEME_COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'dark': '#1f2937',
    'light': '#f3f4f6'
}

# Gradientes
GRADIENTS = {
    'primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'success': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    'info': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
    'warm': 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
}