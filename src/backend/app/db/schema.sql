CREATE TABLE IF NOT EXISTS tile_categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent_id INTEGER,
  name TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL,
  level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 3),
  description TEXT,
  status TEXT NOT NULL DEFAULT 'ENABLED' CHECK (status IN ('ENABLED', 'DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0 CHECK (sku_count >= 0),
  path TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(parent_id) REFERENCES tile_categories(id)
);

CREATE TABLE IF NOT EXISTS tile_specs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  width_mm INTEGER NOT NULL CHECK (width_mm BETWEEN 1 AND 9999),
  length_mm INTEGER NOT NULL CHECK (length_mm BETWEEN 1 AND 9999),
  thickness_mm REAL,
  unit TEXT NOT NULL DEFAULT 'mm',
  display_name TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 100,
  status TEXT NOT NULL DEFAULT 'ENABLED' CHECK (status IN ('ENABLED', 'DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0 CHECK (sku_count >= 0),
  remark TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(width_mm, length_mm, unit)
);

CREATE TABLE IF NOT EXISTS tiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sku_code TEXT NOT NULL UNIQUE,
  brand_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  spec_id INTEGER,
  size TEXT NOT NULL,
  surface_finish TEXT NOT NULL,
  color_family TEXT,
  reference_price REAL,
  remark TEXT,
  status TEXT NOT NULL DEFAULT 'DRAFT'
    CHECK (status IN ('PUBLISHED', 'DRAFT', 'NEEDS_COMPLETION', 'DISABLED')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(brand_id) REFERENCES brands(id),
  FOREIGN KEY(category_id) REFERENCES tile_categories(id),
  FOREIGN KEY(spec_id) REFERENCES tile_specs(id)
);

CREATE TABLE IF NOT EXISTS tile_images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tile_id INTEGER NOT NULL,
  object_key TEXT NOT NULL,
  url TEXT NOT NULL,
  is_main INTEGER NOT NULL DEFAULT 0,
  sort_order INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(tile_id) REFERENCES tiles(id)
);

CREATE TABLE IF NOT EXISTS tile_videos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tile_id INTEGER NOT NULL,
  object_key TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_size_bytes INTEGER,
  duration_seconds REAL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  FOREIGN KEY(tile_id) REFERENCES tiles(id)
);

CREATE TABLE IF NOT EXISTS miniapp_sku_favorites (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id TEXT NOT NULL,
  sku_id INTEGER NOT NULL,
  favorite INTEGER NOT NULL DEFAULT 1 CHECK (favorite IN (0, 1)),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(sku_id) REFERENCES tiles(id),
  UNIQUE(client_id, sku_id)
);

