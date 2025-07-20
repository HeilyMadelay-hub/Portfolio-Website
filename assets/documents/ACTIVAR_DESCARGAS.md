# 🚀 Guía Rápida: Activar Descargas Reales

## 📋 **Checklist para ir a producción:**

### ✅ **1. Preparar archivos PDF:**
```bash
# Crear estos 4 archivos en assets/documents/:
CV_Madelay_ES.pdf                    # ← Tu CV en español
CV_Madelay_EN.pdf                    # ← Tu CV in English
Carta_Recomendacion_Madelay_ES.pdf   # ← Carta de recomendación en español
Motivation_Letter_Madelay_EN.pdf     # ← Motivation letter in English (¡NO traducción!)
```

### ✅ **2. Modificar código en `js/landing.js`:**

#### 🔧 **Función downloadCV() - Líneas ~130-140:**
```javascript
// ❌ COMENTAR ESTA LÍNEA:
// alert(message);

// ✅ DESCOMENTAR ESTAS 3 LÍNEAS:
const link = document.createElement('a');
link.href = `assets/documents/${fileName}`;
link.download = downloadName;
link.click();
```

#### 🔧 **Función downloadRecommendation() - Líneas ~160-170:**
```javascript
// ❌ COMENTAR ESTA LÍNEA:
// alert(message);

// ✅ DESCOMENTAR ESTAS 3 LÍNEAS:
const link = document.createElement('a');
link.href = `assets/documents/${fileName}`;
link.download = downloadName;
link.click();
```

### ✅ **3. Testear funcionamiento:**

#### 🇪🇸 **Prueba en español:**
1. Asegúrate que el portfolio esté en español
2. Click "Descargar CV" → Debe descargar `CV_Madelay_ES.pdf`
3. Click "Carta de Recomendación" → Debe descargar `Carta_Recomendacion_Madelay_ES.pdf`

#### 🇺🇸 **Prueba en inglés:**
1. Cambia idioma a inglés (botón EN)
2. Click "Download CV" → Debe descargar `CV_Madelay_EN.pdf`
3. Click "Motivation Letter" → Debe descargar `Motivation_Letter_Madelay_EN.pdf`

### ✅ **4. Verificar nombres de descarga:**
Los archivos se descargan con nombres simplificados:

| Archivo Original | Se descarga como |
|------------------|-------------------|
| `CV_Madelay_ES.pdf` | `CV_Madelay_ES.pdf` |
| `CV_Madelay_EN.pdf` | `CV_Madelay_EN.pdf` |
| `Carta_Recomendacion_Madelay_ES.pdf` | `Carta_Recomendacion_Madelay.pdf` |
| `Motivation_Letter_Madelay_EN.pdf` | `Motivation_Letter_Madelay.pdf` |

### ✅ **5. Verificar textos de la UI:**
Los botones deben mostrar:

| Idioma | Botón CV | Botón Secundario |
|--------|-----------|------------------|
| 🇪🇸 Español | "Descargar CV" | "Carta de Recomendación" |
| 🇺🇸 Inglés | "Download CV" | "Motivation Letter" |

## 🌐 **Adaptación Cultural Importante:**

### 🇪🇸 **Mercado Hispano:**
- **CV tradicional** + **Carta de Recomendación**
- Valoran referencias de terceros
- Enfoque en experiencia y avales externos

### 🇺🇸 **Mercado Anglosajón:**
- **CV conciso** + **Motivation Letter**
- Valoran automotivación y objetivos personales
- Enfoque en capacidades y ambiciones propias

## 🐛 **Solución de problemas:**

### ❌ **"No se descarga nada"**
- Verifica que el archivo PDF existe en `assets/documents/`
- Revisa que el nombre sea exacto (sensible a mayúsculas)
- Abre la consola del navegador para ver errores

### ❌ **"Descarga archivo con nombre raro"**
- Verifica la variable `downloadName` en el código
- Asegúrate que no hay caracteres especiales

### ❌ **"Botón sigue diciendo 'Recommendation Letter'"**
- Verifica que la traducción se actualizó correctamente
- Recarga la página completamente (Ctrl+F5)
- Revisa que `currentLanguage` se esté actualizando

### ❌ **"Descarga siempre el mismo idioma"**
- Verifica que la variable `currentLanguage` se esté actualizando
- Revisa que cambiar idioma funciona correctamente
- Testea el cambio de idioma antes de probar descargas

## 💡 **Tips adicionales:**

- 📱 **Testea en móvil** - Las descargas funcionan diferente
- 🌐 **Prueba diferentes navegadores** - Chrome, Firefox, Safari
- 📊 **Analytics** - Considera trackear qué idioma se descarga más
- 🔄 **Actualizaciones** - Mantén ambas versiones sincronizadas
- 🎯 **Contenido diferente** - La motivation letter NO debe ser traducción de la carta de recomendación

## 🏆 **Resultado esperado:**

Un sistema que demuestra:
- 🌍 **Comprensión cultural** de diferentes mercados laborales
- 🤖 **Inteligencia UX** que anticipa necesidades del usuario
- 🎯 **Estrategia de hiring** adaptada por región
- ⚙️ **Atención al detalle** técnico y de negocio

---

**🎯 ¡Listo!** Una vez completados estos pasos, tendrás descarga automática culturalmente adaptada funcionando perfectamente.
