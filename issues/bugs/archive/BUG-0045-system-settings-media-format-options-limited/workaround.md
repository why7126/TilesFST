---
bug_id: BUG-0045-system-settings-media-format-options-limited
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
---

# 临时规避方案

## 1. 可用性规避

1. **使用现有 3 种格式上传**：JPEG/PNG/WebP 图片与 MP4/MOV/AVI 视频仍可正常上传（在 effective 配置启用前提下）。
2. **通过 env 扩展（运维）**：管理员可临时修改容器/本地 `ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES` 并重启后端，但 **UI 仍无法勾选** 未在 chip 列表中的类型，且 PATCH system_settings 可能被校验拒绝。

## 2. 操作规避

无安全的前端-only 规避；需代码修复才能完整扩展可配 MIME。

## 3. 风险说明

规避无法通过 UI 启用 GIF/WebM 等格式；业务若依赖此类素材需等待 fix change。
