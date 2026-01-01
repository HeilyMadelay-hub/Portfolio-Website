# Infrastructure

Configuración de infraestructura para el portfolio chatbot.

## Estructura

```
infrastructure/
├── monitoring/          # Configuración de observabilidad
│   └── prometheus.yml   # Configuración de Prometheus
└── ssl/                 # Certificados SSL (gitignored)
    ├── cert.pem
    └── key.pem
```

## Componentes

### Monitoring (`/monitoring`)
- **prometheus.yml**: Configuración de scraping para métricas del backend

### SSL (`/ssl`)
> ⚠️ **IMPORTANTE**: Los certificados SSL están en `.gitignore` y NO deben ser commiteados.

Para configurar SSL:
1. Coloca tus certificados en `infrastructure/ssl/`
2. Nombra el certificado como `cert.pem` y la llave privada como `key.pem`
3. Estos serán montados automáticamente en nginx vía `docker-compose.yml`

Para desarrollo local, puedes generar certificados autofirmados:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout infrastructure/ssl/key.pem \
  -out infrastructure/ssl/cert.pem
```
