"""
Servicio de Catálogo de Maquillaje en Colombia (TiDB Cloud `test`).
Cada producto incluye:
- Su imagen de estudio (`/imagenes_productos/<sku>.svg`) para verse en la tarjeta.
- Su precio en Pesos Colombianos (`$ COP`).
- Su enlace directo a la página exacta del producto (`/products/...`, `/producto/...`, `/.../p`)
  en tiendas de Colombia (Ani-k Makeup, M·A·C Cosmetics / Blush-Bar, Bloshe / Montoc y Farmatodo).
"""
import json
from typing import Dict, Any, List
from servicios.base_de_datos.conexion_tidb import conexion_tidb


class ServicioCatalogoColombia:
    def __init__(self):
        self._tiendas = self._cargar_tiendas_colombia()
        self._catalogo = self._cargar_catalogo_colombia()

    def _cargar_tiendas_colombia(self) -> List[Dict[str, Any]]:
        return [
            {
                "store_id": "store-col-mac",
                "name": "MAC Cosmetics Colombia",
                "store_type": "Marca Profesional de Maquillaje Oficial en Colombia",
                "website_url": "https://www.maccosmetics.com.co",
                "shipping_coverage": "Tiendas oficiales MAC y distribuidores autorizados en toda Colombia"
            },
            {
                "store_id": "store-col-anik",
                "name": "Anik / Anika Makeup Colombia",
                "store_type": "Marca Colombiana de Maquillaje en Tendencia",
                "website_url": "https://anikmakeup.com",
                "shipping_coverage": "Envíos nacionales a Medellín, Bogotá, Cali y toda Colombia"
            },
            {
                "store_id": "store-col-bloshe",
                "name": "Bloshe / Montoc Colombia",
                "store_type": "Maquillaje & Dermocosmética en Colombia",
                "website_url": "https://www.blush-bar.com",
                "shipping_coverage": "Cobertura nacional en Colombia con productos 100% originales"
            },
            {
                "store_id": "store-col-blushbar",
                "name": "Blush-Bar Colombia",
                "store_type": "Boutique de Maquillaje Internacional en Colombia",
                "website_url": "https://www.blush-bar.com",
                "shipping_coverage": "Tiendas físicas y envíos nacionales en Colombia"
            },
            {
                "store_id": "store-col-farmatodo",
                "name": "Farmatodo Colombia",
                "store_type": "Dermocosmética & Belleza Express 24/7",
                "website_url": "https://www.farmatodo.com.co",
                "shipping_coverage": "Domicilio express en 35 min en ciudades principales de Colombia"
            },
            {
                "store_id": "store-col-falabella",
                "name": "Falabella Colombia",
                "store_type": "Gran Tienda por Departamento & Perfumería",
                "website_url": "https://www.falabella.com.co",
                "shipping_coverage": "Cobertura nacional en toda Colombia y retiro en tienda"
            }
        ]

    def _cargar_catalogo_colombia(self) -> List[Dict[str, Any]]:
        return [
            # ==================== BASES DE MAQUILLAJE ====================
            {
                "sku": "COL-BAS-ANK01",
                "name": "Base Bonita 2 en 1 Cobertura Media-Alta Construible",
                "brand": "Ani-k Makeup Colombia",
                "category": "Base de Maquillaje",
                "search_tags": ["base", "bases", "anik", "anika", "bonita", "economica", "rostro", "hidratante"],
                "price_cop": 38000,
                "skin_types": ["seca", "mixta", "normal", "grasa"],
                "skin_tones": ["clara", "media", "bronceada"],
                "undertones": ["oliva", "calido", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Tono 00 Anne / 01 Katy",
                    "media_oliva": "Tono 02 Taylor (Ideal Subtono Oliva / Trigueña)",
                    "bronceada_oliva": "Tono 03 / 04 Bronce",
                    "default": "Tono 02 Taylor"
                },
                "key_benefit": "Fórmula 2 en 1 (base y corrector) de acabado semi-mate natural y textura ligera adaptada a pieles colombianas.",
                "store_name": "Anik / Anika Makeup Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://anikmakeup.com/products/base-bonita",
                "image_url": "/imagenes_productos/COL-BAS-ANK01.svg",
                "image_gradient": "linear-gradient(135deg, #e0b796 0%, #9c6f4f 100%)"
            },
            {
                "sku": "COL-BAS-MAC01",
                "name": "Base Líquida Studio Fix Fluid SPF 15 24Hr Matte + Oil Control",
                "brand": "M·A·C Cosmetics",
                "category": "Base de Maquillaje",
                "search_tags": ["base", "bases", "mac", "studio fix", "rostro", "piel", "cobertura", "oliva"],
                "price_cop": 189000,
                "skin_types": ["mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "poros", "sensibilidad", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "C30 / NC20 Light Olive",
                    "media_oliva": "C40 / NC30-NC35 Medium Olive (Icónico Subtono Oliva)",
                    "bronceada_oliva": "C45 / NC42 Tan Olive",
                    "default": "NC30 / C35 Natural Olive-Beige"
                },
                "key_benefit": "Fórmula transpirable con extracto de alga azucarera y ácido hialurónico que controla el brillo 24h sin oxidar.",
                "store_name": "MAC Cosmetics Colombia",
                "store_badge": "Ficha Oficial del Producto",
                "store_url": "https://www.blush-bar.com/base-liquida-studio-fix-fluid-spf-15-24hr-matte-foundation-oil-control/p",
                "image_url": "/imagenes_productos/COL-BAS-MAC01.svg",
                "image_gradient": "linear-gradient(135deg, #2b211e 0%, #8c6246 100%)"
            },
            {
                "sku": "COL-BAS-BLO01",
                "name": "Base Líquida Húmide Skin Acabado Hidratante & Luminoso",
                "brand": "Montoc / Bloshe Colombia",
                "category": "Base de Maquillaje",
                "search_tags": ["base", "bases", "bloshe", "montoc", "humide", "hidratante", "sensibilidad"],
                "price_cop": 54900,
                "skin_types": ["seca", "mixta", "normal"],
                "skin_tones": ["clara", "media", "bronceada"],
                "undertones": ["oliva", "calido", "neutro", "frio"],
                "safe_for_conditions": ["sensibilidad", "rosacea", "acne", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Light Beige Neutro",
                    "media_oliva": "Medium Olive / Sand",
                    "bronceada_oliva": "Warm Tan",
                    "default": "Medium Sand"
                },
                "key_benefit": "Textura fluida humectante que no marca líneas de expresión y respeta las pieles sensibles con acabado fresco.",
                "store_name": "Bloshe / Montoc Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/base-liquida-humide-skin/p",
                "image_url": "/imagenes_productos/COL-BAS-BLO01.svg",
                "image_gradient": "linear-gradient(135deg, #d9ae8e 0%, #8f5f3f 100%)"
            },
            {
                "sku": "COL-BAS-001",
                "name": "Base Líquida Vogue Resist Larga Duración con Ácido Hialurónico",
                "brand": "Vogue Cosméticos Colombia",
                "category": "Base de Maquillaje",
                "search_tags": ["base", "bases", "vogue", "resist", "economica", "rostro", "piel", "colombiana"],
                "price_cop": 32900,
                "skin_types": ["mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "neutro"],
                "safe_for_conditions": ["acne", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Porcelana / Vainilla",
                    "media_oliva": "Natural / Miel (Equilibrio Oliva)",
                    "bronceada_oliva": "Caramelo / Bronce",
                    "default": "Natural / Caramelo"
                },
                "key_benefit": "Resistente al calor y la humedad de Colombia, no transfiere y mantiene la piel uniforme todo el día.",
                "store_name": "Farmatodo Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.farmatodo.com.co/producto/266100383-base-vogue-resist-glam-tono-caramelo-frasco-x-30-ml",
                "image_url": "/imagenes_productos/COL-BAS-001.svg",
                "image_gradient": "linear-gradient(135deg, #d8b498 0%, #9b7152 100%)"
            },
            {
                "sku": "COL-BAS-005",
                "name": "Base Líquida Easy Blur Natural Airbrush Foundation con Niacinamida",
                "brand": "Huda Beauty",
                "category": "Base de Maquillaje",
                "search_tags": ["base", "bases", "alta gama", "niacinamida", "poros", "acne", "oliva"],
                "price_cop": 175000,
                "skin_types": ["mixta", "grasa", "normal", "seca"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Chai 210B / Custard 220N",
                    "media_oliva": "Baklava 340G / Toasted Coconut 240N (Subtono Oliva)",
                    "bronceada_oliva": "Amaretti 310G / Latte 300N",
                    "default": "Toasted Coconut 240N"
                },
                "key_benefit": "Con 1.5% de Niacinamida calmante y sílice difuminador de poros; libre de alcohol y fragancias irritantes.",
                "store_name": "Blush-Bar Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/base-liquida-easy-blur-foundation/p",
                "image_url": "/imagenes_productos/COL-BAS-005.svg",
                "image_gradient": "linear-gradient(135deg, #c69874 0%, #7d5234 100%)"
            },

            # ==================== CORRECTORES ====================
            {
                "sku": "COL-COR-ANK01",
                "name": "Corrector Líquido Vegano Hidratante Aplicador Jumbo",
                "brand": "Ani-k Makeup Colombia",
                "category": "Corrector",
                "search_tags": ["corrector", "correctores", "anik", "anika", "ojeras", "acne", "economico"],
                "price_cop": 26900,
                "skin_types": ["mixta", "seca", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada"],
                "undertones": ["oliva", "calido", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "00 Snow / 01 Bone",
                    "media_oliva": "02 Radiant (Armoniza con Subtono Oliva)",
                    "bronceada_oliva": "03 Warm Tan",
                    "default": "02 Radiant"
                },
                "key_benefit": "Fórmula vegana cremosa e hidratante de cobertura media-alta construible que no cuartea la ojera.",
                "store_name": "Anik / Anika Makeup Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://anikmakeup.com/products/corrector",
                "image_url": "/imagenes_productos/COL-COR-ANK01.svg",
                "image_gradient": "linear-gradient(135deg, #eccab1 0%, #b58462 100%)"
            },
            {
                "sku": "COL-COR-MAC01",
                "name": "Corrector Líquido Studio Fix 24-Hour Smooth Wear Concealer",
                "brand": "M·A·C Cosmetics",
                "category": "Corrector",
                "search_tags": ["corrector", "correctores", "mac", "studio fix", "ojeras", "acne", "alta gama"],
                "price_cop": 149000,
                "skin_types": ["seca", "mixta", "normal", "grasa"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["sensibilidad", "acne", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "NC15 / NC20",
                    "media_oliva": "NC30 / NC35 (Subtono Oliva sin oxidación)",
                    "bronceada_oliva": "NC42 / NC45",
                    "default": "NC30"
                },
                "key_benefit": "Libre de aceites (oil-free), no comedogénico; cubre ojeras e imperfecciones de acné durante 24 horas.",
                "store_name": "MAC Cosmetics Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/corrector-studio-fix-24-hour-liquid/p",
                "image_url": "/imagenes_productos/COL-COR-MAC01.svg",
                "image_gradient": "linear-gradient(135deg, #3a2b25 0%, #9c7154 100%)"
            },
            {
                "sku": "COL-COR-002",
                "name": "Corrector Maybelline Fit Me Spot Rescue con Ácido Salicílico",
                "brand": "Maybelline New York",
                "category": "Corrector",
                "search_tags": ["corrector", "correctores", "fit me", "acne", "ojeras", "maybelline", "economico"],
                "price_cop": 39900,
                "skin_types": ["mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "neutro", "frio"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Tono 15 Fair / 20 Sand",
                    "media_oliva": "Tono 25 Medium / 40 Caramel (Piel Oliva/Trigueña)",
                    "bronceada_oliva": "Tono 40 Caramel",
                    "default": "Tono 25 Medium"
                },
                "key_benefit": "Especial para piel con tendencia a acné: cubre imperfecciones y ojeras mientras trata brotes sin obstruir poros.",
                "store_name": "Farmatodo Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.farmatodo.com.co/producto/271600331-corrector-maybelline-fit-me-spot-rescue-tono-40-tubo-x-1-und",
                "image_url": "/imagenes_productos/COL-COR-002.svg",
                "image_gradient": "linear-gradient(135deg, #e7c3a6 0%, #b58663 100%)"
            },
            {
                "sku": "COL-COR-003",
                "name": "Corrector Maybelline Super Stay Active Wear 30H",
                "brand": "Maybelline New York",
                "category": "Corrector",
                "search_tags": ["corrector", "correctores", "super stay", "ojeras", "larga duracion", "maybelline"],
                "price_cop": 54900,
                "skin_types": ["mixta", "grasa", "normal", "seca"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "neutro", "frio"],
                "safe_for_conditions": ["acne", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Tono 10 / 15",
                    "media_oliva": "Tono 25 Medium (Subtono Neutro-Oliva)",
                    "bronceada_oliva": "Tono 30 Honey",
                    "default": "Tono 25 Medium"
                },
                "key_benefit": "Alta cobertura respirable de 30 horas que resiste el sudor y la humedad sin cuartearse ni transferir.",
                "store_name": "Farmatodo Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.farmatodo.com.co/producto/297150543-corrector-maybelline---super-stay-30-hr-25-x-10-ml",
                "image_url": "/imagenes_productos/COL-COR-003.svg",
                "image_gradient": "linear-gradient(135deg, #dec0a4 0%, #a57c59 100%)"
            },
            {
                "sku": "COL-COR-BLO01",
                "name": "Corrector Hidratante Liquid Touch Brightening Concealer",
                "brand": "Rare Beauty",
                "category": "Corrector",
                "search_tags": ["corrector", "correctores", "rare beauty", "blush-bar", "hidratante", "sensibilidad"],
                "price_cop": 129000,
                "skin_types": ["seca", "mixta", "normal", "grasa"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["sensibilidad", "acne", "rosacea", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "170W Light Warm Olive",
                    "media_oliva": "230N Medium Neutral Olive (Tono Oliva Puro)",
                    "bronceada_oliva": "320W Tan Olive",
                    "default": "230N Medium Neutral Olive"
                },
                "key_benefit": "Con extractos botánicos calmantes de loto, gardenia y nenúfar blanco; ideal para piel sensible y subtono oliva.",
                "store_name": "Blush-Bar Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/corrector-liquid-touch-brightening-concealer/p",
                "image_url": "/imagenes_productos/COL-COR-BLO01.svg",
                "image_gradient": "linear-gradient(135deg, #f3d6c1 0%, #c89d7c 100%)"
            },

            # ==================== RUBORES E ILUMINADORES ====================
            {
                "sku": "COL-RUB-ANK01",
                "name": "Rubor Líquido Bonita Textura Velvet Multiusos",
                "brand": "Ani-k Makeup Colombia",
                "category": "Rubor e Iluminador",
                "search_tags": ["rubor", "rubores", "blush", "anik", "anika", "mejillas", "liquido", "bonita"],
                "price_cop": 25900,
                "skin_types": ["seca", "mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Tono Rose / Peach",
                    "media_oliva": "Tono Terracota / Mauve (Realza Subtono Oliva)",
                    "bronceada_oliva": "Tono Berry / Coral",
                    "default": "Tono Terracota"
                },
                "key_benefit": "Acabado aterciopelado semi-mate 3 en 1 (mejillas, labios y ojos) que se difumina sin levantar la base.",
                "store_name": "Anik / Anika Makeup Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://anikmakeup.com/products/rubor-liquido-bonita",
                "image_url": "/imagenes_productos/COL-RUB-ANK01.svg",
                "image_gradient": "linear-gradient(135deg, #e07a86 0%, #8b2635 100%)"
            },
            {
                "sku": "COL-RUB-ANK02",
                "name": "Rubor Mineralizado 2 en 1 (Rubor + Iluminador Micropulverizado)",
                "brand": "Ani-k Makeup Colombia",
                "category": "Rubor e Iluminador",
                "search_tags": ["rubor", "rubores", "iluminador", "anik", "anika", "mineralizado", "mejillas"],
                "price_cop": 28900,
                "skin_types": ["seca", "mixta", "normal", "grasa"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["sensibilidad", "acne", "ninguna"],
                "shade_by_profile": {
                    "default": "Coral Dorado / Bronce Perlado"
                },
                "key_benefit": "Pigmentos minerales micropulverizados que aportan efecto luminoso saludable sin marcar textura.",
                "store_name": "Anik / Anika Makeup Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://anikmakeup.com/products/rubor-mineralizado",
                "image_url": "/imagenes_productos/COL-RUB-ANK02.svg",
                "image_gradient": "linear-gradient(135deg, #eb9486 0%, #a84232 100%)"
            },
            {
                "sku": "COL-RUB-MAC01",
                "name": "Rubor Líquido Soft Pinch Liquid Blush Alta Duración",
                "brand": "Rare Beauty",
                "category": "Rubor e Iluminador",
                "search_tags": ["rubor", "rubores", "blush", "rare beauty", "blush-bar", "alta gama"],
                "price_cop": 135000,
                "skin_types": ["seca", "mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "rosacea", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Hope / Bliss",
                    "media_oliva": "Encourage / Worth (Favorito Subtono Oliva)",
                    "bronceada_oliva": "Love / Believe",
                    "default": "Encourage"
                },
                "key_benefit": "Fórmula botánica vegana ultraligera que dura todo el día con un solo punto de producto.",
                "store_name": "Blush-Bar Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/rubor-liquido-soft-pinch-liquid-blush/p",
                "image_url": "/imagenes_productos/COL-RUB-MAC01.svg",
                "image_gradient": "linear-gradient(135deg, #c97b63 0%, #6e3528 100%)"
            },

            # ==================== POLVOS & PRIMERS ====================
            {
                "sku": "COL-POL-ANK01",
                "name": "Polvo Suelto Micropulverizado Efecto Filtro Sin Parabenos",
                "brand": "Ani-k Makeup Colombia",
                "category": "Polvos y Fijadores",
                "search_tags": ["polvo", "polvos", "anik", "anika", "sellar", "matificante", "poros"],
                "price_cop": 32000,
                "skin_types": ["mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "poros", "sensibilidad", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "01 Carlota (Translúcido)",
                    "media_oliva": "02 Scarlett (Banana Suave para Subtono Oliva)",
                    "bronceada_oliva": "04 Cinnamon",
                    "default": "01 Carlota / 02 Scarlett"
                },
                "key_benefit": "Resistente al agua y libre de parabenos; sella el corrector y la base con efecto filtro alisador de poros.",
                "store_name": "Anik / Anika Makeup Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://anikmakeup.com/products/polvo-suelto",
                "image_url": "/imagenes_productos/COL-POL-ANK01.svg",
                "image_gradient": "linear-gradient(135deg, #f2e3d5 0%, #c4a78d 100%)"
            },
            {
                "sku": "COL-PRI-001",
                "name": "Primer Matificante Studio Fix Mattifine 12Hr Shine-Control",
                "brand": "M·A·C Cosmetics",
                "category": "Primer y Preparación",
                "search_tags": ["primer", "mac", "studio fix", "poros", "preparacion", "piel mixta", "piel grasa"],
                "price_cop": 155000,
                "skin_types": ["mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["acne", "sensibilidad", "poros", "ninguna"],
                "shade_by_profile": {
                    "default": "Gel-Crema Invisible Sin Aceites"
                },
                "key_benefit": "Con ácido lactobiónico y extracto de algas; reduce visiblemente la apariencia de los poros y controla el sebo 12h.",
                "store_name": "MAC Cosmetics Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/primer-matificante-mac-studio-fix-mattifine-shine-control-primer/p",
                "image_url": "/imagenes_productos/COL-PRI-001.svg",
                "image_gradient": "linear-gradient(135deg, #f8e6ea 0%, #d99aab 100%)"
            },

            # ==================== LABIOS & OJOS ====================
            {
                "sku": "COL-LAB-MAC01",
                "name": "Labial M·A·Cximal Silky Matte Lipstick",
                "brand": "M·A·C Cosmetics",
                "category": "Labios",
                "search_tags": ["labial", "labiales", "labios", "mac", "macximal", "matte"],
                "price_cop": 119000,
                "skin_types": ["seca", "mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["sensibilidad", "acne", "rosacea", "ninguna"],
                "shade_by_profile": {
                    "clara_oliva": "Velvet Teddy / Mehr",
                    "media_oliva": "Whirl / Warm Teddy / Chili (Espectacular en Subtono Oliva)",
                    "bronceada_oliva": "Marrakesh / Diva",
                    "default": "Warm Teddy"
                },
                "key_benefit": "Enriquecido con aceite de coco orgánico y manteca de karité; 12 horas de color confortable para tu subtono.",
                "store_name": "MAC Cosmetics Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.blush-bar.com/labial-macximal-silky-matte-lipstick/p",
                "image_url": "/imagenes_productos/COL-LAB-MAC01.svg",
                "image_gradient": "linear-gradient(135deg, #721121 0%, #3b0910 100%)"
            },
            {
                "sku": "COL-OJO-001",
                "name": "Kit Pestañina Sky High + Corrector Instant Age Rewind",
                "brand": "Maybelline New York",
                "category": "Ojos",
                "search_tags": ["pestañina", "mascara", "ojos", "delineador", "pestañas", "sky high"],
                "price_cop": 79900,
                "skin_types": ["seca", "mixta", "grasa", "normal"],
                "skin_tones": ["clara", "media", "bronceada", "profunda"],
                "undertones": ["oliva", "calido", "frio", "neutro"],
                "safe_for_conditions": ["sensibilidad", "acne", "ninguna"],
                "shade_by_profile": {
                    "default": "Blackest Black + Corrector Neutralizer"
                },
                "key_benefit": "Pestañina Sky High oftalmológicamente probada para ojos sensibles junto con el corrector favorito de Maybelline.",
                "store_name": "Farmatodo Colombia",
                "store_badge": "Enlace Directo al Producto",
                "store_url": "https://www.farmatodo.com.co/producto/8801393-combo-maybelline-sky-high-waterproof--corrector-age-rewind",
                "image_url": "/imagenes_productos/COL-OJO-001.svg",
                "image_gradient": "linear-gradient(135deg, #d4a5a5 0%, #5c3c3c 100%)"
            }
        ]

    def sincronizar_catalogo_en_tidb(self) -> bool:
        """Sincroniza las tiendas, fotos y enlaces directos de productos en TiDB Cloud (`test`)."""
        def _op(conn):
            with conn.cursor() as cur:
                for st in self._tiendas:
                    cur.execute(
                        """
                        INSERT INTO colombia_virtual_stores (
                            store_id, store_name, store_type, website_url, shipping_coverage
                        ) VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            store_name = VALUES(store_name),
                            website_url = VALUES(website_url)
                        """,
                        (
                            st["store_id"],
                            st["name"],
                            st["store_type"],
                            st["website_url"],
                            st["shipping_coverage"]
                        )
                    )
                for p in self._catalogo:
                    cur.execute(
                        """
                        INSERT INTO makeup_products_colombia (
                            sku, product_name, brand, category, search_tags_json,
                            price_cop, skin_types_json, skin_tones_json, undertones_json,
                            safe_conditions_json, key_benefit, store_name, store_url,
                            image_gradient, image_url
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            product_name = VALUES(product_name),
                            brand = VALUES(brand),
                            price_cop = VALUES(price_cop),
                            key_benefit = VALUES(key_benefit),
                            store_name = VALUES(store_name),
                            store_url = VALUES(store_url),
                            image_url = VALUES(image_url)
                        """,
                        (
                            p["sku"],
                            p["name"],
                            p["brand"],
                            p["category"],
                            json.dumps(p["search_tags"], ensure_ascii=False),
                            int(p["price_cop"]),
                            json.dumps(p["skin_types"], ensure_ascii=False),
                            json.dumps(p["skin_tones"], ensure_ascii=False),
                            json.dumps(p["undertones"], ensure_ascii=False),
                            json.dumps(p["safe_for_conditions"], ensure_ascii=False),
                            p["key_benefit"],
                            p["store_name"],
                            p["store_url"],
                            p["image_gradient"],
                            p["image_url"]
                        )
                    )
            return True

        return bool(conexion_tidb.ejecutar_consulta(_op))

    def buscar_y_recomendar(
        self,
        skin_profile: Dict[str, Any],
        max_price_cop: int = 190000,
        query: str = "",
        category: str = "todos",
        store_filter: str = "todas"
    ) -> Dict[str, Any]:
        skin_type = skin_profile.get("skin_type", "mixta")
        skin_tone = skin_profile.get("skin_tone", "media")
        undertone = skin_profile.get("undertone", "oliva")
        conditions = skin_profile.get("conditions", ["ninguna"])
        if isinstance(conditions, str):
            conditions = [conditions]

        q_clean = (query or "").strip().lower()
        cat_clean = (category or "todos").strip().lower()
        store_clean = (store_filter or "todas").strip().lower()

        resultados = []
        for item in self._catalogo:
            if item["price_cop"] > int(max_price_cop):
                continue

            if store_clean != "todas" and store_clean not in item["store_name"].lower():
                continue

            if cat_clean != "todos" and cat_clean not in item["category"].lower():
                continue

            if q_clean:
                searchable = " ".join([
                    item["name"].lower(),
                    item["brand"].lower(),
                    item["category"].lower(),
                    item["store_name"].lower(),
                    " ".join(item["search_tags"])
                ])
                if q_clean not in searchable:
                    continue

            score = 65
            razones = []

            if skin_type in item["skin_types"]:
                score += 14
                razones.append(f"Ideal para tu piel {skin_type}")

            if undertone in item["undertones"]:
                score += 12
                razones.append(f"Armoniza con tu subtono {undertone}")

            if skin_tone in item["skin_tones"]:
                score += 4

            cond_activas = [c for c in conditions if c != "ninguna"]
            if cond_activas:
                cond_ok = [c for c in cond_activas if c in item["safe_for_conditions"]]
                if cond_ok:
                    score += 5
                    razones.append(f"Seguro para {', '.join(cond_ok)}")
            else:
                score += 5

            score = min(score, 99)

            clave_tono = f"{skin_tone}_{undertone}"
            mapa_tonos = item.get("shade_by_profile", {})
            tono_sugerido = mapa_tonos.get(clave_tono, mapa_tonos.get("default", "Tono Estándar"))

            enriquecido = dict(item)
            enriquecido["affinity_score"] = score
            enriquecido["recommended_shade"] = tono_sugerido
            enriquecido["formatted_price_cop"] = f"${item['price_cop']:,}".replace(",", ".")
            enriquecido["personalized_reason"] = (
                " · ".join(razones)
                if razones else
                f"Ideal para piel {skin_type} y subtono {undertone}"
            )
            resultados.append(enriquecido)

        resultados.sort(key=lambda x: (-x["affinity_score"], x["price_cop"]))

        return {
            "total_matches": len(resultados),
            "applied_max_price_cop": int(max_price_cop),
            "formatted_max_price_cop": f"${int(max_price_cop):,}".replace(",", "."),
            "applied_skin_profile": {
                "skin_type": skin_type,
                "skin_tone": skin_tone,
                "undertone": undertone,
                "conditions": conditions
            },
            "colombia_stores": self._tiendas,
            "products": resultados
        }
