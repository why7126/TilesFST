---
change_id: fix-admin-content-padding-too-large
bug_id: BUG-0054-admin-content-padding-too-large
status: proposed
created_at: 2026-07-03 18:41:48
updated_at: 2026-07-03 23:36:41
sprint: sprint-004
---

# OpenSpec Change Trace

## Readiness Report

```yaml
bug: BUG-0054-admin-content-padding-too-large
status: approved
readiness: Ready
approved: true
change: fix-admin-content-padding-too-large
related_requirement: REQ-0013-admin-shell-padding-refine
sprint: sprint-004
```

BUG-0054 has complete capture, bug, root-cause, workaround, acceptance, review, and trace artifacts. It is approved and ready for OpenSpec fix planning.

## Bug Analysis Report

| Area | Result |
|---|---|
| 现象 | 管理端全局右侧内容区域内边距过大，内容显示面积偏小 |
| 复现 | `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/settings` 等 AdminLayout 页面 |
| 直接原因 | `.main-content` 旧 padding、`.content-inner` 1080px 上限、页面级 max-width 分叉 |
| 根因分类 | code / design / test |
| 严重等级 | medium |
| Hotfix | 不需要，常规 fix |

## Impact Analysis

| Area | Impact |
|---|---|
| Backend API | 无 |
| Database | 无 |
| Web Admin | AdminLayout 主内容区域与多个管理端页面视觉密度 |
| Storefront / Miniapp | 无 |
| OpenAPI / Orval | 无需执行 |
| Docker / Env | 无 |
| Tests | 需要前端布局测试 / 静态断言 |
| Docs | OpenSpec/BUG trace 同步；长期 docs 暂不需要 |

## Validation Plan

- `openspec validate fix-admin-content-padding-too-large --strict`
- `python scripts/validate-directory-structure.py`
- 相关 Vitest：`AdminLayout.test.tsx`、`AdminSidebar.collapse.test.tsx`、受影响页面 smoke/静态断言
- 视觉验收：1440、1920、collapsed、tablet、mobile smoke

## Implementation Record

```yaml
implemented_at: 2026-07-03 23:36:41
content_inner_strategy: "max-width: min(1440px, 100%)"
changed_files:
  - src/web/src/features/admin/styles/admin-home.css
  - src/web/src/features/admin/styles/tile-sku-management.css
  - src/web/src/features/admin/styles/system-settings.css
  - src/web/src/features/admin/components/AdminLayout.test.tsx
api_changed: false
database_changed: false
orval_required: false
docker_compose_required: false
backend_pytest_required: false
knowledge_base_incident: "not_added"
knowledge_base_reason: "本次为已知 Admin Shell 布局收敛修复，未发现新的生产故障模式。"
visual_browser_validation:
  status: blocked
  reason: "Playwright package exists, but managed Chromium is not installed; system Chrome launch failed in current sandbox. 4.x visual checklist remains pending for a browser-capable environment."
```

## Validation Record

| 时间 | 类型 | 结果 |
|---|---|---|
| 2026-07-03 23:33:15 | Vitest | `pnpm --dir src/web exec vitest run src/features/admin/components/AdminLayout.test.tsx src/features/admin/components/AdminSidebar.collapse.test.tsx src/pages/admin/LogAuditPage.test.tsx src/pages/admin/ApiDocsPage.test.tsx` 通过：4 files, 29 tests |
| 2026-07-03 23:34:00 | Build | `pnpm --dir src/web build` 通过；存在 Tailwind v4 at-rule 与 chunk size 既有 warning |
| 2026-07-03 23:36:41 | OpenSpec | `openspec validate fix-admin-content-padding-too-large --strict` 通过 |
| 2026-07-03 23:36:41 | Directory | `python scripts/validate-directory-structure.py` 通过 |
| 2026-07-03 23:36:41 | Static CSS scan | 旧 `48px 56px 72px`、`.content-inner max-width: 1080px`、SKU `content-inner 1120px` 未在管理端样式中出现；剩余 `1120px` 为响应式 media breakpoint |

## Change History

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-03 23:36:41 | `/opsx-apply` | 完成 CSS 修复、静态断言、Vitest、build、OpenSpec 与目录校验；浏览器视觉验收因当前环境缺少可启动浏览器保持 pending |
| 2026-07-03 18:51:53 | `/sprint-propose` | 纳入 `sprint-004` |
| 2026-07-03 18:41:48 | `/bug-opsx` | 创建 OpenSpec Change 并生成 proposal/design/spec/tasks/trace |
