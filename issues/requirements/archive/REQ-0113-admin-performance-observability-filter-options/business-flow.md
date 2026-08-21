---
requirement_id: REQ-0113-admin-performance-observability-filter-options
created_at: 2026-08-12 19:09:40
updated_at: 2026-08-12 21:33:00
---

# 业务流程

## 1. 范围流程

```text
系统管理员
  |
  v
进入管理端性能观测页
  |
  v
选择时间范围
  |
  +--> GET /api/v1/admin/performance-events/filter-options?start_time=...&end_time=...
  |       |
  |       +--> 后端校验系统管理员权限
  |       +--> 按时间范围读取 performance_events 动态维度
  |       +--> 合并后端固定端类型与指标枚举
  |       +--> 返回 6 大维度候选值
  |
  v
选择端类型 / 版本号 / 页面 / 网络 / 指标
  |
  +--> GET /api/v1/admin/performance-events/summary
  |       |
  |       +--> 返回聚合列表、分页 total、样本量与分位耗时
  |
  v
点击聚合行“查看样本”
  |
  +--> GET /api/v1/admin/performance-events/samples
          |
          +--> 返回受控样本字段，不返回敏感 payload
```

## 2. 候选值口径

```text
时间范围
  |
  +--> client_types  : 后端固定枚举
  +--> metrics       : 后端固定枚举
  +--> app_versions  : performance_events distinct app_version
  +--> page_keys     : performance_events distinct page_key
  +--> device_classes: performance_events distinct device_class
  +--> network_types : performance_events distinct network_type
```

候选值仅按时间范围过滤，不受端类型、版本号、页面、网络、指标等其他筛选项影响。

## 3. 与父需求差异

| 项目 | REQ-0107 | REQ-0113 |
|---|---|---|
| 核心目标 | 建立 RUM 采集、上报、聚合和样本查询 | 补齐管理端筛选候选值接口和展示顺序契约 |
| 主要端 | Web、微信小程序、后端、多端采集 | Web 管理端和后端管理端 API |
| 数据模型 | 定义并落库 `performance_events` | 复用已有 `performance_events`，默认不改表结构 |
| UI 范围 | 管理端性能观测入口与基础列表 | 筛选控件、聚合列表字段顺序、样本页字段顺序 |
| API 范围 | 上报、summary、samples | 新增 filter-options |

## 4. 异常与降级

| 场景 | 预期行为 |
|---|---|
| 未登录 | 返回统一 401，前端沿用管理端鉴权处理。 |
| 非系统管理员 | 返回统一权限错误，前端展示权限不足或请求失败反馈。 |
| 时间参数非法 | 返回统一参数错误，前端展示候选值加载失败。 |
| 时间范围内无性能事件 | 候选值动态维度为空数组，固定枚举仍可返回。 |
| 候选值接口失败 | 前端显示可感知错误反馈，不把失败误报为暂无性能样本。 |
| summary / samples 为空 | 使用现有空态展示，不展示敏感调试信息。 |

## 5. 数据与权限边界

- 候选值接口只面向系统管理员。
- 候选值不得返回完整 URL、Header、Cookie、签名 URL、Authorization、原始 payload 或可识别个人身份的数据。
- 本需求默认不新增数据库字段；如实现阶段需要新增索引，必须同步 SQLite / MySQL schema、数据库文档和测试。
- OpenAPI / Orval / Web API 封装必须与后端 Schema 保持一致。
