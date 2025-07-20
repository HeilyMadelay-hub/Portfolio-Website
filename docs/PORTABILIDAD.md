# 📦 GUÍA DE PORTABILIDAD

## Qué archivos/carpetas COPIAR al mover el proyecto:

### ✅ SÍ copiar:
```
portfolio/
├── index.html
├── css/
├── js/
├── assets/
├── start.bat
├── package.json       # ⚠️ IMPORTANTE: Lista de dependencias
├── package-lock.json  # Versiones exactas
├── README.md
├── .gitignore
└── [futuras carpetas: profesional/, interprete/, creativo/]
```

### ❌ NO copiar:
```
portfolio/
└── node_modules/      # ❌ Muy pesado (100MB+), se regenera con npm install
```

## 🚀 Pasos para mover el proyecto:

### Método 1: Copiar manualmente
1. Selecciona TODO excepto `node_modules`
2. Copia al nuevo directorio
3. Ejecuta `start.bat` o `npm install`

### Método 2: Usando ZIP
```bash
# Crear ZIP sin node_modules (en Windows)
# Selecciona todos los archivos EXCEPTO node_modules
# Click derecho → Enviar a → Carpeta comprimida
```

### Método 3: Usando Git (Recomendado)
```bash
# En el directorio original:
git init
git add .
git commit -m "Portfolio inicial"

# Subir a GitHub (opcional)
git remote add origin https://github.com/tu-usuario/portfolio-heily.git
git push -u origin main

# En cualquier otro lugar:
git clone https://github.com/tu-usuario/portfolio-heily.git
cd portfolio-heily
npm install
```

## 📝 ¿Por qué funciona así?

1. **package.json** = Lista de la compra
   - Dice QUÉ dependencias necesitas
   - Es pequeño (2KB)
   - Se debe copiar SIEMPRE

2. **node_modules** = Los productos comprados
   - Contiene las dependencias instaladas
   - Es MUY pesado (100MB+)
   - Se regenera con `npm install`
   - NO se debe copiar

3. **npm install** = Ir de compras
   - Lee package.json
   - Descarga las dependencias
   - Crea node_modules

## 💡 Analogía simple:

```
📝 package.json    = Receta de cocina (ingredientes)
📦 node_modules    = Ingredientes comprados
🛒 npm install     = Ir al supermercado

Cuando mudas la cocina, llevas la receta, no los ingredientes.
```

---

Por eso el `start.bat` verifica automáticamente si necesitas "ir de compras" 🛒