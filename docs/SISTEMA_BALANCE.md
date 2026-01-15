# 🛒 Sistema de Balance y Compras - Documentación

## ✨ Funcionalidades Implementadas

### 1. 💰 Sistema de Balance Inicial

- **Saldo Inicial**: Cada usuario tiene un saldo de $3,000.00 USD al registrarse
- **Archivo**: `data/user_balances.csv` almacena los saldos de todos los usuarios
- **Inicialización**: Script `initialize_balances.py` configura saldos para 500 usuarios

### 2. 🛍️ Modal de Compra con Cantidad

Cuando un usuario hace clic en "🛒 Comprar Ahora":

1. **Apertura del Modal**: Se abre una ventana modal con información del producto
2. **Selector de Cantidad**: Input numérico para elegir cuántas unidades comprar (1-100)
3. **Cálculo en Tiempo Real**:
   - Precio unitario del producto
   - Cantidad seleccionada
   - Total a pagar = Precio × Cantidad
   - Saldo actual del usuario
   - Saldo resultante después de la compra

### 3. ✅ Validación de Saldo

El sistema verifica automáticamente si el usuario tiene saldo suficiente:

- **Saldo Suficiente** ✅: Muestra mensaje verde con saldo restante
- **Saldo Insuficiente** ⚠️: Muestra alerta roja indicando el monto faltante
- **Bloqueo de Compra**: No permite confirmar compras sin saldo suficiente

### 4. 💳 Proceso de Compra

Al confirmar la compra:

1. **Validación Final**: Verifica saldo disponible
2. **Registro de Transacción**: Guarda en `data/interactions.csv`
3. **Actualización de Saldo**: Deduce el monto total del saldo del usuario
4. **Confirmación Visual**:
   - Mensaje de éxito con balloons 🎈
   - Muestra el nuevo saldo disponible
   - Recarga la interfaz para mostrar cambios

### 5. 📊 Visualización de Saldo

- **Header Principal**: Muestra saldo actual en tiempo real
- **Formato**: "$X,XXX.XX" con dos decimales
- **Actualización**: Se actualiza después de cada compra

## 🔧 Funciones Técnicas

### `initialize_user_balance(user_id)`

- Inicializa el saldo de un usuario si no existe
- Crea registro con $3,000.00 inicial
- Actualiza archivo CSV

### `get_user_balance(user_id)`

- Obtiene el saldo actual del usuario
- Retorna float con saldo disponible
- Maneja excepciones y retorna $3,000 por defecto

### `update_user_balance(user_id, amount_to_deduct)`

- Deduce monto del saldo del usuario
- Actualiza archivo CSV
- Retorna True/False según éxito

### `save_purchase(user_id, product_id, product_name, category, price, quantity=1)`

- Valida saldo antes de comprar
- Guarda transacción con cantidad
- Actualiza saldo automáticamente
- Retorna tupla (success: bool, message: str)

## 📁 Archivos Modificados

1. **app.py** (Principal)

   - Añadido sistema de balance
   - Implementado modal de cantidad
   - Validaciones de saldo
   - UI mejorada con métricas de saldo

2. **data/user_balances.csv** (Nuevo)

   - Estructura: `user_id, saldo_disponible`
   - 500 usuarios con $3,000 cada uno

3. **initialize_balances.py** (Nuevo)
   - Script de inicialización
   - Configura saldos iniciales

## 🎯 Flujo de Usuario

### Cliente

1. **Login**: Ingresa con nombre de usuario y password "12345"
2. **Ver Saldo**: En header aparece saldo disponible
3. **Explorar Productos**: Tab "Recomendaciones"
4. **Seleccionar Producto**: Click en "🛒 Comprar Ahora"
5. **Modal Aparece**:
   - Seleccionar cantidad (1-100)
   - Ver total y saldo resultante
6. **Validación Visual**:
   - Verde ✅ si tiene saldo
   - Rojo ⚠️ si falta dinero
7. **Confirmar**: Click en "✅ Confirmar Compra"
8. **Resultado**:
   - Mensaje de éxito con balloons
   - Saldo actualizado
   - Producto agregado al historial

### Director

- Puede ver estadísticas de usuarios
- Monitorea compras y patrones
- Acceso completo a analytics

## 🚀 Cómo Usar

### Iniciar la Aplicación

```bash
cd c:\Users\jeanm\Documents\Proyecto_III_Unidad
streamlit run app.py
```

### Acceder

- **URL**: http://localhost:8501
- **Director**:
  - Username: `director`
  - Password: `12345`
- **Clientes**:
  - Username: Cualquier nombre de usuario (ej: "Juan García")
  - Password: `12345`

### Inicializar Saldos (si es necesario)

```bash
python initialize_balances.py
```

## ⚠️ Validaciones Implementadas

1. **Saldo Insuficiente**: No permite comprar si no hay fondos
2. **Cantidad Mínima**: Mínimo 1 producto
3. **Cantidad Máxima**: Máximo 100 productos por transacción
4. **Producto Válido**: Verifica existencia del producto
5. **Usuario Válido**: Verifica autenticación

## 📈 Mejoras Futuras Sugeridas

- [ ] Sistema de recarga de saldo
- [ ] Historial de transacciones con fechas
- [ ] Límites de compra por categoría
- [ ] Descuentos por volumen
- [ ] Sistema de puntos/recompensas
- [ ] Carrito de compras múltiples
- [ ] Método de pago múltiple
- [ ] Exportar historial a PDF

## 🐛 Notas de Depuración

- Los saldos se guardan en CSV y persisten entre sesiones
- El archivo `user_balances.csv` debe existir antes de iniciar
- Si hay errores, ejecutar `initialize_balances.py`
- Los cambios de saldo son inmediatos (sin caché)

---

**Desarrollado con**: Python 3.12, Streamlit, TensorFlow, Pandas
**Última actualización**: 2025-01-13
