CREATE TABLE IF NOT EXISTS schema_migrations (
  version VARCHAR(128) PRIMARY KEY,
  applied_at DATETIME(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
  id CHAR(36) PRIMARY KEY,
  username VARCHAR(128) NOT NULL UNIQUE,
  phone VARCHAR(64),
  email VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(128),
  role VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'active',
  avatar_object_key VARCHAR(512),
  remark TEXT,
  token_version INT NOT NULL DEFAULT 0,
  last_login_at VARCHAR(64),
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  CONSTRAINT chk_users_role CHECK (role IN ('admin', 'employee', 'store_owner')),
  CONSTRAINT chk_users_status CHECK (status IN ('active', 'disabled', 'deleted'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS brands (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(128) NOT NULL UNIQUE,
  sort_order INT NOT NULL,
  short_name VARCHAR(128),
  english_name VARCHAR(128),
  logo_object_key VARCHAR(512),
  description TEXT,
  status VARCHAR(32) NOT NULL DEFAULT 'ENABLED',
  sku_count INT NOT NULL DEFAULT 0,
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  CONSTRAINT chk_brands_status CHECK (status IN ('ENABLED', 'DISABLED')),
  CONSTRAINT chk_brands_sku_count CHECK (sku_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tile_categories (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  parent_id BIGINT,
  name VARCHAR(128) NOT NULL,
  code VARCHAR(128) NOT NULL UNIQUE,
  sort_order INT NOT NULL,
  level INT NOT NULL,
  description TEXT,
  status VARCHAR(32) NOT NULL DEFAULT 'ENABLED',
  sku_count INT NOT NULL DEFAULT 0,
  path VARCHAR(512) NOT NULL,
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_tile_categories_parent
    FOREIGN KEY(parent_id) REFERENCES tile_categories(id),
  CONSTRAINT chk_tile_categories_level CHECK (level BETWEEN 1 AND 3),
  CONSTRAINT chk_tile_categories_status CHECK (status IN ('ENABLED', 'DISABLED')),
  CONSTRAINT chk_tile_categories_sku_count CHECK (sku_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tile_specs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  width_mm INT NOT NULL,
  length_mm INT NOT NULL,
  thickness_mm DOUBLE,
  unit VARCHAR(32) NOT NULL DEFAULT 'mm',
  display_name VARCHAR(128) NOT NULL,
  sort_order INT NOT NULL DEFAULT 100,
  status VARCHAR(32) NOT NULL DEFAULT 'ENABLED',
  sku_count INT NOT NULL DEFAULT 0,
  remark TEXT,
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  UNIQUE KEY uq_tile_specs_size_unit (width_mm, length_mm, unit),
  CONSTRAINT chk_tile_specs_width CHECK (width_mm BETWEEN 1 AND 9999),
  CONSTRAINT chk_tile_specs_length CHECK (length_mm BETWEEN 1 AND 9999),
  CONSTRAINT chk_tile_specs_status CHECK (status IN ('ENABLED', 'DISABLED')),
  CONSTRAINT chk_tile_specs_sku_count CHECK (sku_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tiles (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(180) NOT NULL,
  sku_code VARCHAR(128) NOT NULL UNIQUE,
  brand_id BIGINT NOT NULL,
  category_id BIGINT NOT NULL,
  spec_id BIGINT,
  size VARCHAR(128) NOT NULL,
  surface_finish VARCHAR(128) NOT NULL,
  color_family VARCHAR(128),
  reference_price DOUBLE,
  remark TEXT,
  status VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_tiles_brand FOREIGN KEY(brand_id) REFERENCES brands(id),
  CONSTRAINT fk_tiles_category FOREIGN KEY(category_id) REFERENCES tile_categories(id),
  CONSTRAINT fk_tiles_spec FOREIGN KEY(spec_id) REFERENCES tile_specs(id),
  CONSTRAINT chk_tiles_status CHECK (status IN ('PUBLISHED', 'DRAFT', 'NEEDS_COMPLETION', 'DISABLED')),
  INDEX idx_tiles_brand_status (brand_id, status),
  INDEX idx_tiles_category_status (category_id, status),
  INDEX idx_tiles_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tile_images (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  tile_id BIGINT NOT NULL,
  object_key VARCHAR(512) NOT NULL,
  url VARCHAR(768) NOT NULL,
  is_main TINYINT NOT NULL DEFAULT 0,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_tile_images_tile FOREIGN KEY(tile_id) REFERENCES tiles(id),
  INDEX idx_tile_images_tile_sort (tile_id, sort_order, id),
  INDEX idx_tile_images_object_key (object_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tile_videos (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  tile_id BIGINT NOT NULL,
  object_key VARCHAR(512) NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_size_bytes BIGINT,
  duration_seconds DOUBLE,
  sort_order INT NOT NULL DEFAULT 0,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_tile_videos_tile FOREIGN KEY(tile_id) REFERENCES tiles(id),
  INDEX idx_tile_videos_tile_sort (tile_id, sort_order, id),
  INDEX idx_tile_videos_object_key (object_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS login_logs (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36),
  login_identifier VARCHAR(255) NOT NULL,
  result VARCHAR(32) NOT NULL,
  failure_reason VARCHAR(255),
  ip VARCHAR(128),
  user_agent TEXT,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_login_logs_user FOREIGN KEY(user_id) REFERENCES users(id),
  CONSTRAINT chk_login_logs_result CHECK (result IN ('success', 'failed')),
  INDEX idx_login_logs_user_created (user_id, created_at),
  INDEX idx_login_logs_identifier_created (login_identifier, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS profile_activity_logs (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36) NOT NULL,
  action_type VARCHAR(64) NOT NULL,
  summary VARCHAR(255) NOT NULL,
  metadata TEXT,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_profile_activity_logs_user FOREIGN KEY(user_id) REFERENCES users(id),
  INDEX idx_profile_activity_logs_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS password_change_attempts (
  id CHAR(36) PRIMARY KEY,
  user_id CHAR(36) NOT NULL,
  success TINYINT NOT NULL,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_password_change_attempts_user FOREIGN KEY(user_id) REFERENCES users(id),
  CONSTRAINT chk_password_change_attempts_success CHECK (success IN (0, 1)),
  INDEX idx_password_change_attempts_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS topics (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(128) NOT NULL UNIQUE,
  title VARCHAR(180) NOT NULL,
  status VARCHAR(32) NOT NULL,
  cover_object_key VARCHAR(512),
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  CONSTRAINT chk_topics_status CHECK (status IN ('ENABLED', 'DISABLED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS banners (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  display_client VARCHAR(64) NOT NULL,
  position VARCHAR(64) NOT NULL,
  image_object_key VARCHAR(512) NOT NULL,
  image_source VARCHAR(64) NOT NULL,
  sku_gallery_asset_id BIGINT,
  jump_type VARCHAR(64) NOT NULL,
  sku_id BIGINT,
  external_url VARCHAR(768),
  topic_id BIGINT,
  sort_order INT NOT NULL DEFAULT 100,
  valid_from VARCHAR(64),
  valid_to VARCHAR(64),
  status VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
  remark TEXT,
  created_at VARCHAR(64) NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  UNIQUE KEY uq_banners_client_position_title (display_client, position, title),
  CONSTRAINT fk_banners_sku FOREIGN KEY(sku_id) REFERENCES tiles(id),
  CONSTRAINT fk_banners_topic FOREIGN KEY(topic_id) REFERENCES topics(id),
  CONSTRAINT fk_banners_gallery_asset FOREIGN KEY(sku_gallery_asset_id) REFERENCES tile_images(id),
  CONSTRAINT chk_banners_status CHECK (status IN ('DRAFT', 'ONLINE', 'OFFLINE', 'EXPIRED')),
  CONSTRAINT chk_banners_image_source CHECK (image_source IN ('sku_main_image', 'sku_gallery_image', 'custom_upload', 'topic_cover')),
  INDEX idx_banners_status_position (display_client, position, status),
  INDEX idx_banners_sort (sort_order, updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS system_settings (
  `key` VARCHAR(128) PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at VARCHAR(64) NOT NULL,
  updated_by CHAR(36) NULL,
  CONSTRAINT fk_system_settings_updated_by FOREIGN KEY(updated_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS audit_logs (
  id CHAR(36) PRIMARY KEY,
  actor_user_id CHAR(36) NULL,
  domain VARCHAR(64) NOT NULL,
  action_type VARCHAR(64) NOT NULL,
  summary VARCHAR(255) NOT NULL,
  metadata TEXT NULL,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_audit_logs_actor FOREIGN KEY(actor_user_id) REFERENCES users(id),
  INDEX idx_audit_logs_domain_created (domain, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS request_logs (
  id CHAR(36) PRIMARY KEY,
  request_id VARCHAR(128) NOT NULL,
  actor_user_id CHAR(36) NULL,
  actor_role VARCHAR(32),
  client_type VARCHAR(32) NOT NULL DEFAULT 'backend',
  method VARCHAR(16) NOT NULL,
  path VARCHAR(768) NOT NULL,
  status_code INT NOT NULL,
  duration_ms INT NOT NULL,
  ip_address_masked VARCHAR(128),
  user_agent_summary VARCHAR(512),
  summary VARCHAR(255) NOT NULL,
  error_code VARCHAR(64),
  result VARCHAR(32) NOT NULL DEFAULT 'success',
  metadata TEXT,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_request_logs_actor FOREIGN KEY(actor_user_id) REFERENCES users(id),
  CONSTRAINT chk_request_logs_result CHECK (result IN ('success', 'failed')),
  INDEX idx_request_logs_created (created_at),
  INDEX idx_request_logs_request_id (request_id),
  INDEX idx_request_logs_actor_created (actor_user_id, created_at),
  INDEX idx_request_logs_status_created (status_code, created_at),
  INDEX idx_request_logs_path_created (path(255), created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usage_events (
  id CHAR(36) PRIMARY KEY,
  request_id VARCHAR(128),
  actor_user_id CHAR(36) NULL,
  actor_role VARCHAR(32),
  client_type VARCHAR(32) NOT NULL DEFAULT 'web_admin',
  event_name VARCHAR(64) NOT NULL,
  event_category VARCHAR(64) NOT NULL,
  page_path VARCHAR(768),
  session_id VARCHAR(128),
  ip_address_masked VARCHAR(128),
  user_agent_summary VARCHAR(512),
  summary VARCHAR(255) NOT NULL,
  duration_ms INT NULL,
  result VARCHAR(32) NOT NULL DEFAULT 'success',
  metadata TEXT,
  created_at VARCHAR(64) NOT NULL,
  CONSTRAINT fk_usage_events_actor FOREIGN KEY(actor_user_id) REFERENCES users(id),
  CONSTRAINT chk_usage_events_result CHECK (result IN ('success', 'failed')),
  INDEX idx_usage_events_created (created_at),
  INDEX idx_usage_events_event_created (event_name, created_at),
  INDEX idx_usage_events_request_id (request_id),
  INDEX idx_usage_events_actor_created (actor_user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
