#!/bin/bash

echo "================================================"
echo " Sistema de Recomendación con IA - Setup"
echo "================================================"
echo ""

# Crear carpetas necesarias
echo "[1/5] Creando directorios..."
mkdir -p data
mkdir -p models
echo "    ✓ OK - Directorios creados"
echo ""

# Instalar dependencias
echo "[2/5] Instalando dependencias..."
echo "    (Esto puede tomar varios minutos)"
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "    ✗ ERROR - Fallo en instalación de dependencias"
    exit 1
fi
echo "    ✓ OK - Dependencias instaladas"
echo ""

# Generar datos
echo "[3/5] Generando dataset sintético..."
python3 generate_data.py
if [ $? -ne 0 ]; then
    echo "    ✗ ERROR - Fallo en generación de datos"
    exit 1
fi
echo "    ✓ OK - Dataset generado"
echo ""

# Entrenar modelo
echo "[4/5] Entrenando modelo de red neuronal..."
echo "    (Esto puede tomar 2-5 minutos)"
python3 model.py
if [ $? -ne 0 ]; then
    echo "    ✗ ERROR - Fallo en entrenamiento del modelo"
    exit 1
fi
echo "    ✓ OK - Modelo entrenado exitosamente"
echo ""

# Iniciar aplicación
echo "[5/5] Iniciando aplicación Streamlit..."
echo ""
echo "================================================"
echo " INSTALACIÓN COMPLETADA!"
echo "================================================"
echo ""
echo " La aplicación se abrirá en tu navegador"
echo " URL: http://localhost:8501"
echo ""
echo " Para detener: Presiona Ctrl+C"
echo "================================================"
echo ""

streamlit run app.py
