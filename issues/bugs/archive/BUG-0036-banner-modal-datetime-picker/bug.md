---
bug_id: BUG-0036-banner-modal-datetime-picker
title: Banner弹窗有效期DateTime选择器无法选择时分秒
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）「有效期开始」「有效期结束」字段使用原生 `<input type="datetime-local">`，无法满足运营配置精确生效/失效时间的需求：

1. **时分秒不可选**：HTML5 `datetime-local` 精度为分钟，**不支持**秒；提交时 `valid_from` 硬编码追加 `:00+00:00`、`valid_to` 追加 `:59+00:00`，用户无法指定任意秒值。
2. **交互不完整**：在暗色管理端（`color-scheme: dark` + 自定义 `.input` 样式）下，部分浏览器/OS 仅展示日期选择或时间选择器难以操作，表现为「只能选日期」。
3. **展示格式不符**：控件值为 `YYYY-MM-DDTHH:mm`；列表 `formatBannerDateTime` 截断至分钟（`slice(0, 16)`），与 capture 要求的 `yyyy/mm/dd hh:mm:ss` 展示不一致。
4. **与原型形态差异**：REQ-0016 弹窗 HTML 原型为 **单个**「有效期」输入，示例 `2026-06-01 00:00 至 2026-07-01 23:59`；当前实现为 **两个** 独立字段（「有效期开始」「有效期结束」）。字段数量与格式须在 `/bug-complete` acceptance 中裁定（HTML > PNG > acceptance 优先级）。

根因类型为 **frontend-ui**（缺 DS DateTime 组件 + 依赖原生控件）。后端 `BannerAdminService.validate_validity` 与 `_parse_dt` 已接受 ISO datetime（含秒），**无需** API 变更即可支持精确时间。

# 复现步骤

1. 以 admin 或 employee 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 进入「Banner 管理」列表页（`/admin/banners`）。
3. 点击「+ 新增 Banner」或某行「编辑」，打开弹窗。
4. 找到「有效期开始」「有效期结束」字段，点击日期/时间控件。
5. 尝试通过 UI 选择具体的小时、分钟、秒。
6. 可选：保存后观察列表「有效期」列与再次编辑时回填值是否含秒。
7. 可选：并排对照 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-sku-detail.html` 中有效期字段形态。

# 期望结果

- 运营可通过 **DateTime 选择器**（非裸 `datetime-local`）配置有效期开始与结束，至少支持 **年-月-日 时:分:秒** 精度（若 acceptance 裁定 UI 仅到分钟、秒由策略填充，须在 acceptance 中写明）。
- 展示格式可读且一致：弹窗输入区与列表「有效期」列对齐（目标格式以 acceptance 定稿：`yyyy/mm/dd hh:mm:ss` 或 prototype 的 `YYYY-MM-DD HH:mm` 区间形态）。
- 提交 payload 的 `valid_from` / `valid_to` 为合法 ISO datetime，后端校验通过；`time_status`（ACTIVE / PENDING / EXPIRED）按配置时刻正确计算。
- 视觉与交互对齐 REQ-0016 AC-027（公共字段含有效期）及弹窗 prototype（字段数量与并排 PNG 以 `/bug-complete` 裁定）。

# 实际结果

- `BannerFormModal.tsx` 使用 `type="datetime-local"`，无项目内 DateTime 复合组件（无 shadcn Calendar / `react-day-picker` 等依赖）。
- 提交逻辑强制秒值：`valid_from: validFrom ? \`${validFrom}:00+00:00\` : null`，`valid_to: validTo ? \`${validTo}:59+00:00\` : null`。
- 编辑回填：`setValidFrom(banner.valid_from?.slice(0, 16) ?? '')`，丢弃秒与展示格式信息。
- `formatBannerDateTime` 仅显示到分钟，列表不展示秒。
- 与 `capture.md` 描述一致：无法通过 UI 选择时分秒，或格式与需求不符。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增、编辑 Banner 时无法精确配置生效/失效时刻 |
| Banner 运营逻辑 | `valid_from` / `valid_to` 精度受限 → `time_status`、上线/待生效/已过期展示可能不符合运营预期 |
| REQ-0016 验收 | AC-027（有效期字段）、AC-051（modal HTML/PNG 并排）未达标 |
| 关联 Change | `add-banner-management`（sprint-003，已 applied）交付即存在 |
| 同域 BUG | 可与 BUG-0031～0035（Banner 弹窗 UI）合并为同一 `fix-banner-modal-*` change |
| 后端 / API / DB | 无变更需求（ISO 解析与校验已就绪） |

不影响权限边界、MinIO、SQLite schema、小程序或店主端只读展示。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断 Banner 创建/保存（可留空有效期或仅选到分钟），但 **削弱** 运营对生效窗口的精确控制能力。
- 修复需引入或组合 DS 级 DateTime 输入（前端为主），工作量大于纯 CSS 文案类 BUG，但无后端迁移风险。
- 属于 REQ-0016 首版实现缺口，非线上回归；宜与 Banner 弹窗 UI 簇一并纳入 `fix-*` change，而非独立 hotfix。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗有效期字段（问题点） | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| 列表有效期展示 | `src/web/src/features/admin/lib/banner-display.ts` → `formatBannerDateTime` |
| 后端有效期校验 | `src/backend/app/services/banner_admin_service.py` → `validate_validity`、`_parse_dt` |
| 弹窗原型 HTML | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-*.html` |
| 父 Change | `openspec/changes/add-banner-management/` |
| UI 规范 | `rules/ui-design.md`（semantic token、组件优先级） |

**裁定说明**：单字段区间 vs 双字段、秒是否必选、展示格式以 prototype HTML 与 `/bug-complete` acceptance 为准；若与 capture 的 `yyyy/mm/dd hh:mm:ss` 冲突，在 fix change delta spec 中 MODIFIED 消化。
