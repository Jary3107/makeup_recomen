import os
import unittest
from servicios.inteligencia_artificial.agente_recomendador import AgenteRecomendadorIA
from servicios.catalogo_maquillaje.catalogo_colombia import ServicioCatalogoColombia
from servicios.gestion_usuarias.servicio_usuarias import ServicioUsuarias
from servicios.atencion_cliente.servicio_atencion import ServicioAtencionCliente
from servicios.servidor_principal.servidor_api import OrquestadorBellezaColombia, CARPETA_INTERFAZ


class PruebasSistemaCustomMatchColombia(unittest.TestCase):
    def setUp(self):
        self.agente_ia = AgenteRecomendadorIA()
        self.catalogo = ServicioCatalogoColombia()
        self.usuarias = ServicioUsuarias()
        self.atencion = ServicioAtencionCliente()
        self.orquestador = OrquestadorBellezaColombia()

    def test_diagnostico_piel_sin_facciones(self):
        res = self.agente_ia.analizar_perfil_piel({
            "skin_type": "mixta",
            "skin_tone": "media",
            "undertone": "oliva",
            "conditions": ["acne", "sensibilidad"]
        })
        self.assertEqual(res["skin_type"], "mixta")
        self.assertEqual(res["undertone"], "oliva")
        self.assertNotIn("api_key", res)
        self.assertTrue(len(res["ai_skin_summary"]) > 20)

    def test_inicio_sesion_recupera_datos_guardados(self):
        res_login = self.orquestador.iniciar_sesion_y_cargar_datos({
            "email": "valeria@leclat.co",
            "password": ""
        })
        self.assertEqual(res_login["status"], "OK")
        usuaria = res_login["user"]
        self.assertIsNotNone(usuaria.get("skin_profile"))
        self.assertEqual(usuaria["skin_profile"]["undertone"], "oliva")
        self.assertGreater(res_login["catalog"]["total_matches"], 0)

    def test_productos_tienen_foto_y_link_directo(self):
        res = self.orquestador.buscar_catalogo_por_datos_y_precio({
            "email": "valeria@leclat.co",
            "query": "",
            "max_price_cop": 200000
        })
        productos = res["catalog"]["products"]
        self.assertGreaterEqual(len(productos), 15)
        for p in productos:
            self.assertTrue(p.get("image_url", "").startswith("/imagenes_productos/"))
            ruta_foto = os.path.join(CARPETA_INTERFAZ, p["image_url"].lstrip("/").replace("/", os.sep))
            self.assertTrue(os.path.exists(ruta_foto), f"Falta foto: {ruta_foto}")
            self.assertTrue(
                "/products/" in p["store_url"]
                or "/producto/" in p["store_url"]
                or p["store_url"].endswith("/p")
            )

    def test_servicio_atencion_personalizada_y_servicio_al_cliente(self):
        info = self.orquestador.obtener_info_atencion_cliente("valeria@leclat.co")
        self.assertEqual(info["status"], "OK")
        self.assertEqual(len(info["advisors"]), 3)
        self.assertIn("CustomMatch", info["channels"]["marca"])

        ticket_res = self.orquestador.registrar_solicitud_atencion({
            "email": "valeria@leclat.co",
            "name": "Valeria Montoya",
            "whatsapp": "+57 310 456 7890",
            "topic": "Duda sobre mi tono exacto de Base o Corrector",
            "message": "Quiero saber si el tono 02 de Ani-k me sirve para subtono oliva."
        })
        self.assertEqual(ticket_res["status"], "OK")
        self.assertTrue(ticket_res["ticket"]["ticket_id"].startswith("CM-COL-"))
        self.assertIn("CustomMatch", ticket_res["ticket"]["advisor_response"])


if __name__ == "__main__":
    unittest.main()
