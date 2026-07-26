## Why

[BUG-0045-system-settings-media-format-options-limited](issues/bugs/archive/BUG-0045-system-settings-media-format-options-limited/) 已评审：media Tab 图片/视频格式各仅 3 种，需扩展主流 MIME 并与 env/后端校验对齐。

## What Changes

- 扩展 `IMAGE_MIME_OPTIONS`（8）与 `VIDEO_MIME_OPTIONS`（7）。
- 同步 `.env.example`、`.env.docker`、`system_settings_service._validate_media` 默认子集。
- MODIFIED system-settings 分组字段 + object-storage effective MIME。
- pytest + vitest。

## Capabilities

### Modified Capabilities

- `system-settings`：MODIFIED「系统设置分组字段范围」— MIME 选项 catalog。
- `object-storage`：MODIFIED「管理端上传必须写入 MinIO 单桶」— effective MIME 子集说明。

## Impact

Web + 后端 + env；无 schema 变更。

## Rollback Plan

恢复 3 项 MIME 常量与 env 默认值。
