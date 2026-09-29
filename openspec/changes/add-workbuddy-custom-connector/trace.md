---
change_id: add-workbuddy-custom-connector
status: applied
lifecycle_stage: change
source_requirement: REQ-0132-workbuddy-custom-connector
sprint: sprint-029
change_type: add
created_at: 2026-09-04 17:55:26
updated_at: 2026-09-11 09:12:44
---

# Change 追踪

## 远程协议与部署准备返修（2026-09-11）

补齐原范围内协议契约、官方 SDK 实际 HTTP 互操作和非 root 单实例部署准备；源码偏差根因 confirmed，证据入口 `remote-acceptance.md`。新增 7.13–7.15 完成，8.1 原生 HTTPS 与 8.3 跨主机/企业策略仍未完成，REQ 保持 pending。观测沿用既有来源头和审计，不将身份/业务替身测试标作真实日志落库。未自动创建 follow-up。

## 基本信息

```yaml
change_id: add-workbuddy-custom-connector
status: applied
lifecycle_stage: change
source_requirement: REQ-0132-workbuddy-custom-connector
sprint: sprint-029
change_type: add
impact:
  backend: true
  web: false
  miniapp: false
  admin: true
  database: false
  storage: true
  api: true
  deployment: true
  connectors: true
capabilities:
  new:
    - workbuddy-custom-connector
  modified: []
product_data_collection_observability:
  status: applicable
  affected_layers:
    - backend_api
    - request_logs
    - task_traces
    - task_trace_spans
    - admin_web_indirect
    - object_storage_indirect
    - deployment
  reason: 连接器将作为直接 API 调用方访问 ProjectTilesFST，并在第二阶段执行管理端写操作、媒体上传和远程 MCP 服务部署，涉及请求来源识别、工具调用审计、任务链路、错误摘要、环境变量和凭据安全。
  validation: 新增隔离 Docker 真实 stdio、SQLite 与 MinIO 验收，全部实际管理写请求的 request_logs/Task Trace/spans 关联通过；品牌/类目缺口已补齐。输入、权限、媒体对象/URL、单机多进程幂等与容器重启已验证，详见 local-acceptance.md；HTTPS 原生与跨主机/企业保留策略仍待验。
```

## Requirement Readiness Report

```yaml
status: partially_ready
reason: REQ 六件套已齐全且状态为 in_sprint；本 REQ 第一阶段不新增管理端 UI，prototype 缺失不阻断 req-opsx。media-upload best practice 为 draft，作为横切验收提示保留。
review_gate: pass
sprint_gate: pass
iteration: sprint-029
```

## 原型与 UI 冲突