CREATE INDEX IF NOT EXISTS idx_miniapp_sku_favorites_client
  ON miniapp_sku_favorites(client_id, favorite, updated_at);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  phone TEXT,
  email TEXT,
  password_hash TEXT NOT NULL,
  display_name TEXT,
  role TEXT NOT NULL CHECK (role IN ('admin', 'employee', 'store_owner')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'disabled', 'deleted')),
  avatar_object_key TEXT,
  remark TEXT,
  token_version INTEGER NOT NULL DEFAULT 0,
  theme_mode TEXT NOT NULL DEFAULT 'system'
    CHECK (theme_mode IN ('system', 'dark_flagship', 'comfort_dark', 'light')),
  last_login_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS brands (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  sort_order INTEGER NOT NULL,
  short_name TEXT,
  english_name TEXT,
  logo_object_key TEXT,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'ENABLED' CHECK (status IN ('ENABLED', 'DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0 CHECK (sku_count >= 0),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS brand_certificates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 100,
  type TEXT NOT NULL CHECK (type IN ('QUALITY', 'INSPECTION', 'GREEN_BUILDING', 'HONOR', 'OTHER')),
  certificate_no TEXT,
  issuer TEXT,
  file_url TEXT NOT NULL,
  file_key TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_mime_type TEXT NOT NULL,
  file_size_bytes INTEGER NOT NULL CHECK (file_size_bytes > 0),
  is_permanent INTEGER NOT NULL DEFAULT 0 CHECK (is_permanent IN (0, 1)),
  effective_date TEXT,
  expiry_date TEXT,
  is_visible INTEGER NOT NULL DEFAULT 1 CHECK (is_visible IN (0, 1)),
  remark TEXT,
  deleted_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(brand_id) REFERENCES brands(id)
);

CREATE INDEX IF NOT EXISTS idx_brand_certificates_brand_visible
  ON brand_certificates(brand_id, is_visible, deleted_at);
CREATE INDEX IF NOT EXISTS idx_brand_certificates_type_deleted
  ON brand_certificates(type, deleted_at);
CREATE UNIQUE INDEX IF NOT EXISTS uq_brand_certificates_brand_name_active
  ON brand_certificates(brand_id, name)
  WHERE deleted_at IS NULL;

CREATE TABLE IF NOT EXISTS login_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  login_identifier TEXT NOT NULL,
  result TEXT NOT NULL CHECK (result IN ('success', 'failed')),
  failure_reason TEXT,
  ip TEXT,
  user_agent TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS profile_activity_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  metadata TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_profile_activity_logs_user_created
  ON profile_activity_logs(user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS password_change_attempts (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  success INTEGER NOT NULL CHECK (success IN (0, 1)),
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_password_change_attempts_user_created
  ON password_change_attempts(user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS topics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ENABLED', 'DISABLED')),
  cover_object_key TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS banners (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  display_client TEXT NOT NULL,
  position TEXT NOT NULL,
  image_object_key TEXT NOT NULL,
  image_source TEXT NOT NULL,
  sku_gallery_asset_id INTEGER,
  jump_type TEXT NOT NULL,
  sku_id INTEGER,
  external_url TEXT,
  topic_id INTEGER,
  brand_id INTEGER,
  sort_order INTEGER NOT NULL DEFAULT 100,
  valid_from TEXT,
  valid_to TEXT,
  status TEXT NOT NULL DEFAULT 'DRAFT'
    CHECK (status IN ('DRAFT', 'ONLINE', 'OFFLINE', 'EXPIRED')),
  remark TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  CHECK (display_client = 'MINIAPP_HOME'),
  CHECK (position IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')),
  CHECK (jump_type IN ('SKU_DETAIL', 'BRAND_DETAIL', 'EXTERNAL_LINK', 'TOPIC_PAGE', 'NO_JUMP')),
  CHECK (image_source IN ('sku_main_image', 'sku_gallery_image', 'custom_upload', 'topic_cover', 'brand_logo')),
  UNIQUE(display_client, position, title),
  FOREIGN KEY(sku_id) REFERENCES tiles(id),
  FOREIGN KEY(topic_id) REFERENCES topics(id),
  FOREIGN KEY(brand_id) REFERENCES brands(id),
  FOREIGN KEY(sku_gallery_asset_id) REFERENCES tile_images(id)
);

CREATE TABLE IF NOT EXISTS system_settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  updated_by TEXT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id TEXT PRIMARY KEY,
  actor_user_id TEXT NULL REFERENCES users(id),
  domain TEXT NOT NULL,
  action_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  metadata TEXT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_domain_created
  ON audit_logs(domain, created_at DESC);

CREATE TABLE IF NOT EXISTS request_logs (
  id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL,
  actor_user_id TEXT NULL REFERENCES users(id),
  actor_role TEXT,
  client_type TEXT NOT NULL DEFAULT 'backend',
  method TEXT NOT NULL,
  path TEXT NOT NULL,
  status_code INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL,
  ip_address_masked TEXT,
  user_agent_summary TEXT,
  summary TEXT NOT NULL,
  error_code TEXT,
  result TEXT NOT NULL DEFAULT 'success' CHECK (result IN ('success', 'failed')),
  metadata TEXT,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_request_logs_created
  ON request_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_request_logs_request_id
  ON request_logs(request_id);
CREATE INDEX IF NOT EXISTS idx_request_logs_actor_created
  ON request_logs(actor_user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_request_logs_status_created
  ON request_logs(status_code, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_request_logs_path_created
  ON request_logs(path, created_at DESC);

CREATE TABLE IF NOT EXISTS usage_events (
  id TEXT PRIMARY KEY,
  request_id TEXT,
  actor_user_id TEXT NULL REFERENCES users(id),
  actor_role TEXT,
  client_type TEXT NOT NULL DEFAULT 'web_admin',
  event_name TEXT NOT NULL,
  event_category TEXT NOT NULL,
  page_path TEXT,
  session_id TEXT,
  ip_address_masked TEXT,
  user_agent_summary TEXT,
  summary TEXT NOT NULL,
  duration_ms INTEGER,
  result TEXT NOT NULL DEFAULT 'success' CHECK (result IN ('success', 'failed')),
  metadata TEXT,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_usage_events_created
  ON usage_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_events_event_created
  ON usage_events(event_name, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_events_request_id
  ON usage_events(request_id);
CREATE INDEX IF NOT EXISTS idx_usage_events_actor_created
  ON usage_events(actor_user_id, created_at DESC);
