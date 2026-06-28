---
sprint_id: sprint-003
title: Sprint 003 迭代经验复盘
status: draft
created_at: 2026-06-28 19:42:56
updated_at: 2026-06-28 19:42:56
owner: product
related_iteration: iterations/archive/sprint-003/
related_requirements:
  - REQ-0014-profile-page
  - REQ-0015-password-change
  - REQ-0009-tile-spec-management
  - REQ-0012-object-storage-key-layout
  - REQ-0016-banner-management
  - REQ-0017-system-settings
related_bugs:
  - BUG-0021-sidebar-menu-icons-indistinguishable
  - BUG-0022-profile-basic-info-redundant-role-status
  - BUG-0023-profile-duplicate-save-buttons
  - BUG-0024-change-password-error-wrong-field
  - BUG-0025-change-password-toggle-button-misalignment
  - BUG-0026-change-password-cancel-confirm-redundant
  - BUG-0027-tile-spec-list-ui-inconsistency
  - BUG-0028-tile-spec-modal-form-layout
  - BUG-0029-tile-spec-list-not-refresh-after-create
  - BUG-0030-banner-list-ui-inconsistency
  - BUG-0031-banner-modal-image-section-label
  - BUG-0032-banner-modal-upload-button-label
  - BUG-0033-banner-modal-form-layout-overflow
  - BUG-0034-banner-modal-link-selector-combined
  - BUG-0035-banner-modal-sku-hero-image-no-effect
  - BUG-0036-banner-modal-datetime-picker
  - BUG-0037-tile-spec-status-confirm-ui-inconsistency
  - BUG-0038-tile-sku-modal-spec-hint-styling
  - BUG-0039-banner-list-display-position-column
  - BUG-0040-banner-modal-width-too-narrow
  - BUG-0041-sidebar-user-menu-avatar-missing
  - BUG-0042-system-settings-page-title-v2-suffix
  - BUG-0043-system-settings-duplicate-save-buttons
  - BUG-0045-system-settings-media-format-options-limited
  - BUG-0046-system-settings-reset-confirm-ui-inconsistency
  - BUG-0047-system-settings-save-tip-layout-shift
  - BUG-0048-banner-modal-width-css-cascade-overridden
related_changes:
  - add-admin-profile-page
  - add-admin-password-change
  - add-tile-spec-management
  - update-object-storage-key-layout
  - add-banner-management
  - add-system-settings
  - fix-sidebar-menu-icons-indistinguishable
  - fix-profile-basic-info-redundant-role-status
  - fix-profile-duplicate-save-buttons
  - fix-change-password-modal-errors
  - fix-tile-spec-admin-ui
  - fix-tile-spec-status-confirm-ui
  - fix-banner-admin-ui
  - fix-tile-sku-modal-spec-hint-styling
  - fix-banner-list-and-modal-ui
  - fix-sidebar-user-menu-avatar
  - fix-banner-modal-width-css-cascade
  - fix-profile-activities-display-limit
  - fix-system-settings-page-title-v2-suffix
  - fix-system-settings-duplicate-save-buttons
  - fix-system-settings-media-format-options
  - fix-system-settings-reset-confirm-ui
  - fix-system-settings-save-tip-layout-shift
source: /sprint-exps
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 003 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-06-28 10:03:15 ~ 2026-07-12 23:59:59 |
| 实际关闭 | 2026-06-28 19:39:54（同日归档） |
| REQ | 6（全部 done / archive） |
| BUG | 27（全部 done / archive） |
| Change | 23（7 add/update + 16 fix-*） |
| Change archived | **23/23** |
| 估算 | 80 SP / 54 人天（终态） |
| 初始范围 | 2 REQ（0014+0015）→ 同日滚动扩至 6 REQ + 27 BUG |
| `/sprint-propose` 滚动更新 | ≥15 次（见 `sprint.md` §变更记录） |
| fix-* 占比 | 16/23 ≈ **70%** |
| acceptance-report 细项 AC | 大量 `[ ]` 待人工 sign-off |
| 延后项 | REQ-0013（未评审）；系统设置 P1b 登录锁定（design 可选） |

### 交付主线（时间线摘要）

| 时段 | 事件 |
|------|------|
| 10:03 | 创建 sprint-003（REQ-0014/0015） |
| 10:15~11:40 | 滚动纳入 REQ-0009/0012/0016/0017 |
| 10:35~19:02 | 滚动纳入 BUG-0021~0048 及对应 fix-* |
| 12:15~19:34 | 各 add/fix change apply + archive |
| 19:39 | `/sprint-archive` 关闭迭代 |

证据：`iterations/archive/sprint-003/sprint.md` §变更记录、`acceptance-report.md`。

## 2. 流程复盘

### 做得好的

