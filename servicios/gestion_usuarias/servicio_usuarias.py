"""
Servicio de Registro e Inicio de Sesión de Usuarias con Perfil de Piel Guardado en TiDB Cloud.
Cuando la usuaria se registra o inicia sesión, sus datos de piel (tipo, tono, subtono y
condiciones) quedan guardados en TiDB Cloud (`test`) para no volver a preguntarle el cuestionario.
"""
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from servicios.base_de_datos.conexion_tidb import conexion_tidb

ARCHIVO_RESPALDO = os.path.join(os.path.dirname(__file__), "respaldo_usuarias.json")


class ServicioUsuarias:
    def __init__(self):
        self._usuarias: Dict[str, Dict[str, Any]] = {}
        self._cargar_respaldo_local()

    def _cargar_respaldo_local(self):
        if os.path.exists(ARCHIVO_RESPALDO):
            try:
                with open(ARCHIVO_RESPALDO, "r", encoding="utf-8") as f:
                    self._usuarias = json.load(f)
            except Exception:
                self._usuarias = {}

        if "valeria@leclat.co" not in self._usuarias:
            self._usuarias["valeria@leclat.co"] = {
                "user_id": "usr-col-001",
                "name": "Valeria Montoya",
                "email": "valeria@leclat.co",
                "city": "Bogotá, Colombia",
                "password_hash": self._encriptar_clave("belleza123"),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "skin_profile": {
                    "skin_type": "mixta",
                    "skin_tone": "media",
                    "undertone": "oliva",
                    "conditions": ["acne", "sensibilidad"],
                    "last_max_price_cop": 190000,
                    "ai_skin_summary": (
                        "Piel mixta de tono medio y subtono oliva con tendencia a acné y sensibilidad. "
                        "Se priorizan bases y correctores oil-free, no comedogénicos y con pigmentos "
                        "neutros-oliva que no oxiden a naranja."
                    ),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
            }
            self._guardar_respaldo_local()

    def _guardar_respaldo_local(self):
        try:
            with open(ARCHIVO_RESPALDO, "w", encoding="utf-8") as f:
                json.dump(self._usuarias, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @staticmethod
    def _encriptar_clave(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def sincronizar_usuaria_demo_en_tidb(self):
        demo = self._usuarias.get("valeria@leclat.co")
        if demo:
            self._guardar_en_tidb(demo)

    def _guardar_en_tidb(self, usuaria: Dict[str, Any]) -> bool:
        def _op(conn):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO registered_users (user_id, full_name, email, city_colombia, password_hash)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        full_name = VALUES(full_name),
                        city_colombia = VALUES(city_colombia)
                    """,
                    (
                        usuaria["user_id"],
                        usuaria["name"],
                        usuaria["email"],
                        usuaria.get("city", "Bogotá, Colombia"),
                        usuaria["password_hash"]
                    )
                )
                sp = usuaria.get("skin_profile")
                if sp and sp.get("skin_type"):
                    cur.execute(
                        """
                        INSERT INTO user_skin_profiles (
                            user_id, skin_type, skin_tone, undertone,
                            conditions_json, last_max_price_cop, ai_skin_summary
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            skin_type = VALUES(skin_type),
                            skin_tone = VALUES(skin_tone),
                            undertone = VALUES(undertone),
                            conditions_json = VALUES(conditions_json),
                            last_max_price_cop = VALUES(last_max_price_cop),
                            ai_skin_summary = VALUES(ai_skin_summary)
                        """,
                        (
                            usuaria["user_id"],
                            sp["skin_type"],
                            sp["skin_tone"],
                            sp["undertone"],
                            json.dumps(sp.get("conditions", []), ensure_ascii=False),
                            int(sp.get("last_max_price_cop", 190000)),
                            sp.get("ai_skin_summary", "")
                        )
                    )
            return True

        return bool(conexion_tidb.ejecutar_consulta(_op))

    def _consultar_usuaria_en_tidb(self, email: str) -> Optional[Dict[str, Any]]:
        def _op(conn):
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.user_id, u.full_name, u.email, u.city_colombia, u.password_hash, u.created_at,
                        p.skin_type, p.skin_tone, p.undertone, p.conditions_json,
                        p.last_max_price_cop, p.ai_skin_summary, p.updated_at
                    FROM registered_users u
                    LEFT JOIN user_skin_profiles p ON u.user_id = p.user_id
                    WHERE u.email = %s
                    LIMIT 1
                    """,
                    (email,)
                )
                fila = cur.fetchone()
                if not fila:
                    return None
                perfil_piel = None
                if fila.get("skin_type"):
                    conds = fila.get("conditions_json")
                    if isinstance(conds, str):
                        try:
                            conds = json.loads(conds)
                        except Exception:
                            conds = ["ninguna"]
                    elif not isinstance(conds, list):
                        conds = ["ninguna"]
                    perfil_piel = {
                        "skin_type": fila["skin_type"],
                        "skin_tone": fila["skin_tone"],
                        "undertone": fila["undertone"],
                        "conditions": conds,
                        "last_max_price_cop": int(fila.get("last_max_price_cop") or 190000),
                        "ai_skin_summary": fila.get("ai_skin_summary") or "",
                        "updated_at": str(fila.get("updated_at") or datetime.now(timezone.utc).isoformat())
                    }
                return {
                    "user_id": fila["user_id"],
                    "name": fila["full_name"],
                    "email": fila["email"],
                    "city": fila.get("city_colombia") or "Bogotá, Colombia",
                    "password_hash": fila["password_hash"],
                    "created_at": str(fila.get("created_at") or datetime.now(timezone.utc).isoformat()),
                    "skin_profile": perfil_piel
                }

        return conexion_tidb.ejecutar_consulta(_op)

    def registrar_usuaria(
        self,
        name: str,
        email: str,
        password: str,
        city: str = "Bogotá, Colombia",
        skin_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        correo = email.strip().lower()
        if not correo or not name.strip():
            return {"status": "ERROR", "message": "Debes ingresar nombre y correo electrónico."}

        existente_tidb = self._consultar_usuaria_en_tidb(correo)
        if existente_tidb or correo in self._usuarias:
            return {"status": "ERROR", "message": "El correo ya está registrado. Inicia sesión con tu cuenta."}

        nueva = {
            "user_id": f"usr-col-{uuid.uuid4().hex[:8]}",
            "name": name.strip(),
            "email": correo,
            "city": city.strip() or "Bogotá, Colombia",
            "password_hash": self._encriptar_clave(password or "123456"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "skin_profile": skin_profile
        }
        self._usuarias[correo] = nueva
        self._guardar_respaldo_local()
        guardado_tidb = self._guardar_en_tidb(nueva)

        return {
            "status": "OK",
            "saved_in_tidb": guardado_tidb,
            "user": self._datos_publicos(nueva)
        }

    def iniciar_sesion(self, email: str, password: str) -> Dict[str, Any]:
        correo = email.strip().lower()
        usuaria_tidb = self._consultar_usuaria_en_tidb(correo)
        if usuaria_tidb:
            self._usuarias[correo] = usuaria_tidb
            self._guardar_respaldo_local()
            usuaria = usuaria_tidb
        else:
            usuaria = self._usuarias.get(correo)

        if not usuaria:
            return {"status": "ERROR", "message": "Usuaria no encontrada. Regístrate primero."}

        if password and usuaria["password_hash"] != self._encriptar_clave(password):
            return {"status": "ERROR", "message": "Contraseña incorrecta."}

        return {
            "status": "OK",
            "loaded_from_tidb": usuaria_tidb is not None,
            "user": self._datos_publicos(usuaria)
        }

    def guardar_perfil_piel(self, email: str, datos_piel: Dict[str, Any]) -> Dict[str, Any]:
        correo = email.strip().lower()
        usuaria_tidb = self._consultar_usuaria_en_tidb(correo)
        if usuaria_tidb:
            self._usuarias[correo] = usuaria_tidb

        usuaria = self._usuarias.get(correo)
        if not usuaria:
            return {"status": "ERROR", "message": "Usuaria no encontrada."}

        datos_piel["updated_at"] = datetime.now(timezone.utc).isoformat()
        usuaria["skin_profile"] = datos_piel
        self._guardar_respaldo_local()
        guardado_tidb = self._guardar_en_tidb(usuaria)

        return {
            "status": "OK",
            "saved_in_tidb": guardado_tidb,
            "user": self._datos_publicos(usuaria)
        }

    def actualizar_ultimo_presupuesto(self, email: str, max_price_cop: int) -> None:
        correo = email.strip().lower()
        usuaria = self._usuarias.get(correo)
        if usuaria and usuaria.get("skin_profile"):
            usuaria["skin_profile"]["last_max_price_cop"] = int(max_price_cop)
            self._guardar_respaldo_local()
            self._guardar_en_tidb(usuaria)

    def obtener_usuaria(self, email: str) -> Optional[Dict[str, Any]]:
        correo = email.strip().lower()
        usuaria_tidb = self._consultar_usuaria_en_tidb(correo)
        if usuaria_tidb:
            self._usuarias[correo] = usuaria_tidb
            self._guardar_respaldo_local()
            return self._datos_publicos(usuaria_tidb)
        usuaria = self._usuarias.get(correo)
        return self._datos_publicos(usuaria) if usuaria else None

    @staticmethod
    def _datos_publicos(usuaria: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "user_id": usuaria["user_id"],
            "name": usuaria["name"],
            "email": usuaria["email"],
            "city": usuaria.get("city", "Bogotá, Colombia"),
            "created_at": usuaria["created_at"],
            "skin_profile": usuaria.get("skin_profile")
        }
