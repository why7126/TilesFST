---
requirement_id: REQ-0132-workbuddy-custom-connector
title: 腾讯 WorkBuddy 自定义连接器支持业务流程
owner: product
source: requirement.md
priority: P1
created_at: 2026-09-04 16:55:18
updated_at: 2026-09-04 16:55:18
---

# REQ-0132 业务流程

## 1. 总体流程

```text
WorkBuddy 用户
  |
  | 自然语言查询 / 维护意图
  v
WorkBuddy + Skill
  |
  | MCP tool call
  v
ProjectTilesFST MCP Server
  |
  | 调用 /api/v1，携带连接器来源、鉴权和 request id
  v
ProjectTilesFST FastAPI
  |
  +--> 只读查询：SKU / 品牌 / 类目 / 详情 / 目录摘要
  |
  +--> dry-run：生成拟变更草稿，不写数据库、不上传对象存储
  |
  +--> 第二阶段真实写操作：鉴权 + scope + 幂等 + 审计
          |
          +--> SKU 创建/编辑/上下架
          +--> 品牌/类目维护
          +--> 媒体上传，经后端校验和 MinIO 适配层
```

## 2. 第一阶段：本地 stdio PoC

```text
开发/演示机器
  |
  +--> WorkBuddy 本地配置 command/args/env
          |
          v
      stdio MCP Server
          |
          v
      本地或测试 FastAPI base URL
          |
          +--> search_tile_skus
          +--> get_tile_sku_detail
          +--> list_tile_brands
          +--> list_tile_categories
          +--> summarize_catalog
          +--> preview_* dry-run 工具
```

第一阶段目标是验证工具粒度、查询准确性、摘要质量和用户价值。该阶段不执行真实管理端写操作，不直接写数据库，不上传对象存储。

## 3. 第二阶段：HTTPS 远程 MCP 服务

```text
WorkBuddy 企业 Agent / 多用户
  |
  | HTTPS SSE / streamable HTTP
  v
远程 MCP Server
  |
  +--> 工具级权限 scope
  +--> 超时 / 限流 / 错误摘要
  +--> 服务端凭据注入
  |
  v
ProjectTilesFST API
  |
  +--> RequestLoggingMiddleware
  +--> Auth / RBAC
  +--> Service / Repository
  +--> Task Trace
  +--> MinIO Adapter
```

第二阶段目标是把连接器从本地 PoC 升级为企业可用服务，开放真实管理端写操作，并具备审计、观测、部署和安全边界。

## 4. 写操作确认流程

```text
用户提出维护意图
  |
  v
WorkBuddy 调用 preview 工具
  |
  v
返回拟变更摘要、字段差异、缺失项、风险和权限要求
  |
  v
用户明确确认
  |
  v
WorkBuddy 调用真实写工具
  |
  v
后端鉴权、scope 校验、幂等校验、Pydantic 校验
  |
  v
Service 执行业务写入 / 上传
  |
  v
request_logs + task_traces 记录结果
  |
  v
返回业务对象 ID、状态、错误码或审计追踪入口
```

删除操作不进入 MVP。若后续需要开放删除，应作为独立需求或独立 Change 评审。

## 5. 媒体上传流程

```text
WorkBuddy 生成上传意图
  |
  v
preview_media_upload 校验文件类型、大小、用途和目标资源
  |
  v
用户确认
  |
  v
upload_tile_media 调用后端上传 API
  |
  v
FastAPI 校验 MIME / 大小 / 扩展名
  |
  v
MinIO 单桶 + 标准前缀写入
  |
  v
DB 记录 object_key 和媒体元数据
  |
  v
/media/{object_key} 代理读取和业务接口回显
```

媒体上传必须从后端授权上传链路进入，不允许连接器直连未授权对象存储。

## 6. 与父需求差异

本需求没有父 REQ。它复用现有 SKU、品牌、类目、媒体上传和日志审计能力，但交付对象是 WorkBuddy 连接器集成层，不替代原业务能力本身。

## 7. 观测流程

```text
MCP tool call
  |
  +--> client_request_id / tool_call_id
  |
  v
FastAPI request_logs
  |
  +--> client_type = workbuddy_connector
  +--> request_id = 服务端可信请求 ID
  +--> resource_type / resource_id / result / error summary
  |
  v
任务类操作
  |
  +--> task_traces.parent_request_id
  +--> task_trace_spans
```

连接器属于直接 API 调用入口，不要求伪造 `usage_events`。若后续新增管理端连接器配置 UI，则 UI 行为按 Web 管理端行为事件规则采集。
