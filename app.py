"""
Punto de entrada principal de L'Éclat AI Colombia.
Inicia el servidor principal conectado a TiDB Cloud (`test`), al Agente de IA
y a la interfaz web con fotos y enlaces directos a productos en Colombia.
Uso:
    python app.py
"""

from servicios.servidor_principal.servidor_api import iniciar_servidor

if __name__ == "__main__":
    iniciar_servidor(8000)
