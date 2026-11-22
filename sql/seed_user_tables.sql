-- =============================================================================
-- Seed Data for User, Request, Organization tables (SQLite compatible)
-- =============================================================================

-- =============================================================================
-- ORGANIZATIONS (Contactos para derivación automática)
-- =============================================================================

-- Municipalidades (por comuna)
INSERT OR REPLACE INTO organizations (id, name, type, email, phone, contact_person, commune, priority_order, is_active, auto_send, created_at, updated_at) VALUES
    (1, 'Municipalidad de Santiago', 'municipality', 'medioambiente@munistgo.cl', '+56 2 2698 1234', 'Dirección de Medio Ambiente', 'Santiago', 1, 1, 1, datetime('now'), datetime('now')),
    (2, 'Municipalidad de Estación Central', 'municipality', 'medioambiente@estacioncentral.cl', '+56 2 2777 1234', 'Dirección de Aseo y Ornato', 'Estación Central', 1, 1, 1, datetime('now'), datetime('now')),
    (3, 'Municipalidad de Ñuñoa', 'municipality', 'parques@nunoa.cl', '+56 2 2333 4455', 'Dirección de Parques y Jardines', 'Ñuñoa', 1, 1, 1, datetime('now'), datetime('now')),
    (4, 'Municipalidad de Providencia', 'municipality', 'medioambiente@providencia.cl', '+56 2 2333 5566', 'Departamento de Áreas Verdes', 'Providencia', 1, 1, 1, datetime('now'), datetime('now')),
    (5, 'Municipalidad de La Reina', 'municipality', 'medioambiente@lareina.cl', '+56 2 2244 5566', 'Dirección de Medio Ambiente', 'La Reina', 1, 1, 1, datetime('now'), datetime('now')),
    (6, 'Municipalidad de Las Condes', 'municipality', 'parques@lascondes.cl', '+56 2 2244 6677', 'Dirección de Parques', 'Las Condes', 1, 1, 1, datetime('now'), datetime('now')),
    (7, 'Municipalidad de Vitacura', 'municipality', 'medioambiente@vitacura.cl', '+56 2 2244 7788', 'Departamento de Áreas Verdes', 'Vitacura', 1, 1, 1, datetime('now'), datetime('now')),
    (8, 'Municipalidad de Lo Barnechea', 'municipality', 'medioambiente@lobarnechea.cl', '+56 2 2244 8899', 'Dirección de Medio Ambiente', 'Lo Barnechea', 1, 1, 1, datetime('now'), datetime('now')),
    (9, 'Municipalidad de Independencia', 'municipality', 'medioambiente@independencia.cl', '+56 2 2777 2233', 'Dirección de Aseo y Ornato', 'Independencia', 1, 1, 1, datetime('now'), datetime('now')),
    (10, 'Municipalidad de Recoleta', 'municipality', 'parques@recoleta.cl', '+56 2 2777 3344', 'Dirección de Parques', 'Recoleta', 1, 1, 1, datetime('now'), datetime('now')),
    (11, 'Municipalidad de Conchalí', 'municipality', 'medioambiente@conchali.cl', '+56 2 2777 4455', 'Dirección de Medio Ambiente', 'Conchalí', 1, 1, 1, datetime('now'), datetime('now')),
    (12, 'Municipalidad de Huechuraba', 'municipality', 'parques@huechuraba.cl', '+56 2 2777 5566', 'Dirección de Parques', 'Huechuraba', 1, 1, 1, datetime('now'), datetime('now')),
    (13, 'Municipalidad de Quilicura', 'municipality', 'medioambiente@quilicura.cl', '+56 2 2777 6677', 'Dirección de Medio Ambiente', 'Quilicura', 1, 1, 1, datetime('now'), datetime('now')),
    (14, 'Municipalidad de Pudahuel', 'municipality', 'parques@pudahuel.cl', '+56 2 2777 7788', 'Dirección de Parques', 'Pudahuel', 1, 1, 1, datetime('now'), datetime('now')),
    (15, 'Municipalidad de Lo Prado', 'municipality', 'medioambiente@loprado.cl', '+56 2 2777 8899', 'Dirección de Medio Ambiente', 'Lo Prado', 1, 1, 1, datetime('now'), datetime('now')),
    (16, 'Municipalidad de Cerro Navia', 'municipality', 'parques@cerronavia.cl', '+56 2 2777 9900', 'Dirección de Parques', 'Cerro Navia', 1, 1, 1, datetime('now'), datetime('now')),
    (17, 'Municipalidad de Quinta Normal', 'municipality', 'medioambiente@quintanormal.cl', '+56 2 2777 0011', 'Dirección de Medio Ambiente', 'Quinta Normal', 1, 1, 1, datetime('now'), datetime('now')),
    (18, 'Municipalidad de Renca', 'municipality', 'parques@renca.cl', '+56 2 2777 1122', 'Dirección de Parques', 'Renca', 1, 1, 1, datetime('now'), datetime('now')),
    (19, 'Municipalidad de San Miguel', 'municipality', 'medioambiente@sanmiguel.cl', '+56 2 2777 2233', 'Dirección de Medio Ambiente', 'San Miguel', 1, 1, 1, datetime('now'), datetime('now')),
    (20, 'Municipalidad de San Joaquín', 'municipality', 'parques@sanjuaquin.cl', '+56 2 2777 3344', 'Dirección de Parques', 'San Joaquín', 1, 1, 1, datetime('now'), datetime('now')),
    (21, 'Municipalidad de La Granja', 'municipality', 'medioambiente@lagranja.cl', '+56 2 2777 4455', 'Dirección de Medio Ambiente', 'La Granja', 1, 1, 1, datetime('now'), datetime('now')),
    (22, 'Municipalidad de La Florida', 'municipality', 'parques@laflorida.cl', '+56 2 2777 5566', 'Dirección de Parques', 'La Florida', 1, 1, 1, datetime('now'), datetime('now')),
    (23, 'Municipalidad de La Pintana', 'municipality', 'medioambiente@lapintana.cl', '+56 2 2777 6677', 'Dirección de Medio Ambiente', 'La Pintana', 1, 1, 1, datetime('now'), datetime('now')),
    (24, 'Municipalidad de San Ramón', 'municipality', 'parques@sanramon.cl', '+56 2 2777 7788', 'Dirección de Parques', 'San Ramón', 1, 1, 1, datetime('now'), datetime('now')),
    (25, 'Municipalidad de El Bosque', 'municipality', 'medioambiente@elbosque.cl', '+56 2 2777 8899', 'Dirección de Medio Ambiente', 'El Bosque', 1, 1, 1, datetime('now'), datetime('now')),
    (26, 'Municipalidad de Pedro Aguirre Cerda', 'municipality', 'parques@pedroaguirrecerda.cl', '+56 2 2777 9900', 'Dirección de Parques', 'Pedro Aguirre Cerda', 1, 1, 1, datetime('now'), datetime('now')),
    (27, 'Municipalidad de Puente Alto', 'municipality', 'medioambiente@puentealto.cl', '+56 2 2777 0011', 'Dirección de Medio Ambiente', 'Puente Alto', 1, 1, 1, datetime('now'), datetime('now')),
    (28, 'Municipalidad de La Cisterna', 'municipality', 'parques@lacisterna.cl', '+56 2 2777 1122', 'Dirección de Parques', 'La Cisterna', 1, 1, 1, datetime('now'), datetime('now')),
    (29, 'Municipalidad de San Bernardo', 'municipality', 'medioambiente@sanbernardo.cl', '+56 2 2777 2233', 'Dirección de Medio Ambiente', 'San Bernardo', 1, 1, 1, datetime('now'), datetime('now')),
    (30, 'Municipalidad de Buin', 'municipality', 'parques@buin.cl', '+56 2 2777 3344', 'Dirección de Parques', 'Buin', 1, 1, 1, datetime('now'), datetime('now')),
    (31, 'Municipalidad de Calera de Tango', 'municipality', 'medioambiente@caleradetango.cl', '+56 2 2777 4455', 'Dirección de Medio Ambiente', 'Calera de Tango', 1, 1, 1, datetime('now'), datetime('now')),
    (32, 'Municipalidad de Peñaflor', 'municipality', 'parques@penaflor.cl', '+56 2 2777 5566', 'Dirección de Parques', 'Peñaflor', 1, 1, 1, datetime('now'), datetime('now')),
    (33, 'Municipalidad de Talagante', 'municipality', 'medioambiente@talagante.cl', '+56 2 2777 6677', 'Dirección de Medio Ambiente', 'Talagante', 1, 1, 1, datetime('now'), datetime('now')),
    (34, 'Municipalidad de El Monte', 'municipality', 'parques@elmonte.cl', '+56 2 2777 7788', 'Dirección de Parques', 'El Monte', 1, 1, 1, datetime('now'), datetime('now')),
    (35, 'Municipalidad de Isla de Maipo', 'municipality', 'medioambiente@islademaipo.cl', '+56 2 2777 8899', 'Dirección de Medio Ambiente', 'Isla de Maipo', 1, 1, 1, datetime('now'), datetime('now')),
    (36, 'Municipalidad de María Pinto', 'municipality', 'parques@mariapinto.cl', '+56 2 2777 9900', 'Dirección de Parques', 'María Pinto', 1, 1, 1, datetime('now'), datetime('now')),
    (37, 'Municipalidad de Melipilla', 'municipality', 'medioambiente@melipilla.cl', '+56 2 2777 0011', 'Dirección de Medio Ambiente', 'Melipilla', 1, 1, 1, datetime('now'), datetime('now')),
    (38, 'Municipalidad de Alhué', 'municipality', 'parques@alhue.cl', '+56 2 2777 1122', 'Dirección de Parques', 'Alhué', 1, 1, 1, datetime('now'), datetime('now')),
    (39, 'Municipalidad de Curacaví', 'municipality', 'medioambiente@curacavi.cl', '+56 2 2777 2233', 'Dirección de Medio Ambiente', 'Curacaví', 1, 1, 1, datetime('now'), datetime('now')),
    (40, 'Municipalidad de Padre Hurtado', 'municipality', 'parques@padrehurtado.cl', '+56 2 2777 3344', 'Dirección de Parques', 'Padre Hurtado', 1, 1, 1, datetime('now'), datetime('now'));

