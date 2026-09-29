## 背景

ProjectTilesFST 已具备 SKU、品牌、类目、媒体上传、管理端权限、请求日志和 Task Trace 等基础能力，但企业内部人员在 WorkBuddy 场景下仍需要离开对话窗口到管理端或资料表中反复查询商品资料、整理目录摘要和准备维护草稿。

本变更将 ProjectTilesFST 封装为腾讯 WorkBuddy 自定义连接器能力：第一阶段交付本地 stdio MCP + Skill 只读 PoC 和管理端写操作 dry-run，第二阶段演进为 HTTPS 远程 MCP 服务、企业级鉴权审计和受控真实写操作。

## 变更内容

- 新增 WorkBuddy 自定义连接器能力规格，定义 MCP Server、外部 Skill、连接器交付包和本地/远程两阶段部署形态。
- 新增首批只读 MCP 工具契约：SKU 搜索、商品详情、品牌查询、类目查询和目录摘要。
- 新增第一阶段管理端写操作 dry-run 契约，覆盖 SKU 创建/编辑、上下架、品牌/类目维护和媒体上传预览，要求不写数据库、不上传对象存储、不改变业务状态。
- 新增第二阶段真实写操作契约，覆盖工具级 scope、鉴权、幂等、人工确认、审计、错误摘要和媒体上传后端适配层边界。
- 明确连接器目录归属：运行时代码位于 `src/mcp/workbuddy/`，WorkBuddy manifest、`mcp.json`、外部 Skill、图标和打包说明位于 `connectors/workbuddy/`。
- 明确产品数据采集与链路观测：连接器作为直接 API 调用入口，不伪造 `usage_events`，但必须写入 `request_logs`，高风险写操作、上传、批量或长耗时工具接入 `task_traces` 和 `task_trace_spans`。
- 明确 API、OpenAPI、Orval、部署文档、环境变量示例、测试和安全脱敏的同步要求。

## 能力

### 新增能力

- `workbuddy-custom-connector`: 腾讯 WorkBuddy 自定义连接器能力，覆盖 MCP 工具、外部 Skill、目录交付包、本地 stdio PoC、HTTPS 远程服务、权限审计、dry-run、真实写操作和媒体上传边界。

### 修改能力

- 无。本变更复用现有 SKU、品牌、类目、对象存储、鉴权、API 治理和产品数据采集与链路观测能力，不改变这些正式能力的既有 requirement；若实现阶段发现必须变更其行为，应在本 Change 中追加对应 delta spec 或拆分后续 Change。

## 影响范围

```yaml
impact:
  backend: true
  web: false
  miniapp: false
  admin: true
  database: possible
  storage: true
  api: true
  deployment: true
  connectors: true
capabilities:
  new:
    - workbuddy-custom-connector
  modified: []
```

- 后端/API：连接器工具通过 `/api/v1` 调用 ProjectTilesFST；若现有接口不能满足 AI 工具场景，可新增只读聚合接口或 dry-run 接口，并同步统一响应 envelope、错误码、OpenAPI、Orval、API 文档和集成测试。
- 管理端：第一阶段不新增管理端 UI；第二阶段如需配置连接器凭据、权限或审计查询，应复用现有 Design System 和管理端组件。
- 数据库：第一阶段 dry-run 不写数据库；第二阶段如新增连接器凭据、scope、审计索引、幂等记录或工具调用记录，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。
- 对象存储：媒体上传必须经后端授权上传接口和 MinIO 适配层；第一阶段只做 `preview_media_upload`。
- 部署：第一阶段提供本地 stdio 配置；第二阶段提供 HTTPS 远程 MCP 服务、健康检查、环境变量、Docker Compose 或生产等价部署说明。
