---
change_id: update-brand-logo-fst-favicon
change_type: update
status: applied
created_at: 2026-07-01 22:35:50
updated_at: 2026-07-02 03:18:58
owner: frontend
related_requirement: REQ-0025-brand-logo-fst-favicon
related_sprint: sprint-004
---

# Change Trace

## 基本信息

```yaml
change_id: update-brand-logo-fst-favicon
change_type: update
status: applied
related_requirement: REQ-0025-brand-logo-fst-favicon
related_sprint: sprint-004
impact:
  backend: false
  web: true
  admin: true
  miniapp: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - admin-dashboard
    - web-client
artifacts:
  proposal: proposal.md
  design: design.md
  specs:
    - specs/admin-dashboard/spec.md
    - specs/web-client/spec.md
  tasks: tasks.md
readiness: applied
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| trace.md | present |
| prototype/web | present |
| status | in_sprint（已完成 req-review） |
| readiness | ready |

## Impact Report

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - admin-dashboard
    - web-client
```

## Conflict Report

| 来源 | 结论 |
|---|---|
| HTML / PNG prototype | 品牌区三元素同行结构优先 |
| legacy context | `家居建材管理后台` 为旧文案 |
| acceptance.md | `家居建材资料库` 为最终副标题 |
| openspec/specs/admin-dashboard | `TILESFST` 旧品牌必须被替换 |

Resolution：实现阶段 MUST 以 `菲尚特FST` 与 `家居建材资料库` 为准；Banner 管理列表页仅为视觉承载，不进入业务范围。

## PNG / Prototype Checklist

- [x] Sidebar 展开态展示 Logo、`菲尚特FST`、version badge、`家居建材资料库`。
- [x] 收起按钮与 Logo 同行，hover 边框不贴边。
- [x] Logo 无底纹、无边框、无投影，不变形。
- [x] 1366×768 与 1440×1024 无重叠、无裁切、无布局抖动。
- [x] favicon 显示菲尚特 Logo，不显示默认图标。

## Apply Verification

| 项 | 结果 |
|---|---|
| Web asset | `src/web/public/logos/64x64.png`、`128x128.png`、`256x256.png` 已作为 Web Logo 与图标资源 |
| Entry HTML | `src/web/index.html` 已声明 favicon 指向 `/logos/64x64.png`、`/logos/128x128.png`，apple-touch-icon 指向 `/logos/256x256.png` |
| Admin Sidebar | `AdminSidebar` 展开态渲染 Logo、`菲尚特FST`、`PRODUCT_VERSION`、`家居建材资料库` 与收起按钮；收起态保留 Logo |
| Tests | `pnpm --dir src/web exec vitest run src/features/admin/components/AdminSidebar.user-mgmt.test.tsx src/features/admin/components/AdminSidebar.collapse.test.tsx src/features/admin/components/AdminSidebar.icons.test.tsx src/features/admin/components/AdminLayout.test.tsx` 通过，17 tests |
| Build | `pnpm --dir src/web build` 通过，`dist/logos/64x64.png`、`dist/logos/128x128.png`、`dist/logos/256x256.png` 与 `dist/index.html` 图标声明存在 |
| Visual | 使用真实 build CSS + 真实 Logo + 同构 Sidebar DOM 的临时静态验收页完成 1366×768、1440×1024 展开态与 1366×768 收起态截图检查；实际 Web preview `/admin/dashboard` 因未连接后端登录态只能进入登录页 |
| Out of scope | 未修改后端 API、OpenAPI、Orval、SQLite、Pydantic Schema、MinIO、Docker Compose、小程序 |

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-01 22:35:50 | `/req-opsx REQ-0025` | 创建 OpenSpec Change `update-brand-logo-fst-favicon`，状态 proposed |
| 2026-07-02 03:18:58 | `/opsx-apply update-brand-logo-fst-favicon` | 完成 Web Logo 资产、Sidebar 品牌区、favicon/apple-touch-icon、测试与构建验证；状态 applied |