-- Empresas con RSE
INSERT OR REPLACE INTO organizations (id, name, type, email, phone, contact_person, region, priority_order, is_active, auto_send, created_at, updated_at) VALUES
    (41, 'Constructora Andes S.A.', 'company', 'rse@andes.cl', '+56 2 2666 1111', 'Gerencia RSE', 'Metropolitana', 1, 1, 1, datetime('now'), datetime('now')),
    (42, 'Inmobiliaria Verde Urbana', 'company', 'sostenibilidad@verdeurbana.cl', '+56 2 2666 2222', 'Jefa de Sostenibilidad', 'Metropolitana', 2, 1, 1, datetime('now'), datetime('now')),
    (43, 'Empresa Eléctrica Metropolitana', 'company', 'comunidad@eem.cl', '+56 2 2666 3333', 'Relaciones Comunitarias', 'Metropolitana', 3, 1, 1, datetime('now'), datetime('now')),
    (44, 'Aguas Andinas', 'company', 'rse@aguasandinas.cl', '+56 2 2666 4444', 'Gerencia Sostenibilidad', 'Metropolitana', 4, 1, 1, datetime('now'), datetime('now')),
    (45, 'Cencosud', 'company', 'sostenibilidad@cencosud.cl', '+56 2 2666 5555', 'Gerencia RSE', 'Metropolitana', 5, 1, 1, datetime('now'), datetime('now')),
    (46, 'Banco de Chile', 'company', 'rse@bancochile.cl', '+56 2 2666 6666', 'Gerencia Sostenibilidad', 'Metropolitana', 6, 1, 1, datetime('now'), datetime('now')),
    (47, 'CCU', 'company', 'sostenibilidad@ccu.cl', '+56 2 2666 7777', 'Gerencia RSE', 'Metropolitana', 7, 1, 1, datetime('now'), datetime('now')),
    (48, 'Entel', 'company', 'rse@entel.cl', '+56 2 2666 8888', 'Gerencia Sostenibilidad', 'Metropolitana', 8, 1, 1, datetime('now'), datetime('now'));

