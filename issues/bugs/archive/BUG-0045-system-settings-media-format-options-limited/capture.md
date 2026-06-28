---
bug_id: BUG-0045-system-settings-media-format-options-limited
status: captured
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 17:53:48
severity_hint: medium
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug:
captured_via: capture
classification_rationale: 媒体与存储 Tab 可勾选格式仅 3 种，低于主流业务场景与 upload 链路常用 MIME，属配置能力缺口
---

# 现象

「系统设置 → 媒体与存储」Tab 中，「支持图片格式」与「支持视频格式」各仅提供 3 种可选项（图片：JPG/PNG/WebP；视频：MP4/MOV/AVI），选项偏少，无法覆盖更多主流格式。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置 → 媒体与存储」（`/admin/settings/media`）。
3. 查看「支持图片格式」「支持视频格式」区域的格式切换控件。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 提供更多主流图片格式（如 GIF、SVG、HEIC/HEIF、BMP、TIFF 等）与视频格式（如 WebM、MKV、MPEG、3GP 等）供勾选；与上传校验及 `.env` 默认能力对齐。 |
| **实际** | 图片与视频各仅 3 种格式选项。 |

# 初步线索

- `SystemSettingsPage.tsx`：`IMAGE_MIME_OPTIONS`（3 项）、`VIDEO_MIME_OPTIONS`（3 项）。
- 后端 `system_settings_service.py` 默认允许集合可能更宽；前端 UI 选项未同步扩展。
- 关联 REQ-0017 AC-018（允许 MIME 列表可配）。

# 附件

- screenshots/
- logs/