1. **评审门禁有效**：Sprint 内 REQ/BUG 均为 approved/in_sprint/done；REQ-0013 正确留在「延后项」。
2. **fix 合并策略**：同页/同模块 BUG 合并 change（如 BUG-0024~0026 → `fix-change-password-modal-errors`；BUG-0030~0036 → `fix-banner-admin-ui`），减少 archive 碎片。
3. **依赖顺序可执行**：Banner BUG-0048 明确「须在 list/modal fix archive 前 apply」；sprint-apply 队列整体未出现 MODIFIED 标题硬失败。
4. **Docker 冒烟脚本**：`scripts/smoke-banner-docker.sh`、`scripts/smoke-system-settings-docker.sh` 纳入 tasks，可复用于后续迭代。
5. **workflow-sync + promote**：REQ-0017 archive 后 promote 顺畅；BUG-0021 因 trace YAML 损坏需人工修复（见问题）。

### 问题

1. **同日滚动扩 scope**：从 2 REQ 扩至 6 REQ + 27 BUG，容量估算从 ~29 人天涨至 54 人天，但仍在单日内 apply/archive——**计划容量与执行节奏脱节**，acceptance 人工勾选被跳过。
2. **fix 比例过高（70%）**：每个 add-* 后紧跟 1~5 个 fix-*，说明 add 阶段 acceptance / 原型 gate 未吸收 Sprint 002 行动项（AdminListPage、横切 confirm/toast）。
3. **sprint-propose 过于频繁**：开发中多次 propose 扩 scope，增加 sprint-apply 队列重算与 archive 顺序认知负担。
4. **归档 delta 冲突再现**：`add-system-settings` archive 时 `system-settings` ADDED 与已合并 fix-* 主 spec 冲突，需删除 ADDED delta 后重试（同 Sprint 002 `add-tile-sku-management` 模式）。
5. **trace 文档质量**：BUG-0021 `trace.md` YAML 块未闭合 ` ``` `，导致 workflow-sync 无法写 `status: done`，阻塞 promote。

### 优化建议

1. **冻结 scope 窗口**：Sprint 启动后 N 小时内允许 propose；进入 apply 后新 BUG 默认下一 Sprint（除 P0 热修）。
2. **add-* apply 前强制横切 checklist**：引用 `best-practices/admin-list-page-consistency.md`、`admin-form-page-consistency.md`、`admin-modal-width-css-cascade.md`。
3. **archive 预检**：`openspec archive --dry-run` 或脚本检测 ADDED 与 `openspec/specs/` 重名 Requirement。
4. **trace.md 校验**：`bug-complete` / workflow-sync 前校验 YAML fence 闭合（可纳入 CI `--check`）。

## 3. 需求与设计

### PRD 与原型

- **REQ-0016 Banner**、**REQ-0017 系统设置** 体量大（多 Tab/多弹窗变体），上线后各产生 **7+ / 5** 个 UI fix，与 Sprint 002 SKU 模式类似。
- **HTML prototype 存在但仍出列表/弹窗类 BUG**：Banner、规格列表分页（BUG-0027/0030）说明 **port CSS 未强制 DOM 契约**，而非缺原型。
- **REQ-0017 AC-009/011/012** 双保存按钮、原生 confirm、inline save-tip 在 PRD 层未与 Profile/列表页横切模式对齐，导致 BUG-0043/0046/0047。
- **PNG Golden 大量延后**：系统设置 5 Tab PNG、部分 Banner PNG 未导出；依赖 HTML gate + vitest，sign-off 风险 **待确认**。

### 评审深度

- **BUG-0023/0043 模式重复**：Profile 与 SystemSettings 重复「页头+footer 双 CTA」，review 未引用 BUG-0023 作为父模式预防。
- **BUG-0048 本可在 design 阶段规定**：「弹窗 MUST 单一专属 class，禁止叠加 `modal-card`」——SKU 已采用 `sku-modal-card` 先例。

### 文档模板建议

| 字段/门禁 | 建议 |
|-----------|------|
| `acceptance.md` 管理端表单页 | MUST 含「单保存 CTA」「DS confirm」「AdminToast 无 layout shift」 |
| `acceptance.md` 管理端弹窗 | MUST 含「Computed width 验收」「矮视口 scroll」 |
| `req-complete` 大模块 | MUST 含列表 DOM 对齐用户管理 baseline 的横切 AC |
| `design.md` CSS Port | MUST 声明 modal 类名策略（禁止 modal-card 叠加） |

## 4. 开发与质量

### 重复 BUG 模式

| 模式 | 次数 | 关联 BUG | 根因摘要 |
|------|------|----------|----------|
| **列表分页/表头不一致** | 2 | BUG-0027, BUG-0030 | 未复用 UserManagement 分页 DOM；`best-practices/admin-list-page-consistency.md` 未在 apply 前强制执行 |
| **页头+底部重复保存** | 2 | BUG-0023, BUG-0043 | add-* AC 允许双 CTA；无 FormPage 模板 |
| **原生 confirm vs DS modal** | 2+ | BUG-0026, BUG-0046, BUG-0037 | 快捷 `window.confirm`；AC 未限定呈现形式 |
| **inline tip 布局抖动** | 1 | BUG-0047 | 重复 BUG-0015 模式；未用 AdminToast |
| **弹窗宽度 CSS 层叠** | 2 | BUG-0040, BUG-0048 | `modal-card` + 专属类双挂载；未测 bundle Computed |
| **弹窗 scroll/备注宽度** | 2 | BUG-0033, BUG-0028 | 未统一 flex scroll 弹窗骨架 |
| **保存后列表未刷新** | 1 | BUG-0029 | onSuccess 未调 reload（纯前端逻辑） |
| **侧栏/Shell 数据未贯通** | 2 | BUG-0041, BUG-0021 | Layout 未消费 profile/me；nav 占位 icon |
| **Banner 弹窗专项** | 7 | BUG-0031~0036, 0035 | 新模块首版未对齐 Brand/SKU 上传与 Combobox 模式 |

### 测试与归档

- **Vitest 补强有效**：分页 DOM、modal width CSS 栈、confirm 结构、单按钮断言在 fix change 中补齐。
- **Pytest**：system-settings、banner 各有专项测试；object-storage effective limits 与 upload 联动已覆盖。
- **Docker 冒烟**：banner/system-settings 脚本读取 `.env` 端口（如 `HOST_PORT_BACKEND=8010`），避免硬编码 8000。
- **归档**：`add-system-settings` ADDED 冲突；fix-* 先 archive 导致主 spec 超前合并——需在 add archive 流程文档化。

## 5. 可复用抽象

| 机会 | 涉及 REQ/页面 | 建议 |
|------|---------------|------|
| **`AdminListPage` 模板**（Sprint 002 A-002 未落地） | 规格、Banner 列表 | `/req-capture` 统一 hero/table/pagination |
| **`AdminFormPage` / Settings Shell** | Profile、SystemSettings | 单 CTA、footer actions、dirty guard、AdminToast |
| **`AdminConfirmModal` 统一** | 规格启停、设置 reset、改密取消 | 禁止 `window.confirm`；design-system 验收页示例 |
| **Modal 类名规范** | Banner、SKU、User、Brand | 仅 `{feature}-modal-card`；Vitest import 全站 admin CSS |
| **`SearchableSelect` / Combobox** | Banner SKU/专题 | 已用于 BUG-0034；上升为 shared/ui |
| **`MediaUploadField` 状态机**（Sprint 002 A-003） | Banner 图、Profile 头像 | 从 BrandFormModal 提取 |
| **OpenSpec tasks 模板** | 所有 UI add-* | 默认：HTML gate、Computed width、Docker smoke、PNG 可选 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P0 | 完成 Sprint 003 `acceptance-report.md` 核心 AC 人工勾选 | QA 对照各 REQ/BUG acceptance + trace | QA | open |
| A-002 | P1 | 落地 `AdminListPage` / 列表 DOM 契约（延续 Sprint 002 A-002） | `/req-capture` AdminListPage 模板 | 前端 | open |
| A-003 | P1 | 落地 `AdminFormPage` 单 CTA + AdminToast + DS confirm | `/req-capture`；引用 `admin-form-page-consistency.md` | 前端 | open |
| A-004 | P1 | Modal 宽度：禁止 `modal-card` 叠加；Vitest CSS 栈 gate | 团队确认后更新 `rules/ui-design.md` 建议项 | 前端 | open |
| A-005 | P2 | Sprint scope 冻结策略（apply 后新 BUG 默认下一 Sprint） | 下一 `/sprint-propose` 写入 sprint.md 约定 | 项目经理 | open |
| A-006 | P2 | `openspec archive` ADDED 冲突预检脚本 | `/req-capture` 或 AGENTS.md 补充（延续 A-007） | 架构 | open |
| A-007 | P2 | trace.md YAML fence CI 校验 | `scripts/validate-issue-trace.py` | 工具链 | open |
| A-008 | P2 | 导出 REQ-0017 五 Tab PNG Golden | 人工 1440×1024 截图至 prototype/web | 设计/QA | open |
| A-009 | P3 | 系统设置 P1b 登录失败锁定 | 单独 `/req-capture` 或 backlog | 后端 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-003-retrospective.md` | 新建 | 本文档 |
| `best-practices/admin-list-page-consistency.md` | 更新 | 补充 BUG-0027/0030/0039 |
| `best-practices/admin-form-page-consistency.md` | 新建 | 单 CTA、confirm、toast |
| `best-practices/admin-modal-width-css-cascade.md` | 新建 | BUG-0048 层叠模式 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-06-28 19:42:56 | 初稿（`/sprint-exps sprint-003`） |
