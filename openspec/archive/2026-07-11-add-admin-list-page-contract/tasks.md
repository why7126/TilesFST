## 1. 模板契约

- [x] 1.1 扩展 `AdminListPage` 或等价模板组合，覆盖标题、指标卡、筛选/搜索、列表、分页和状态态。
- [x] 1.2 扩展 `AdminListPageContent` 或等价类型，描述主操作、指标卡、筛选项、列定义、行操作、分页状态和 loading/empty/error 文案。
- [x] 1.3 将分页、sticky action column、fixed toast、confirm modal 的结构契约接入模板或明确为可复用组合。

## 2. Design System 验收页

- [x] 2.1 在 `/design-system` 增加 AdminListPage 管理端列表章节或验收样例。
- [x] 2.2 样例展示完整列表、loading、empty、error、单页分页和多页分页边界态。
- [x] 2.3 样例标注 BUG-0055 关联的 8 个管理端列表页矩阵。

## 3. 代表页面接入

- [x] 3.1 选择 1 个低风险代表管理端列表页接入 `AdminListPage` 或等价模板组合。
- [x] 3.2 验证代表页筛选变化、重置、每页条数切换均回到第 1 页。
- [x] 3.3 验证代表页 sticky action column、危险操作确认、fixed toast 和权限禁用态不回退。

## 4. 测试与校验

- [x] 4.1 补充模板结构测试，覆盖模块顺序、分页 DOM 和 sticky action column。
- [x] 4.2 补充 `/design-system` AdminListPage 样例渲染测试或等价 smoke。
- [x] 4.3 运行前端测试和 Design System 裸 Hex / semantic token 校验。
- [x] 4.4 确认本 Change 不需要 OpenAPI/Orval、数据库迁移、MinIO 或 Docker Compose 配置变更。
