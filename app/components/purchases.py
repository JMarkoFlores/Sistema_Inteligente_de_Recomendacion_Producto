"""
Gestión de compras y historial
"""
import pandas as pd
import os
from datetime import datetime
from app.components.balance import deduct_balance

PURCHASES_FILE = 'data/user_purchases.csv'


def initialize_purchases_file():
    """Crea el archivo de compras si no existe"""
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists(PURCHASES_FILE):
        df = pd.DataFrame(columns=[
            'user_id', 'product_id', 'product_name', 'category', 
            'price', 'quantity', 'total', 'timestamp'
        ])
        df.to_csv(PURCHASES_FILE, index=False)


def save_purchase(user_id, product_id, product_name, category, price, quantity=1):
    """
    Guarda una compra y descuenta del saldo del usuario
    
    Args:
        user_id: ID del usuario
        product_id: ID del producto
        product_name: Nombre del producto
        category: Categoría del producto
        price: Precio unitario
        quantity: Cantidad comprada
        
    Returns:
        tuple: (success, message)
    """
    initialize_purchases_file()
    
    total = price * quantity
    
    # Descontar del saldo
    success, new_balance, balance_message = deduct_balance(user_id, total)
    
    if not success:
        return False, balance_message
    
    try:
        # Registrar la compra
        new_purchase = pd.DataFrame({
            'user_id': [user_id],
            'product_id': [product_id],
            'product_name': [product_name],
            'category': [category],
            'price': [price],
            'quantity': [quantity],
            'total': [total],
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        df = pd.read_csv(PURCHASES_FILE)
        df = pd.concat([df, new_purchase], ignore_index=True)
        df.to_csv(PURCHASES_FILE, index=False)
        
        return True, f"✅ Compra registrada. Saldo actual: ${new_balance:.2f}"
        
    except Exception as e:
        print(f"Error al guardar compra: {e}")
        return False, f"❌ Error al registrar la compra: {str(e)}"


def get_user_purchases(user_id):
    """Obtiene el historial de compras de un usuario"""
    initialize_purchases_file()
    
    try:
        df = pd.read_csv(PURCHASES_FILE)
        user_purchases = df[df['user_id'] == user_id]
        return user_purchases
    except Exception as e:
        print(f"Error al obtener compras: {e}")
        return pd.DataFrame()


def update_user_stats(user_id, interactions_df):
    """Actualiza las estadísticas del usuario después de una compra"""
    # Esta función puede extenderse para actualizar métricas adicionales
    pass
