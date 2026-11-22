-- =============================================================================
-- Seed Data for Trama Urbana Verde
-- Based on Business Model Canvas - Hackatón Urbanismo 2026
-- Run after init.sql
-- =============================================================================

-- =============================================================================
-- IMPACT METRICS (KPIs)
-- =============================================================================
INSERT INTO impact_metrics (metric_key, value, label, icon, display_order) VALUES
    ('total_m2_recovered', 2450, 'm² de suelo vivo recuperados', 'leaf', 1),
    ('total_spaces', 12, 'Espacios intervenidos', 'map-pin', 2),
    ('total_volunteers', 340, 'Voluntarios activos', 'users', 3),
    ('total_communes', 5, 'Comunas de Santiago', 'building-2', 4),
    ('total_partners', 9, 'Socios estratégicos', 'handshake', 5),
    ('total_communities', 8, 'Comunidades organizadas', 'users-round', 6)
ON CONFLICT (metric_key) DO UPDATE SET
    value = EXCLUDED.value,
    label = EXCLUDED.label,
    icon = EXCLUDED.icon,
    display_order = EXCLUDED.display_order,
    updated_at = NOW();

-- =============================================================================
-- PARTNERS (Socios Clave del Canvas)
-- =============================================================================
INSERT INTO partners (name, type, description, logo_url, website_url, is_active, display_order) VALUES
    -- Municipalidades
    (
        'Municipalidad de Santiago',
        'municipality',
        'Permisos de uso temporario, subvenciones y gestión de espacios residuales en el centro histórico',
        '/images/partners/municipalidad-santiago.svg',
        'https://www.munistgo.cl',
        TRUE, 1
    ),
    (
        'Municipalidad de Estación Central',
        'municipality',
        'Gestión de lotes baldíos y veredas anchas para corredores verdes',
        '/images/partners/municipalidad-estacion-central.svg',
        'https://www.estacioncentral.cl',
        TRUE, 2
    ),
    (
        'Municipalidad de Ñuñoa',
        'municipality',
        'Programa de plazas de bolsillo y huertos comunitarios en barrios densos',
        '/images/partners/municipalidad-nunoa.svg',
        'https://www.nunoa.cl',
        TRUE, 3
    ),
    -- Empresas RSE
    (
        'Constructora Andes S.A.',
        'company_rse',
        'Cedencia de terrenos residuales, materiales de construcción y mano de obra voluntaria',
        '/images/partners/constructora-andes.svg',
        'https://www.andes.cl',
        TRUE, 4
    ),
    (
        'Inmobiliaria Verde Urbana',
        'company_rse',
        'Aportes RSE, materiales reciclados y mobiliario urbano sostenible',
        '/images/partners/inmobiliaria-verde-urbana.svg',
        'https://www.verdeurbana.cl',
        TRUE, 5
    ),
    (
        'Empresa Eléctrica Metropolitana',
        'company_rse',
        'Financiamiento de iluminación solar para espacios recuperados',
        '/images/partners/electrica-metropolitana.svg',
        'https://www.eem.cl',
        TRUE, 6
    ),
    -- Gobierno
    (
        'Gobierno Regional Metropolitano',
        'municipality',
        'Fondos concursables de mejoramiento urbano y medioambiental (FNDR, FRRL)',
        '/images/partners/gobierno-regional.svg',
        'https://www.gobiernosantiago.cl',
        TRUE, 7
    ),
    -- ONGs y Academia
    (
        'ONG Santiago Verde',
        'ngo',
        'Asesoría técnica en especies nativas, diseño ecológico y monitoreo de biodiversidad',
        '/images/partners/santiago-verde.svg',
        'https://www.santiagoverde.cl',
        TRUE, 8
    ),
    (
        'Universidad de Chile - FAU',
        'university',
        'Diseño urbano participativo, investigación acción y monitoreo de impacto social',
        '/images/partners/fau-uchile.svg',
        'https://www.fau.uchile.cl',
        TRUE, 9
    ),
    -- Viveros
    (
        'Vivero Nativo Cordillera',
        'nursery',
        'Provisión de especies nativas (quillay, peumo, boldo, arrayán) y sustrato orgánico',
        '/images/partners/vivero-cordillera.svg',
        'https://www.viverocordillera.cl',
        TRUE, 10
    ),
    -- Comunidades
    (
        'Junta de Vecinos Barrio Yungay',
        'community',
        'Gestión local, custodia de espacios y organización de actividades comunitarias',
        '/images/partners/jjvv-yungay.svg',
        NULL,
        TRUE, 11
    ),
    (
        'Junta de Vecinos Barrio Brasil',
        'community',
        'Participación en huerto comunitario y corredor verde Matucana',
        '/images/partners/jjvv-brasil.svg',
        NULL,
        TRUE, 12
    )
ON CONFLICT DO NOTHING;

