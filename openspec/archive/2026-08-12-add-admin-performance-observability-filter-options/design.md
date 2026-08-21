# 设计：管理端性能观测筛选候选值接口

## D1 实施策略

采用现有 RUM 能力的增量扩展策略：

- 后端在 `admin-performance-events` 路由下新增候选值查询接口。
- Repository 基于 `performance_events` 按时间范围查询动态维度候选值。
- Service 合并固定枚举候选值与动态候选值，统一返回 `value` / `label`。
- Web 管理端通过 Orval/封装 API 加载候选值，并用共享筛选下拉组件渲染。
- 不新增独立页面，不新增落库字段。

UI 策略采用 Design System / shared components，不做 CSS Port。筛选控件优先复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper。

## D2 API 契约

推荐接口：

```text
GET /api/v1/admin/performance-events/filter-options
```

查询参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `start_time` | string | 否 | 时间范围起点，格式与 summary/samples 保持一致。 |
| `end_time` | string | 否 | 时间范围终点，格式与 summary/samples 保持一致。 |

响应数据建议：

```yaml
client_types:
  - value: web_admin
    label: 管理端 Web
app_versions:
  - value: 0.1.0
    label: 0.1.0
    count: 21
page_keys:
  - value: admin/performance
    label: admin/performance
    count: 21
device_classes:
  - value: desktop
    label: desktop
    count: 21
network_types:
  - value: wifi
    label: wifi
    count: 21
metrics:
  - value: full_load
    label: 完整加载
```

`count` 可用于排序与调试，前端首期不必须展示。若实现阶段决定不返回 `count`，必须保持 spec、schema、测试一致。

## D3 候选值口径

候选值仅受 `start_time`、`end_time` 影响。当前已选端类型、版本号、页面、网络、指标不得改变候选值列表；接口仍返回设备候选值供字段展示、后续排障或样本跳转口径使用。

动态维度：

- `app_versions`：`performance_events.app_version` 非空值。
- `page_keys`：`performance_events.page_key` 非空值。
- `device_classes`：`performance_events.device_class` 非空值。
- `network_types`：`performance_events.network_type` 非空值。

排序：

- 固定枚举按产品定义顺序。
- 动态维度按最近出现时间倒序，样本数倒序，value 升序。
- 单个动态维度默认限制 100 项。

## D4 UI Contract

事实源优先级：

```text
prototype/web/context.md > acceptance.md > rules/ui-design.md > openspec/specs/real-user-performance-monitoring/spec.md
```

页面入口：

- `/admin/performance`
- `/admin/performance/samples`

筛选区顺序：

```text
时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标
```

聚合列表字段顺序：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作
```

样本页上下文顺序：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标
```

样本列表字段顺序：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id
```

视觉 token 与交互：

- 延续管理端“工业石材 · 暗色旗舰风”。
- 使用 semantic token 和既有管理端样式。
- 长文本字段必须截断、title/tooltip 或等价可访问处理。
- 候选值失败态与性能样本空态必须区分。
- 不新增营销式 hero、解释性卡片或页面级一次性弹层样式。

权限规则：

- 候选值接口仅系统管理员可访问。
- 管理端页面按现有鉴权与导航权限展示。

Mock/API 边界：

- 本 Change 接入真实候选值 API。
- 不引入长期 Mock 数据源。
- 若本地无性能事件数据，动态候选值为空数组，固定枚举仍可返回。

## D5 知识库与横切门禁

必须引用并执行：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-022-retrospective.md`

实现阶段必须记录：

- 筛选下拉复用 shared wrapper。
- 分页 DOM 使用 `page-summary` + `page-right`。
- 表头与普通字段 nowrap，长文本不撑宽整表。
- sticky 操作列在横向滚动和窄屏下可达。
- 后端真实分页参数与 total 保持。

## D6 冲突处理

当前无 HTML/PNG 原型；`prototype/web/context.md` 为最高 UI 事实源。若实现与 acceptance 或既有 spec 冲突，按以下顺序裁决：

```text
prototype/web/context.md > acceptance.md > rules/ui-design.md > openspec/specs/real-user-performance-monitoring/spec.md
```

无冲突需要拆分；本 Change 可作为单一 OpenSpec Change 推进。
