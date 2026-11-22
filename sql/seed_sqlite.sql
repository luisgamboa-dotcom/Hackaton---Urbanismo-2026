







INSERT OR REPLACE INTO impact_metrics (id, metric_key, value, label, icon, display_order, created_at, updated_at) VALUES
    (1, 'total_m2_recovered', 2450, 'm² de suelo vivo recuperados', 'leaf', 1, datetime('now'), datetime('now')),
    (2, 'total_spaces', 12, 'Espacios intervenidos', 'map-pin', 2, datetime('now'), datetime('now')),
    (3, 'total_volunteers', 340, 'Voluntarios activos', 'users', 3, datetime('now'), datetime('now')),
    (4, 'total_communes', 5, 'Comunas de Santiago', 'building-2', 4, datetime('now'), datetime('now')),
    (5, 'total_partners', 12, 'Socios estratégicos', 'handshake', 5, datetime('now'), datetime('now')),
    (6, 'total_communities', 8, 'Comunidades organizadas', 'users-round', 6, datetime('now'), datetime('now'));




INSERT OR REPLACE INTO partners (id, name, type, description, logo_url, website_url, is_active, display_order, created_at, updated_at) VALUES
    (1, 'Municipalidad de Santiago', 'municipality', 'Permisos de uso temporario, subvenciones y gestión de espacios residuales en el centro histórico', '/images/partners/municipalidad-santiago.png', 'https://www.munistgo.cl', 1, 1, datetime('now'), datetime('now')),
    (2, 'Municipalidad de Estación Central', 'municipality', 'Gestión de lotes baldíos y veredas anchas para corredores verdes', '/images/partners/municipalidad-estacion-central.png', 'https://www.estacioncentral.cl', 1, 2, datetime('now'), datetime('now')),
    (3, 'Municipalidad de Ñuñoa', 'municipality', 'Programa de plazas de bolsillo y huertos comunitarios en barrios densos', '/images/partners/municipalidad-nunoa.png', 'https://www.nunoa.cl', 1, 3, datetime('now'), datetime('now')),
    (4, 'Constructora Andes S.A.', 'company_rse', 'Cedencia de terrenos residuales, materiales de construcción y mano de obra voluntaria', '/images/partners/constructora-andes.png', 'https://www.andes.cl', 1, 4, datetime('now'), datetime('now')),
    (5, 'Inmobiliaria Verde Urbana', 'company_rse', 'Aportes RSE, materiales reciclados y mobiliario urbano sostenible', '/images/partners/inmobiliaria-verde-urbana.png', 'https://www.verdeurbana.cl', 1, 5, datetime('now'), datetime('now')),
    (6, 'Empresa Eléctrica Metropolitana', 'company_rse', 'Financiamiento de iluminación solar para espacios recuperados', '/images/partners/electrica-metropolitana.png', 'https://www.eem.cl', 1, 6, datetime('now'), datetime('now')),
    (7, 'Gobierno Regional Metropolitano', 'municipality', 'Fondos concursables de mejoramiento urbano y medioambiental (FNDR, FRRL)', '/images/partners/gobierno-regional.png', 'https://www.gobiernosantiago.cl', 1, 7, datetime('now'), datetime('now')),
    (8, 'ONG Santiago Verde', 'ngo', 'Asesoría técnica en especies nativas, diseño ecológico y monitoreo de biodiversidad', '/images/partners/santiago-verde.png', 'https://www.santiagoverde.cl', 1, 8, datetime('now'), datetime('now')),
    (9, 'Universidad de Chile - FAU', 'university', 'Diseño urbano participativo, investigación acción y monitoreo de impacto social', '/images/partners/fau-uchile.png', 'https://www.fau.uchile.cl', 1, 9, datetime('now'), datetime('now')),
    (10, 'Vivero Nativo Cordillera', 'nursery', 'Provisión de especies nativas (quillay, peumo, boldo, arrayán) y sustrato orgánico', '/images/partners/vivero-cordillera.png', 'https://www.viverocordillera.cl', 1, 10, datetime('now'), datetime('now')),
    (11, 'Junta de Vecinos Barrio Yungay', 'community', 'Gestión local, custodia de espacios y organización de actividades comunitarias', '/images/partners/jjvv-yungay.png', NULL, 1, 11, datetime('now'), datetime('now')),
    (12, 'Junta de Vecinos Barrio Brasil', 'community', 'Participación en huerto comunitario y corredor verde Matucana', '/images/partners/jjvv-brasil.png', NULL, 1, 12, datetime('now'), datetime('now'));




