# Infraestructura OCI — Andina IA

Notas y checklist para el despliegue obligatorio en Oracle Cloud Infrastructure (Fase 7).

## Checklist de servicios a utilizar
- [ ] **OCIR (Container Registry):** construir y publicar la imagen Docker.
- [ ] **Cómputo:** elegir entre OCI Compute (VM simple), Container Instances, u OKE.
- [ ] **Object Storage:** bucket para los documentos originales de Andina Bank.
- [ ] **Base de datos vectorial:** Oracle Autonomous Database (AI Vector Search) o Qdrant/Weaviate sobre Compute/OKE.
- [ ] **OCI Vault:** almacenar API keys del LLM/embeddings y credenciales de BD.
- [ ] **VCN + Load Balancer:** red segmentada y balanceo de tráfico.
- [ ] **CI/CD:** OCI DevOps o GitHub Actions para build + deploy automático.

## Comandos de referencia (completar durante la Fase 7)

```bash
# Build de la imagen
docker build -t andina-ia:latest -f docker/Dockerfile .

# Login a OCIR
docker login <region>.ocir.io -u '<tenancy-namespace>/<usuario>' -p '<auth-token>'

# Tag y push
docker tag andina-ia:latest <region>.ocir.io/<tenancy-namespace>/andina-ia:latest
docker push <region>.ocir.io/<tenancy-namespace>/andina-ia:latest
```

## Evidencia de deploy
Una vez desplegado, documentar aquí (y en el README principal):
- URL pública de acceso.
- Capturas de pantalla o video del agente respondiendo en vivo.
