---
bug_id: BUG-0045-system-settings-media-format-options-limited
title: 系统设置媒体与存储图片/视频格式各仅 3 种
severity: medium
status: pending_review
owner: product
discovered_at: 2026-06-28 17:53:48
environment: local|docker
related_requirement: REQ-0017-system-settings
related_change: add-system-settings
related_bug: null
---

# 缺陷说明

「系统设置 → 媒体与存储」Tab（`/admin/settings/media`）中，「支持图片格式」与「支持视频格式」chip 控件各仅提供 3 种可选项。图片为 JPG / PNG / WebP；视频为 MP4 / MOV / AVI。选项偏少，管理员无法通过 UI 启用更多主流 MIME 类型，与瓷砖业务常见素材格式及 upload 链路扩展需求不符。

> **Scope 说明**：本 BUG 聚焦 **可勾选 MIME 选项扩展及前后端校验对齐**；不包含最大 MB 下拉、MinIO 只读字段或 object key 规则。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置 → 媒体与存储」（`/admin/settings/media`）。
3. 查看「支持图片格式」「支持视频格式」区域 chip 数量与标签。
4. （可选）尝试 PATCH 含 UI 未列出的 MIME（如 `image/gif`），后端 `_validate_media` 可能因不在 `allowed_subset` 而拒绝。

# 期望结果

- 图片格式 **SHOULD** 扩展至主流集合，至少包含：JPEG、PNG、WebP、GIF、SVG、BMP、TIFF、HEIC/HEIF（具体清单于 `/bug-complete` 定稿）。
- 视频格式 **SHOULD** 扩展至主流集合，至少包含：MP4、MOV、AVI、WebM、MKV、MPEG、3GP 等（具体清单于 `/bug-complete` 定稿）。
- 前端 chip、后端 `system_settings_service._validate_media` 默认/ env 子集、`.env.example` **MUST** 三者对齐。
- PATCH 后下一次 `POST /uploads` **MUST** 按新 effective MIME 校验（REQ-0017 AC-020）。

# 实际结果

- `IMAGE_MIME_OPTIONS` / `VIDEO_MIME_OPTIONS` 各硬编码 3 项（`SystemSettingsPage.tsx` L38–48）。
- `.env.example` 中 `ALLOWED_IMAGE_TYPES` 4 项、`ALLOWED_VIDEO_TYPES` 3 项，未覆盖 WebM 等。
- 后端校验 `allowed_subset` 取自 env 默认，前端无法勾选 env 未声明的类型。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 media Tab | 格式配置能力不足 |
| 上传链路 | 管理员无法在 UI 启用更多 MIME；effective settings 受限 |
| REQ-0017 AC-018 / AC-020 | MIME 列表可配但选项过少 |
| 后端 | `system_settings_service.py`、`config.py`、`.env.example` |
| 数据库 | 无 schema 变更（KV 存逗号分隔字符串） |
| Orval | 无（payload 仍为 string） |
| 店主端 / 小程序 | 间接（上传校验随 effective 配置变化） |

# 严重等级说明

严重程度为 `medium`。

理由：

- **影响配置能力**：不崩溃，但限制平台可接受媒体类型，业务扩展受阻。
- **100% 稳定复现**：进入 media Tab 即见。
- **修复面跨前后端**：需同步 UI 选项、env 默认、后端校验子集与测试；无 hotfix 紧迫性但需完整链路验收。

# 代码线索

| 线索 | 路径 |
|---|---|
| 前端 MIME 选项 | `src/web/src/pages/admin/SystemSettingsPage.tsx`（L38–48, L417–444） |
| 后端校验 | `src/backend/app/services/system_settings_service.py`（L160–181） |
| Env 默认 | `.env.example`、`src/backend/.env.docker` |
| Effective merge | `src/backend/app/services/effective_settings_service.py` |
| Upload 校验 | `src/backend/app/api/v1/uploads.py` |
| 测试 | `src/backend/tests/test_system_settings.py`、`test_upload_settings.py` |
| 建议 Change | `fix-system-settings-media-format-options` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0017 交付后配置选项不足，非全新 REQ） |
| 根因类型 | 前端/后端/env 默认 MIME 集合过窄且未同步扩展 |
| 是否回归 | 否（初始实现即 3 种） |
| 建议修复 Change | `fix-system-settings-media-format-options` |