-- Colegios
INSERT OR REPLACE INTO organizations (id, name, type, email, phone, contact_person, commune, region, priority_order, is_active, auto_send, created_at, updated_at) VALUES
    (49, 'Colegio República de México', 'school', 'direccion@republicamexico.cl', '+56 2 2666 1111', 'Director(a)', 'Santiago', 'Metropolitana', 1, 1, 1, datetime('now'), datetime('now')),
    (50, 'Colegio San Ignacio El Bosque', 'school', 'direccion@sanignacio.cl', '+56 2 2666 2222', 'Director(a)', 'Providencia', 'Metropolitana', 2, 1, 1, datetime('now'), datetime('now')),
    (51, 'Colegio Verbo Divino', 'school', 'direccion@verbodivino.cl', '+56 2 2666 3333', 'Director(a)', 'Las Condes', 'Metropolitana', 3, 1, 1, datetime('now'), datetime('now')),
    (52, 'Liceo Experimental Manuel de Salas', 'school', 'direccion@manuelsalas.cl', '+56 2 2666 4444', 'Director(a)', 'Ñuñoa', 'Metropolitana', 4, 1, 1, datetime('now'), datetime('now')),
    (53, 'Colegio Alianza Francesa', 'school', 'direccion@alianzafrancesa.cl', '+56 2 2666 5555', 'Director(a)', 'Vitacura', 'Metropolitana', 5, 1, 1, datetime('now'), datetime('now')),
    (54, 'Colegio Nido de Águilas', 'school', 'direccion@nido.cl', '+56 2 2666 6666', 'Director(a)', 'Lo Barnechea', 'Metropolitana', 6, 1, 1, datetime('now'), datetime('now')),
    (55, 'Colegio Craighouse', 'school', 'direccion@craighouse.cl', '+56 2 2666 7777', 'Director(a)', 'Lo Barnechea', 'Metropolitana', 7, 1, 1, datetime('now'), datetime('now')),
    (56, 'The Grange School', 'school', 'direccion@grange.cl', '+56 2 2666 8888', 'Director(a)', 'La Reina', 'Metropolitana', 8, 1, 1, datetime('now'), datetime('now'));