-- =============================================================================
-- SPACES (Espacios de Intervención - Ejemplos reales)
-- =============================================================================
INSERT INTO spaces (name, description, address, commune, latitude, longitude, area_m2, status, category, image_url, before_image_url, started_at, completed_at) VALUES
    -- Completados
    (
        'Plaza Pocket Yungay',
        'Transformación de esquina residual en plaza de bolsillo con especies nativas (quillay, peumo), mobiliario modular de madera reciclada y señalética inclusiva. Incluye zona de estar para adultos mayores y juegos infantiles de bajo impacto.',
        'Compañía 1245, esquina Rosas',
        'Santiago',
        -33.4372,
        -70.6506,
        180,
        'completed',
        'pocket_park',
        '/images/spaces/plaza-yungay-after.jpg',
        '/images/spaces/plaza-yungay-before.jpg',
        '2025-03-15',
        '2025-06-20'
    ),
    (
        'Jardín Comunitario Santa Lucía',
        'Recuperación de terreno eriazo de 320 m² en falda del cerro Santa Lucía. Huertos elevados con riego por goteo, compostera comunitaria y zona de talleres. Gestionado por junta de vecinos y colegio aledaño.',
        'Merced 350',
        'Santiago',
        -33.4389,
        -70.6421,
        320,
        'completed',
        'community_garden',
        '/images/spaces/jardin-santa-lucia-after.jpg',
        '/images/spaces/jardin-santa-lucia-before.jpg',
        '2025-01-10',
        '2025-05-15'
    ),
    (
        'Plaza Activa Matta Norte',
        'Intervención táctica en vereda ancha: jardineras modulares con flora nativa, bancas de pallets certificados, mesa de ping-pong y mural comunitario. Proyecto piloto de "calles completas".',
        'Av. Matta 1200',
        'Santiago',
        -33.4567,
        -70.6534,
        150,
        'completed',
        'pocket_park',
        '/images/spaces/plaza-matta-after.jpg',
        '/images/spaces/plaza-matta-before.jpg',
        '2024-11-01',
        '2025-02-28'
    ),
    -- En Progreso
    (
        'Corredor Verde Matucana',
        'Intervención lineal de 320 m² en veredas anchas y bandejones centrales. Jardineras modulares conectadas por senderos peatonales, arbolado nativo (arrayanes, pataguas) y mobiliario de descanso. Conecta Metro Matucana con Parque Quinta Normal.',
        'Matucana 500 - 800',
        'Estación Central',
        -33.4451,
        -70.6823,
        320,
        'in_progress',
        'green_corridor',
        '/images/spaces/corredor-matucana-progress.jpg',
        '/images/spaces/corredor-matucana-before.jpg',
        '2025-08-01',
        NULL
    ),
    (
        'Huerto Escolar República de México',
        'Transformación de patio de concreto en huerto educativo con 12 camas de cultivo, invernadero modular, zona de compostaje y aula al aire libre. Alianzas con escuela básica y universidad.',
        'República de México 0200',
        'Santiago',
        -33.4489,
        -70.6542,
        450,
        'in_progress',
        'community_garden',
        '/images/spaces/huerto-escuela-progress.jpg',
        '/images/spaces/huerto-escuela-before.jpg',
        '2025-09-15',
        NULL
    ),
    (
        'Plaza Inclusiva Ñuñoa',
        'Diseño universal en esquina de 200 m²: pavimento táctil, juegos inclusivos, zona de sombra con pérgola vegetal, bebedero accesible y bancas ergonómicas. Primera plaza 100% accesible del proyecto.',
        'Irarrázaval 3500',
        'Ñuñoa',
        -33.4598,
        -70.6012,
        200,
        'in_progress',
        'resting_area',
        '/images/spaces/plaza-inclusiva-progress.jpg',
        '/images/spaces/plaza-inclusiva-before.jpg',
        '2025-10-01',
        NULL
    ),
    -- Identificados (Por iniciar)
    (
        'Lote Baldío Franklin',
        'Terreno de 800 m² en zona Franklin, actualmente microbasural. Potencial para mini bosque urbano (Miyawaki) con 300 árboles nativos densos. Requiere limpieza, remediación de suelo y permiso municipal.',
        'Franklin 850',
        'Santiago',
        -33.4621,
        -70.6589,
        800,
        'identified',
        'urban_forest',
        NULL,
        '/images/spaces/lote-franklin-before.jpg',
        NULL,
        NULL
    ),
    (
        'Bandejón Central Santa Rosa',
        'Bandejón de 1.2 km de extensión, 15 m de ancho. Oportunidad para corredor verde lineal conectando 3 comunas. Requiere coordinación intermunicipal y estudio de factibilidad hidráulica.',
        'Av. Santa Rosa (tramo completo)',
        'San Miguel / La Cisterna / El Bosque',
        -33.5123,
        -70.6456,
        18000,
        'identified',
        'green_corridor',
        NULL,
        '/images/spaces/bandejon-santa-rosa-before.jpg',
        NULL,
        NULL
    ),
    (
        'Esquina Residual Los Nogales',
        'Esquina de 90 m² en población Los Nogales, usada como estacionamiento informal. Solicitada por junta de vecinos para plaza de bolsillo con juegos infantiles y zona de estar para adultos mayores.',
        'Los Nogales 0450',
        'Estación Central',
        -33.4534,
        -70.6912,
        90,
        'identified',
        'pocket_park',
        NULL,
        '/images/spaces/esquina-nogales-before.jpg',
        NULL,
        NULL
    ),
    (
        'Terreno Errazo Lo Prado',
        'Lote de 1.200 m² en zona industrial reconvertida. Potencial para huerto comunitario a gran escala con zona de mercado campesino, compostaje industrial y capacitación en agricultura urbana.',
        'Av. Lo Prado 2500',
        'Lo Prado',
        -33.4234,
        -70.7234,
        1200,
        'identified',
        'community_garden',
        NULL,
        '/images/spaces/terreno-loprado-before.jpg',
        NULL,
        NULL
    )
