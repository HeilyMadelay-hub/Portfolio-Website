# MadGPT Frontend

Frontend moderno para el chatbot MadGPT construido con React 18 y Vite.

## 🚀 Tecnologías

- **React 18** - Biblioteca de UI
- **Vite** - Build tool rápido y moderno
- **Framer Motion** - Animaciones fluidas
- **Lucide React** - Iconos modernos
- **Axios** - Cliente HTTP

## 📦 Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Construir para producción
npm run build

# Previsualizar build de producción
npm run preview
```

## 🎨 Características

- ✅ Interfaz moderna estilo Gemini
- ✅ Tema oscuro elegante
- ✅ Componentes React modulares
- ✅ Sin dependencias deprecadas
- ✅ Build optimizado con Vite
- ✅ Hot Module Replacement (HMR)
- ✅ ESLint configurado

## 📁 Estructura del Proyecto

```
src/
├── components/
│   ├── Sidebar/        # Navegación lateral
│   ├── ChatArea/       # Área principal del chat
│   └── MessageInput/   # Input de mensajes
├── App.jsx             # Componente principal
├── App.css            # Estilos globales
├── main.jsx           # Punto de entrada
└── index.css          # Estilos base
```

## 🔧 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo en http://localhost:3000
- `npm run build` - Construye la aplicación para producción
- `npm run preview` - Previsualiza la build de producción
- `npm run lint` - Ejecuta el linter para verificar el código

## 🎯 Próximos Pasos

1. Agregar logo/imagen en el círculo del ChatArea
2. Implementar lógica de chat con backend
3. Agregar autenticación de usuarios
4. Implementar persistencia de conversaciones
5. Agregar más animaciones con Framer Motion

## 📝 Notas

- El proyecto usa Vite en lugar de Create React App para mejor rendimiento
- Todas las dependencias están actualizadas sin warnings de deprecación
- ESLint está configurado para mejores prácticas de React
