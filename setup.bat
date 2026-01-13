@echo off
echo ================================================
echo  Sistema de Recomendacion con IA - Setup
echo ================================================
echo.

REM Crear carpetas necesarias
echo [1/5] Creando directorios...
if not exist "data" mkdir data
if not exist "models" mkdir models
echo     OK - Directorios creados
echo.

REM Instalar dependencias
echo [2/5] Instalando dependencias...
echo     (Esto puede tomar varios minutos)
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo     ERROR - Fallo en instalacion de dependencias
    pause
    exit /b 1
)
echo     OK - Dependencias instaladas
echo.

REM Generar datos
echo [3/5] Generando dataset sintetico...
python generate_data.py
if %errorlevel% neq 0 (
    echo     ERROR - Fallo en generacion de datos
    pause
    exit /b 1
)
echo     OK - Dataset generado
echo.

REM Entrenar modelo
echo [4/5] Entrenando modelo de red neuronal...
echo     (Esto puede tomar 2-5 minutos)
python model.py
if %errorlevel% neq 0 (
    echo     ERROR - Fallo en entrenamiento del modelo
    pause
    exit /b 1
)
echo     OK - Modelo entrenado exitosamente
echo.

REM Iniciar aplicacion
echo [5/5] Iniciando aplicacion Streamlit...
echo.
echo ================================================
echo  INSTALACION COMPLETADA!
echo ================================================
echo.
echo  La aplicacion se abrira en tu navegador
echo  URL: http://localhost:8501
echo.
echo  Para detener: Presiona Ctrl+C
echo ================================================
echo.

streamlit run app.py

pause
