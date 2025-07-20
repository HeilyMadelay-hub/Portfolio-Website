# 🌟 Portfolio Heily - Multi-Personalidad

Un portfolio único con tres experiencias diferentes que representan distintos aspectos de mi personalidad como desarrolladora.

## 🎯 Vista General

```
- Landing Principal: Página de entrada con 3 portales animados
- Portfolio Profesional: Estilo minimalista con partículas (Brittany v2)
- Portfolio Intérprete: Con chatbot IA que conoce mi historia
- Portfolio Creativo: Experiencia 3D narrativa
```

## 🚀 Quick Start

### Opción más fácil:
```bash
# Solo haz doble click en:
start.bat
```

### Opción manual:
```bash
# 1. Instalar dependencias (primera vez)
npm install

# 2. Iniciar el servidor
npm run dev:landing
```

El landing estará disponible en `http://localhost:3000`

## 📦 Mover el proyecto a otro directorio

**IMPORTANTE**: Si mueves el proyecto a otro lugar, necesitas reinstalar las dependencias:

```bash
# En el nuevo directorio:
cd C:\tu\nuevo\directorio\portfolio
npm install
npm run dev:landing

# O simplemente ejecuta:
start.bat
```

### ¿Por qué reinstalar?
- La carpeta `node_modules` no se debe copiar (es muy pesada ~100MB)
- Las dependencias se instalan específicamente para cada sistema
- El `start.bat` detecta automáticamente si necesitas instalarlas

### Crear ZIP portable:
```bash
# Doble click en:
crear-zip.bat
```

📖 Ver más detalles en [PORTABILIDAD.md](PORTABILIDAD.md)

## 📁 Estructura

```
portfolio/
├── index.html          # Landing principal
├── css/               # Estilos del landing
├── js/                # Scripts del landing
├── assets/            # Imágenes y recursos
├── start.bat          # Script de inicio automático
├── package.json       # Dependencias del proyecto
├── .gitignore         # Archivos ignorados (incluye node_modules)
├── profesional/       # Portfolio profesional (próximamente)
├── interprete/        # Portfolio con chatbot (próximamente)
└── creativo/          # Portfolio 3D (próximamente)
```

## 🎨 Características del Landing

- ✨ Animación de carga
- 🎴 Efecto de barajado de cartas (presiona 'S')
- 🖱️ Efecto parallax con el mouse
- 📱 Totalmente responsive
- 🎯 Transiciones suaves entre portfolios
- 🌟 Partículas flotantes animadas

## 🛠️ Tecnologías

- HTML5 / CSS3 / JavaScript Vanilla
- Node.js + npm (para el servidor de desarrollo)
- live-server (servidor local con auto-reload)
- Animaciones CSS personalizadas
- Diseño responsive mobile-first

## 💡 Tips

1. **Para desarrollo**: El servidor se recarga automáticamente al guardar cambios
2. **Para producción**: Los archivos están listos para subir a cualquier hosting estático
3. **Sin Node.js**: Puedes abrir `index.html` directamente, pero algunas funciones pueden no funcionar

---

Hecho con ❤️ por Heily