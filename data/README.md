# Data

Directorio de datos persistentes. **Este directorio está en `.gitignore`**.

## Estructura

```
data/
└── chroma/     # Datos de ChromaDB (vectorstore)
```

## ChromaDB

Los datos de ChromaDB se persisten en `data/chroma/` y son montados como volumen en Docker.

### Referencia en docker-compose.yml
```yaml
chromadb:
  volumes:
    - ./data/chroma:/chroma/chroma
```

### Backup
Para hacer backup de los embeddings:
```bash
tar -czvf chroma-backup-$(date +%Y%m%d).tar.gz data/chroma/
```

### Restaurar
```bash
tar -xzvf chroma-backup-YYYYMMDD.tar.gz
```
