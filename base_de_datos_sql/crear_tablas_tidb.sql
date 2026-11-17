-- =============================================================================
-- CUSTOMMATCH COLOMBIA — ESQUEMA DE BASE DE DATOS DISTRIBUIDA EN TIDB CLOUD
-- Base de datos objetivo: `test`
-- Host: gateway01.us-east-1.prod.aws.tidbcloud.com (Puerto 4000)
-- =============================================================================

USE test;

-- 1. Tabla de Usuarias Registradas en Colombia
CREATE TABLE IF NOT EXISTS registered_users (
    user_id VARCHAR(64) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    city_colombia VARCHAR(120) DEFAULT 'Bogotá, Colombia',
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Perfil Cutáneo Guardado (Para no volver a preguntar al iniciar sesión)
CREATE TABLE IF NOT EXISTS user_skin_profiles (
    user_id VARCHAR(64) PRIMARY KEY,
    skin_type VARCHAR(40) NOT NULL,
    skin_tone VARCHAR(40) NOT NULL,
    undertone VARCHAR(40) NOT NULL,
    conditions_json TEXT NOT NULL,
    last_max_price_cop INT DEFAULT 190000,
    ai_skin_summary TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Tabla de Tiendas Virtuales de Maquillaje en Colombia
CREATE TABLE IF NOT EXISTS colombia_virtual_stores (
    store_id VARCHAR(64) PRIMARY KEY,
    store_name VARCHAR(140) NOT NULL,
    store_type VARCHAR(160),
    website_url VARCHAR(500) NOT NULL,
    shipping_coverage VARCHAR(255)
);

-- 4. Tabla de Catálogo de Productos de Maquillaje en Colombia (con foto y link directo)
CREATE TABLE IF NOT EXISTS makeup_products_colombia (
    sku VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(220) NOT NULL,
    brand VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    search_tags_json TEXT,
    price_cop INT NOT NULL,
    skin_types_json TEXT NOT NULL,
    skin_tones_json TEXT NOT NULL,
    undertones_json TEXT NOT NULL,
    safe_conditions_json TEXT NOT NULL,
    key_benefit TEXT,
    store_name VARCHAR(140) NOT NULL,
    store_url VARCHAR(500) NOT NULL,
    image_gradient VARCHAR(255),
    image_url VARCHAR(600)
);

-- 5. Tabla de Atención Personalizada y Servicio al Cliente (CustomMatch Colombia)
CREATE TABLE IF NOT EXISTS solicitudes_atencion_cliente (
    ticket_id VARCHAR(64) PRIMARY KEY,
    user_email VARCHAR(180) NOT NULL,
    user_name VARCHAR(150) NOT NULL,
    whatsapp_colombia VARCHAR(60),
    topic VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    assigned_advisor VARCHAR(150) NOT NULL,
    advisor_response TEXT,
    status VARCHAR(40) DEFAULT 'EN_ATENCION',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
