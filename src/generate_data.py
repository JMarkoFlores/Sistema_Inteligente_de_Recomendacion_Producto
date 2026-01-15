"""
Generador de Dataset Sintético para Sistema de Recomendación
Este script crea datos realistas de comercio electrónico para entrenar el modelo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración de semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

# Definir productos por categoría
PRODUCTS = {
    'Electrónica': ['Laptop HP', 'Mouse Inalámbrico', 'Teclado Mecánico', 'Monitor 24"', 
                    'Auriculares Bluetooth', 'Webcam HD', 'Tablet Android', 'Cargador USB-C',
                    'Hub USB', 'Mousepad Gaming'],
    'Ropa': ['Camiseta Deportiva', 'Jeans Clásicos', 'Zapatillas Running', 'Chaqueta Invierno',
             'Vestido Casual', 'Pantalón Formal', 'Sudadera con Capucha', 'Zapatos Formales',
             'Shorts Deportivos', 'Camisa de Vestir'],
    'Hogar': ['Lámpara LED', 'Cojines Decorativos', 'Juego de Sábanas', 'Organizador Cocina',
              'Espejo de Pared', 'Alfombra Moderna', 'Set de Toallas', 'Reloj de Pared',
              'Cortinas Blackout', 'Macetas Decorativas'],
    'Deportes': ['Mancuernas 5kg', 'Colchoneta Yoga', 'Botella Térmica', 'Cuerda Saltar',
                 'Pelota Fitness', 'Banda Elástica', 'Guantes Gimnasio', 'Bicicleta Estática',
                 'Pesas Ajustables', 'Kit Yoga Completo'],
    'Libros': ['Python para Todos', 'El Arte de la Guerra', 'Sapiens', 'Inteligencia Artificial',
               'Cien Años Soledad', 'Data Science Handbook', '1984', 'Deep Learning',
               'Clean Code', 'El Principito']
}

def generate_synthetic_data(n_users=500, n_interactions=5000):
    """
    Genera un dataset sintético de interacciones usuario-producto
    
    Args:
        n_users: Número de usuarios a generar
        n_interactions: Número de interacciones (compras/ratings) a generar
    
    Returns:
        DataFrame con el dataset completo
    """
    
    # Crear lista de todos los productos con IDs y categorías
    products_list = []
    product_id = 1
    
    for category, items in PRODUCTS.items():
        for item in items:
            products_list.append({
                'product_id': product_id,
                'product_name': item,
                'category': category,
                'price': round(random.uniform(10, 500), 2)
            })
            product_id += 1
    
    products_df = pd.DataFrame(products_list)
    
    # Generar perfiles de usuario (cada usuario tiene preferencias por ciertas categorías)
    user_profiles = []
    categories = list(PRODUCTS.keys())
    
    for user_id in range(1, n_users + 1):
        # Cada usuario tiene 1-3 categorías favoritas
        favorite_categories = random.sample(categories, k=random.randint(1, 3))
        user_profiles.append({
            'user_id': user_id,
            'favorite_categories': favorite_categories,
            'spending_power': random.choice(['bajo', 'medio', 'alto'])
        })
    
    # Generar interacciones basadas en los perfiles
    interactions = []
    
    for _ in range(n_interactions):
        # Seleccionar usuario aleatorio
        user = random.choice(user_profiles)
        user_id = user['user_id']
        
        # 70% de probabilidad de comprar de categoría favorita
        if random.random() < 0.7 and user['favorite_categories']:
            category = random.choice(user['favorite_categories'])
            available_products = products_df[products_df['category'] == category]
        else:
            available_products = products_df
        
        # Seleccionar producto
        product = available_products.sample(1).iloc[0]
        
        # Generar rating basado en si es categoría favorita
        if product['category'] in user['favorite_categories']:
            rating = random.choices([3, 4, 5], weights=[0.1, 0.3, 0.6])[0]
        else:
            rating = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.2, 0.4, 0.2, 0.1])[0]
        
        # Cantidad comprada (1-3 unidades)
        purchase_count = random.randint(1, 3)
        
        # Fecha aleatoria en los últimos 6 meses
        days_ago = random.randint(0, 180)
        purchase_date = datetime.now() - timedelta(days=days_ago)
        
        interactions.append({
            'user_id': user_id,
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'rating': rating,
            'purchase_count': purchase_count,
            'price': product['price'],
            'total_spent': round(product['price'] * purchase_count, 2),
            'purchase_date': purchase_date.strftime('%Y-%m-%d')
        })
    
    # Crear DataFrame final
    interactions_df = pd.DataFrame(interactions)
    
    # Agregar algunas estadísticas por usuario
    user_stats = interactions_df.groupby('user_id').agg({
        'rating': 'mean',
        'purchase_count': 'sum',
        'total_spent': 'sum',
        'product_id': 'count'
    }).reset_index()
    
    user_stats.columns = ['user_id', 'avg_rating', 'total_purchases', 
                          'total_spent', 'num_interactions']
    
    print(f"✅ Dataset generado exitosamente!")
    print(f"📊 Usuarios: {n_users}")
    print(f"📦 Productos únicos: {len(products_df)}")
    print(f"🛒 Interacciones: {len(interactions_df)}")
    print(f"📈 Categorías: {len(categories)}")
    
    return interactions_df, products_df, user_stats

if __name__ == "__main__":
    # Generar datos
    interactions, products, user_stats = generate_synthetic_data(
        n_users=500, 
        n_interactions=5000
    )
    
    # Guardar en CSV
    interactions.to_csv('data/interactions.csv', index=False)
    products.to_csv('data/products.csv', index=False)
    user_stats.to_csv('data/user_stats.csv', index=False)
    
    print("\n📁 Archivos guardados en carpeta 'data/':")
    print("   - interactions.csv")
    print("   - products.csv")
    print("   - user_stats.csv")
    
    # Mostrar ejemplos
    print("\n🔍 Vista previa de interacciones:")
    print(interactions.head(10))
    print(f"\n📊 Distribución de ratings:")
    print(interactions['rating'].value_counts().sort_index())