INSERT OR REPLACE INTO spaces (id, name, description, address, commune, latitude, longitude, area_m2, status, category, image_url, before_image_url, started_at, completed_at, created_at, updated_at) VALUES
    (1, 'Plaza Pocket Yungay', 'Transformación de esquina residual en plaza de bolsillo con especies nativas (quillay, peumo), mobiliario modular de madera reciclada y señalética inclusiva. Incluye zona de estar para adultos mayores y juegos infantiles de bajo impacto.', 'Compañía 1245, esquina Rosas', 'Santiago', -33.4372, -70.6506, 180, 'completed', 'pocket_park', '/images/spaces/space-1-after-opt.jpg', '/images/spaces/space-1-before-opt.jpg', '2025-03-15', '2025-06-20', datetime('now'), datetime('now')),
    (2, 'Jardín Comunitario Santa Lucía', 'Recuperación de terreno eriazo de 320 m² en falda del cerro Santa Lucía. Huertos elevados con riego por goteo, compostera comunitaria y zona de talleres. Gestionado por junta de vecinos y colegio aledaño.', 'Merced 350', 'Santiago', -33.4389, -70.6421, 320, 'completed', 'community_garden', '/images/spaces/space-2-after-opt.jpg', '/images/spaces/space-2-before-opt.jpg', '2025-01-10', '2025-05-15', datetime('now'), datetime('now')),
    (3, 'Plaza Activa Matta Norte', 'Intervención táctica en vereda ancha: jardineras modulares con flora nativa, bancas de pallets certificados, mesa de ping-pong y mural comunitario. Proyecto piloto de "calles completas".', 'Av. Matta 1200', 'Santiago', -33.4567, -70.6534, 150, 'completed', 'pocket_park', '/images/spaces/space-3-after-opt.jpg', '/images/spaces/space-3-before-opt.jpg', '2024-11-01', '2025-02-28', datetime('now'), datetime('now')),
    (4, 'Corredor Verde Matucana', 'Intervención lineal de 320 m² en veredas anchas y bandejones centrales. Jardineras modulares conectadas por senderos peatonales, arbolado nativo (arrayanes, pataguas) y mobiliario de descanso. Conecta Metro Matucana con Parque Quinta Normal.', 'Matucana 500 - 800', 'Estación Central', -33.4451, -70.6823, 320, 'in_progress', 'green_corridor', '/images/spaces/space-4-after-opt.jpg', '/images/spaces/space-4-before-opt.jpg', '2025-08-01', NULL, datetime('now'), datetime('now')),
    (5, 'Huerto Escolar República de México', 'Transformación de patio de concreto en huerto educativo con 12 camas de cultivo, invernadero modular, zona de compostaje y aula al aire libre. Alianzas con escuela básica y universidad.', 'República de México 0200', 'Santiago', -33.4489, -70.6542, 450, 'in_progress', 'community_garden', '/images/spaces/space-5-after-opt.jpg', '/images/spaces/space-5-before-opt.jpg', '2025-09-15', NULL, datetime('now'), datetime('now')),
    (6, 'Plaza Inclusiva Ñuñoa', 'Diseño universal en esquina de 200 m²: pavimento táctil, juegos inclusivos, zona de sombra con pérgola vegetal, bebedero accesible y bancas ergonómicas. Primera plaza 100% accesible del proyecto.', 'Irarrázaval 3500', 'Ñuñoa', -33.4598, -70.6012, 200, 'in_progress', 'resting_area', '/images/spaces/space-6-after-opt.jpg', '/images/spaces/space-6-before-opt.jpg', '2025-10-01', NULL, datetime('now'), datetime('now')),
    (7, 'Lote Baldío Franklin', 'Terreno de 800 m² en zona Franklin, actualmente microbasural. Potencial para mini bosque urbano (Miyawaki) con 300 árboles nativos densos. Requiere limpieza, remediación de suelo y permiso municipal.', 'Franklin 850', 'Santiago', -33.4621, -70.6589, 800, 'identified', 'urban_forest', '/images/spaces/space-7-after-opt.jpg', '/images/spaces/space-7-before-opt.jpg', NULL, NULL, datetime('now'), datetime('now')),
    (8, 'Bandejón Central Santa Rosa', 'Bandejón de 1.2 km de extensión, 15 m de ancho. Oportunidad para corredor verde lineal conectando 3 comunas. Requiere coordinación intermunicipal y estudio de factibilidad hidráulica.', 'Av. Santa Rosa (tramo completo)', 'San Miguel / La Cisterna / El Bosque', -33.5123, -70.6456, 18000, 'identified', 'green_corridor', '/images/spaces/space-8-after-opt.jpg', '/images/spaces/space-8-before-opt.jpg', NULL, NULL, datetime('now'), datetime('now')),
    (9, 'Esquina Residual Los Nogales', 'Esquina de 90 m² en población Los Nogales, usada como estacionamiento informal. Solicitada por junta de vecinos para plaza de bolsillo con juegos infantiles y zona de estar para adultos mayores.', 'Los Nogales 0450', 'Estación Central', -33.4534, -70.6912, 90, 'identified', 'pocket_park', '/images/spaces/space-9-after-opt.jpg', '/images/spaces/space-9-before-opt.jpg', NULL, NULL, datetime('now'), datetime('now')),
    (10, 'Terreno Errazo Lo Prado', 'Lote de 1.200 m² en zona industrial reconvertida. Potencial para huerto comunitario a gran escala con zona de mercado campesino, compostaje industrial y capacitación en agricultura urbana.', 'Av. Lo Prado 2500', 'Lo Prado', -33.4234, -70.7234, 1200, 'identified', 'community_garden', '/images/spaces/space-10-after-opt.jpg', '/images/spaces/space-10-before-opt.jpg', NULL, NULL, datetime('now'), datetime('now')),
    (11, 'Lote Abandonado San Pablo', 'Terreno baldío de 450 m² abandonado hace más de 10 años. Acumula escombros, maleza y residuos domésticos. Vecinos reportan presencia de roedores y riesgo de incendios. Potencial para plaza de bolsillo tras remediación.', 'San Pablo 3200', 'Estación Central', -33.4567, -70.7012, 450, 'identified', 'abandoned_land', NULL, NULL, NULL, NULL, datetime('now'), datetime('now')),
    (12, 'Vertedero Ilegal Mapocho Sur', 'Sitio eriazo usado como vertedero informal de escombros de construcción y residuos voluminosos. Afecta ribera sur del río Mapocho. Urgente intervención sanitaria y recuperación como corredor verde ribereño.', 'Costanera Sur 1500 (ribera Mapocho)', 'Pedro Aguirre Cerda', -33.4891, -70.6789, 1200, 'identified', 'dumping_ground', NULL, NULL, NULL, NULL, datetime('now'), datetime('now')),
    (13, 'Ex-Fábrica Textil Abandonada', 'Antigua fábrica textil de 2.500 m² cerrada en 2015. Estructura deteriorada, techos colapsados, suelo potencialmente contaminado. Vecinos solicitan demolición y recuperación como parque urbano con memoria histórica.', 'Av. Ecuador 2800', 'San Joaquín', -33.4967, -70.6234, 2500, 'identified', 'abandoned_land', NULL, NULL, NULL, NULL, datetime('now'), datetime('now')),
    (14, 'Microbasural Población La Victoria', 'Esquina de 180 m² usada como punto de acopio informal de basura domiciliaria y poda. Genera focos de insalubridad y malos olores. Junta de vecinos solicita limpieza y transformación en área de juegos infantil.', 'Víctor Jara 0450', 'Pedro Aguirre Cerda', -33.4912, -70.6567, 180, 'identified', 'dumping_ground', NULL, NULL, NULL, NULL, datetime('now'), datetime('now'));




