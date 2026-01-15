"""
Script para inicializar los saldos de todos los usuarios con $3000
"""
import pandas as pd
import os

def initialize_all_balances():
    """Inicializa el saldo de todos los usuarios con $3000"""
    try:
        # Leer todos los usuarios únicos de interactions
        interactions = pd.read_csv('data/interactions.csv')
        unique_users = interactions['user_id'].unique()
        
        # Crear DataFrame de saldos
        balances = pd.DataFrame({
            'user_id': unique_users,
            'saldo_disponible': [3000.0] * len(unique_users)
        })
        
        # Guardar
        balances.to_csv('data/user_balances.csv', index=False)
        
        print(f"✅ Saldos inicializados para {len(unique_users)} usuarios")
        print(f"💰 Saldo inicial: $3000.00 por usuario")
        print(f"📁 Archivo guardado: data/user_balances.csv")
        
        # Mostrar muestra
        print("\n📊 Muestra de saldos:")
        print(balances.head(10))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    initialize_all_balances()
