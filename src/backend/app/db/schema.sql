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

CREATE TABLE IF NOT EXISTS tiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sku_code TEXT NOT NULL UNIQUE,
  brand_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
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
  FOREIGN KEY(category_id) REFERENCES tile_categories(id)
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
