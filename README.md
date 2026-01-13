# 🛒 Sistema Inteligente de Recomendación de Productos

Sistema avanzado de recomendación de productos basado en **Redes Neuronales Artificiales (ANN)** con **Collaborative Filtering**, implementado en Python con interfaz interactiva en Streamlit.

## 📋 Descripción

Este proyecto implementa un sistema de recomendación que utiliza embeddings neuronales para aprender patrones complejos de preferencias de usuarios. El modelo predice qué productos podrían gustarle a un usuario basándose en su historial de compras y comportamiento de usuarios similares.

### ✨ Características Principales

- 🧠 **Red Neuronal Multicapa**: Arquitectura profunda con embeddings de 50 dimensiones
- 🎯 **Recomendaciones Personalizadas**: Basadas en historial y preferencias del usuario
- 📊 **Interfaz Interactiva**: Dashboard completo en Streamlit con visualizaciones
- 📈 **Análisis de Perfil**: Estadísticas detalladas de comportamiento del usuario
- 🏷️ **Filtrado por Categorías**: Exploración dirigida de productos
- 💾 **Modelo Persistente**: Sistema de guardado y carga de modelos entrenados

## 🏗️ Arquitectura del Modelo

### Estructura de la Red Neuronal

```
Entrada: [User ID, Product ID]
    ↓
Embedding Layer (Usuario): 50 dimensiones
Embedding Layer (Producto): 50 dimensiones
    ↓
Concatenación: Vector de 100 dimensiones
    ↓
Dense Layer 1: 128 neuronas + ReLU + Dropout (30%)
    ↓
Dense Layer 2: 64 neuronas + ReLU + Dropout (20%)
    ↓
Dense Layer 3: 32 neuronas + ReLU
    ↓
Output Layer: 1 neurona (Rating predicho: 0-5)
```

### Métricas de Evaluación

- **MAE (Mean Absolute Error)**: Error promedio absoluto en las predicciones
- **RMSE (Root Mean Square Error)**: Raíz del error cuadrático medio
- **MSE (Mean Square Error)**: Error cuadrático medio

## 📁 Estructura del Proyecto

