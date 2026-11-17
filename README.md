## Recomendación de Maquillaje según tu Piel

Plataforma distribuida de recomendación dermocosmética y catálogo de maquillaje en Colombia conectada a TiDB Cloud  y Google AI .

## Estructura de Carpetas 

- **`app.py`**: Punto de entrada para iniciar el servidor en `http://localhost:8000`.
- **`base_de_datos_sql/crear_tablas_tidb.sql`**: Comandos SQL de creación de tablas en TiDB Cloud.
- **`interfaz_web/`**:
  - `index.html`: Interfaz web editorial con bienvenida guiada de 3 pasos y catálogo.
  - `estilos.css`: Diseño visual moderno tipo revista de belleza.
  - `logica_interfaz.js`: Lógica del navegador, sesión persistente y filtro de precios en `$ COP`.
  - `imagenes_productos/`: Fotos de cada producto del catálogo colombiano.
- **`servicios/`**:
  - `base_de_datos/conexion_tidb.py`: Conexión segura SSL/TLS a TiDB Cloud.
  - `inteligencia_artificial/agente_recomendador.py`: Agente de IA para análisis de tipo de piel, tono, subtono y condiciones.
  - `catalogo_maquillaje/catalogo_colombia.py`: Productos en tiendas de Colombia (**MAC Cosmetics, Anik, Bloshe, Blush-Bar y Farmatodo**) con fotos, precios en `$ COP` y enlaces directos al producto.
  - `gestion_usuarias/servicio_usuarias.py`: Registro e inicio de sesión guardando los datos de la usuaria en TiDB Cloud para no volver a preguntar el cuestionario.
  - `servidor_principal/servidor_api.py`: Orquestador principal de la aplicación.
- **`pruebas/pruebas_sistema.py`**: Pruebas unitarias y de integración.
