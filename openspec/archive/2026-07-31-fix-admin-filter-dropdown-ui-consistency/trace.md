---
change_id: fix-admin-filter-dropdown-ui-consistency
type: fix
status: archived
created_at: 2026-07-31 21:48:40
updated_at: 2026-07-31 23:00:57
source_bug: BUG-0098-admin-filter-dropdown-ui-consistency
source_requirement: null
iteration: sprint-015
---

# Change Trace

## 来源

- BUG: `BUG-0098-admin-filter-dropdown-ui-consistency`
- 标题：管理端筛选条件下拉框位置和 UI 样式不统一
- 严重等级：medium
- 根因分类：design

## 状态

```yaml
change_id: fix-admin-filter-dropdown-ui-consistency
type: fix
status: archived
source_bug: BUG-0098-admin-filter-dropdown-ui-consistency
iteration: sprint-015
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 23:00:57 | `/opsx-archive BUG-0098` | Change 已归档至 `openspec/archive/2026-07-31-fix-admin-filter-dropdown-ui-consistency/`，delta 已合并到 `openspec/specs/design-system/spec.md`，关联 BUG 已迁入 archive。 |
| 2026-07-31 22:56:00 | `/opsx-modify BUG-0098` | 验收返修：将用户管理页 `/admin/users` 角色 / 状态 / 登录情况筛选、日志审计页 `/admin/logs` 日志类型 / 时间范围 / 状态结果筛选、接口文档页 `/admin/api-docs` METHOD / TAG / AUTH 筛选、系统设置页 `/admin/settings` 基础信息与媒体配置下拉、界面主题切换器统一为共享 `AdminFilterSelect` 交互；分页每页条数保留原生控件以维持分页语义。补充相关页面与主题测试验证统一 class、真实点击选择、筛选查询参数、配置保存类型和主题偏好同步不变。 |
| 2026-07-31 22:43:00 | `/opsx-modify BUG-0098` | 验收返修：将瓷砖规格页 `/admin/tile-specs` 状态筛选、品牌证书页 `/admin/brand-certificates` 所属品牌 / 证书类型 / 有效状态 / 展示状态筛选、Banner 管理页 `/admin/banners` 展示端 / 状态 / 时间状态筛选调整为共享 `AdminFilterSelect` 交互；补充三页测试验证统一菜单 class、筛选选择与重置后原查询参数语义不变。 |
| 2026-07-31 22:35:00 | `/opsx-modify BUG-0098` | 验收返修：将瓷砖类目页 `/admin/tile-categories` 的状态与层级筛选从原生 `<select>` 调整为共享 `AdminFilterSelect` 交互，使用统一 `admin-filter-dropdown` 触发器、弹层和选项样式；补充类目页测试验证两个筛选菜单 class、选择 `ENABLED` / `2` 与重置后 `status: undefined`、`level: undefined` 查询语义不变。 |
| 2026-07-31 22:19:30 | `/opsx-modify BUG-0098` | 验收返修：新增共享 `AdminFilterSelect`，将瓷砖品牌页 `/admin/brands` 的状态筛选从原生 `<select>` 调整为统一 `admin-filter-dropdown` 交互，使用共享筛选下拉触发器、弹层和选项样式；共享 `filter-card` 补充 `position/z-index/overflow` 以承载品牌页下拉浮层；补充共享组件与品牌页测试验证 class、展开菜单、选择 `ENABLED` 与重置后 `status: undefined` 查询语义不变。 |
| 2026-07-31 22:12:00 | `/opsx-apply BUG-0098` | 实现管理端筛选下拉共享样式基准：`SearchableSelect` 默认接入 `admin-filter-dropdown` class，`user-management.css` 统一原生 `.select`、SKU 自定义下拉、级联类目下拉和搜索下拉的触发器、弹层、选项、空态、清空按钮、层级与窄屏行为；移除 Banner / 日志审计重复下拉视觉规则，仅保留日志审计描述行和层级特化。前端测试与构建通过；Design System 校验已运行，失败项为既有全仓治理债，未新增指向本次共享下拉组件的违规。 |
| 2026-07-31 21:54:35 | `/sprint-propose sprint-015` | Change 纳入 sprint-015 正式范围，待 `/opsx-apply`。 |
| 2026-07-31 21:48:40 | `/bug-opsx BUG-0098` | 基于已评审 BUG 创建 OpenSpec fix Change。 |

## 实现记录

- Web / 管理端：受影响。统一入口为 `src/web/src/features/admin/styles/user-management.css` 与 `src/web/src/shared/ui/searchable-select.tsx`，覆盖品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档、界面主题相关管理端筛选下拉基准。
- API：不影响；未新增、删除、改名筛选字段，未改变查询参数语义。
- 数据库 / Pydantic Schema：不影响。
- Orval / OpenAPI：不需要，未变更接口契约。
- 小程序：不影响。
- Docker Compose / 对象存储：不影响。
- Web / Design System 文档：本次为既有管理端共享样式收敛，未新增 token 或设计规范章节，文档不适用。
- 复盘沉淀：属于样式一致性修复，已复用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，暂无新增 incident 知识库条目。

## 验收返修记录

- 反馈：统一筛选下拉需要明确应用到瓷砖品牌页。
- 调整：新增 `AdminFilterSelect`，`BrandManagementPage` 状态筛选改用共享筛选下拉组件，视觉与 SKU / 搜索下拉共享基准；筛选卡片层级改为可承载弹层。
- 文档决策：不改变 BUG acceptance、API/DB/部署/对象存储边界；active spec delta 已包含 `/admin/brands` 覆盖矩阵，无需扩展规格边界。
- 验证：共享组件测试覆盖展开、选中、禁用；品牌页测试覆盖选择、重置、查询参数语义；相关 Vitest 通过。
- 反馈：统一筛选下拉需要明确应用到瓷砖类目页。
- 调整：`TileCategoryManagementPage` 状态与层级筛选改用共享 `AdminFilterSelect`，保留原查询字段与重置行为。
- 文档决策：不改变 BUG acceptance、API/DB/部署/对象存储边界；active spec delta 已包含 `/admin/tile-categories` 覆盖矩阵，无需扩展规格边界。
- 验证：类目页测试覆盖状态和层级菜单 class、选择、重置、查询参数语义；相关 Vitest 通过。
- 反馈：统一筛选下拉需要明确应用到瓷砖规格页、品牌证书页、Banner 管理页。
- 调整：`TileSpecManagementPage` 状态筛选、`BrandCertificateManagementPage` 所属品牌 / 证书类型 / 有效状态 / 展示状态筛选、`BannerManagementPage` 展示端 / 状态 / 时间状态筛选改用共享 `AdminFilterSelect`。
- 文档决策：不改变 BUG acceptance、API/DB/部署/对象存储边界；active spec delta 已包含 `/admin/tile-specs`、`/admin/brand-certificates`、`/admin/banners` 覆盖矩阵，无需扩展规格边界。
- 验证：三页页面测试覆盖统一菜单 class、筛选选择、重置、查询参数语义；相关 Vitest 通过。
- 反馈：统一筛选下拉需要明确应用到用户管理页、系统设置页、日志审计页、接口文档页、界面主题。
- 调整：`UserManagementPage` 角色 / 状态 / 登录情况筛选、`LogAuditPage` 日志类型 / 时间范围 / 状态结果筛选、`ApiDocsPage` METHOD / TAG / AUTH 筛选、`SystemSettingsPage` 基础信息与媒体配置下拉、`ThemeSwitcher` 主题切换器改用共享 `AdminFilterSelect`；分页每页条数不属于筛选条件，保持原生分页控件。
- 文档决策：不改变 BUG acceptance、API/DB/部署/对象存储边界；active spec delta 已包含 `/admin/users`、`/admin/settings`、`/admin/logs`、`/admin/api-docs` 与 theme switcher 覆盖矩阵，无需扩展规格边界。
- 验证：用户、系统设置、日志审计、接口文档、主题与登录/布局相关测试覆盖统一菜单 class、真实点击选择、查询参数、配置保存类型与主题偏好同步；相关 Vitest 与生产构建通过。

## 验收复核

- AC-001：通过，共享筛选下拉样式覆盖 `.select`、SKU 下拉、类目级联和 `SearchableSelect`。
- AC-002：通过，共享弹层使用一致宽度、偏移、边框、阴影、`z-index: 100`，日志审计保留更高局部层级。
- AC-003：通过，统一选项 normal / selected / empty / loading / disabled 基础 class 与视觉规则。
- AC-004：通过，保留页面原有 reset / clear 行为，视觉状态由共享 class 承载。
- AC-005：通过，未修改 API 请求字段或筛选语义。
- AC-006：部分通过；本次未新增裸 Hex，Design System 校验已运行但全仓存在既有未授权原生控件与旧 Hex 违规。
- AC-007：通过，Vitest 覆盖移动过滤网格、浮层层级和组件禁用/空态；构建通过。
