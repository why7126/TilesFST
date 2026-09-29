---
created_at: 2026-09-04 17:55:26
updated_at: 2026-09-11 09:12:44
---

## 1. 连接器骨架与目录

- [x] 1.1 在 `src/mcp/workbuddy/` 建立 MCP server 入口、tool registry、schema、后端 API adapter、鉴权/审计 adapter 和运行时 README。
- [x] 1.2 在 `connectors/workbuddy/` 建立 WorkBuddy manifest、`mcp.json`、外部 Skill、图标占位、打包说明和本地 stdio 配置示例。
- [x] 1.3 确认 WorkBuddy 外部 Skill 不进入 `.agents/skills/`，并通过目录结构校验。

## 2. 第一阶段 stdio PoC

- [x] 2.1 实现本地 stdio MCP Server 启动配置，支持 ProjectTilesFST API base URL、测试凭据、超时和日志级别环境变量。
- [x] 2.2 实现 `search_tile_skus`、`get_tile_sku_detail`、`list_tile_brands`、`list_tile_categories` 和 `summarize_catalog` 只读工具。
- [x] 2.3 为只读工具补充输入 schema、输出 schema、分页/筛选参数、字段白名单和脱敏错误摘要。
- [x] 2.4 实现管理端写操作 dry-run 工具，覆盖 SKU 创建/编辑、上下架、品牌/类目维护和媒体上传预览。
- [x] 2.5 验证 dry-run 不写数据库、不上传对象存储、不改变上下架或主数据状态。

## 3. 安全、权限与观测

- [x] 3.1 为连接器 API 调用注入 `client_type=workbuddy_connector` 或等价来源、`client_request_id` 和脱敏 metadata。
- [x] 3.2 确认连接器不伪造 `usage_events`，所有后端业务 API 调用进入 `request_logs`。
- [x] 3.3 为真实写操作、媒体上传、批量或长耗时工具接入 `task_traces` 和 `task_trace_spans`。
- [x] 3.4 实现或复用连接器凭据、工具级 scope、鉴权失败、scope 不足和脱敏错误摘要处理。
- [x] 3.5 确认日志、Trace、审计摘要和 AI 输出不包含 Authorization、Cookie、Token、真实密钥、完整 payload、完整 prompt、本机绝对路径或真实客户敏感数据。

## 4. 第二阶段远程 MCP 与真实写操作

- [x] 4.1 设计并实现 HTTPS 远程 MCP 服务入口，明确 SSE 或 streamable HTTP 传输方式、健康检查、超时、限流和日志配置。
- [x] 4.2 实现真实写操作工具或受控接口，覆盖 SKU 创建/编辑、SKU 上下架、品牌/类目维护和媒体上传。
- [x] 4.3 为真实写操作补充高风险确认规则、幂等键、Pydantic 校验、业务对象 ID 返回和审计追踪入口。
- [x] 4.4 确认删除类操作未进入 MVP；如需开放，输出独立 follow-up 需求建议但不自动创建。

## 5. API、部署与文档同步

- [x] 5.1 若新增或修改 HTTP API、请求头、响应字段、错误码或 Schema，同步 OpenAPI、Orval、`docs/03-api-index.md`、API 治理说明和集成测试。
- [x] 5.2 若新增 DB 表、字段、索引、迁移或保留周期，同步 SQLite/MySQL schema、迁移、`docs/04-database-design.md` 和测试；若不涉及，记录 N/A 原因。
- [x] 5.3 若新增远程 MCP 服务或环境变量，同步 `.env.example`、部署 env 示例、Docker Compose 或生产等价部署说明和健康检查。
- [x] 5.4 同步 `docs/01-architecture.md`、`docs/02-deployment.md`、`connectors/README.md` 或其他受影响长期文档；不适用项写明原因。

## 6. 验证

