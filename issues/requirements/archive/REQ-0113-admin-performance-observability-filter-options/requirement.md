---
requirement_id: REQ-0113-admin-performance-observability-filter-options
title: 管理端性能观测提供筛选维度候选值接口
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0107-real-user-page-load-rum
created_at: 2026-08-12 19:07:23
updated_at: 2026-08-12 21:36:17
---

# REQ-0113 管理端性能观测提供筛选维度候选值接口

## 1. 需求背景

`REQ-0107-real-user-page-load-rum` 已建立真实用户性能事件采集、聚合查询和样本查询基础能力。管理端性能观测页可以按端类型、页面、版本、网络、设备和指标排查慢页面或版本性能波动，但当前筛选体验仍依赖前端静态选项或缺少可选值来源，页面、版本号、设备、网络等维度容易退化为纯文本输入。

性能观测数据本身具有较强的维度枚举特征。若管理端无法基于已有性能事件提供候选值，研发、测试和产品在排查时需要记住准确的 `page_key`、`app_version`、`network_type`、`device_class` 或 `metric_name`，容易出现输入错误、筛选无结果和前后端展示口径不一致。

本需求用于补齐管理端性能观测筛选维度候选值接口，并将筛选区、聚合列表和样本页字段顺序固化为同一套展示契约，提升性能排障的可发现性、一致性和可测试性。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 系统管理员 | 在管理端快速选择端类型、版本、页面、网络和指标，查看匹配的性能聚合与样本。 |
| 研发 / 运维人员 | 用一致的维度顺序定位慢页面、慢版本、异常网络或设备表现，减少手输 key 的错误。 |
| 测试人员 | 在发布前后按版本号和页面筛选性能样本，验证回归风险和字段展示顺序。 |
| 产品负责人 | 用稳定的筛选与字段展示口径对比不同页面和版本的真实用户体验。 |

## 3. 范围

### 3.1 本期包含

- 后端新增管理端性能观测筛选候选值接口，供系统管理员查询。
- 候选值接口返回 6 大维度：端类型、版本号、页面、设备、网络、指标。
- 候选值仅按时间范围返回，不随端类型、版本号、页面、设备、网络或指标等其他已选筛选项级联收敛。
- 版本号、页面、设备、网络候选值基于性能事件数据按时间范围聚合生成。
- 端类型和指标由后端返回受控枚举及展示标签，前端不得再维护另一套冲突口径。
- 管理端性能观测页筛选区按固定顺序展示：时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标；设备不作为本期筛选项展示。
- 管理端聚合列表和样本页字段顺序按本需求定义展示。
- API 变更同步 OpenAPI、Orval、接口文档和后端 / Web 管理端相关测试。

### 3.2 本期不包含

- 不做候选值级联筛选；除时间范围外，其他筛选条件不影响候选值返回范围。
- 不新增趋势图、告警、SLA、实时大屏或复杂 BI 分析。
- 不调整 RUM 事件采集字段模型；若后续发现采集字段不足，另行记录需求或 BUG。
- 不接入第三方 APM、RUM、OpenTelemetry 或云监控平台。
- 不对历史性能事件做回填、清洗或重算。
- 不开放给非系统管理员或普通端用户查询候选值。

## 4. 功能要求

### FR-001 管理端候选值接口

后端 MUST 新增管理端性能观测筛选候选值接口。

接口能力 MUST 满足：

- 仅系统管理员可访问，复用现有管理端性能观测 API 权限边界。
- 支持 `start_time`、`end_time` 查询参数，时间字段格式和现有 summary / samples 接口保持一致。
- 返回统一 `ApiResponse` 包装结构。
- 返回 6 大维度候选值：`client_types`、`app_versions`、`page_keys`、`device_classes`、`network_types`、`metrics`。
- 每个候选项 SHOULD 包含 `value` 与 `label`；数据聚合项可额外包含 `count` 或最近出现时间，是否展示由实现阶段确认。
- 空数据时返回空数组，不应返回错误。
- 权限不足、未登录和参数非法时遵守现有统一错误响应与错误码。

推荐路径为：

```text
GET /api/v1/admin/performance-events/filter-options
```

### FR-002 候选值来源与口径

候选值接口 MUST 按时间范围从 `performance_events` 中提取数据维度候选值。

候选值来源口径：

| 维度 | 来源 | 说明 |
|---|---|---|
| 端类型 | 后端固定枚举 | 包含 `web_admin`、`web_catalog`、`wechat_miniapp` 及展示标签。 |
| 版本号 | 性能事件数据 | 从 `app_version` 非空值中按时间范围提取。 |
| 页面 | 性能事件数据 | 从 `page_key` 非空值中按时间范围提取。 |
| 设备 | 性能事件数据 | 从 `device_class` 非空值中按时间范围提取。 |
| 网络 | 性能事件数据 | 从 `network_type` 非空值中按时间范围提取。 |
| 指标 | 后端固定枚举优先 | 包含 Web 与小程序已支持指标及展示标签；后续新增指标时由后端口径扩展。 |

候选值 MUST 仅受 `start_time`、`end_time` 影响。当前已选端类型、版本号、页面、网络、指标不得改变候选值列表，避免首期复杂级联逻辑造成状态不一致。

### FR-003 候选值排序与限制

候选值接口 SHOULD 定义稳定排序与数量限制，避免数据量增长后影响管理端体验。

排序建议：

