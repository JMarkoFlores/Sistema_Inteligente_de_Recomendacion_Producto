# 🚀 GUÍA DE INICIO RÁPIDO

## Instalación en 3 Pasos

### 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Generar Datos y Entrenar Modelo

```bash
python generate_data.py
python model.py
```

### 3️⃣ Ejecutar Aplicación

```bash
streamlit run app.py
```

## 💡 Comandos Útiles

### Activar Entorno Virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Verificar Instalación

```bash
python --version  # Debe ser 3.8+
pip list
```

### Re-entrenar Modelo

```bash
python model.py
```

### Ejecutar en Puerto Diferente

```bash
streamlit run app.py --server.port 8502
```

## 📊 Estructura de Datos

### interactions.csv

```
user_id, product_id, product_name, category, rating, purchase_count, price, total_spent, purchase_date
1, 5, Auriculares Bluetooth, Electrónica, 5, 1, 45.99, 45.99, 2025-11-23
```

### products.csv

```
product_id, product_name, category, price
1, Laptop HP, Electrónica, 499.99
```

## ⚙️ Configuración

### Ajustar Tamaño de Dataset

En `generate_data.py`, línea 120:

```python
generate_synthetic_data(n_users=500, n_interactions=5000)
# Cambia los números según necesites
```

### Modificar Arquitectura del Modelo

En `model.py`, línea 27:

```python
ProductRecommendationANN(
    n_users=...,
    n_products=...,
    embedding_dim=50  # Cambia dimensión de embeddings
)
```

### Cambiar Número de Épocas

En `model.py`, línea 268:

```python
model.train(interactions, epochs=30)  # Ajusta épocas
```

## 🎯 Uso de la Aplicación

1. **Selecciona tu Usuario**: En el sidebar, elige un ID de usuario (1-500)
2. **Ajusta Recomendaciones**: Usa el slider para cambiar cantidad
3. **Filtra por Categoría**: Explora productos específicos
4. **Revisa tu Perfil**: Ve estadísticas en la pestaña "Mi Perfil"
5. **Consulta Historial**: Revisa compras previas y descarga CSV

## 🐛 Problemas Comunes

### "No such file or directory: 'data/interactions.csv'"

**Solución:** Ejecuta `python generate_data.py` primero

### "Cannot load model"

**Solución:** Ejecuta `python model.py` para entrenar

### Streamlit no inicia

**Solución:** Verifica que instalaste: `pip install streamlit`

### Error de memoria

**Solución:** Reduce `n_users` y `n_interactions` en `generate_data.py`

## 📈 Próximos Pasos

1. ✅ Ejecuta el sistema básico
2. 🔍 Explora diferentes usuarios y sus recomendaciones
3. 📊 Analiza las métricas del modelo
4. 🎨 Personaliza la interfaz modificando `app.py`
5. 🧪 Experimenta con diferentes arquitecturas en `model.py`

## 💬 ¿Necesitas Ayuda?

Revisa el `README.md` completo para documentación detallada.

---

**¡Éxito con tu proyecto! 🎉**
