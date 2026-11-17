"""
Servidor Principal (API Gateway) de CustomMatch Colombia.
Conecta:
1. Base de datos en la nube TiDB Cloud (`servicios/base_de_datos/conexion_tidb.py`)
2. Agente Recomendador con IA (`servicios/inteligencia_artificial/agente_recomendador.py`)
3. Catálogo de Maquillaje de Colombia (`servicios/catalogo_maquillaje/catalogo_colombia.py`)
4. Gestión de Usuarias y Perfiles Guardados (`servicios/gestion_usuarias/servicio_usuarias.py`)
5. Servicio de Atención Personalizada y Servicio al Cliente (`servicios/atencion_cliente/servicio_atencion.py`)
6. Interfaz Web y Fotos de Productos (`interfaz_web/` e `interfaz_web/imagenes_productos/`)
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from servicios.base_de_datos.conexion_tidb import conexion_tidb
from servicios.inteligencia_artificial.agente_recomendador import AgenteRecomendadorIA
from servicios.catalogo_maquillaje.catalogo_colombia import ServicioCatalogoColombia
from servicios.gestion_usuarias.servicio_usuarias import ServicioUsuarias
from servicios.atencion_cliente.servicio_atencion import ServicioAtencionCliente

CARPETA_INTERFAZ = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "interfaz_web")
)


class OrquestadorBellezaColombia:
    def __init__(self):
        self.agente_ia = AgenteRecomendadorIA(nombre_agente="custommatch-ia-colombia-01")
        self.servicio_catalogo = ServicioCatalogoColombia()
        self.servicio_usuarias = ServicioUsuarias()
        self.servicio_atencion = ServicioAtencionCliente()

        self.tidb_listo = conexion_tidb.inicializar_tablas()
        if self.tidb_listo:
            self.servicio_usuarias.sincronizar_usuaria_demo_en_tidb()
            self.servicio_catalogo.sincronizar_catalogo_en_tidb()

    def registrar_usuaria_con_piel(self, datos: dict) -> dict:
        datos_piel = {
            "skin_type": datos.get("skin_type", "mixta"),
            "skin_tone": datos.get("skin_tone", "media"),
            "undertone": datos.get("undertone", "oliva"),
            "conditions": datos.get("conditions", ["ninguna"]),
            "last_max_price_cop": int(datos.get("max_price_cop", 190000))
        }
        diagnostico_ia = self.agente_ia.analizar_perfil_piel(datos_piel)
        perfil_piel = {
            "skin_type": datos_piel["skin_type"],
            "skin_tone": datos_piel["skin_tone"],
            "undertone": datos_piel["undertone"],
            "conditions": datos_piel["conditions"],
            "last_max_price_cop": datos_piel["last_max_price_cop"],
            "ai_skin_summary": diagnostico_ia["ai_skin_summary"]
        }
        res_registro = self.servicio_usuarias.registrar_usuaria(
            name=datos.get("name", ""),
            email=datos.get("email", ""),
            password=datos.get("password", ""),
            city=datos.get("city", "Bogotá, Colombia"),
            skin_profile=perfil_piel
        )
        if res_registro.get("status") != "OK":
            return res_registro

        res_catalogo = self.servicio_catalogo.buscar_y_recomendar(
            skin_profile=perfil_piel,
            max_price_cop=datos_piel["last_max_price_cop"],
            query="",
            category="todos"
        )
        consejo_ia = self.agente_ia.generar_consejo_busqueda(
            perfil_piel=perfil_piel,
            termino_busqueda="Catálogo completo para tu piel",
            categoria="todos",
            precio_maximo_cop=datos_piel["last_max_price_cop"],
            cantidad_resultados=res_catalogo["total_matches"]
        )
        return {
            "status": "OK",
            "saved_in_tidb": res_registro.get("saved_in_tidb", False),
            "user": res_registro["user"],
            "ai_advice": consejo_ia,
            "catalog": res_catalogo
        }

    def iniciar_sesion_y_cargar_datos(self, datos: dict) -> dict:
        res_login = self.servicio_usuarias.iniciar_sesion(
            email=datos.get("email", ""),
            password=datos.get("password", "")
        )
        if res_login.get("status") != "OK":
            return res_login

        usuaria = res_login["user"]
        perfil_piel = usuaria.get("skin_profile") or {
            "skin_type": "mixta",
            "skin_tone": "media",
            "undertone": "oliva",
            "conditions": ["ninguna"],
            "last_max_price_cop": 190000,
            "ai_skin_summary": "Perfil cutáneo recuperado de tu cuenta."
        }
        precio_max = int(perfil_piel.get("last_max_price_cop", 190000))

        res_catalogo = self.servicio_catalogo.buscar_y_recomendar(
            skin_profile=perfil_piel,
            max_price_cop=precio_max,
            query="",
            category="todos"
        )
        consejo_ia = self.agente_ia.generar_consejo_busqueda(
            perfil_piel=perfil_piel,
            termino_busqueda="Tus recomendaciones guardadas",
            categoria="todos",
            precio_maximo_cop=precio_max,
            cantidad_resultados=res_catalogo["total_matches"]
        )
        return {
            "status": "OK",
            "loaded_from_tidb": res_login.get("loaded_from_tidb", False),
            "user": usuaria,
            "ai_advice": consejo_ia,
            "catalog": res_catalogo
        }

    def actualizar_perfil_piel_guardado(self, datos: dict) -> dict:
        correo = datos.get("email", "").strip().lower()
        precio_max = int(datos.get("max_price_cop", 190000))
        datos_piel = {
            "skin_type": datos.get("skin_type", "mixta"),
            "skin_tone": datos.get("skin_tone", "media"),
            "undertone": datos.get("undertone", "oliva"),
            "conditions": datos.get("conditions", ["ninguna"]),
            "last_max_price_cop": precio_max
        }
        diagnostico_ia = self.agente_ia.analizar_perfil_piel(datos_piel)
        perfil_piel = {
            "skin_type": datos_piel["skin_type"],
            "skin_tone": datos_piel["skin_tone"],
            "undertone": datos_piel["undertone"],
            "conditions": datos_piel["conditions"],
            "last_max_price_cop": precio_max,
            "ai_skin_summary": diagnostico_ia["ai_skin_summary"]
        }
        res_guardado = self.servicio_usuarias.guardar_perfil_piel(correo, perfil_piel)
        if res_guardado.get("status") != "OK":
            return res_guardado

        res_catalogo = self.servicio_catalogo.buscar_y_recomendar(
            skin_profile=perfil_piel,
            max_price_cop=precio_max,
            query=datos.get("query", ""),
            category=datos.get("category", "todos")
        )
        consejo_ia = self.agente_ia.generar_consejo_busqueda(
            perfil_piel=perfil_piel,
            termino_busqueda=datos.get("query", "") or "Perfil actualizado",
            categoria=datos.get("category", "todos"),
            precio_maximo_cop=precio_max,
            cantidad_resultados=res_catalogo["total_matches"]
        )
        return {
            "status": "OK",
            "saved_in_tidb": res_guardado.get("saved_in_tidb", False),
            "user": res_guardado["user"],
            "ai_advice": consejo_ia,
            "catalog": res_catalogo
        }

    def buscar_catalogo_por_datos_y_precio(self, datos: dict) -> dict:
        correo = (datos.get("email") or "").strip().lower()
        usuaria = self.servicio_usuarias.obtener_usuaria(correo) if correo else None

        if usuaria and usuaria.get("skin_profile"):
            perfil_piel = usuaria["skin_profile"]
        else:
            perfil_piel = {
                "skin_type": datos.get("skin_type", "mixta"),
                "skin_tone": datos.get("skin_tone", "media"),
                "undertone": datos.get("undertone", "oliva"),
                "conditions": datos.get("conditions", ["acne", "sensibilidad"])
            }

        precio_max = int(
            datos.get("max_price_cop")
            or perfil_piel.get("last_max_price_cop")
            or 190000
        )
        if correo and usuaria:
            self.servicio_usuarias.actualizar_ultimo_presupuesto(correo, precio_max)

        query = datos.get("query", "")
        category = datos.get("category", "todos")
        store_filter = datos.get("store_filter", "todas")

        res_catalogo = self.servicio_catalogo.buscar_y_recomendar(
            skin_profile=perfil_piel,
            max_price_cop=precio_max,
            query=query,
            category=category,
            store_filter=store_filter
        )
        consejo_ia = self.agente_ia.generar_consejo_busqueda(
            perfil_piel=perfil_piel,
            termino_busqueda=query,
            categoria=category,
            precio_maximo_cop=precio_max,
            cantidad_resultados=res_catalogo["total_matches"]
        )
        return {
            "status": "OK",
            "ai_advice": consejo_ia,
            "catalog": res_catalogo
        }

    def obtener_info_atencion_cliente(self, email: str = "") -> dict:
        return self.servicio_atencion.obtener_directorio_atencion(email)

    def registrar_solicitud_atencion(self, datos: dict) -> dict:
        correo = (datos.get("email") or "valeria@leclat.co").strip().lower()
        usuaria = self.servicio_usuarias.obtener_usuaria(correo)
        perfil_piel = usuaria.get("skin_profile") if usuaria else None
        return self.servicio_atencion.crear_solicitud_atencion(datos, perfil_piel)


orquestador = OrquestadorBellezaColombia()


class ManejadorSolicitudesHTTP(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _agregar_cabeceras_seguridad(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")

    def _enviar_json(self, codigo: int, datos: dict):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self._agregar_cabeceras_seguridad()
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _servir_archivo(self, ruta_relativa: str, tipo_contenido: str):
        ruta_completa = os.path.abspath(os.path.join(CARPETA_INTERFAZ, ruta_relativa))
        if not ruta_completa.startswith(CARPETA_INTERFAZ) or not os.path.exists(ruta_completa):
            self.send_error(404, "Archivo no encontrado")
            return
        with open(ruta_completa, "rb") as f:
            contenido = f.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo_contenido)
        self._agregar_cabeceras_seguridad()
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def _leer_cuerpo(self) -> dict:
        longitud = int(self.headers.get("Content-Length", 0))
        crudo = self.rfile.read(longitud).decode("utf-8") if longitud > 0 else "{}"
        return json.loads(crudo)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._servir_archivo("index.html", "text/html; charset=utf-8")
        elif parsed.path in ("/estilos.css", "/styles.css"):
            self._servir_archivo("estilos.css", "text/css; charset=utf-8")
        elif parsed.path in ("/logica_interfaz.js", "/app.js"):
            self._servir_archivo("logica_interfaz.js", "application/javascript; charset=utf-8")
        elif parsed.path.startswith("/imagenes_productos/"):
            nombre_img = os.path.basename(parsed.path)
            mime = "image/svg+xml; charset=utf-8" if nombre_img.endswith(".svg") else "image/jpeg"
            self._servir_archivo(os.path.join("imagenes_productos", nombre_img), mime)
        elif parsed.path == "/api/v1/support/info":
            qs = parse_qs(parsed.query)
            email = qs.get("email", [""])[0]
            self._enviar_json(200, orquestador.obtener_info_atencion_cliente(email))
        elif parsed.path == "/api/v1/health":
            self._enviar_json(200, {
                "platform": "CustomMatch Colombia",
                "status": "HEALTHY",
                "tidb_cloud": conexion_tidb.obtener_estado()
            })
        else:
            self.send_error(404, "Ruta no encontrada")

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            datos = self._leer_cuerpo()
            if parsed.path == "/api/v1/auth/register":
                res = orquestador.registrar_usuaria_con_piel(datos)
                codigo = 200 if res.get("status") == "OK" else 400
                self._enviar_json(codigo, res)
            elif parsed.path == "/api/v1/auth/login":
                res = orquestador.iniciar_sesion_y_cargar_datos(datos)
                codigo = 200 if res.get("status") == "OK" else 400
                self._enviar_json(codigo, res)
            elif parsed.path == "/api/v1/profile/update-skin":
                res = orquestador.actualizar_perfil_piel_guardado(datos)
                codigo = 200 if res.get("status") == "OK" else 400
                self._enviar_json(codigo, res)
            elif parsed.path == "/api/v1/catalog/search":
                res = orquestador.buscar_catalogo_por_datos_y_precio(datos)
                self._enviar_json(200, res)
            elif parsed.path == "/api/v1/support/create":
                res = orquestador.registrar_solicitud_atencion(datos)
                codigo = 200 if res.get("status") == "OK" else 400
                self._enviar_json(codigo, res)
            else:
                self._enviar_json(404, {"error": "Endpoint no encontrado"})
        except Exception as exc:
            self._enviar_json(500, {"status": "ERROR", "message": str(exc)})


def iniciar_servidor(puerto: int = 8000, host: str = "127.0.0.1"):
    servidor = ThreadingHTTPServer((host, int(puerto)), ManejadorSolicitudesHTTP)
    print(f"CustomMatch Colombia corriendo en http://{host}:{puerto}")
    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
