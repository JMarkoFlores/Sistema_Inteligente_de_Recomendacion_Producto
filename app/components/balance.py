"""
Gestión de saldo de usuarios
Saldo inicial: $3000.00 por usuario
"""
import pandas as pd
import os
from datetime import datetime

BALANCE_FILE = 'data/user_balance.csv'
INITIAL_BALANCE = 3000.00


def initialize_balance_file():
    """Crea el archivo de saldo si no existe"""
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists(BALANCE_FILE):
        df = pd.DataFrame(columns=['user_id', 'balance', 'last_updated'])
        df.to_csv(BALANCE_FILE, index=False)


def get_user_balance(user_id):
    """
    Obtiene el saldo actual de un usuario
    Si no existe, crea uno con saldo inicial de $3000
    """
    initialize_balance_file()
    
    try:
        df = pd.read_csv(BALANCE_FILE)
        
        if user_id in df['user_id'].values:
            balance = df[df['user_id'] == user_id]['balance'].iloc[0]
            return float(balance)
        else:
            # Usuario nuevo - asignar saldo inicial
            new_row = pd.DataFrame({
                'user_id': [user_id],
                'balance': [INITIAL_BALANCE],
                'last_updated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(BALANCE_FILE, index=False)
            return INITIAL_BALANCE
            
    except Exception as e:
        print(f"Error al obtener saldo: {e}")
        return INITIAL_BALANCE


def update_user_balance(user_id, new_balance):
    """
    Actualiza el saldo de un usuario
    """
    initialize_balance_file()
    
    try:
        df = pd.read_csv(BALANCE_FILE)
        
        if user_id in df['user_id'].values:
            df.loc[df['user_id'] == user_id, 'balance'] = new_balance
            df.loc[df['user_id'] == user_id, 'last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            new_row = pd.DataFrame({
                'user_id': [user_id],
                'balance': [new_balance],
                'last_updated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            })
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(BALANCE_FILE, index=False)
        return True
        
    except Exception as e:
        print(f"Error al actualizar saldo: {e}")
        return False


def deduct_balance(user_id, amount):
    """
    Descuenta un monto del saldo del usuario
    Retorna (success, new_balance, message)
    """
    current_balance = get_user_balance(user_id)
    
    if current_balance < amount:
        return False, current_balance, f"Saldo insuficiente. Necesitas ${amount:.2f} pero tienes ${current_balance:.2f}"
    
    new_balance = current_balance - amount
    success = update_user_balance(user_id, new_balance)
    
    if success:
        return True, new_balance, f"Compra exitosa. Nuevo saldo: ${new_balance:.2f}"
    else:
        return False, current_balance, "Error al procesar el pago"


def add_balance(user_id, amount):
    """Añade saldo a un usuario (para reembolsos o recargas)"""
    current_balance = get_user_balance(user_id)
    new_balance = current_balance + amount
    success = update_user_balance(user_id, new_balance)
    return success, new_balance
