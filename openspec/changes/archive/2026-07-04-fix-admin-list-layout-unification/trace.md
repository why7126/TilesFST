---
change_id: fix-admin-list-layout-unification
status: implemented
created_at: 2026-07-03 18:51:13
updated_at: 2026-07-04 07:48:50
source_bug: BUG-0055-admin-list-layout-unification
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0055-admin-list-layout-unification/`
- 创建命令: `/bug-opsx BUG-0055-admin-list-layout-unification`
- OpenSpec CLI: `openspec new change "fix-admin-list-layout-unification"`

## 状态

```yaml
status: implemented
bug_status_at_creation: approved
iteration: sprint-004
related_requirements:
  - REQ-0005-brand-management
  - REQ-0005-tile-category-management
  - REQ-0005-user-management
  - REQ-0006-tile-sku-management
  - REQ-0009-tile-spec-management
  - REQ-0016-banner-management
  - REQ-0022-admin-api-docs-menu
  - REQ-0024-product-usage-logging
api_impact: none
database_impact: none
orval_required: false
docker_compose_required: false
```

## 实施摘要

| 范围 | 结果 |
|---|---|
| 公共分页 | 新增 `src/web/src/features/admin/lib/pagination.ts`，统一最多 5 个可点击页码窗口 |
| 公共 sticky 操作列 | 在 `user-management.css` 沉淀 `admin-sticky-action-cell`，各列表页复用 |
| 页面顺序 | `BannerManagementPage`、`UserManagementPage`、`ApiDocsPage` 已按标题 → 指标卡 → 筛选/搜索 → 列表校验 |
| 筛选交互 | SKU、品牌、类目、规格、Banner、日志审计移除显式【查询】/【搜索】按钮；保留统一【重置】入口；日志审计状态/结果改为下拉并覆盖常见 HTTP 状态码 |
| 列表操作列 | SKU、品牌、类目、规格、Banner、用户、日志审计、接口文档最后一列接入 sticky action column 契约 |
| 分页 | 8 个目标页面均使用 `getPaginationWindow` 输出页码按钮 |

## 验证记录

| 命令 | 结果 | 说明 |
|---|---|---|
| `pnpm --dir src/web exec vitest run src/features/admin/lib/pagination.test.ts src/pages/admin/TileSkuManagementPage.test.tsx src/pages/admin/BrandManagementPage.test.tsx src/pages/admin/TileCategoryManagementPage.test.tsx src/pages/admin/TileSpecManagementPage.test.tsx src/pages/admin/BannerManagementPage.test.tsx src/pages/admin/UserManagementPage.test.tsx src/pages/admin/LogAuditPage.test.tsx src/pages/admin/ApiDocsPage.test.tsx` | PASS | 9 files, 49 tests |
| `pnpm --dir src/web run build` | PASS | Vite build 通过；存在既有 lightningcss unknown at-rule 与 chunk size warning |
| `openspec validate fix-admin-list-layout-unification --strict` | PASS | Change strict 校验通过 |
| `python scripts/validate-directory-structure.py` | PASS | 目录结构校验通过 |
| `pnpm --dir src/web test -- LogAuditPage.test.tsx` | PASS | 43 files, 193 tests；覆盖状态/结果下拉、`422` 选项与查询参数映射 |

## 未执行项

| 项 | 状态 | 原因 |
|---|---|---|
| 1366px / 1440px / 1920px 浏览器截图验收 | PASS | 用户确认 1366px、1440px、1920px desktop 视口下 8 个页面视觉验收均无问题 |
| 横向滚动 sticky 操作列验收 | PASS | 用户确认横向滚动时最后一列固定浮动无表头/表体错位 |
| 筛选区与分页区桌面宽度验收 | PASS | 用户确认常见桌面宽度下无重叠、裁切或跳动 |
| tablet / mobile smoke | PASS | 用户确认 tablet / mobile 下无明显横向溢出或控件重叠 |
| 后端 pytest | not required | 本 Change 不修改后端代码、API、数据模型 |
| Orval | not required | 本 Change 不修改 OpenAPI 或生成客户端 |
| 数据库迁移 | not required | 本 Change 不修改 SQLite schema 或 Pydantic schema |
| Docker Compose 验证 | not required | 本 Change 不修改 Docker、nginx、环境变量或后端服务 |
| 知识库 incident | not required | 本次为已知 admin-list 一致性横切问题修复，已复用 best-practice，无新增事故知识沉淀 |

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-04 07:48:50 | 补充修复 | 日志审计状态/结果筛选由输入框改为下拉；补齐常见 HTTP 状态码与 `422 参数校验错误`；若当前列表出现静态集合外状态码则动态追加 |
| 2026-07-04 07:47:39 | 视觉验收确认 | 用户确认 4 项视觉验收任务均通过；Change 任务完成度更新为 30/30 |
| 2026-07-04 07:25:16 | 补充修复 | 接口文档页 Method badge 拆分 GET/POST/PUT/PATCH/DELETE 五种独立颜色；ApiDocsPage Vitest 13 passed；Web build 通过 |
| 2026-07-04 00:15:30 | 补充修复 | 接口文档页删除 `SWAGGER POLICY` 面板；保留 hero OpenAPI/Swagger 链接与行级 Swagger 详情动作；ApiDocsPage Vitest 12 passed |
| 2026-07-04 00:02:53 | 补充修复 | 品牌/规格筛选项补齐 SKU 同款 Label 与表单关联；日志审计重置按钮宽度改为 SKU 同款自然宽度；修正 SKU/品牌/规格表体 sticky class 到操作列 |
| 2026-07-03 23:49:55 | `/opsx-apply` | 完成代码实现、前端回归测试、build、OpenSpec strict 与目录结构校验；浏览器多视口目视验收保持 pending |
| 2026-07-03 23:30:35 | `/sprint-propose sprint-004` | 纳入 sprint-004；待 `/opsx-apply fix-admin-list-layout-unification` |
| 2026-07-03 18:51:13 | `/bug-opsx` | 创建 `fix-admin-list-layout-unification` 并生成 OpenSpec 工件 |
