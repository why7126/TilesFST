## Context

- **BUG**: BUG-0045（medium）
- **MIME 清单**（acceptance AC-001）：
  - 图片：jpeg, png, webp, gif, svg+xml, bmp, tiff, heic
  - 视频：mp4, quicktime, x-msvideo, webm, x-matroska, mpeg, 3gpp

## Decisions

### D1：三处对齐

前端 chips、env `ALLOWED_*_TYPES`、后端 `_validate_media` allowed_subset MUST 一致。

## Test Plan

- pytest PATCH 新 MIME + upload 校验
- vitest media tab chip 数量
