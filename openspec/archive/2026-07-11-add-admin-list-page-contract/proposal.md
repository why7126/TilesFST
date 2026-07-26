## Why

管理端 SKU、品牌、类目、规格、Banner、用户、日志审计与接口文档等列表页已多次出现模块顺序、筛选、分页、sticky 操作列和反馈布局漂移。REQ-0028 将 BUG-0055 的逐页修复经验沉淀为 `AdminListPage` 页面模板契约、Design System 验收样例和新增列表页复用门禁，避免后续继续靠局部 CSS 修补维持一致性。

## What Changes

- 新增 Design System 层的 `AdminListPage` 模板契约，覆盖标题、指标卡、筛选/搜索、表格列表、分页和 sticky action column。
- 扩展管理端列表页输入模型或等价组合能力，描述标题、主操作、指标卡、筛选项、表格列、行操作、分页状态以及 loading/empty/error 等状态态。
- 在 `/design-system` 增加 AdminListPage 管理端列表验收样例，展示完整列表、边界态、分页边界和 BUG-0055 关联页面矩阵。
- 修改 Web 客户端管理端列表页横切一致性能力，将现有 8 个页面的一致性规则升级为“优先复用 AdminListPage 模板或等价组合”的复用门禁。
- 不新增或修改后端 API、数据库、MinIO、Docker Compose、店主 Web 展示端或微信小程序行为。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `design-system`: 增加 AdminListPage 模板契约与 `/design-system` 验收样例要求。
- `web-client`: 将管理端列表页横切一致性要求补强为模板复用门禁，明确新增或迁移管理端列表页应优先使用 AdminListPage 或等价模板组合。

## Impact

- Web 管理端：影响 `src/web/src/shared/templates/admin-list-page.tsx`、相关模板类型、`/design-system` 验收页和后续首批代表页面迁移。
- Design System：要求复用 semantic token、`cn()`、现有管理端样式基线，禁止新增裸 Hex。
- 测试：需要补充 Vitest / Testing Library 测试，覆盖模块顺序、筛选重置、分页 DOM、sticky action column 和 `/design-system` 样例渲染。
- API / 数据库 / Orval / MinIO / Docker：无契约变更；不需要 Orval；Docker Compose 验证可作为 Web 生产构建后的可选验收。
