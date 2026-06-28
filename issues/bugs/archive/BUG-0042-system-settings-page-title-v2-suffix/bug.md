---
bug_id: BUG-0042-system-settings-page-title-v2-suffix
title: 系统设置页眉标多余 V2 后缀
severity: low
status: pending_review
owner: product
discovered_at: 2026-06-28 17:53:48
environment: local|docker
related_requirement: REQ-0017-system-settings
related_change: add-system-settings
related_bug: null
---

# 缺陷说明

Web 管理端「系统设置」页（`/admin/settings/*`）页头 `page-hero` 区域眉标（eyebrow）显示为 `SYSTEM / SYSTEM SETTINGS / V2`，末尾 `/ V2` 为多余版本后缀。用户期望眉标为 `SYSTEM / SYSTEM SETTINGS`，与 REQ-0017 AC-006 及侧栏分组命名一致，不应在页内眉标重复产品版本信息（版本已由侧栏 `ProductVersionBadge` 展示）。

> **Scope 说明**：本 BUG 仅聚焦 **页头眉标文案**；不包含 Tab 标题、summary-grid、保存逻辑或其它 Shell 结构。

# 复现步骤

1. 以 `admin` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 侧栏进入「系统设置」（默认重定向至 `/admin/settings/basic`）。
3. 观察页头 `settings-page-hero` 内 `.eyebrow` 文案。
4. （可选）切换至 media/security 等 Tab，眉标后缀均相同。

# 期望结果

- 页头眉标 **MUST** 为 `SYSTEM / SYSTEM SETTINGS`，**MUST NOT** 含 `/ V2` 或任意版本号后缀。
- 视觉 **MUST** 继续使用 semantic token（`.eyebrow`），无裸 Hex。

# 实际结果

- 眉标硬编码为 `SYSTEM / SYSTEM SETTINGS / V2`（`SystemSettingsPage.tsx` 约 L798）。
- 所有 5 个 Tab 共用同一页头，均展示多余后缀。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 `/admin/settings/*` | 页头文案与 AC-006 / 用户期望不一致 |
| `admin` 角色 | 唯一可访问者，均可见 |
| REQ-0017 验收 | AC-006 要求 `SYSTEM / SETTINGS`；prototype HTML 亦含 `/ V2`，修复时需 reconcile |
| 后端 / API / 数据库 / Orval | 无 |
| 店主端 / 小程序 | 无 |

**与 REQ-0017 / 已交付 Change 关系**

| 项 | 说明 |
|---|---|
| REQ-0017 AC-006 | 页头眉标含 `SYSTEM / SETTINGS` |
| `add-system-settings` | 按 prototype HTML port，prototype 亦含 `/ V2` |
| 用户反馈 | 明确要求去除 `/ V2` |
| 本 BUG | 交付后文案 polish，非功能回归 |

# 严重等级说明

严重程度为 `low`。

理由：

- **不阻塞功能**：仅影响页头展示文案。
- **100% 稳定复现**：任意 Tab 均可见。
- **修复面极小**：单行文案修改；可选同步 prototype HTML 与 delta spec。

# 代码线索

| 线索 | 路径 |
|---|---|
| 眉标硬编码 | `src/web/src/pages/admin/SystemSettingsPage.tsx`（L798） |
| 样式 | `src/web/src/features/admin/styles/system-settings.css` |
| Prototype | `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-*.html` |
| 建议 Change | `fix-system-settings-page-title-v2-suffix` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0017 交付后的 UI 文案偏差） |
| 根因类型 | 前端硬编码文案，port prototype 时带入版本后缀 |
| 是否回归 | 否（自 `add-system-settings` 起即存在） |
| 建议修复 Change | `fix-system-settings-page-title-v2-suffix` |