```
Proyecto_III_Unidad/
│
├── generate_data.py       # Generador de dataset sintético
├── model.py                # Implementación de la red neuronal
├── app.py                  # Aplicación Streamlit
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
├── data/                  # Datos generados (se crea automáticamente)
│   ├── interactions.csv   # Interacciones usuario-producto
│   ├── products.csv       # Catálogo de productos
│   └── user_stats.csv     # Estadísticas por usuario
│
└── models/                # Modelos entrenados (se crea automáticamente)
    └── recommendation_model/
        ├── model.keras           # Modelo TensorFlow/Keras
        ├── user_encoder.pkl      # Codificador de usuarios
        ├── product_encoder.pkl   # Codificador de productos
        └── config.pkl            # Configuración del modelo
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- 4GB de RAM mínimo recomendado

### Paso 1: Clonar o Descargar el Proyecto

Si tienes Git instalado:

```bash
git clone <url-del-repositorio>
cd Proyecto_III_Unidad
```

### Paso 2: Crear Entorno Virtual (Recomendado)

#### En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### En Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 📊 Uso del Sistema

### 1. Generar Dataset Sintético

Primero, genera los datos de ejemplo:

```bash
python generate_data.py
```

**Salida esperada:**

```
✅ Dataset generado exitosamente!
📊 Usuarios: 500
📦 Productos únicos: 50
🛒 Interacciones: 5000
📈 Categorías: 5
```

Este script creará:

- 500 usuarios con preferencias únicas
- 50 productos en 5 categorías (Electrónica, Ropa, Hogar, Deportes, Libros)
- 5000 interacciones (compras y ratings)

### 2. Entrenar el Modelo

Entrena la red neuronal con los datos generados:

```bash
python model.py
```

**Proceso de entrenamiento:**

1. Carga los datos del paso anterior
2. Prepara y normaliza los datos
3. Construye la arquitectura de la red neuronal
4. Entrena durante 30 épocas con early stopping
5. Evalúa el modelo y muestra métricas
6. Guarda el modelo entrenado

**Tiempo estimado:** 2-5 minutos (depende del hardware)

**Métricas esperadas:**

- MAE: < 0.5
- RMSE: < 0.7

### 3. Ejecutar la Aplicación Streamlit

Inicia la interfaz web interactiva:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🎨 Funcionalidades de la Interfaz

### 🎯 Pestaña "Recomendaciones"

- **Estadísticas del usuario**: Compras realizadas, rating promedio, total gastado
- **Gráfico de categorías favoritas**: Visualización de preferencias
- **Top productos recomendados**: Tarjetas visuales con rating estimado y precio
- **Filtrado por categoría**: Explora recomendaciones específicas

### 📊 Pestaña "Mi Perfil"

- **Distribución de ratings**: Gráfico de barras de tus valoraciones
- **Gasto por categoría**: Gráfico circular del presupuesto por tipo
- **Evolución temporal**: Línea de tiempo de compras mensuales

### 📜 Pestaña "Historial"

- **Lista completa de compras**: Tabla detallada con fechas, productos y montos
- **Exportación a CSV**: Descarga tu historial completo
- **Filtrado y búsqueda**: Explora tu historial de forma eficiente

## 🔬 Detalles Técnicos

### Dataset Sintético

El generador crea datos realistas con las siguientes características:

- **Usuarios**: 500 perfiles con preferencias por 1-3 categorías
- **Productos**: 50 items distribuidos en 5 categorías
- **Ratings**: Escala 1-5, con sesgo hacia categorías favoritas
- **Compras**: Fechas en últimos 6 meses, cantidades 1-3 unidades
- **Precios**: Rango $10 - $500 según tipo de producto

### Modelo de Collaborative Filtering

**Técnica**: Neural Collaborative Filtering (NCF)

El modelo aprende representaciones latentes (embeddings) de usuarios y productos que capturan características implícitas no observables directamente. Estos embeddings se procesan a través de capas densas para predecir ratings.

**Ventajas:**

- Captura relaciones no lineales complejas
- Maneja cold start parcial con generalización
- Escalable a millones de usuarios/productos
- Mejora continua con más datos

### Hiperparámetros

```python
embedding_dim = 50          # Dimensionalidad de embeddings
learning_rate = 0.001       # Tasa de aprendizaje
batch_size = 64             # Tamaño de batch
epochs = 30                 # Épocas máximas (con early stopping)
dropout_rates = [0.3, 0.2]  # Regularización
optimizer = Adam            # Optimizador
loss = MSE                  # Función de pérdida
```

### Proceso de Recomendación

1. **Codificación**: User ID y Product ID → índices numéricos
2. **Embedding**: Índices → vectores densos de 50 dimensiones
3. **Procesamiento**: Concatenación + capas densas
4. **Predicción**: Rating estimado (0-5)
5. **Ranking**: Ordenamiento por rating predicho
6. **Filtrado**: Exclusión de productos ya comprados
7. **Top-N**: Selección de mejores N recomendaciones

## 📈 Posibles Mejoras y Extensiones

### Corto Plazo

- [ ] Agregar filtros de precio
- [ ] Implementar búsqueda de productos
- [ ] Añadir comparación de productos
- [ ] Sistema de feedback en tiempo real

### Mediano Plazo

- [ ] Incorporar features adicionales (texto, imágenes)
- [ ] Implementar modelos híbridos (content + collaborative)
- [ ] Sistema de A/B testing
- [ ] API REST para integraciones

### Largo Plazo

- [ ] Usar transformers para embeddings de texto
- [ ] Recomendaciones en tiempo real con streaming
- [ ] Personalización contextual (hora, ubicación)
- [ ] Explicabilidad avanzada (LIME, SHAP)

## 🐛 Solución de Problemas

### Error: "No module named 'tensorflow'"

```bash
pip install tensorflow==2.15.0
```

### Error: "Model not found"

Asegúrate de ejecutar los scripts en orden:

1. `python generate_data.py`
2. `python model.py`
3. `streamlit run app.py`

### La aplicación Streamlit no carga

Verifica que el puerto 8501 no esté en uso:

```bash
streamlit run app.py --server.port 8502
```

### Rendimiento lento

Reduce el tamaño del dataset en `generate_data.py`:

```python
generate_synthetic_data(n_users=200, n_interactions=2000)
```

## 📚 Referencias y Recursos

### Librerías Utilizadas

- **TensorFlow/Keras**: Framework de deep learning
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **Streamlit**: Framework de interfaces web
- **Plotly**: Visualizaciones interactivas
- **Scikit-learn**: Preprocesamiento y métricas

### Papers Relacionados

- He et al. (2017) - "Neural Collaborative Filtering"
- Koren et al. (2009) - "Matrix Factorization Techniques"
- Rendle (2010) - "Factorization Machines"

### Tutoriales Recomendados

- [TensorFlow Recommenders](https://www.tensorflow.org/recommenders)
- [Collaborative Filtering Guide](https://developers.google.com/machine-learning/recommendation)

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura de Inteligencia Artificial aplicada al Comercio Electrónico.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🙏 Agradecimientos

Gracias a la comunidad de desarrolladores de TensorFlow, Keras y Streamlit por sus excelentes herramientas de código abierto.

---

**¡Disfruta explorando el sistema de recomendación! 🚀**
