CREATE TABLE IF NOT EXISTS tile_categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  model TEXT NOT NULL,
  category_id INTEGER,
  color TEXT,
  size TEXT,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
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

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  phone TEXT,
  email TEXT,
  password_hash TEXT NOT NULL,
  display_name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin', 'employee', 'store_owner')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'disabled')),
  last_login_at TEXT,
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
