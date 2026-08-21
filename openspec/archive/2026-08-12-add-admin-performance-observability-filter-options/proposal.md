# 提案：管理端性能观测筛选候选值接口

## 背景

`REQ-0107-real-user-page-load-rum` 已交付 RUM 上报、聚合和样本查询能力。当前管理端性能观测页已能查看聚合与样本，但筛选项缺少统一候选值来源，页面、版本号、设备、网络等维度容易依赖手工输入或前端临时口径，导致排障时输入错误、无结果和字段展示顺序漂移。

`REQ-0113-admin-performance-observability-filter-options` 已评审通过并纳入 `sprint-023`。本 Change 将其转为 OpenSpec 实施计划，补齐管理端候选值 API、前端筛选控件和字段顺序契约。

## 变更范围

- 新增管理端性能观测筛选候选值接口，返回端类型、版本号、页面、设备、网络、指标 6 大维度。
- 候选值仅按时间范围返回，不做其他筛选项级联收敛。
- 端类型和指标由后端固定枚举及 label 返回；版本号、页面、设备、网络由性能事件数据按时间范围提取。
- 管理端性能观测筛选区顺序固定为：时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标；设备候选值由接口返回但不作为本期筛选控件展示。
- 聚合列表和样本页字段顺序按 REQ 验收契约展示。
- 同步 OpenAPI、Orval、API 文档、后端测试和 Web 管理端测试。

## 非目标

- 不接入第三方 APM/RUM 平台。
- 不新增趋势图、告警、SLA、实时大屏或复杂 BI 分析。
- 不调整 RUM 事件采集模型。
- 不做候选值级联筛选。
- 默认不修改数据库表结构；若实现阶段确认需要新增索引，需同步 SQLite/MySQL schema 与数据库文档。

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new:
    - 管理端性能观测筛选候选值接口
  modified:
    - real-user-performance-monitoring
    - Web 管理端性能观测页
    - Web 管理端性能样本页
```

## 验收摘要

- 后端接口权限、时间范围、空数据、固定枚举、动态候选值和排序可测试。
- Web 筛选区、聚合列表、样本页上下文和样本表字段顺序可测试。
- 样本页继续不展示完整 URL、Header、Cookie、签名 URL、Authorization 或原始 payload。
- OpenAPI、Orval 与 `docs/03-api-index.md` 同步。
