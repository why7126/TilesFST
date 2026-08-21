## 背景

Banner、日志审计、用户管理等管理端列表在列展示、换行、分页、冻结操作列和真实分页上反复返修。项目已有字段展示 adapter 检查表，但还缺少面向表格布局、分页 DOM、sticky 操作列和后端真实分页的统一契约。

本变更将 REQ-0112 沉淀为 Design System 与测试治理层面的 OpenSpec Change，先建立可复用契约和验收 gate，再由 `/opsx-apply` 落实代表页面、知识库与测试。

## 变更内容

- 建立管理端列表页列展示与分页一致性契约，覆盖 nowrap 默认、有效期例外、sticky 操作列、分页 DOM、真实分页与筛选后页码恢复。
- 扩展 Design System 管理端列表基础组件规范，明确 `AdminListPage` 或等价模板应承载列展示和分页契约。
- 扩展测试治理规范，要求前端测试覆盖分页 DOM、nowrap/sticky 行为、真实分页请求参数和筛选后分页重置。
- 更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，将 sprint-022 T-002 行动项转为可执行 gate。
- 不在本 Change 中重构所有管理端列表；代表页优先覆盖 Banner 管理、日志审计、用户管理。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `design-system`：补充管理端列表列展示与分页一致性契约。
- `testing`：补充管理端列表列展示、sticky 操作列和真实分页回归测试要求。

## 影响范围

- 后端：可能受影响，仅当代表页面缺少后端真实分页字段或响应总数时需要补齐。
- Web 管理端：受影响，代表页需对齐列表布局、分页和操作列契约。
- 小程序：不涉及。
- 管理端：受影响。
- 数据库：不涉及。
- 对象存储：不涉及。
- API：条件影响；若分页请求或响应结构变化，必须同步 Pydantic Schema、OpenAPI、Orval、API 文档和测试。

