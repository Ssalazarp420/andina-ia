"""
Fase 7 - Autenticación compartida para los clientes de OCI Generative AI Inference.

Soporta dos modos vía la variable de entorno OCI_AUTH_MODE:

- "config_file" (default, uso local en la máquina del desarrollador):
  autenticación con API Key + archivo ~/.oci/config + .pem.
- "resource_principal" (uso en producción: Container Instances, OKE, Functions):
  el propio recurso de OCI se autentica solo ante Generative AI Inference,
  sin necesitar distribuir ningún archivo .pem dentro del contenedor.
  Requiere que el recurso esté agregado a un Dynamic Group con una política
  IAM que le dé permiso de uso sobre el servicio Generative AI.
"""

from src.config import settings


def get_oci_auth_kwargs() -> dict:
    """Devuelve los kwargs de autenticación listos para pasarle directo a
    GenerativeAiInferenceClient(**get_oci_auth_kwargs(), ...)."""

    if settings.OCI_AUTH_MODE == "resource_principal":
        from oci.auth.signers import get_resource_principals_signer

        signer = get_resource_principals_signer()
        return {"config": {}, "signer": signer}

    # Modo por defecto: config_file (uso local)
    import oci

    config = oci.config.from_file(settings.OCI_CONFIG_FILE, settings.OCI_CONFIG_PROFILE)
    if settings.OCI_REGION:
        config["region"] = settings.OCI_REGION
    return {"config": config}
