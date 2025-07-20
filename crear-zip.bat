@echo off
echo ========================================
echo  Creando ZIP portable del portfolio
echo ========================================
echo.

REM Crear nombre con fecha
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set fecha=%datetime:~0,8%

set zipname=portfolio-heily-%fecha%.zip

echo Preparando archivos para comprimir...
echo (Excluyendo node_modules)
echo.

REM Usar PowerShell para crear ZIP excluyendo node_modules
powershell -Command "Compress-Archive -Path @('index.html','css','js','assets','*.json','*.md','*.bat','.gitignore') -DestinationPath '%zipname%' -Force"

if exist %zipname% (
    echo.
    echo ✅ ZIP creado exitosamente: %zipname%
    echo.
    echo 📦 Contenido del ZIP:
    echo    - Todos los archivos del proyecto
    echo    - SIN node_modules (se instalará con npm install)
    echo.
    echo 🚀 Para usar en otro lugar:
    echo    1. Descomprime el ZIP
    echo    2. Ejecuta start.bat o npm install
    echo.
) else (
    echo ❌ Error al crear el ZIP
)

echo.
pause