-- Universidades
INSERT OR REPLACE INTO organizations (id, name, type, email, phone, contact_person, commune, region, priority_order, is_active, auto_send, created_at, updated_at) VALUES
    (57, 'Universidad de Chile - FAU', 'university', 'fau@uchile.cl', '+56 2 2978 1111', 'Decanato FAU', 'Santiago', 'Metropolitana', 1, 1, 1, datetime('now'), datetime('now')),
    (58, 'Pontificia Universidad Católica - FADEU', 'university', 'fadeu@uc.cl', '+56 2 2354 2222', 'Decanato FADEU', 'Santiago', 'Metropolitana', 2, 1, 1, datetime('now'), datetime('now')),
    (59, 'Universidad de Santiago - FAU', 'university', 'fau@usach.cl', '+56 2 2718 3333', 'Decanato FAU', 'Estación Central', 'Metropolitana', 3, 1, 1, datetime('now'), datetime('now')),
    (60, 'Universidad Diego Portales - Arquitectura', 'university', 'arquitectura@udp.cl', '+56 2 2666 4444', 'Dirección Escuela', 'Santiago', 'Metropolitana', 4, 1, 1, datetime('now'), datetime('now')),
    (61, 'Universidad Central - Arquitectura', 'university', 'arquitectura@ucentral.cl', '+56 2 2666 5555', 'Dirección Escuela', 'Santiago', 'Metropolitana', 5, 1, 1, datetime('now'), datetime('now')),
    (62, 'Universidad Mayor - Arquitectura', 'university', 'arquitectura@umayor.cl', '+56 2 2666 6666', 'Dirección Escuela', 'Santiago', 'Metropolitana', 6, 1, 1, datetime('now'), datetime('now')),
    (63, 'Universidad Finis Terrae - Arquitectura', 'university', 'arquitectura@uft.cl', '+56 2 2666 7777', 'Dirección Escuela', 'Providencia', 'Metropolitana', 7, 1, 1, datetime('now'), datetime('now')),
    (64, 'Universidad del Desarrollo - Arquitectura', 'university', 'arquitectura@udd.cl', '+56 2 2666 8888', 'Dirección Escuela', 'Las Condes', 'Metropolitana', 8, 1, 1, datetime('now'), datetime('now'));

