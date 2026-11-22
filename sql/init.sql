-- =============================================================================
-- Schema Initialization for Trama Urbana Verde
-- Run this script to create all tables in PostgreSQL/Supabase
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- SPACES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(500),
    commune VARCHAR(100),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    area_m2 INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'identified',
    category VARCHAR(50),
    image_url VARCHAR(500),
    before_image_url VARCHAR(500),
    started_at DATE,
    completed_at DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for spaces
CREATE INDEX IF NOT EXISTS ix_spaces_name ON spaces(name);
CREATE INDEX IF NOT EXISTS ix_spaces_commune ON spaces(commune);
CREATE INDEX IF NOT EXISTS ix_spaces_status ON spaces(status);
CREATE INDEX IF NOT EXISTS ix_spaces_category ON spaces(category);
CREATE INDEX IF NOT EXISTS ix_spaces_commune_status ON spaces(commune, status);
CREATE INDEX IF NOT EXISTS ix_spaces_status_category ON spaces(status, category);

-- Updated at trigger for spaces
CREATE OR REPLACE FUNCTION update_spaces_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_spaces_updated_at ON spaces;
CREATE TRIGGER trigger_spaces_updated_at
    BEFORE UPDATE ON spaces
    FOR EACH ROW
    EXECUTE FUNCTION update_spaces_updated_at();

-- =============================================================================
-- PARTNERS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS partners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    logo_url VARCHAR(500),
    website_url VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for partners
CREATE INDEX IF NOT EXISTS ix_partners_name ON partners(name);
CREATE INDEX IF NOT EXISTS ix_partners_type ON partners(type);
CREATE INDEX IF NOT EXISTS ix_partners_type_active ON partners(type, is_active);
CREATE INDEX IF NOT EXISTS ix_partners_display_order ON partners(display_order);

-- Updated at trigger for partners
CREATE OR REPLACE FUNCTION update_partners_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_partners_updated_at ON partners;
CREATE TRIGGER trigger_partners_updated_at
    BEFORE UPDATE ON partners
    FOR EACH ROW
    EXECUTE FUNCTION update_partners_updated_at();

-- =============================================================================
-- IMPACT METRICS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS impact_metrics (
    id SERIAL PRIMARY KEY,
    metric_key VARCHAR(100) NOT NULL UNIQUE,
    value BIGINT NOT NULL DEFAULT 0,
    label VARCHAR(255) NOT NULL,
    icon VARCHAR(100),
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for impact_metrics
CREATE UNIQUE INDEX IF NOT EXISTS uq_impact_metrics_key ON impact_metrics(metric_key);
CREATE INDEX IF NOT EXISTS ix_impact_metrics_display_order ON impact_metrics(display_order);

-- Updated at trigger for impact_metrics
CREATE OR REPLACE FUNCTION update_impact_metrics_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_impact_metrics_updated_at ON impact_metrics;
CREATE TRIGGER trigger_impact_metrics_updated_at
    BEFORE UPDATE ON impact_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_impact_metrics_updated_at();

-- =============================================================================
-- COMMUNITIES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS communities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    commune VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    contact_person VARCHAR(255),
    member_count INTEGER NOT NULL DEFAULT 0,
    space_id INTEGER REFERENCES spaces(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for communities
CREATE INDEX IF NOT EXISTS ix_communities_name ON communities(name);
CREATE INDEX IF NOT EXISTS ix_communities_commune ON communities(commune);
CREATE INDEX IF NOT EXISTS ix_communities_space_id ON communities(space_id);
CREATE INDEX IF NOT EXISTS ix_communities_commune_space ON communities(commune, space_id);

-- Updated at trigger for communities
CREATE OR REPLACE FUNCTION update_communities_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_communities_updated_at ON communities;
CREATE TRIGGER trigger_communities_updated_at
    BEFORE UPDATE ON communities
    FOR EACH ROW
    EXECUTE FUNCTION update_communities_updated_at();

-- =============================================================================
-- ROW LEVEL SECURITY (Optional - for Supabase)
-- =============================================================================
-- Enable RLS on all tables (uncomment if using Supabase with auth)
-- ALTER TABLE spaces ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE partners ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE impact_metrics ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE communities ENABLE ROW LEVEL SECURITY;

-- Example policies (customize based on your auth needs):
-- CREATE POLICY "Public read access" ON spaces FOR SELECT USING (true);
-- CREATE POLICY "Public read access" ON partners FOR SELECT USING (true);
-- CREATE POLICY "Public read access" ON impact_metrics FOR SELECT USING (true);
-- CREATE POLICY "Public read access" ON communities FOR SELECT USING (true);

-- =============================================================================
-- VERIFICATION
-- =============================================================================
-- Verify tables created
\dt spaces partners impact_metrics communities

-- Check indexes
\di spaces partners impact_metrics communities