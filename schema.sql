-- =============================================================================
-- Munib and Co - Chartered Certified Accountant
-- PostgreSQL schema reference
--
-- This file documents the schema Django will create when you run
-- `python manage.py migrate` against a PostgreSQL database (USE_POSTGRES=True
-- in your .env). You do NOT need to run this file manually -- Django's
-- migrations are the source of truth and will create/alter these tables for
-- you, including Django's own auth/session/admin tables which are omitted
-- here for brevity. This file is provided for documentation, review, and
-- academic submission purposes.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- accounts_user  (custom user model, extends Django's AbstractUser)
-- ---------------------------------------------------------------------------
CREATE TABLE accounts_user (
    id                  BIGSERIAL PRIMARY KEY,
    password            VARCHAR(128) NOT NULL,
    last_login          TIMESTAMPTZ NULL,
    is_superuser        BOOLEAN NOT NULL DEFAULT FALSE,
    username            VARCHAR(150) NOT NULL UNIQUE,
    first_name          VARCHAR(150) NOT NULL DEFAULT '',
    last_name           VARCHAR(150) NOT NULL DEFAULT '',
    email               VARCHAR(254) NOT NULL DEFAULT '',
    is_staff            BOOLEAN NOT NULL DEFAULT FALSE,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    phone               VARCHAR(20) NOT NULL DEFAULT '',
    address             VARCHAR(255) NOT NULL DEFAULT '',
    cnic                VARCHAR(20) NOT NULL DEFAULT '',
    company_name        VARCHAR(150) NOT NULL DEFAULT '',
    profile_photo       VARCHAR(100) NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- services_service
-- ---------------------------------------------------------------------------
CREATE TABLE services_service (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(150) NOT NULL,
    slug                VARCHAR(170) NOT NULL UNIQUE,
    icon                VARCHAR(40) NOT NULL DEFAULT 'bi-receipt',
    short_description   VARCHAR(300) NOT NULL,
    description         TEXT NOT NULL,
    fee_note            VARCHAR(150) NOT NULL DEFAULT '',
    "order"             INTEGER NOT NULL DEFAULT 0,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- appointments_appointment
-- ---------------------------------------------------------------------------
CREATE TABLE appointments_appointment (
    id                  BIGSERIAL PRIMARY KEY,
    user_id             BIGINT NULL REFERENCES accounts_user(id) ON DELETE SET NULL,
    name                VARCHAR(150) NOT NULL,
    email               VARCHAR(254) NOT NULL,
    phone               VARCHAR(20) NOT NULL,
    service_id          BIGINT NULL REFERENCES services_service(id) ON DELETE SET NULL,
    preferred_date      DATE NOT NULL,
    preferred_time      TIME NOT NULL,
    message             TEXT NOT NULL DEFAULT '',
    status              VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending','confirmed','completed','cancelled')),
    admin_notes         TEXT NOT NULL DEFAULT '',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_appointment_status ON appointments_appointment(status);
CREATE INDEX idx_appointment_date ON appointments_appointment(preferred_date);

-- ---------------------------------------------------------------------------
-- blog_blogpost
-- ---------------------------------------------------------------------------
CREATE TABLE blog_blogpost (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    slug                VARCHAR(220) NOT NULL UNIQUE,
    author_id           BIGINT NULL REFERENCES accounts_user(id) ON DELETE SET NULL,
    category            VARCHAR(20) NOT NULL DEFAULT 'news'
                        CHECK (category IN ('tax','secp','audit','news','guides')),
    featured_image      VARCHAR(100) NULL,
    excerpt             VARCHAR(300) NOT NULL,
    content             TEXT NOT NULL,
    is_published        BOOLEAN NOT NULL DEFAULT TRUE,
    published_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- contact_contactmessage
-- ---------------------------------------------------------------------------
CREATE TABLE contact_contactmessage (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(150) NOT NULL,
    email               VARCHAR(254) NOT NULL,
    phone               VARCHAR(20) NOT NULL DEFAULT '',
    subject             VARCHAR(200) NOT NULL,
    message             TEXT NOT NULL,
    is_read             BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- core_testimonial
-- ---------------------------------------------------------------------------
CREATE TABLE core_testimonial (
    id                  BIGSERIAL PRIMARY KEY,
    client_name         VARCHAR(120) NOT NULL,
    designation         VARCHAR(150) NOT NULL DEFAULT '',
    photo               VARCHAR(100) NULL,
    content             TEXT NOT NULL,
    rating              SMALLINT NOT NULL DEFAULT 5,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- core_faq
-- ---------------------------------------------------------------------------
CREATE TABLE core_faq (
    id                  BIGSERIAL PRIMARY KEY,
    question            VARCHAR(250) NOT NULL,
    answer              TEXT NOT NULL,
    "order"             INTEGER NOT NULL DEFAULT 0,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE
);

-- ---------------------------------------------------------------------------
-- core_document
-- ---------------------------------------------------------------------------
CREATE TABLE core_document (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    category            VARCHAR(20) NOT NULL DEFAULT 'other'
                        CHECK (category IN ('income_tax','sales_tax','secp','checklist','other')),
    description         VARCHAR(300) NOT NULL DEFAULT '',
    file                VARCHAR(100) NOT NULL,
    uploaded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- core_teammember
-- ---------------------------------------------------------------------------
CREATE TABLE core_teammember (
    id                  BIGSERIAL PRIMARY KEY,
    name                VARCHAR(120) NOT NULL,
    designation         VARCHAR(150) NOT NULL,
    bio                 TEXT NOT NULL DEFAULT '',
    photo               VARCHAR(100) NULL,
    "order"             INTEGER NOT NULL DEFAULT 0,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE
);

-- =============================================================================
-- Notes
-- =============================================================================
-- 1. Django additionally creates auth_group, auth_permission,
--    accounts_user_groups, accounts_user_user_permissions, django_admin_log,
--    django_content_type, django_migrations and django_session tables
--    automatically -- these support the built-in admin panel, permissions
--    and session framework and do not need to be created manually.
-- 2. All *_id foreign key columns are BIGINT and indexed automatically by
--    Django/PostgreSQL.
-- 3. To generate this exact schema yourself (recommended over running this
--    file by hand), set USE_POSTGRES=True in your .env, create an empty
--    PostgreSQL database, and run:
--        python manage.py migrate
-- =============================================================================
