---
bug_id: BUG-0045-system-settings-media-format-options-limited
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 前端 MIME 选项硬编码为各 3 项

`SystemSettingsPage.tsx` L38–48：

```tsx
const IMAGE_MIME_OPTIONS = [JPG, PNG, WebP];  // 3 项
const VIDEO_MIME_OPTIONS = [MP4, MOV, AVI];   // 3 项
```

media Tab chip 仅渲染上述常量，管理员无法在 UI 勾选更多类型。

### 1.2 后端校验子集与 env 默认同样偏窄

`system_settings_service._validate_media` 中 `allowed_subset` 取自 `ALLOWED_IMAGE_TYPES` / `ALLOWED_VIDEO_TYPES` env；`.env.example` 图片 4 项（含 `image/jpg` 别名）、视频 3 项。即使前端扩展，PATCH 超出 env 子集的 MIME 仍会被 400 拒绝。

### 1.3 初始实现以 MVP 最小集交付

`add-system-settings` P0 仅保证 MIME 列表可配与 upload effective 联动；未扩展至业务常见全量格式。

## 2. 根本原因

### 2.1 前后端/env 三处 MIME _catalog_ 未统一维护

缺少单一来源（如 shared 常量或 `rules/media.md` 附录）驱动 UI chips、env 默认与后端校验，导致扩展需改多处且易遗漏。

### 2.2 REQ AC-018 只要求「可配」未规定最低选项数量

验收通过 3 种即满足「允许 MIME 列表可写」，用户反馈选项过少属交付后配置能力缺口。

## 3. 触发条件

1. `admin` 访问 `/admin/settings/media`。
2. 查看「支持图片格式」「支持视频格式」chip 区域 → 各仅 3 个可点选项。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend + backend-config |
| 是否接口缺陷 | 间接（PATCH 校验限制可选集） |
| 主要修复面 | 前端常量、`.env.example`、`_validate_media` 默认、pytest |
| 建议 Change | `fix-system-settings-media-format-options` |

## 5. 后续修复建议

1. 扩展 `IMAGE_MIME_OPTIONS` 至 8 项、`VIDEO_MIME_OPTIONS` 至 7 项（见 acceptance AC-001 清单）。
2. 同步 `.env.example`、`src/backend/.env.docker`。
3. 更新 `_validate_media` 默认 frozenset 与 env 一致。
4. 补充 pytest：PATCH 新 MIME + upload 校验生效。
