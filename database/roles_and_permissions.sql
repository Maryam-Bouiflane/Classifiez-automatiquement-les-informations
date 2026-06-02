-- =========================================
-- SECURITY SETUP (STRICT ACCESS)
-- Database: churn_db
-- =========================================

-- =========================================
-- Application database user
-- Used by the API only
-- =========================================
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_backend') THEN
      CREATE ROLE app_backend WITH LOGIN PASSWORD 'user_password';
   END IF;
END
$$;

-- Allow connection to DB
GRANT CONNECT ON DATABASE churn_db TO app_backend;

-- Allow schema usage (required to access tables)
GRANT USAGE ON SCHEMA public TO app_backend;

-- =========================================
-- Remove all table access first (safety baseline)
-- =========================================
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM app_backend;

-- =========================================
-- Explicit permissions (ONLY what is needed)
-- =========================================

-- employees
GRANT SELECT, INSERT ON TABLE employees TO app_backend;

-- predictions_log
GRANT SELECT, INSERT ON TABLE predictions_log TO app_backend;

-- sequences (required for SERIAL / IDENTITY)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_backend;

-- =========================================
-- Default deny for future tables
-- (important: prevents accidental access)
-- =========================================
ALTER DEFAULT PRIVILEGES IN SCHEMA public
REVOKE ALL ON TABLES FROM app_backend;

-- If you later want to explicitly allow new tables,
-- you must add GRANT manually (safe by design)