ON CONFLICT DO NOTHING;

-- =============================================================================
-- COMMUNITIES (Comunidades / Juntas de Vecinos)
-- =============================================================================
INSERT INTO communities (name, commune, contact_email, contact_phone, contact_person, member_count, space_id) VALUES
    (
        'Junta de Vecinos Barrio Yungay',
        'Santiago',
        'contacto@jjvvyungay.cl',
        '+56 2 2698 1234',
        'María González',
        450,
        1
    ),
    (
        'Junta de Vecinos Barrio Brasil',
        'Santiago',
        'juntavecinosbrasil@gmail.com',
        '+56 9 8765 4321',
        'Carlos Rodríguez',
        380,
        2
    ),
    (
        'Junta de Vecinos Matta Norte',
        'Santiago',
        'mattanorte@vecino.cl',
        '+56 2 2777 8899',
        'Ana Martínez',
        520,
        3
    ),
    (
        'Comunidad Escolar República de México',
        'Santiago',
        'huertos@republicamexico.cl',
        '+56 2 2666 7788',
        'Prof. Patricia Silva',
        320,
        5
    ),
    (
        'Junta de Vecinos Villa Ñuñoa',
        'Ñuñoa',
        'villanunoa@jjvv.cl',
        '+56 2 2333 4455',
        'Roberto Pérez',
        610,
        6
    ),
    (
        'Junta de Vecinos Los Nogales',
        'Estación Central',
        'losnogales.vecino@gmail.com',
        '+56 9 1234 5678',
        'Luisa Fernández',
        290,
        9
    ),
    (
        'Comité de Vivienda Lo Prado',
        'Lo Prado',
        'comite.loprado@vivenda.cl',
        '+56 2 2555 6677',
        'Jorge Soto',
        410,
        10
    ),
    (
        'Red de Huertos Urbanos Santiago',
        'Múltiples',
        'redhuertos@stgo.cl',
        '+56 9 9988 7766',
        'Coordinación rotativa',
        1200,
        NULL
    )
ON CONFLICT DO NOTHING;

-- =============================================================================
-- UPDATE METRICS BASED ON SEED DATA
-- =============================================================================
-- Recalculate metrics from actual data
UPDATE impact_metrics SET
    value = (SELECT COUNT(*) FROM spaces),
    updated_at = NOW()
WHERE metric_key = 'total_spaces';

UPDATE impact_metrics SET
    value = (SELECT COALESCE(SUM(area_m2), 0) FROM spaces WHERE status = 'completed'),
    updated_at = NOW()
WHERE metric_key = 'total_m2_recovered';

UPDATE impact_metrics SET
    value = (SELECT COUNT(*) FROM partners WHERE is_active = TRUE),
    updated_at = NOW()
WHERE metric_key = 'total_partners';

UPDATE impact_metrics SET
    value = (SELECT COUNT(DISTINCT commune) FROM spaces WHERE commune IS NOT NULL),
    updated_at = NOW()
WHERE metric_key = 'total_communes';

UPDATE impact_metrics SET
    value = (SELECT COUNT(*) FROM communities),
    updated_at = NOW()
WHERE metric_key = 'total_communities';

-- Volunteers: estimate based on communities + spaces
UPDATE impact_metrics SET
    value = (SELECT COALESCE(SUM(member_count), 0) FROM communities) + 100,
    updated_at = NOW()
WHERE metric_key = 'total_volunteers';

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================
-- SELECT * FROM impact_metrics ORDER BY display_order;
-- SELECT * FROM partners ORDER BY display_order;
-- SELECT name, commune, status, category, area_m2 FROM spaces ORDER BY status, name;
-- SELECT * FROM communities ORDER BY name;