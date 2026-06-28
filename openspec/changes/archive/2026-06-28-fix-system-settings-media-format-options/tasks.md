## 1. 准备

- [x] 1.1 阅读 BUG-0045 acceptance（8+7 MIME 清单）

## 2. 前端

- [x] 2.1 扩展 `IMAGE_MIME_OPTIONS` / `VIDEO_MIME_OPTIONS`
- [x] 2.2 勾选 AC-001

## 3. 后端与 env

- [x] 3.1 更新 `.env.example`、`.env.docker`
- [x] 3.2 更新 `_validate_media` 默认 frozenset
- [x] 3.3 pytest PATCH + upload 用例（AC-002～AC-004）

## 4. 测试

- [x] 4.1 `pytest tests/test_system_settings.py` 及相关 upload 测试
- [x] 4.2 `pnpm vitest run SystemSettingsPage`

## 5. 追溯与归档

- [x] 5.1 trace.md；评估 incidents（不需要）
- [x] 5.2 `/opsx-archive fix-system-settings-media-format-options`
