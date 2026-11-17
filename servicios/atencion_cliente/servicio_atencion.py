"""
Servicio de Atención Personalizada y Servicio al Cliente — CustomMatch Colombia.
Permite:
1. Consultar el directorio de Asesoras de Belleza / Dermocosmética y canales de contacto
   oficiales en Colombia (WhatsApp directo, Línea Nacional, Correo e Instagram).
2. Crear solicitudes de Atención Personalizada que se guardan en TiDB Cloud (`test`)
   en la tabla `solicitudes_atencion_cliente`, asignando automáticamente una especialista
   según el tema y los datos de piel guardados de la usuaria.
"""
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List
from servicios.base_de_datos.conexion_tidb import conexion_tidb

ARCHIVO_RESPALDO_TICKETS = os.path.join(os.path.dirname(__file__), "respaldo_solicitudes.json")


class ServicioAtencionCliente:
    def __init__(self):
        self._canales_oficiales = self._cargar_canales_contacto()
        self._asesoras = self._cargar_asesoras_especialistas()
        self._solicitudes: List[Dict[str, Any]] = []
        self._cargar_respaldo_local()

    def _cargar_canales_contacto(self) -> Dict[str, Any]:
        return {
            "marca": "CustomMatch Colombia — Atención Personalizada",
            "linea_nacional": "01 8000 415 920",
            "telefono_bogota": "(601) 745 8890",
            "whatsapp_oficial": "+57 300 912 4580",
            "whatsapp_url": "https://wa.me/573009124580?text=Hola%20CustomMatch%20Colombia,%20quiero%20asesor%C3%ADa%20personalizada%20para%20mi%20maquillaje",
            "correo_soporte": "atencion@custommatch.co",
            "instagram": "@custommatch.co",
            "horario_atencion": "Lunes a Sábado: 8:00 a.m. a 8:00 p.m. (Hora Colombia)",
            "sede_principal": "Calle 82 # 12-15, Zona T · Bogotá, Colombia"
        }

    def _cargar_asesoras_especialistas(self) -> List[Dict[str, Any]]:
        return [
            {
                "advisor_id": "ase-col-01",
                "name": "Dra. Mariana Vélez",
                "role": "Especialista en Piel Mixta, Grasa, Acné y Sensibilidad",
                "city": "Bogotá, Colombia",
                "experience": "8 años en Dermocosmética Clínica",
                "specialty_tags": ["acne", "sensibilidad", "piel", "dermocosmetica", "ingredientes"],
                "whatsapp": "+57 300 912 4580",
                "whatsapp_url": "https://wa.me/573009124580?text=Hola%20Dra.%20Mariana%20de%20CustomMatch,%20necesito%20asesor%C3%ADa%20para%20mi%20piel",
                "email": "mariana.velez@custommatch.co",
                "availability": "En línea · Respuesta en < 15 min",
                "avatar_initials": "MV",
                "accent_color": "#b85c6b"
            },
            {
                "advisor_id": "ase-col-02",
                "name": "Laura Restrepo",
                "role": "Maquilladora Senior · Experta en Tonos y Subtono Oliva (MAC, Ani-k, Blush-Bar)",
                "city": "Medellín, Colombia",
                "experience": "6 años en Colorimetría y Visagismo",
                "specialty_tags": ["tono", "subtono", "base", "corrector", "mac", "anik"],
                "whatsapp": "+57 314 680 2310",
                "whatsapp_url": "https://wa.me/573146802310?text=Hola%20Laura%20de%20CustomMatch,%20quiero%20ayuda%20para%20elegir%20mi%20tono%20exacto",
                "email": "laura.restrepo@custommatch.co",
                "availability": "En línea · Asesoría de Tonos",
                "avatar_initials": "LR",
                "accent_color": "#c97b63"
            },
            {
                "advisor_id": "ase-col-03",
                "name": "Valentina Gómez",
                "role": "Coordinadora de Servicio al Cliente, Presupuesto y Tiendas Aliadas",
                "city": "Cali, Colombia",
                "experience": "Especialista en Compras Online y Envíos en Colombia",
                "specialty_tags": ["tienda", "compra", "envio", "precio", "pedido", "soporte"],
                "whatsapp": "+57 318 440 9921",
                "whatsapp_url": "https://wa.me/573184409921?text=Hola%20Valentina%20de%20CustomMatch,%20tengo%20una%20consulta%20de%20servicio%20al%20cliente",
                "email": "valentina.gomez@custommatch.co",
                "availability": "En línea · Soporte Inmediato",
                "avatar_initials": "VG",
                "accent_color": "#9b6b56"
            }
        ]

    def _cargar_respaldo_local(self):
        if os.path.exists(ARCHIVO_RESPALDO_TICKETS):
            try:
                with open(ARCHIVO_RESPALDO_TICKETS, "r", encoding="utf-8") as f:
                    self._solicitudes = json.load(f)
            except Exception:
                self._solicitudes = []

    def _guardar_respaldo_local(self):
        try:
            with open(ARCHIVO_RESPALDO_TICKETS, "w", encoding="utf-8") as f:
                json.dump(self._solicitudes, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def obtener_directorio_atencion(self, email_usuaria: str = "") -> Dict[str, Any]:
        """Retorna los canales de contacto, asesoras y las solicitudes recientes de la usuaria."""
        solicitudes_usuaria = self.listar_solicitudes_usuaria(email_usuaria)
        return {
            "status": "OK",
            "channels": self._canales_oficiales,
            "advisors": self._asesoras,
            "user_tickets": solicitudes_usuaria
        }

    def crear_solicitud_atencion(self, datos: Dict[str, Any], perfil_piel: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Registra una solicitud de atención personalizada en TiDB Cloud (`test`),
        asigna la especialista ideal y genera una respuesta orientativa inmediata.
        """
        nombre = (datos.get("name") or "Usuaria CustomMatch").strip()
        correo = (datos.get("email") or "valeria@leclat.co").strip().lower()
        whatsapp = (datos.get("whatsapp") or "+57 300 000 0000").strip()
        tema = (datos.get("topic") or "Asesoría de TonoExacto (Base / Corrector)").strip()
        mensaje = (datos.get("message") or "").strip()

        if not mensaje:
            return {"status": "ERROR", "message": "Por favor escribe tu consulta o mensaje para nuestra asesora."}

        # Seleccionar la asesora especialista según el tema elegido
        tema_lower = (tema + " " + mensaje).lower()
        if any(k in tema_lower for k in ["acné", "acne", "sensib", "rosácea", "rosacea", "brote", "alergia", "piel"]):
            asesora = self._asesoras[0]  # Dra. Mariana Vélez
        elif any(k in tema_lower for k in ["tienda", "enlace", "compra", "envío", "envio", "pedido", "precio"]):
            asesora = self._asesoras[2]  # Valentina Gómez
        else:
            asesora = self._asesoras[1]  # Laura Restrepo (Experta en Tonos y Subtonos)

        sp = perfil_piel or {"skin_type": "mixta", "skin_tone": "media", "undertone": "oliva"}
        respuesta_inmediata = (
            f"¡Hola {nombre}! Tu solicitud fue asignada a {asesora['name']} ({asesora['role']}). "
            f"Vemos en tu cuenta de CustomMatch tus datos guardados (piel {sp.get('skin_type', 'mixta')}, "
            f"tono {sp.get('skin_tone', 'media')}, subtono {sp.get('undertone', 'oliva')}). "
            f"Te contactaremos al WhatsApp {whatsapp} y al correo {correo} en menos de 15 minutos."
        )

        ticket_id = f"CM-COL-{uuid.uuid4().hex[:6].upper()}"
        nueva_solicitud = {
            "ticket_id": ticket_id,
            "user_email": correo,
            "user_name": nombre,
            "whatsapp_colombia": whatsapp,
            "topic": tema,
            "message": mensaje,
            "assigned_advisor": asesora["name"],
            "advisor_role": asesora["role"],
            "advisor_whatsapp_url": asesora["whatsapp_url"],
            "advisor_response": respuesta_inmediata,
            "status": "EN_ATENCION",
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        }

        self._solicitudes.insert(0, nueva_solicitud)
        self._guardar_respaldo_local()
        guardado_tidb = self._guardar_ticket_en_tidb(nueva_solicitud)

        return {
            "status": "OK",
            "saved_in_tidb": guardado_tidb,
            "ticket": nueva_solicitud,
            "user_tickets": self.listar_solicitudes_usuaria(correo)
        }

    def _guardar_ticket_en_tidb(self, ticket: Dict[str, Any]) -> bool:
        def _op(conn):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO solicitudes_atencion_cliente (
                        ticket_id, user_email, user_name, whatsapp_colombia,
                        topic, message, assigned_advisor, advisor_response, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        ticket["ticket_id"],
                        ticket["user_email"],
                        ticket["user_name"],
                        ticket["whatsapp_colombia"],
                        ticket["topic"],
                        ticket["message"],
                        ticket["assigned_advisor"],
                        ticket["advisor_response"],
                        ticket["status"]
                    )
                )
            return True

        return bool(conexion_tidb.ejecutar_consulta(_op))

    def listar_solicitudes_usuaria(self, email: str = "") -> List[Dict[str, Any]]:
        correo = (email or "").strip().lower()

        def _op(conn):
            with conn.cursor() as cur:
                if correo:
                    cur.execute(
                        """
                        SELECT ticket_id, user_email, user_name, whatsapp_colombia,
                               topic, message, assigned_advisor, advisor_response, status, created_at
                        FROM solicitudes_atencion_cliente
                        WHERE user_email = %s
                        ORDER BY created_at DESC
                        LIMIT 10
                        """,
                        (correo,)
                    )
                else:
                    cur.execute(
                        """
                        SELECT ticket_id, user_email, user_name, whatsapp_colombia,
                               topic, message, assigned_advisor, advisor_response, status, created_at
                        FROM solicitudes_atencion_cliente
                        ORDER BY created_at DESC
                        LIMIT 10
                        """
                    )
                filas = cur.fetchall() or []
                for f in filas:
                    f["created_at"] = str(f.get("created_at") or "")
                return filas

        desde_tidb = conexion_tidb.ejecutar_consulta(_op)
        if desde_tidb is not None and len(desde_tidb) > 0:
            return desde_tidb

        if correo:
            return [s for s in self._solicitudes if s.get("user_email") == correo][:10]
        return self._solicitudes[:10]
