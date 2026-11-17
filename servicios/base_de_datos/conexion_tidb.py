"""
Módulo de Conexión Segura a la Base de Datos en la Nube (TiDB Cloud).
Todas las credenciales se leen exclusivamente desde variables de entorno (`.env`),
evitando exponer usuarios, hosts o contraseñas en el repositorio.
"""

import os
import ssl
from pathlib import Path
from typing import Any, Callable, Dict, Optional

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
ARCHIVO_ENV = RAIZ_PROYECTO / ".env"
ARCHIVO_SQL_INICIAL = RAIZ_PROYECTO / "base_de_datos_sql" / "crear_tablas_tidb.sql"


def cargar_variables_entorno() -> None:
    if not ARCHIVO_ENV.exists():
        return
    for linea in ARCHIVO_ENV.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        valor = valor.strip().strip('"').strip("'")
        if clave:
            os.environ[clave] = valor


cargar_variables_entorno()


class ConectorTiDBCloud:
    """
    Gestiona la conexión segura mediante SSL/TLS y consultas SQL parametrizadas
    hacia TiDB Cloud (previniendo inyección SQL y fugas de credenciales).
    """

    _config: Dict[str, Any] = {
        "host": os.environ.get("TIDB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("TIDB_PORT", "4000")),
        "user": os.environ.get("TIDB_USER", "root"),
        "password": os.environ.get("TIDB_PASSWORD", ""),
        "database": os.environ.get("TIDB_DATABASE", "test"),
        "ssl": os.environ.get("TIDB_SSL", "true").lower() in ("true", "1", "yes"),
    }
    _conectado: bool = False
    _ultimo_mensaje: str = "Esperando conexión a TiDB Cloud..."

    @classmethod
    def obtener_conexion(cls, incluir_bd: bool = True):
        import pymysql

        parametros: Dict[str, Any] = {
            "host": cls._config["host"],
            "port": int(cls._config["port"]),
            "user": cls._config["user"],
            "password": cls._config["password"],
            "charset": "utf8mb4",
            "connect_timeout": 6,
            "autocommit": True,
            "cursorclass": pymysql.cursors.DictCursor,
        }
        if incluir_bd:
            parametros["database"] = cls._config["database"]
        if cls._config.get("ssl"):
            contexto_ssl = ssl.create_default_context()
            parametros["ssl"] = contexto_ssl
        return pymysql.connect(**parametros)

    @classmethod
    def inicializar_tablas(cls) -> bool:
        """Crea las tablas en TiDB Cloud y asegura la columna `image_url`."""
        if not cls._config.get("password"):
            cls._conectado = False
            cls._ultimo_mensaje = "Modo Respaldo Local Activo (Sin credenciales en .env)"
            return False
        try:
            conn = cls.obtener_conexion(incluir_bd=True)
            nombre_bd = cls._config["database"]
            with conn.cursor() as cur:
                if ARCHIVO_SQL_INICIAL.exists():
                    script_sql = ARCHIVO_SQL_INICIAL.read_text(encoding="utf-8")
                    lineas_limpias = [
                        l for l in script_sql.splitlines() if not l.strip().startswith("--")
                    ]
                    sql_limpio = "\n".join(lineas_limpias)
                    sentencias = [s.strip() for s in sql_limpio.split(";") if s.strip()]
                    for stmt in sentencias:
                        if stmt.upper().startswith("USE "):
                            continue
                        cur.execute(stmt)
                try:
                    cur.execute(
                        "ALTER TABLE makeup_products_colombia ADD COLUMN image_url VARCHAR(600)"
                    )
                except Exception:
                    pass
            conn.close()
            cls._conectado = True
            cls._ultimo_mensaje = f"Conectado de forma segura a TiDB Cloud (BD: {nombre_bd})"
            return True
        except Exception:
            cls._conectado = False
            cls._ultimo_mensaje = "Modo Respaldo Local Activo"
            return False

    @classmethod
    def ejecutar_consulta(cls, operacion: Callable[[Any], Any]) -> Optional[Any]:
        if not cls._config.get("password"):
            return None
        try:
            conn = cls.obtener_conexion(incluir_bd=True)
            try:
                resultado = operacion(conn)
                cls._conectado = True
                return resultado
            finally:
                conn.close()
        except Exception:
            cls._conectado = False
            cls._ultimo_mensaje = "Modo Respaldo Local Activo"
            return None

    @classmethod
    def obtener_estado(cls) -> Dict[str, Any]:
        return {
            "tidb_connected": cls._conectado,
            "status_message": cls._ultimo_mensaje,
            "database": cls._config["database"],
        }


conexion_tidb = ConectorTiDBCloud()
