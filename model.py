"""
Sistema de Recomendación de Productos usando Redes Neuronales
Implementa Collaborative Filtering con embeddings y ANN
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime

class ProductRecommendationANN:
    """
    Red Neuronal para Recomendación de Productos
    Usa embeddings para usuarios y productos + capas densas
    """
    
    def __init__(self, n_users, n_products, embedding_dim=50):
        """
        Inicializa el modelo de recomendación
        
        Args:
            n_users: Número total de usuarios
            n_products: Número total de productos
            embedding_dim: Dimensionalidad de los embeddings
        """
        self.n_users = n_users
        self.n_products = n_products
        self.embedding_dim = embedding_dim
        self.model = None
        self.user_encoder = LabelEncoder()
        self.product_encoder = LabelEncoder()
        self.history = None
        
    def build_model(self):
        """
        Construye la arquitectura de la red neuronal
        
        Arquitectura:
        - Embeddings para usuarios y productos
        - Concatenación de embeddings
        - Capas densas con dropout
        - Salida: rating predicho
        """
        
        # Entrada: usuario y producto
        user_input = layers.Input(shape=(1,), name='user_input')
        product_input = layers.Input(shape=(1,), name='product_input')
        
        # Embeddings para usuarios
        user_embedding = layers.Embedding(
            input_dim=self.n_users,
            output_dim=self.embedding_dim,
            name='user_embedding'
        )(user_input)
        user_vec = layers.Flatten(name='user_flatten')(user_embedding)
        
        # Embeddings para productos
        product_embedding = layers.Embedding(
            input_dim=self.n_products,
            output_dim=self.embedding_dim,
            name='product_embedding'
        )(product_input)
        product_vec = layers.Flatten(name='product_flatten')(product_embedding)
        
        # Concatenar embeddings
        concat = layers.Concatenate(name='concat')([user_vec, product_vec])
        
        # Capas densas (red neuronal multicapa)
        dense1 = layers.Dense(128, activation='relu', name='dense1')(concat)
        dropout1 = layers.Dropout(0.3, name='dropout1')(dense1)
        
        dense2 = layers.Dense(64, activation='relu', name='dense2')(dropout1)
        dropout2 = layers.Dropout(0.2, name='dropout2')(dense2)
        
        dense3 = layers.Dense(32, activation='relu', name='dense3')(dropout2)
        
        # Capa de salida: rating predicho (0-5)
        output = layers.Dense(1, activation='linear', name='output')(dense3)
        
        # Crear modelo
        self.model = Model(inputs=[user_input, product_input], outputs=output)
        
        # Compilar modelo
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae', 'mse']
        )
        
        return self.model
    
    def prepare_data(self, interactions_df):
        """
        Prepara los datos para entrenamiento
        
        Args:
            interactions_df: DataFrame con columnas user_id, product_id, rating
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        
        # Codificar usuarios y productos a índices numéricos
        interactions_df['user_encoded'] = self.user_encoder.fit_transform(
            interactions_df['user_id']
        )
        interactions_df['product_encoded'] = self.product_encoder.fit_transform(
            interactions_df['product_id']
        )
        
        # Actualizar número de usuarios y productos únicos
        self.n_users = interactions_df['user_encoded'].nunique()
        self.n_products = interactions_df['product_encoded'].nunique()
        
        # Preparar features (X) y target (y)
        X_user = interactions_df['user_encoded'].values
        X_product = interactions_df['product_encoded'].values
        y = interactions_df['rating'].values
        
        # Dividir en train/test (80/20)
        X_user_train, X_user_test, X_product_train, X_product_test, y_train, y_test = \
            train_test_split(X_user, X_product, y, test_size=0.2, random_state=42)
        
        return (X_user_train, X_product_train), (X_user_test, X_product_test), y_train, y_test
    
    def train(self, interactions_df, epochs=20, batch_size=64, verbose=1):
        """
        Entrena el modelo
        
        Args:
            interactions_df: DataFrame con interacciones
            epochs: Número de épocas de entrenamiento
            batch_size: Tamaño del batch
            verbose: Nivel de verbosidad
        
        Returns:
            History object con métricas de entrenamiento
        """
        
        print("🔄 Preparando datos...")
        (X_user_train, X_product_train), \
        (X_user_test, X_product_test), \
        y_train, y_test = self.prepare_data(interactions_df)
        
        print(f"✅ Datos preparados:")
        print(f"   - Usuarios únicos: {self.n_users}")
        print(f"   - Productos únicos: {self.n_products}")
        print(f"   - Datos entrenamiento: {len(y_train)}")
        print(f"   - Datos validación: {len(y_test)}")
        
        # Construir modelo si no existe
        if self.model is None:
            print("\n🏗️  Construyendo red neuronal...")
            self.build_model()
            print(self.model.summary())
        
        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=0.00001
        )
        
        # Entrenar modelo
        print(f"\n🚀 Entrenando modelo ({epochs} épocas)...")
        self.history = self.model.fit(
            [X_user_train, X_product_train],
            y_train,
            validation_data=([X_user_test, X_product_test], y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=verbose
        )
        
        # Evaluar modelo
        print("\n📊 Evaluando modelo...")
        test_loss, test_mae, test_mse = self.model.evaluate(
            [X_user_test, X_product_test],
            y_test,
            verbose=0
        )
        
        rmse = np.sqrt(test_mse)
        
        print(f"✅ Métricas finales:")
        print(f"   - MAE: {test_mae:.4f}")
        print(f"   - RMSE: {rmse:.4f}")
        print(f"   - Loss: {test_loss:.4f}")
        
        return self.history
    
    def predict_rating(self, user_id, product_id):
        """
        Predice el rating que un usuario daría a un producto
        
        Args:
            user_id: ID del usuario
            product_id: ID del producto
        
        Returns:
            Rating predicho (0-5)
        """
        
        try:
            # Codificar usuario y producto
            user_encoded = self.user_encoder.transform([user_id])[0]
            product_encoded = self.product_encoder.transform([product_id])[0]
            
            # Predecir
            prediction = self.model.predict(
                [np.array([user_encoded]), np.array([product_encoded])],
                verbose=0
            )[0][0]
            
            # Limitar rating entre 0 y 5
            prediction = np.clip(prediction, 0, 5)
            
            return prediction
        
        except ValueError:
            # Usuario o producto no visto en entrenamiento
            return None
    
    def recommend_products(self, user_id, products_df, top_n=10, exclude_purchased=None):
        """
        Recomienda productos para un usuario
        
        Args:
            user_id: ID del usuario
            products_df: DataFrame con información de productos
            top_n: Número de recomendaciones a retornar
            exclude_purchased: Lista de product_ids ya comprados (opcional)
        
        Returns:
            DataFrame con top_n productos recomendados
        """
        
        if exclude_purchased is None:
            exclude_purchased = []
        
        # Obtener todos los productos
        all_products = products_df['product_id'].unique()
        
        # Filtrar productos ya comprados
        candidate_products = [p for p in all_products if p not in exclude_purchased]
        
        # Predecir ratings para todos los productos candidatos
        predictions = []
        
        for product_id in candidate_products:
            rating = self.predict_rating(user_id, product_id)
            
            if rating is not None:
                predictions.append({
                    'product_id': product_id,
                    'predicted_rating': rating
                })
        
        # Crear DataFrame y ordenar por rating predicho
        recommendations = pd.DataFrame(predictions)
        recommendations = recommendations.sort_values('predicted_rating', ascending=False)
        recommendations = recommendations.head(top_n)
        
        # Agregar información del producto
        recommendations = recommendations.merge(
            products_df[['product_id', 'product_name', 'category', 'price']],
            on='product_id',
            how='left'
        )
        
        return recommendations
    
    def save_model(self, filepath='models/recommendation_model'):
        """
        Guarda el modelo y encoders
        
        Args:
            filepath: Ruta base para guardar archivos
        """
        
        os.makedirs(filepath, exist_ok=True)
        
        # Guardar modelo Keras
        self.model.save(f'{filepath}/model.keras')
        
        # Guardar encoders
        joblib.dump(self.user_encoder, f'{filepath}/user_encoder.pkl')
        joblib.dump(self.product_encoder, f'{filepath}/product_encoder.pkl')
        
        # Guardar configuración
        config = {
            'n_users': self.n_users,
            'n_products': self.n_products,
            'embedding_dim': self.embedding_dim,
            'saved_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        joblib.dump(config, f'{filepath}/config.pkl')
        
        print(f"💾 Modelo guardado en: {filepath}")
    
    def load_model(self, filepath='models/recommendation_model'):
        """
        Carga el modelo y encoders
        
        Args:
            filepath: Ruta base de archivos guardados
        """
        
        # Cargar modelo Keras
        self.model = keras.models.load_model(f'{filepath}/model.keras')
        
        # Cargar encoders
        self.user_encoder = joblib.load(f'{filepath}/user_encoder.pkl')
        self.product_encoder = joblib.load(f'{filepath}/product_encoder.pkl')
        
        # Cargar configuración
        config = joblib.load(f'{filepath}/config.pkl')
        self.n_users = config['n_users']
        self.n_products = config['n_products']
        self.embedding_dim = config['embedding_dim']
        
        print(f"✅ Modelo cargado desde: {filepath}")


def train_and_save_model():
    """
    Función principal para entrenar y guardar el modelo
    """
    
    print("=" * 60)
    print("🤖 SISTEMA DE RECOMENDACIÓN - ENTRENAMIENTO")
    print("=" * 60)
    
    # Cargar datos
    print("\n📂 Cargando datos...")
    interactions = pd.read_csv('data/interactions.csv')
    products = pd.read_csv('data/products.csv')
    
    print(f"✅ Datos cargados:")
    print(f"   - Interacciones: {len(interactions)}")
    print(f"   - Productos: {len(products)}")
    
    # Crear y entrenar modelo
    model = ProductRecommendationANN(
        n_users=interactions['user_id'].nunique(),
        n_products=interactions['product_id'].nunique(),
        embedding_dim=50
    )
    
    # Entrenar
    history = model.train(
        interactions,
        epochs=30,
        batch_size=64
    )
    
    # Guardar modelo
    model.save_model('models/recommendation_model')
    
    print("\n✨ ¡Entrenamiento completado exitosamente!")
    
    return model, history


if __name__ == "__main__":
    # Crear carpetas necesarias
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Entrenar modelo
    model, history = train_and_save_model()
