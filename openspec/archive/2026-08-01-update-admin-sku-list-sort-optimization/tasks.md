## 1. Implementation

- [x] 1.1 调整管理端 SKU 列表默认排序，使未上架 SKU（`status != PUBLISHED`）排在已上架 SKU 前面。
- [x] 1.2 确保未上架 SKU 分组内按 `created_at DESC` 排序，并在时间为空或重复时使用稳定兜底字段。
- [x] 1.3 确保已上架 SKU 分组内按 `published_at DESC` 排序，并在时间为空或重复时使用稳定兜底字段。
- [x] 1.4 确保排序在分页前对完整结果集生效，搜索、品牌、类目、状态、素材完整度筛选组合后不回归。
- [x] 1.5 保持管理端 SKU 列表 UI、筛选区、分页、状态标签、操作列、加载态、空态和失败态不变；不新增排序控件或额外筛选项。
- [x] 1.6 若实现涉及 API 响应字段、排序参数或派生字段变化，同步 Pydantic Schema、OpenAPI、Orval、docs/03-api-index.md 和前端调用。

## 2. Tests

- [x] 2.1 补充或更新后端 pytest，覆盖未上架 SKU 优先于已上架 SKU。
- [x] 2.2 补充或更新后端 pytest，覆盖未上架 SKU 按 `created_at DESC`、已上架 SKU 按 `published_at DESC`。
- [x] 2.3 补充或更新后端 pytest，覆盖时间为空或重复时的稳定排序。
- [x] 2.4 补充或更新后端 pytest，覆盖关键词、品牌、类目、状态、素材完整度筛选和分页后的排序稳定性。
- [x] 2.5 补充或更新前端 Vitest/Testing Library 测试，覆盖 SKU 列表渲染顺序或 API 返回顺序映射。
- [x] 2.6 如发生 API 契约变化，运行 OpenAPI/Orval 生成并补充相关前端类型使用测试。

## 3. Documentation

- [x] 3.1 如 API 排序语义、字段或参数发生变化，同步 `docs/03-api-index.md` 与相关 API 治理说明。
- [x] 3.2 在实现说明或 Change trace 中记录未上架状态集合、发布时间空值兜底策略和排序实现层级。
- [x] 3.3 在 Change design 或验收记录中确认 `knowledge_base_refs` 已覆盖 `admin-list` 横切 AC。

## 4. Validation

- [x] 4.1 运行相关后端 pytest。
- [x] 4.2 运行相关前端 Vitest/Testing Library 测试。
- [x] 4.3 视检管理端 SKU 列表，确认分页 DOM、指标卡 DOM、筛选下拉、fixed toast、状态操作确认和 `window.confirm` 横切 AC 无回归。
- [x] 4.4 运行 `openspec validate update-admin-sku-list-sort-optimization --strict`。

## 验收返修记录

- [x] 2026-08-01 07:48:32 `/opsx-modify`：验收反馈要求 SKU 下架后发布时间不要清空，管理端仍需显示最近一次发布时间；已移除列表/详情查询对非 `PUBLISHED` 状态 `published_at` 的隐藏派生，补充后端测试，并同步 delta spec、design、REQ acceptance、API 索引、Sprint release-note 与 acceptance-report。
- [x] 2026-08-01 08:05:03 `/opsx-modify`：验收反馈要求 SKU 列表页筛选区域参照其他页面占满可用宽度；已将筛选区 grid 从 6 列预留改为 5 列实际控件布局，并补充前端 CSS 回归测试，同步 delta spec、design、REQ acceptance 与 Sprint acceptance-report。