```yaml
prototype_present: false
ui_explore_gate: not_applicable
reason: 第一阶段不新增 Web 管理端 UI；第二阶段若新增配置、权限或审计页面，应在实现阶段复用既有 Design System。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-04 18:17:47 | `/opsx-apply` | 完成 WorkBuddy MCP 运行时、连接器交付包、stdio PoC、HTTPS MCP 入口、受控写工具、文档与验证；状态更新为 applied |
| 2026-09-04 17:55:26 | `/req-opsx` | 从 REQ-0132 创建 OpenSpec Change，状态为 proposed |

## 安全与完整性返修

最新本地部署验收结果见 `local-acceptance.md`（2026-09-08）。新增专属 Compose、合成数据验收脚本和恢复手册；修正 DISABLED 下架契约、媒体前置校验，以及品牌/类目连接器维护请求缺失 Task Trace。当前本地结果不替代远程原生与企业部署验收。

本轮文档同步：tasks、design、delta spec、REQ acceptance、Sprint acceptance-report/release-note、API 索引、部署说明、外部中文 Skill。无业务 HTTP 请求/响应 schema 或 SQLite/MySQL schema 变化，9 个受影响 OpenAPI 路径比较无差异，因此无需 Orval/数据库文档；无 Web、小程序或管理端 UI 改动，无需 UI 文档。任务 8.2 本地范围完成，8.1 与 8.3 仍未完成。

以下为 2026-09-06 历史返修证据。

root_cause_status: confirmed

根因证据：返修前 `tools/write.py::_write_gate` 对空 payload 和单字符幂等键返回通过；`preview_manage_brand` 空创建 payload 返回空 missing_fields；`safe_error_result` 保留合成 token 字符串；`http_server.py::_authorize` 未配置 Token 时直接返回。这些只读探针与源码证据确认验收缺口，未执行真实写入。

调整：Pydantic 动态工具输入模型与基础业务 payload 校验，预览复用缺失/无效字段规则；错误采用固定摘要，预览不回传完整 payload；外部 Skill 中文化；连接器入口增加持久化幂等预约和跨进程去重，未知结果不重试；远程使用按用户凭据映射、auth/me 验真、scope 交集、匿名拒绝、Origin 拒绝、202 通知与限流；工具审计只记稳定元数据。

验证：`uv run --project src/backend pytest tests/test_workbuddy_connector.py tests/test_workbuddy_hardening.py -q` 为 52 passed（既有 Pydantic 弃用提示 1 条），ruff 通过。证据覆盖非法写入零调用、预览、同键重复/冲突、并发一次执行、跨进程账本、未知结果阻断、凭据隔离/撤销/过期/越权、HTTP 限流和审计脱敏；均为本地自动化与测试替身，不代表真实上传或企业远程验收。剩余项见 tasks 第 8 节和 REQ acceptance 矩阵。

product_data_collection_observability：本轮适用 backend_api、request_logs、connector_audit；任务链路继续复用既有后端实现，实际落库关联仍待验。幂等目录仅为连接器自身元数据，不读写业务数据库，无 SQLite/MySQL schema 迁移；无 Web、小程序、管理端 UI 变化。后端业务 API 与 Web Orval 输入不变，独立 MCP OpenAPI 通过 TestClient 检查，文档登记新增传输层错误与配置；Docker/HTTPS/真实存储验收未执行。更新设计、delta spec、任务、REQ AC、Sprint 证据、API/部署文档与交付说明，无需更新数据库或 UI 文档。

### 原生只读历史证据

2026-09-06 14:31:56，通过 WorkBuddy App 的 MCP 服务管理执行重连与信任，在已有 SKU 查询任务提交仅允许原生 MCP 工具的验证请求。首次原生执行报告缺少 text 字段；`src/mcp/workbuddy/server.py` 的 tools/call 返回非标准 type=json 内容块，根因 confirmed。改为 type=text、text 为 JSON 序列化业务结果，并通过 isError 表示工具失败。该修复不改变业务参数、后端 API 或权限。

本机配置已固定解释器绝对路径与 PYTHONPATH，使用本地既有凭据刷新过期 Token（旧请求 HTTP 401/40102），保持真实写工具关闭，配置权限 600。真实凭据和机器配置不进入仓库。

证据来源：Codex 通过原生应用自动化读取 WorkBuddy 任务的 14:31 原生 MCP 验证报告，列出 `mcp__projecttilesfst-workbuddy__search_tile_skus` ok=true、pagination.page_size=10、item count=10；`mcp__projecttilesfst-workbuddy__summarize_catalog` ok=true、sample_count=5。请求明确禁止脚本、子进程、API 直连、配置读取和登录替代。此证据是 App 内原生调用报告，非独立抓包；证明本机只读工具联通，不证明其他工具、远程 HTTPS 或企业鉴权审计已验收。

验证：连接器 pytest 30 passed，包含文本内容块、可解析 JSON 与 isError 成败映射；ruff 通过。观测适用层级延续 backend_api/request_logs，无新增 DB、日志字段、UI 或部署拓扑，无需 Orval 或 Docker Compose 重验。

## 分页验收返修

root_cause_status: confirmed

附件截图逐项视觉对照表（仅记录反馈摘要，不保存截图中的商品数据）：

| 截图编号 | 页面/状态 | 期望表现 | 实际表现与偏差 | 检查方式 | 处置结论 | 证据入口 |
|---|---|---|---|---|---|---|
| S1 | WorkBuddy MCP 配置 | 本地连接参数可解析 | 用户截图含环境变量占位符 | 配置截图对照 | 本次分页返修不改本机配置 | 用户提供的 MCP 配置截图 |
| S2 | WorkBuddy 查询反馈 | SKU 查询分页可用 | page_size=5 被拒绝，改用 10 后取前 5 条 | 后端校验代码和本地回归测试 | 修正 schema 与运行时归一化 | 用户提供的查询反馈截图；tests/test_workbuddy_connector.py |
| S2 | WorkBuddy 加载反馈 | 内置连接器正常调用 | 报告手动启动 stdio 子进程、defer_loading、23 个工具 | 截图文本核对 | 仅证明用户报告的手动 MCP 查询；原生连接器加载不在本次修复证明范围 | 用户提供的查询反馈截图 |

根因证据：`src/backend/app/services/tile_sku_admin_service.py` 的 `VALID_PAGE_SIZES` 和 `list_skus` 明确拒绝非 10/20/50/100。修复前 `schemas/tools.py` 声明连续范围、`tools/catalog.py` 直接传入 5；摘要也直接把 sample_size 作为 page_size。回归测试使用后端真实枚举约束测试替身，修复前 12 failed / 15 passed，包含 page_size=5、摘要 5 条及 schema 枚举缺失。

调整：搜索默认 20，整数分页向上取合法档位并封顶 100；摘要以合法分页取数，再按 sample_size 截取。搜索仍返回后端原分页结果，保留页码和筛选条件。

本次 product_data_collection_observability 适用层级为 backend_api、request_logs：沿用 API adapter 和来源请求头，无新增日志字段或行为事件。DB、Task Trace、存储、Web、小程序、管理端 UI、权限和部署变更均 N/A。后端 HTTP 请求/响应/错误码契约未变，无需 Orval、数据库迁移、Docker Compose 或长期 API/部署文档更新。

验证结果：`uv run --project src/backend pytest tests/test_workbuddy_connector.py -q` 为 27 passed（既有 Pydantic 弃用提示 1 条）；ruff、OpenSpec strict、OpenSpec 语言、目录结构、上下文预算和产品观测门禁均通过。根因脚本退出 0，但因无关联 BUG 未自动检查根因，根因结论以本节代码与失败/通过测试证据为准。本地自动化证据不代表 WorkBuddy 原生连接器或 HTTPS 企业部署验收通过。