-- Redes Sociales (para derivación final)
INSERT OR REPLACE INTO organizations (id, name, type, email, phone, contact_person, region, priority_order, is_active, auto_send, custom_subject, created_at, updated_at) VALUES
    (65, 'Trama Urbana Verde - Instagram', 'social_media', 'instagram@tramaurbanaverde.cl', NULL, 'Equipo Comunicaciones', 'Metropolitana', 1, 1, 0, 'Publicación en Instagram: Solicitud ciudadana de recuperación urbana', datetime('now'), datetime('now')),
    (66, 'Trama Urbana Verde - Twitter/X', 'social_media', 'twitter@tramaurbanaverde.cl', NULL, 'Equipo Comunicaciones', 'Metropolitana', 2, 1, 0, 'Hilo en Twitter/X: Solicitud ciudadana de recuperación urbana', datetime('now'), datetime('now')),
    (67, 'Trama Urbana Verde - LinkedIn', 'social_media', 'linkedin@tramaurbanaverde.cl', NULL, 'Equipo Comunicaciones', 'Metropolitana', 3, 1, 0, 'Publicación en LinkedIn: Solicitud ciudadana de recuperación urbana', datetime('now'), datetime('now')),
    (68, 'Trama Urbana Verde - Facebook', 'social_media', 'facebook@tramaurbanaverde.cl', NULL, 'Equipo Comunicaciones', 'Metropolitana', 4, 1, 0, 'Publicación en Facebook: Solicitud ciudadana de recuperación urbana', datetime('now'), datetime('now'));

-- =============================================================================
-- CONFIGURATION SETTINGS (stored as a simple key-value approach)
-- =============================================================================

-- Tabla de configuración para plazos y parámetros del sistema (SQLite compatible)
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR REPLACE INTO system_config (key, value, description, updated_at) VALUES
    ('routing_wait_days', '15', 'Días de espera antes de derivar al siguiente destinatario', CURRENT_TIMESTAMP),
    ('routing_enabled', '1', 'Habilitar derivación automática (1=sí, 0=no)', CURRENT_TIMESTAMP),
    ('moderation_required', '1', 'Requerir moderación antes de publicar solicitudes (1=sí, 0=no)', CURRENT_TIMESTAMP),
    ('max_photo_size_mb', '5', 'Tamaño máximo de foto en MB', CURRENT_TIMESTAMP),
    ('allowed_photo_types', 'image/jpeg,image/png,image/webp', 'Tipos MIME permitidos para fotos', CURRENT_TIMESTAMP),
    ('support_cooldown_hours', '24', 'Horas antes de poder apoyar otra solicitud (anti-spam)', CURRENT_TIMESTAMP),
    ('auto_approve_after_days', '60', 'Días para auto-aprobar si hay respuesta positiva sin acción manual', CURRENT_TIMESTAMP);