- [x] 6.1 补充 MCP 工具单元测试、后端 API adapter 测试、dry-run 无副作用测试和权限越权测试。
- [x] 6.2 补充直接 API 请求日志、Task Trace、脱敏和媒体上传链路聚焦测试。
- [x] 6.3 运行 `python scripts/validate-product-data-observability-gates.py --change add-workbuddy-custom-connector` 或等价聚焦校验。
- [x] 6.4 运行 OpenSpec 校验、OpenSpec 语言校验、目录结构校验和 Sprint scope 校验。
- [x] 6.5 如涉及 Docker Compose 或远程 MCP 服务，运行本地 Compose 或等价 smoke，记录证据来源和证明边界。

## 验收返修记录

- [x] 7.13 补齐无状态 Streamable HTTP 版本协商、JSON-RPC 输入/错误、通知/响应、媒体协商和请求体限额，保留 stdio 兼容。
- [x] 7.14 固定官方 MCP SDK 实际 HTTP 互操作及既有工具回归通过，证据见 remote-acceptance.md；不代替原生 HTTPS。
- [x] 7.15 提供独立非 root 镜像、单实例 Compose、私有 env 示例、凭据目录与网关手册；实际容器 smoke 验证健康、鉴权拒绝和持久化卷重启。

- [x] 7.9 增加独立 Compose 与真实 stdio 验收脚本，专属数据卷、internal 网络、不读取业务 env，验证全部写入/只读/预览。
- [x] 7.10 修正下架 DISABLED 与 DRAFT 兼容语义，补齐媒体扩展名、无路径文件名和非空 Base64 防护。
- [x] 7.11 补齐品牌/类目连接器写入 Task Trace，验证成功/失败、观测降级和非连接器行为不变。
- [x] 7.12 核对单机多进程去重、实际命名卷重启、媒体对象/URL、日志落库及敏感标记，记录手册与 local-acceptance.md 证据。

- [x] 7.5 以 Pydantic 校验工具参数和基础业务 payload，品牌/类目/SKU 预览复用校验规则。
- [x] 7.6 增加持久化幂等预约、同键冲突、并发拦截和未知结果恢复规则，记录实际保证范围。
- [x] 7.7 固定安全错误摘要、精简预览数据、中文化 Skill，并记录不含完整参数/结果的工具审计。
- [x] 7.8 远程入口按用户映射凭据、后端验真、scope 交集和配置缺失拒绝访问，补隔离/撤销/越权自动化证据。

## 剩余部署验收

- [ ] 8.1 使用真实 HTTPS 网关和 WorkBuddy 远程原生客户端验证协议兼容、认证与通知；不能以 TestClient 替代。
- [x] 8.2 在隔离测试数据上验证全部真实写操作、媒体边界文件、对象存在性/URL、request_logs 与 Task Trace 落库关联。证据为 local-acceptance.md；媒体边界使用 1 MiB 测试配置，视频仅验证传输，不代表原生/生产验收。
- [ ] 8.3 验证多进程/实际持久化卷与跨主机共享目录保证，确认幂等账本保留与人工恢复流程。

8.3 本轮已验证单机四进程、实际命名卷重启及失败同键阻断，提供人工核对/保留流程；跨主机目录保证、企业保留周期及恢复责任人仍未验收，保持未完成。

- [x] 7.4 修复原生客户端拒绝非标准 JSON 内容块的问题，tools/call 使用文本内容块和 isError；补充成功/失败回归测试，并在 WorkBuddy App 内重连后验证搜索与摘要工具成功。

- [x] 7.1 根据 REQ-0132 WorkBuddy 分页反馈，将 SKU 搜索 schema 限定为 10/20/50/100，默认 20；运行时整数向上归一化并封顶 100。
- [x] 7.2 目录摘要以合法 SKU 分页取数，再按 sample_size 截取，保持后端汇总不变。
- [x] 7.3 补充后端枚举契约、分页边界、筛选透传和摘要截取回归测试；同步设计、delta spec、REQ AC 与 Sprint 验收证据。
