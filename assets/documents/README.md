# 📁 Documentos para Descarga

Esta carpeta debe contener los documentos PDF que se pueden descargar desde el portfolio.

## 🌐 **DESCARGA INTELIGENTE POR IDIOMA Y CULTURA**

El sistema detecta automáticamente el idioma seleccionado en el portfolio y descarga la versión correspondiente **adaptada culturalmente**:

### 📄 **Archivos requeridos:**

#### 🇪🇸 **Versiones en Español (Mercado Hispano):**
1. **CV_Madelay_ES.pdf** - Curriculum Vitae en español
2. **Carta_Recomendacion_Madelay_ES.pdf** - Carta de recomendación (típico en mercado hispano)

#### 🇺🇸 **Versiones en Inglés (Mercado Anglosajón):**
1. **CV_Madelay_EN.pdf** - Curriculum Vitae in English  
2. **Motivation_Letter_Madelay_EN.pdf** - Carta de motivación (típico en mercado internacional)

### 🎭 **Adaptación Cultural:**

| Mercado | Documento Secundario | Razón Cultural |
|---------|---------------------|------------------|
| 🇪🇸 Hispano | **Carta de Recomendación** | Valoran referencias de terceros |
| 🇺🇸 Anglosajón | **Motivation Letter** | Valoran automotivación y objetivos personales |

### 🔄 **Lógica de Descarga:**

```javascript
// Si el usuario tiene el portfolio en español:
currentLanguage === 'es' → CV_Madelay_ES.pdf + Carta_Recomendacion_Madelay_ES.pdf

// Si el usuario tiene el portfolio en inglés:
currentLanguage === 'en' → CV_Madelay_EN.pdf + Motivation_Letter_Madelay_EN.pdf
```

### 📥 **Nombres de descarga:**

| Idioma | Archivo Original | Nombre al Descargar |
|--------|------------------|---------------------|
| 🇪🇸 ES | `CV_Madelay_ES.pdf` | `CV_Madelay_ES.pdf` |
| 🇺🇸 EN | `CV_Madelay_EN.pdf` | `CV_Madelay_EN.pdf` |
| 🇪🇸 ES | `Carta_Recomendacion_Madelay_ES.pdf` | `Carta_Recomendacion_Madelay.pdf` |
| 🇺🇸 EN | `Motivation_Letter_Madelay_EN.pdf` | `Motivation_Letter_Madelay.pdf` |

## 🔧 **Cómo activar las descargas:**

### 1️⃣ **Agregar los archivos PDF:**
```
assets/documents/
├── CV_Madelay_ES.pdf                    ← CV en español
├── CV_Madelay_EN.pdf                    ← CV in English
├── Carta_Recomendacion_Madelay_ES.pdf   ← Carta de recomendación
├── Motivation_Letter_Madelay_EN.pdf     ← Motivation letter
└── README.md
```

### 2️⃣ **Activar descarga real en el código:**
Ve a `js/landing.js` y descomenta las líneas de descarga:

```javascript
// ✅ DESCOMENTAR ESTAS LÍNEAS:
const link = document.createElement('a');
link.href = `assets/documents/${fileName}`;
link.download = downloadName;
link.click();

// ❌ COMENTAR ESTA LÍNEA:
// alert(message);
```

## 🎯 **Ejemplo de funcionamiento:**

### 🇪🇸 **Usuario en español:**
1. Usuario tiene el portfolio en español
2. **"Descargar CV"** → Descarga `CV_Madelay_ES.pdf`
3. **"Carta de Recomendación"** → Descarga `Carta_Recomendacion_Madelay_ES.pdf`

### 🇺🇸 **Usuario en inglés:**
1. Usuario cambia idioma a inglés
2. **"Download CV"** → Descarga `CV_Madelay_EN.pdf`
3. **"Motivation Letter"** → Descarga `Motivation_Letter_Madelay_EN.pdf`

## 💡 **Ventajas del sistema:**

✅ **Adaptación Cultural Real** - No solo traducción, sino enfoque por mercado
✅ **UX Inteligente** - Sin preguntarle al usuario, sabe qué necesita
✅ **Profesionalismo Internacional** - Demuestra conocimiento de diferentes mercados
✅ **Automático** - Funciona sin intervención manual
✅ **Estrategia de Hiring** - Documentos apropiados para cada mercado laboral

## ⚠️ **Notas importantes:**

- **Nombres exactos**: Los archivos deben tener exactamente estos nombres
- **Contenido diferente**: La motivation letter NO es traducción de la carta de recomendación
- **Estrategia por mercado**: Cada documento diseñado para su mercado objetivo
- **Testeo bilingue**: Verificar ambas versiones funcionan correctamente

## ✨ **Estado actual:**
- ✅ Sistema implementado y funcionando
- ✅ Adaptación cultural automática
- ✅ Detección inteligente de mercado objetivo
- ✅ Textos de UI actualizados ("Motivation Letter" en inglés)
- ⏳ **Pendiente:** Agregar los 4 archivos PDF reales

---

**🎯 Resultado:** Sistema que demuestra comprensión cultural y estrategia de hiring internacional.
