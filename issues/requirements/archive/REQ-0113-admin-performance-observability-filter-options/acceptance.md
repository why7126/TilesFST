---
requirement_id: REQ-0113-admin-performance-observability-filter-options
acceptance_status: passed
created_at: 2026-08-12 19:09:40
updated_at: 2026-08-12 22:03:11
---

# 验收标准

## 功能 AC

- [ ] AC-001 后端新增 `GET /api/v1/admin/performance-events/filter-options` 或等价管理端性能观测候选值接口。
- [ ] AC-002 候选值接口仅系统管理员可访问；未登录返回统一 401，非系统管理员返回统一权限错误。
- [ ] AC-003 候选值接口支持 `start_time`、`end_time`，时间格式和现有 summary / samples 接口保持一致。
- [ ] AC-004 候选值接口返回 `client_types`、`app_versions`、`page_keys`、`device_classes`、`network_types`、`metrics` 六大维度。
- [ ] AC-005 `client_types` 和 `metrics` 由后端固定枚举返回 `value` 与 `label`，前端不维护冲突的展示口径。
- [ ] AC-006 `app_versions`、`page_keys`、`device_classes`、`network_types` 从 `performance_events` 按时间范围提取非空候选值。
- [ ] AC-007 候选值仅按时间范围返回，不随端类型、版本号、页面、网络、指标等其他已选筛选项级联收敛。
- [ ] AC-008 动态候选值排序稳定：最近出现优先，最近时间相同按样本数倒序，再按 value 升序。
- [ ] AC-009 动态候选值为空时返回空数组，不返回错误；前端保留“全部”选项并展示可理解空态。
- [ ] AC-010 管理端筛选区顺序固定为：时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标。
- [ ] AC-011 端类型、版本号、页面、网络、指标均使用可选择控件，不使用纯文本输入；设备不作为本期筛选项展示。
- [ ] AC-012 任一筛选项变化或重置后，聚合列表页码回到第一页。
- [ ] AC-013 聚合列表字段顺序固定为：页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作。
- [ ] AC-014 样本页上下文顺序固定为：页面 > 版本号 > 端类型 > 设备 > 网络 > 指标。
- [ ] AC-015 样本列表字段顺序固定为：页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id。
- [ ] AC-016 聚合列表与样本页空值文案一致：版本未知、设备未知、网络未知。
- [ ] AC-017 样本页不得展示完整 URL、Header、Cookie、签名 URL、Authorization 或原始 payload。
- [ ] AC-018 `request_id` 保持受控截断与复制交互，复制失败或空值有明确反馈。
- [ ] AC-019 API 变更同步 OpenAPI、Orval、Web API 封装和 `docs/03-api-index.md`。
- [ ] AC-020 后端测试覆盖权限、时间范围、空数据、固定枚举、动态候选值和排序。
- [ ] AC-021 Web 测试覆盖候选值加载、筛选顺序、字段顺序、分页重置、候选值失败和样本页安全字段。
- [ ] AC-022 本需求默认不改数据库表结构；若实现阶段新增索引或字段，必须同步 SQLite / MySQL schema、数据库文档和测试。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷

- [ ] AC-XCUT-001 1440x1024 视口下，性能观测页分页 DOM 使用 `page-summary` + `page-right`，与用户管理基准一致。
- [ ] AC-XCUT-002 摘要指标卡 DOM 使用 `.metric-label` / `.metric-value` / `.metric-desc` 或等价共享 `MetricCard` 结构，不使用裸 `strong` / `span` 作为唯一数值结构。
- [ ] AC-XCUT-003 筛选下拉复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper；若不用共享组件，必须在 Change design 中说明理由。
- [ ] AC-XCUT-004 筛选下拉不新增页面级一次性弹层样式，不使用裸 Hex 或 token 等价硬编码颜色，弹层不被表格、滚动容器或 sticky 操作列裁切。
- [ ] AC-XCUT-005 筛选下拉测试覆盖 open/select/clear/reset、已选中态、空态、加载态和筛选 query 语义不变。
- [ ] AC-XCUT-006 候选值加载或聚合查询成功/失败反馈不得引起 hero、筛选区或表格纵向位移；如使用 toast，必须为 fixed toast。
- [ ] AC-XCUT-007 状态变更类操作均需 DS confirm 且无 `window.confirm`；N/A — 本 REQ 不新增启停、删除、冻结、上架/下架等状态变更操作。
- [ ] AC-XCUT-008 表头与普通字段默认 nowrap；页面、版本号、request_id 等长文本必须截断、title/tooltip 或等价可访问处理，不撑宽整表。
- [ ] AC-XCUT-009 有效期/投放周期双行例外不适用；接收时间、事件时间等普通时间字段保持单行。
- [ ] AC-XCUT-010 sticky 操作列在横向滚动和窄屏下可达，不遮挡筛选弹层、toast 或分页。
- [ ] AC-XCUT-011 聚合列表继续使用后端真实分页参数和真实 total；不得全量拉取后前端切片伪分页。
- [ ] AC-XCUT-012 Vitest 或等价前端测试覆盖分页结构、列展示顺序、sticky 操作列和候选值筛选 smoke。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 22:03:11
accepted_by: workflow-sync
source_change: add-admin-performance-observability-filter-options
source_sprint: sprint-023
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