- 端类型按业务固定顺序：管理端 Web > 店主 Web > 微信小程序。
- 指标按产品固定顺序：首屏可用 > 完整加载 > 首个接口完成 > DOM 加载完成 > 小程序启动就绪 > 接口请求耗时 > 接口失败耗时。
- 版本号、页面、设备、网络按最近出现优先；最近时间相同时按样本数倒序，再按 value 升序。

限制建议：

- 单个动态维度默认最多返回 100 个候选项。
- 候选值为空时前端展示“暂无可选值”或仅保留“全部”选项，不影响 summary / samples 查询。

### FR-004 管理端筛选区

Web 管理端性能观测页 MUST 使用候选值接口渲染筛选控件。

筛选区顺序 MUST 固定为：

```text
时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标
```

交互要求：

- 时间范围仍由前端固定选项提供，并驱动候选值接口重新请求。
- 端类型、版本号、页面、网络、指标均使用可选择控件，不使用纯文本输入；设备不作为本期筛选项展示。
- 每个维度保留“全部”选项。
- 切换任一筛选条件后，聚合列表回到第一页。
- 重置按钮恢复默认时间范围和全部维度。
- 候选值加载失败时，页面 MUST 有可感知错误反馈；已有聚合查询不应被静默误导为无数据。

### FR-005 聚合列表字段顺序

管理端性能观测聚合列表 MUST 按以下顺序展示字段：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作
```

字段展示要求：

- 页面展示 `page_key`，长文本应截断或使用既有受控展示样式，避免撑破表格。
- 版本号空值展示“版本未知”。
- 设备空值展示“设备未知”。
- 网络空值展示“网络未知”。
- 指标使用后端候选值或统一指标 label 显示，不直接暴露难读 key 作为唯一文本。
- 操作列保持查看样本入口，并将当前聚合维度带入样本页查询参数。

### FR-006 样本页字段顺序

性能样本页 MUST 延续同一维度顺序展示样本上下文和样本列表。

样本上下文顺序 MUST 为：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标
```

样本列表字段顺序 MUST 为：

```text
页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id
```

样本页展示要求：

- 样本页不得展示完整 URL、Header、Cookie、签名 URL、Authorization 或原始 payload。
- `request_id` 继续使用受控截断与复制交互。
- 时间格式沿用现有本地化展示规则。
- 空值文案与聚合列表保持一致。

### FR-007 API、Orval、文档与测试同步

本需求涉及 API 变更，实施时 MUST 同步：

- FastAPI 路由、Pydantic Schema、Service / Repository 查询逻辑。
- OpenAPI 输出与 Orval 生成客户端。
- Web 管理端 API 封装与页面测试。
- 后端性能事件 API 测试，覆盖权限、时间范围、空数据和候选值内容。
- `docs/03-api-index.md` 中管理端性能观测接口索引。

本需求不要求 DB 表结构变更；实现阶段若需要新增索引或字段，必须同步 SQLite / MySQL schema、数据库文档和测试。

## 5. UI 约束

- 管理端性能观测页 MUST 遵守“工业石材 · 暗色旗舰风” Design System。
- 筛选控件 SHOULD 复用现有管理端筛选组件，例如 `AdminFilterSelect` 或同等 DS 组件。
- UI 样式必须使用 semantic token 和既有管理端样式，不使用裸 Hex。
- 筛选区不得出现纯文本说明式帮助块替代真实控件。
- 长页面、版本号和 request_id 展示必须避免表格横向撑破。
- 加载、空数据、失败、权限不足状态必须保持管理端既有交互风格。

## 6. 关联需求与文档

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父级需求 | `REQ-0107-real-user-page-load-rum` | 已建立 RUM 事件模型、上报、聚合和样本查询能力，本需求补齐管理端筛选候选值体验。 |
| 相关文档 | `docs/03-api-index.md` | 新增候选值接口后需要同步 API 索引。 |
| 相关文档 | `docs/04-database-design.md` | 若实现阶段新增索引或字段，需要同步数据库设计；无 DB 变更时注明不涉及。 |
| 规则 | `rules/api.md` | API 变更需同步 OpenAPI / Orval / 测试和错误响应。 |
| 规则 | `rules/ui-design.md` | Web 管理端 UI 必须遵守 Design System semantic token。 |
| 规则 | `rules/security.md` | 候选值接口属于管理端查询能力，必须保持系统管理员权限边界。 |

## 7. 状态块

```yaml
status: done
lifecycle_stage: review
next_step: /sprint-propose sprint-xxx --req REQ-0113-admin-performance-observability-filter-options
expected_openspec_change: add-admin-performance-observability-filter-options
related_change: add-admin-performance-observability-filter-options
needs_prototype: false
needs_api_change: true
needs_database_change: false
needs_orval: true
needs_docker_validation: false
readiness: Partially Ready
readiness_notes: 已补齐五件套与 prototype 策略，评审通过；admin-list best-practices 为 draft，故 readiness 保持 Partially Ready。
cross_cutting_tags:
  - admin-list
  - admin-performance-observability
  - admin-filter
  - api
  - orval
```

## 8. 待完善项

- 在 `/req-complete` 阶段补齐用户故事、业务流程和验收用例。
- 在 OpenSpec 阶段确认候选值接口响应 Schema 是否需要包含 `count`、`last_seen_at` 或仅返回 `value` / `label`。
- 在实现阶段确认候选值查询是否需要复用现有索引，或新增轻量索引优化。
