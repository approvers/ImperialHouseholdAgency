-- Initialize database for Imperial Household Agency
-- This script runs when the PostgreSQL container first starts

-- Enable UUID extension for ULID storage
CREATE
EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set timezone
SET
timezone = 'UTC';

-- Set default privileges for future objects
ALTER
DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app;
ALTER
DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO app;
ALTER
DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO app;
