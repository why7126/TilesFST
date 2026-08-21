## 1. 契约与文档

- [x] 1.1 更新 Design System / 管理端列表基础组件契约，补齐 nowrap 默认、有效期例外、sticky 操作列、分页 DOM 和真实分页要求。
- [x] 1.2 更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，加入 REQ-0112 的列展示与分页 gate，并保留 sprint-022 T-002 来源。
- [x] 1.3 在实现 trace 中记录 UI Contract 事实源、代表页、Mock/API 边界和 knowledge-base 引用。

## 2. Web 管理端实现

- [x] 2.1 盘点 Banner 管理、日志审计、用户管理三个代表页的列展示、分页 DOM、sticky 操作列和真实分页现状。
- [x] 2.2 为共享 `AdminListPage`、表格 class、分页组件或等价模板补齐列展示与分页契约实现。
- [x] 2.3 对代表页应用契约：表头 nowrap、普通字段单行截断、有效期例外、sticky 操作列、分页 DOM 与 fixed toast / DS confirm 规则。
- [x] 2.4 若发现代表页分页 API 缺少真实分页字段或响应总数，同步后端 Schema、OpenAPI、Orval、API 文档和测试。

## 3. 测试与验收

- [x] 3.1 补充前端测试，覆盖 `page-summary`、`page-right`、真实总数、筛选/搜索/每页条数变化后分页重置。
- [x] 3.2 补充列展示测试或等价断言，覆盖 nowrap 默认、有效期双行例外和 sticky 操作列关键行为。
- [x] 3.3 补充状态操作 fixed toast、DS confirm modal 和无新增 `window.confirm` 的回归测试。
- [x] 3.4 如触发 API 变更，运行后端/API/Orval 相关测试；如未触发，在验收记录中标记 N/A。
- [x] 3.5 记录 1440×1024 与横向滚动/窄屏代表页视觉证据，说明无法自动化项的人工验证结论。

## 4. 校验与收尾

- [x] 4.1 运行 `openspec validate update-admin-list-column-pagination-consistency-contract`。
- [x] 4.2 运行 `python scripts/validate-openspec-language.py`。
- [x] 4.3 运行相关前端测试；若 API 变更，运行相关后端测试和 Orval 生成校验。
- [x] 4.4 更新 REQ / Change / Sprint trace 与验收记录，确认 `admin-list` 横切 AC 已覆盖。
