## 📝 **README.md para `backend/data/`**

```markdown
# 📁 Backend Data - Contenido para RAG System

Esta carpeta contiene toda la información que será procesada y vectorizada por ChromaDB para el sistema RAG del portfolio.

## 🏗️ Estructura

```
data/
├── documents/          # Documentos con información detallada
│   ├── about_me.md    # Biografía y perfil profesional
│   ├── projects.md    # Proyectos detallados
│   ├── experience.md  # Experiencia laboral
│   ├── skills.md      # Habilidades técnicas
│   ├── education.md   # Formación académica
│   └── articles.md    # Artículos y publicaciones
├── portfolio_context.json  # Configuración del sistema
└── README.md          # Este archivo
```

## 📄 Descripción de Archivos

### `portfolio_context.json`
Archivo de configuración principal que controla:
- Estrategia de chunking (tamaño de fragmentos)
- Metadata del portfolio
- Configuración del RAG
- Mapeo de secciones a archivos

### `documents/about_me.md`
**Contenido:** Información personal y profesional detallada
- Perfil profesional completo
- Motivaciones y filosofía de trabajo
- Historia y background
- Soft skills y personalidad

**Ejemplo de estructura:**
```markdown
# Heily Majtan - Desarrolladora Backend & IA

## Perfil Profesional
[Descripción detallada de 3-4 párrafos]

## Motivación
[Por qué programas, qué te impulsa]

## Trayectoria
[Cómo llegaste a donde estás]
```

### `documents/projects.md`
**Contenido:** Descripción completa de todos los proyectos
- Nombre del proyecto
- Tecnologías utilizadas
- Duración y rol
- Descripción detallada
- Logros y métricas
- Arquitectura y decisiones técnicas

**Ejemplo de estructura:**
```markdown
# Proyectos Destacados

## Sistema RAG para Documentación
**Stack:** Python, FastAPI, ChromaDB
**Duración:** 3 meses
**Rol:** Backend Lead

### Descripción
[Explicación detallada del proyecto]

### Logros
- Métrica 1
- Métrica 2
```

### `documents/experience.md`
**Contenido:** Historial laboral completo
- Empresas donde has trabajado
- Roles y responsabilidades
- Logros en cada posición
- Tecnologías usadas
- Duración en cada puesto

### `documents/skills.md`
**Contenido:** Stack técnico y habilidades
- Lenguajes de programación
- Frameworks y librerías
- Bases de datos
- Herramientas y metodologías
- Nivel de dominio

### `documents/education.md`
**Contenido:** Formación académica y certificaciones
- Títulos universitarios
- Bootcamps
- Certificaciones
- Cursos relevantes
- Idiomas

### `documents/articles.md`
**Contenido:** Artículos y contenido creado
- Títulos de artículos
- Resúmenes
- Enlaces
- Temas tratados

## 💡 Guías de Contenido

### 1. **Sé Específico**
```markdown
❌ MAL: "Trabajé en un proyecto de IA"
✅ BIEN: "Desarrollé un sistema RAG con ChromaDB que procesa 10,000+ documentos con 99.9% uptime"
```

### 2. **Incluye Métricas**
```markdown
✅ "Reduje el tiempo de búsqueda en 80%"
✅ "Manejé 1M+ requests diarios"
✅ "Lideré un equipo de 5 desarrolladores"
```

### 3. **Estructura Clara**
- Usa headers (##, ###) para separar secciones
- Párrafos de 3-5 oraciones
- Listas para logros y tecnologías

### 4. **Extensión Recomendada**
- `about_me.md`: 500-1000 palabras
- `projects.md`: 300-500 palabras por proyecto
- `experience.md`: 200-300 palabras por posición
- Otros archivos: 200-500 palabras

## 🔧 Cómo se Procesa

1. **Chunking**: Cada archivo se divide en fragmentos de ~500 caracteres
2. **Vectorización**: Se crean embeddings de cada fragmento
3. **Metadata**: Se añade información de contexto (sección, fecha, etc.)
4. **Indexación**: Se guarda en ChromaDB para búsqueda semántica

## 📝 Actualización

Para actualizar el contenido:
1. Modifica los archivos `.md` correspondientes
2. Ejecuta `python scripts/populate_db.py`
3. El sistema re-indexará automáticamente

## ⚠️ Importante

- **NO** incluyas información sensible (contraseñas, datos privados)
- **SÍ** incluye información profesional relevante
- **Mantén** el contenido actualizado
- **Usa** Markdown válido para mejor procesamiento

---

Última actualización: [8/8/2025]
```