INSERT OR REPLACE INTO communities (id, name, commune, contact_email, contact_phone, contact_person, member_count, space_id, created_at, updated_at) VALUES
    (1, 'Junta de Vecinos Barrio Yungay', 'Santiago', 'contacto@jjvvyungay.cl', '+56 2 2698 1234', 'María González', 450, 1, datetime('now'), datetime('now')),
    (2, 'Junta de Vecinos Barrio Brasil', 'Santiago', 'juntavecinosbrasil@gmail.com', '+56 9 8765 4321', 'Carlos Rodríguez', 380, 2, datetime('now'), datetime('now')),
    (3, 'Junta de Vecinos Matta Norte', 'Santiago', 'mattanorte@vecino.cl', '+56 2 2777 8899', 'Ana Martínez', 520, 3, datetime('now'), datetime('now')),
    (4, 'Comunidad Escolar República de México', 'Santiago', 'huertos@republicamexico.cl', '+56 2 2666 7788', 'Prof. Patricia Silva', 320, 5, datetime('now'), datetime('now')),
    (5, 'Junta de Vecinos Villa Ñuñoa', 'Ñuñoa', 'villanunoa@jjvv.cl', '+56 2 2333 4455', 'Roberto Pérez', 610, 6, datetime('now'), datetime('now')),
    (6, 'Junta de Vecinos Los Nogales', 'Estación Central', 'losnogales.vecino@gmail.com', '+56 9 1234 5678', 'Luisa Fernández', 290, 9, datetime('now'), datetime('now')),
    (7, 'Comité de Vivienda Lo Prado', 'Lo Prado', 'comite.loprado@vivenda.cl', '+56 2 2555 6677', 'Jorge Soto', 410, 10, datetime('now'), datetime('now')),
    (8, 'Red de Huertos Urbanos Santiago', 'Múltiples', 'redhuertos@stgo.cl', '+56 9 9988 7766', 'Coordinación rotativa', 1200, NULL, datetime('now'), datetime('now'));




UPDATE impact_metrics SET value = (SELECT COUNT(*) FROM spaces), updated_at = datetime('now') WHERE metric_key = 'total_spaces';
UPDATE impact_metrics SET value = (SELECT COALESCE(SUM(area_m2), 0) FROM spaces WHERE status = 'completed'), updated_at = datetime('now') WHERE metric_key = 'total_m2_recovered';
UPDATE impact_metrics SET value = (SELECT COUNT(*) FROM partners WHERE is_active = 1), updated_at = datetime('now') WHERE metric_key = 'total_partners';
UPDATE impact_metrics SET value = (SELECT COUNT(DISTINCT commune) FROM spaces WHERE commune IS NOT NULL), updated_at = datetime('now') WHERE metric_key = 'total_communes';
UPDATE impact_metrics SET value = (SELECT COUNT(*) FROM communities), updated_at = datetime('now') WHERE metric_key = 'total_communities';
UPDATE impact_metrics SET value = (SELECT COALESCE(SUM(member_count), 0) FROM communities) + 100, updated_at = datetime('now') WHERE metric_key = 'total_volunteers';