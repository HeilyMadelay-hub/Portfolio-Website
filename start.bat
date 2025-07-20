@echo off
echo ========================================
echo  Portfolio Heily - Setup Automatico
echo ========================================
echo.

REM Verificar si node_modules existe
if exist "node_modules\" (
    echo Dependencias ya instaladas ✓
) else (
    echo Instalando dependencias por primera vez...
    echo Esto puede tomar unos minutos...
    npm install
    echo.
    echo ✅ Dependencias instaladas!
)

echo.
echo ========================================
echo  Iniciando servidor en http://localhost:3000
echo  Presiona Ctrl+C para detener
echo ========================================
echo.

npm run dev:landing