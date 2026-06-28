---
bug_id: BUG-0045-system-settings-media-format-options-limited
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
related_requirement: REQ-0017-system-settings
related_bug: null
---

# 回归验收标准

> 修复 MUST 扩展 media Tab 可勾选 MIME 集合，且前后端/env MUST 对齐。下列 MIME 为最低交付清单。

**图片 MIME（8）**：`image/jpeg`、`image/png`、`image/webp`、`image/gif`、`image/svg+xml`、`image/bmp`、`image/tiff`、`image/heic`

**视频 MIME（7）**：`video/mp4`、`video/quicktime`、`video/x-msvideo`、`video/webm`、`video/x-matroska`、`video/mpeg`、`video/3gpp`

## AC-001 UI MUST 展示扩展后的 chip 选项

**Given** `admin` 访问 `/admin/settings/media`  
**When** 查看格式 chip 区  
**Then** 图片 MUST 至少含 8 个可切换 chip（标签可为 JPG/PNG/WebP/GIF/SVG/BMP/TIFF/HEIC）  
**And** 视频 MUST 至少含 7 个可切换 chip（MP4/MOV/AVI/WebM/MKV/MPEG/3GP）

- [ ] AC-001

## AC-002 PATCH MUST 接受扩展 MIME 子集

**Given** 修复完成  
**When** `admin` PATCH `allowed_image_types` 含 `image/gif,image/jpeg`  
**Then** MUST 返回 200  
**When** PATCH 含 env 未声明的 MIME（如 `image/foo`）  
**Then** MUST 返回 400

- [ ] AC-002

## AC-003 env 默认 MUST 与 UI 选项对齐

**Given** 修复完成  
**When** 检查 `.env.example` 与 `src/backend/.env.docker`  
**Then** `ALLOWED_IMAGE_TYPES` MUST 包含 AC-001 全部图片 MIME  
**And** `ALLOWED_VIDEO_TYPES` MUST 包含 AC-001 全部视频 MIME

- [ ] AC-003

## AC-004 upload MUST 按 effective 新 MIME 校验（REQ AC-020）

**Given** PATCH 启用 `image/gif`  
**When** 上传 `image/gif` 文件  
**Then** MUST 成功（在大小限制内）  
**When** 上传未启用 MIME  
**Then** MUST 400 `FILE_TYPE_NOT_ALLOWED`

- [ ] AC-004

## AC-005 只读字段与 MB 限制 MUST 无回归

**Given** 修复完成  
**When** 查看 media Tab  
**Then** MinIO bucket、Key 规则 MUST 仍只读  
**And** 图片/视频最大 MB 下拉 MUST 行为不变

- [ ] AC-005

## AC-006 测试 MUST 通过

**Given** `/opsx-apply` 完成  
**When** 运行 `pytest tests/test_system_settings.py` 及 upload 相关测试  
**Then** MUST 全部通过  
**And** `SystemSettingsPage` vitest MUST 通过

- [ ] AC-006
