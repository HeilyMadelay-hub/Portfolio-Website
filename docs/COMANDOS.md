# 🎯 COMANDOS RÁPIDOS

## 🚀 Iniciar el proyecto
```bash
# Opción 1: Doble click
start.bat

# Opción 2: Manual
npm install          # Primera vez
npm run dev:landing  # Iniciar servidor
```

## 📦 Portabilidad
```bash
# Crear ZIP sin node_modules
crear-zip.bat

# O manualmente
# Copiar todo EXCEPTO node_modules/
```

## ⌨️ Atajos del Landing

- **`S`** = Barajar las cartas
- **Mouse** = Efecto parallax
- **Hover** = Voltear cartas
- **Click** = Entrar al portfolio

## 🛠️ Estructura de archivos

```
ARCHIVOS PRINCIPALES:
├── start.bat          → Inicia el proyecto automáticamente
├── crear-zip.bat      → Crea ZIP portable
├── package.json       → Lista de dependencias (NO BORRAR)
└── index.html         → Página principal

CARPETAS:
├── css/               → Estilos
├── js/                → JavaScript
├── assets/            → Imágenes
└── node_modules/      → Dependencias (NO COPIAR)
```

## 🔧 Solución de problemas

### El servidor no inicia
```bash
# Verificar Node.js
node --version       # Debe mostrar v14 o superior
npm --version        # Debe mostrar v6 o superior

# Reinstalar dependencias
rm -rf node_modules  # O borrar carpeta manualmente
npm install
```

### La página está en negro
- Espera 0.8 segundos (animación de carga)
- Refresca con F5
- Verifica la consola (F12)

### Las cartas no se mueven
- El efecto parallax requiere mover el mouse
- En móvil, toca las cartas para voltearlas

## 📱 Desarrollo móvil

Para probar en tu celular:
1. Conecta el celular a la misma red WiFi
2. Busca tu IP local: `ipconfig`
3. En el celular: `http://TU-IP:3000`

---
💡 Consejo: Abre la consola (F12) para ver mensajes ocultos 🎮