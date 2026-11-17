"""
Agente de Inteligencia Artificial para Diagnóstico de Piel y Recomendación de Maquillaje.
Lee el proyecto y la clave de API exclusivamente desde variables de entorno (`.env`)
para no exponer secretos en el control de versiones.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from typing import Dict, Any, List
from servicios.base_de_datos.conexion_tidb import cargar_variables_entorno

cargar_variables_entorno()


class AgenteRecomendadorIA:
    def __init__(self, nombre_agente: str = "custommatch-ia-colombia-01"):
        self.worker_id = nombre_agente
        self.vertex_project = os.environ.get("VERTEX_PROJECT", "projects/custommatch-ai")
        self.api_key = os.environ.get("AI_API_KEY", "")

    def _consultar_api_ia(self, texto_prompt: str) -> str:
        if not self.api_key:
            return ""

        id_proyecto = self.vertex_project.replace("projects/", "").strip()
        urls = [
            f"https://aiplatform.googleapis.com/v1/projects/{id_proyecto}/locations/us-central1/publishers/google/models/gemini-1.5-flash:generateContent?key={self.api_key}",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        ]
        cuerpo = json.dumps({
            "contents": [{"parts": [{"text": texto_prompt}]}],
            "generationConfig": {"temperature": 0.35, "maxOutputTokens": 250}
        }).encode("utf-8")

        for url in urls:
            peticion = urllib.request.Request(
                url,
                data=cuerpo,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(peticion, timeout=4.0) as respuesta:
                    datos = json.loads(respuesta.read().decode("utf-8"))
                    candidatos = datos.get("candidates", [])
                    if candidatos:
                        partes = candidatos[0].get("content", {}).get("parts", [])
                        if partes and "text" in partes[0]:
                            return partes[0]["text"].strip()
            except Exception:
                continue
        return ""

    def analizar_perfil_piel(self, datos_piel: Dict[str, Any]) -> Dict[str, Any]:
        skin_type = datos_piel.get("skin_type", "mixta")
        skin_tone = datos_piel.get("skin_tone", "media")
        undertone = datos_piel.get("undertone", "oliva")
        conditions = datos_piel.get("conditions", ["ninguna"])
        if isinstance(conditions, str):
            conditions = [conditions]

        prompt = (
            f"Actúa como dermocosmética experta en Colombia. Analiza este perfil de piel: "
            f"tipo de piel {skin_type}, tono {skin_tone}, subtono {undertone}, "
            f"condiciones {', '.join(conditions)}. "
            f"Escribe en 2 frases qué fórmulas de base, corrector y rubor debe usar."
        )
        resumen_ia = self._consultar_api_ia(prompt)
        if not resumen_ia:
            resumen_ia = self._construir_resumen_experto(skin_type, skin_tone, undertone, conditions)

        return {
            "worker_id": self.worker_id,
            "vertex_project": self.vertex_project,
            "skin_type": skin_type,
            "skin_tone": skin_tone,
            "undertone": undertone,
            "conditions": conditions,
            "ai_skin_summary": resumen_ia,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def generar_consejo_busqueda(
        self,
        perfil_piel: Dict[str, Any],
        termino_busqueda: str,
        categoria: str,
        precio_maximo_cop: int,
        cantidad_resultados: int
    ) -> Dict[str, Any]:
        skin_type = perfil_piel.get("skin_type", "mixta")
        skin_tone = perfil_piel.get("skin_tone", "media")
        undertone = perfil_piel.get("undertone", "oliva")
        conditions = perfil_piel.get("conditions", ["ninguna"])
        if isinstance(conditions, str):
            conditions = [conditions]

        termino = termino_busqueda.strip() if termino_busqueda else (
            categoria if categoria != "todos" else "maquillaje"
        )
        presupuesto_str = f"${int(precio_maximo_cop):,}".replace(",", ".")

        prompt = (
            f"Usuaria con datos guardados: piel {skin_type}, tono {skin_tone}, "
            f"subtono {undertone}, condiciones {', '.join(conditions)}. "
            f"Está buscando '{termino}' con presupuesto máximo de {presupuesto_str}. "
            f"Explica en 2 frases cortas qué características priorizamos para ella."
        )
        consejo = self._consultar_api_ia(prompt)
        if not consejo:
            cond_txt = ", ".join(conditions) if conditions and conditions != ["ninguna"] else "cuidado diario"
            consejo = (
                f"Productos seleccionados para tu piel {skin_type}, tono {skin_tone} y subtono {undertone} ({cond_txt}) "
                f"dentro de tu presupuesto de {presupuesto_str}."
            )

        return {
            "worker_id": self.worker_id,
            "vertex_project": self.vertex_project,
            "api_key_configured": bool(self.api_key),
            "search_term": termino,
            "max_price_cop": int(precio_maximo_cop),
            "formatted_budget_cop": presupuesto_str,
            "advice": consejo
        }

    @staticmethod
    def _construir_resumen_experto(
        skin_type: str,
        skin_tone: str,
        undertone: str,
        conditions: List[str]
    ) -> str:
        mapa_textura = {
            "seca": "texturas hidratantes con ácido hialurónico y escualano que no marquen líneas",
            "mixta": "fórmulas equilibradas oil-free de acabado satinado-natural que controlen el brillo en la zona T",
            "grasa": "fórmulas matificantes de larga duración con niacinamida que regulen el sebo sin obstruir poros",
            "normal": "texturas ligeras de cobertura modulable que realcen la luminosidad natural de la piel"
        }
        mapa_subtono = {
            "oliva": "pigmentos neutros-oliva y dorados suaves que eviten que la base o el corrector oxiden a naranja",
            "calido": "pigmentos dorados, durazno y miel que aporten calidez natural al rostro",
            "frio": "subtonos rosados y neutros-fríos que iluminen sin amarillear",
            "neutro": "tonos beige balanceados que se fundan con el matiz natural de tu piel"
        }
        notas_cond = []
        if "acne" in conditions:
            notas_cond.append("fórmulas 100% no comedogénicas y libres de aceites pesados")
        if "sensibilidad" in conditions or "rosacea" in conditions:
            notas_cond.append("sin fragancias irritantes y con activos calmantes")
        if "poros" in conditions:
            notas_cond.append("polímeros difuminadores que alisen visualmente los poros")

        extra = (
            f" Además, priorizamos {', '.join(notas_cond)}."
            if notas_cond else
            " Todas las recomendaciones están disponibles en tiendas oficiales."
        )
        return (
            f"Perfil guardado para piel {skin_type} de tono {skin_tone} y subtono {undertone}: "
            f"recomendamos {mapa_textura.get(skin_type, mapa_textura['mixta'])}, combinadas con "
            f"{mapa_subtono.get(undertone, mapa_subtono['oliva'])}.{extra}"
        )
