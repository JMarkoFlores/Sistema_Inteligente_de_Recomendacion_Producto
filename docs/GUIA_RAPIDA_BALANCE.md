# 🎯 Guía Rápida - Sistema de Balance

## ✅ Lo que se implementó

### 1. Saldo Inicial: $3,000 por usuario

```
Todos los usuarios comienzan con $3,000.00 USD
```

### 2. Modal de Cantidad

```
Cuando haces clic en "🛒 Comprar Ahora":
→ Se abre ventana modal
→ Puedes elegir cantidad (1-100 unidades)
→ Ves el total a pagar
→ Ves tu saldo actual
→ Ves cuánto te quedará
```

### 3. Validación de Saldo

```
✅ Saldo Suficiente:
   "Saldo suficiente. Quedará: $XXX.XX"
   → Botón Confirmar habilitado

⚠️ Saldo Insuficiente:
   "Saldo insuficiente. Te faltan $XXX.XX"
   → No puedes confirmar la compra
```

### 4. Compra Exitosa

```
Al confirmar:
1. Se valida el saldo nuevamente
2. Se guarda la compra (quantity × precio)
3. Se descuenta del saldo
4. Mensaje: "✅ Compra exitosa de X unidad(es) por $XXX. Saldo restante: $XXX"
5. 🎈 Balloons de celebración
```

### 5. Visualización en Header

```
Header muestra:
🛒 Bienvenido, [Nombre]    |    💰 Saldo Disponible: $X,XXX.XX
```

## 🔍 Ejemplo de Uso

### Caso 1: Compra Normal

```
Usuario: Juan García
Saldo: $3,000.00
Producto: Laptop ($800.00)
Cantidad: 2
Total: $1,600.00

✅ Compra permitida
✅ Nuevo saldo: $1,400.00
```

### Caso 2: Saldo Insuficiente

```
Usuario: María López
Saldo: $500.00
Producto: TV 4K ($1,200.00)
Cantidad: 1
Total: $1,200.00

⚠️ Compra bloqueada
⚠️ Falta: $700.00
```

### Caso 3: Compra Múltiple

```
Usuario: Carlos Pérez
Saldo: $2,000.00
Producto: Mouse ($25.00)
Cantidad: 10
Total: $250.00

✅ Compra permitida
✅ Nuevo saldo: $1,750.00
```

## 📱 Interfaz Visual

```
┌────────────────────────────────────────────────────────────┐
│  🛒 Bienvenido, Juan García        💰 Saldo: $3,000.00    │
└────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Laptop Gaming   │  │  Mouse Gaming    │  │  Teclado Mecánico│
│  💰 $800.00     │  │  💰 $25.00      │  │  💰 $150.00     │
│  ⭐⭐⭐⭐⭐      │  │  ⭐⭐⭐⭐        │  │  ⭐⭐⭐⭐⭐      │
│ [🛒 Comprar]    │  │ [🛒 Comprar]    │  │ [🛒 Comprar]    │
└──────────────────┘  └──────────────────┘  └──────────────────┘

↓ Click en "Comprar"

┌────────────────────────────────────────┐
│  🛒 Comprar: Laptop Gaming            │
│  Precio unitario: $800.00             │
│  Categoría: Electrónica               │
│                                        │
│  Cantidad a comprar: [2] ▲▼           │
│                                        │
│  Total a pagar: $1,600.00             │
│  Saldo actual: $3,000.00              │
│  ✅ Saldo suficiente.                 │
│  Quedará: $1,400.00                   │
│                                        │
│  [✅ Confirmar]    [❌ Cancelar]      │
└────────────────────────────────────────┘
```

## 🚦 Estados del Modal

### Estado 1: Saldo OK

```
╔═══════════════════════════════════════╗
║  Total: $800.00                      ║
║  Saldo: $3,000.00                    ║
║  ✅ Saldo suficiente                 ║
║  Quedará: $2,200.00                  ║
╚═══════════════════════════════════════╝
     Botón Confirmar: HABILITADO
```

### Estado 2: Saldo Insuficiente

```
╔═══════════════════════════════════════╗
║  Total: $3,500.00                    ║
║  Saldo: $3,000.00                    ║
║  ⚠️ Saldo insuficiente               ║
║  Te faltan: $500.00                  ║
╚═══════════════════════════════════════╝
     Usuario puede cancelar o reducir cantidad
```

## 🎮 Controles del Modal

```
Selector de Cantidad:
┌─────────────────────┐
│  Cantidad: [5] ▲▼  │  ← Número editable
└─────────────────────┘
   Min: 1
   Max: 100
   Step: 1

Botones:
[✅ Confirmar Compra]  ← Verde, primario
[❌ Cancelar]          ← Gris, secundario
```

## 📊 Flujo de Datos

```
Usuario Click "Comprar"
        ↓
Modal Aparece con Producto
        ↓
Usuario Selecciona Cantidad
        ↓
Sistema Calcula Total
        ↓
Sistema Consulta Saldo
        ↓
    ┌───────┴───────┐
    │               │
Suficiente    Insuficiente
    │               │
    ↓               ↓
Muestra ✅      Muestra ⚠️
    │               │
Usuario         Usuario
Confirma        Cancela/Ajusta
    │
    ↓
Validar Saldo Final
    ↓
Guardar Compra
    ↓
Descontar Saldo
    ↓
Actualizar UI
    ↓
Mensaje Éxito 🎈
```

## 🔧 Archivos Clave

```
app.py
├── show_client_view()        ← Vista principal del cliente
├── save_purchase()            ← Procesa compras con validación
├── get_user_balance()         ← Obtiene saldo actual
├── update_user_balance()      ← Actualiza saldo
└── initialize_user_balance()  ← Crea saldo si no existe

data/
├── user_balances.csv          ← Archivo de saldos
├── interactions.csv           ← Historial de compras
└── products.csv               ← Catálogo de productos

initialize_balances.py         ← Script de inicialización
```

## 🎯 Pruebas Recomendadas

### Test 1: Compra Normal

1. Login como usuario
2. Ver saldo inicial ($3,000)
3. Comprar 1 producto de $50
4. Verificar saldo ($2,950)

### Test 2: Compra Múltiple

1. Comprar 5 unidades de $100
2. Total: $500
3. Verificar descuento correcto

### Test 3: Saldo Insuficiente

1. Usuario con $100
2. Intentar comprar producto de $200
3. Verificar mensaje de error
4. Verificar que no se procesa

### Test 4: Compra Máxima

1. Seleccionar 100 unidades
2. Ver cálculo correcto
3. Confirmar si hay saldo

### Test 5: Cancelar Compra

1. Abrir modal
2. Click en Cancelar
3. Verificar que no se descuenta nada

---

**🚀 ¡Todo Listo para Usar!**
**URL**: http://localhost:8501
