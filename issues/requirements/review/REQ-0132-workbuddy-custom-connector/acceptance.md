---
requirement_id: REQ-0132-workbuddy-custom-connector
title: 腾讯 WorkBuddy 自定义连接器支持验收标准
acceptance_status: pending
owner: product
source: requirement.md
priority: P1
created_at: 2026-09-04 16:55:18
updated_at: 2026-09-11 09:12:44
---

# REQ-0132 验收标准

## 远程准备证据（2026-09-11）

补齐无状态 Streamable HTTP 版本协商、传输头/请求大小/JSON-RPC 校验，固定官方 SDK 实际 HTTP 互操作及独立单实例 Compose 验证通过。详见 Change `remote-acceptance.md`。AC-006 的本地协议/部署准备已有证据，真实 HTTPS 与 WorkBuddy 原生远程调用仍待验；health 不代表后端/账号有效，跨主机及保留恢复策略仍待确认，整体 acceptance_status 保持 pending。

## 功能 AC

- [ ] AC-001 连接器以 MCP + Skill 方式定义 ProjectTilesFST 能力，工具命名使用业务语义，不暴露通用 HTTP 代理或数据库直连能力。
- [ ] AC-002 第一阶段支持本地 stdio MCP PoC，可连接本地或测试 FastAPI，并完成工具列表、参数 schema 和示例指令验证。
- [ ] AC-003 第一阶段只读工具覆盖 SKU 搜索、商品详情、品牌查询、类目查询和目录摘要。
- [ ] AC-003a SKU 搜索 page_size schema 为 10/20/50/100，默认 20；运行时非标准整数向上归一并封顶 100（5 转为 10），保留筛选条件、页码与后端分页信息；摘要 sample_size=5 时以合法分页取数，最多返回前 5 条，汇总不变。
- [ ] AC-004 第一阶段管理端写操作仅提供 dry-run / 草稿预览，不写数据库、不上传对象存储、不改变上下架状态。
- [ ] AC-005 dry-run 返回拟变更字段、差异、缺失必填项、权限要求、风险提示和下一步人工确认方式。
- [ ] AC-006 第二阶段支持 HTTPS 远程 MCP 服务，明确 SSE 或 streamable HTTP 连接方式、健康检查、超时、限流和错误摘要。
- [ ] AC-007 第二阶段真实写操作首批覆盖 SKU 创建/编辑、SKU 上下架、品牌/类目维护和媒体上传。
- [ ] AC-008 真实写操作必须完成身份鉴权、工具级 scope 校验、Pydantic 输入校验和幂等校验。
- [ ] AC-009 高风险写操作前，WorkBuddy 必须展示目标对象、变更摘要、影响范围和确认动作；删除操作不进入 MVP。
- [ ] AC-010 媒体上传必须调用后端上传 API，经 MIME、大小、扩展名和用途校验后写入 MinIO 适配层，不允许连接器直连对象存储。
- [ ] AC-011 只读查询结果遵守公开数据和管理端数据权限边界，未授权用户不得读取管理端字段。
- [ ] AC-012 连接器凭据不得写入 Git、日志、AI 输出、完整 payload 或可公开文档；`.env.example` 仅使用示例值和安全注释。
- [ ] AC-013 新增或修改 HTTP API、请求头、响应字段、错误码或 Schema 时，同步 OpenAPI、Orval、`docs/03-api-index.md` 和集成测试。
- [ ] AC-014 新增远程 MCP 服务部署时，同步 Docker Compose 或生产等价部署说明、环境变量示例和健康检查。
- [x] AC-015 Skill 文案中文优先，说明工具用途、参数、权限边界、dry-run/真实写入差异、确认规则和错误恢复。

## 本地隔离验收（2026-09-08）

证据入口：`openspec/changes/add-workbuddy-custom-connector/local-acceptance.md`；复跑入口：`python deploy/scripts/verify-workbuddy-local.py`。真实 stdio 连接独立 FastAPI、SQLite、MinIO，覆盖全部写入/只读/预览、媒体上限边界、对象 stat/URL、四进程同键去重、重启和请求日志/Task Trace 落库。

| AC | 已新增证据 | 尚未证明 |
|---|---|---|
| AC-003/004/005/007 | 五种只读、六种预览及全部受控写工具真实调用；预览无业务/存储副作用 | WorkBuddy 原生写入展示、自然语言确认 |
| AC-008/SEC-003 | 实际非法身份/确认/scope 拒绝，四进程并发单次写入，失败同键阻断，单机命名卷重启 | 多主机共享目录和企业恢复/保留策略 |
| AC-010/XCUT | 四类上传与 MinIO 对象/URL一致；1 MiB 测试上限及上限加一字节；MCP 前置扩展名与非空 Base64 防护 | 后端直连接口独立扩展名校验、视频播放、生产大小/全部编码组合不据此判定 |
| AC-OBS-002..006 | 每条实际管理写请求有 Trace 与 spans，包括新增品牌/类目观测；日志身份、关联、敏感标记检查及无伪造行为事件通过 | 企业日志采集与保留策略 |

SKU 下架标准目标为 `DISABLED`，旧 `DRAFT` 仅兼容下架别名，预览必须展示实际目标；不得宣称转为草稿。`invalid_media` 表示输入在后端请求及幂等预约前被拒绝。以上补充不将整体 acceptance_status 改为通过；HTTPS 原生及企业部署验收仍待完成。

## 2026-09-06 安全返修历史口径

验收来源：`tests/test_workbuddy_connector.py` 与 `tests/test_workbuddy_hardening.py`，52 项本地 pytest 通过；非生产或真实远程验收。

| AC | 当前结果与证据 | 剩余验证 |
|---|---|---|
| AC-003a | 分页 schema、整数归一和摘要截取回归通过 | 既有原生只读证据见 Change trace |
| AC-004/005 | 预览不写入，SKU/品牌/类目共用基础 Pydantic 缺失字段检查，字段摘要和下一步指引 | 全部预览在原生客户端展示与人工确认 |
| AC-008/SEC-003 | 非法参数、确认缺失、scope 不足不触发写入；同键并发、跨进程、冲突与未知状态拦截通过 | 隔离业务数据上的真实写入、部署共享卷与恢复流程 |
| AC-012/OBS-005 | 错误消息不透传、审计不含合成敏感数据、幂等记录仅摘要与状态 | 部署日志采集/保留与实际 Trace 脱敏 |
| AC-SEC-001/002/004 | 远程凭据按用户映射；后端 auth/me 验真；过期、撤销、非法角色、scope 拒绝测试通过 | 真实用户与 HTTPS 原生连接验证 |
| AC-015 | 中文 Skill 已覆盖工具、分页、确认、凭据边界和幂等错误恢复 | 交付包安装后的自然语言行为验收 |
| AC-006/014 | HTTP 认证关闭匿名默认、202 通知、Origin 拒绝、限流测试；部署说明与新变量已同步 | 完整远程 MCP 协议兼容、TLS 网关与企业部署 |
| AC-007/010/OBS-003/004/006/XCUT-001..004 | 复用后端 API 和来源头，补充工具审计摘要 | 全部真实写操作、上传边界、对象/URL、请求日志和任务链路实际关联 |

幂等保证限定于连接器入口和同一持久化共享账本：相同后端/用户/键最多发起一次写入尝试；重复结果通过业务查询恢复，不缓存或重放完整响应。不是后端全局去重，也不承诺更换键或不共享存储实例的去重。远程身份映射不改变后端数据范围，不等同于 OAuth。整体 acceptance_status 保持 pending。

## 产品数据采集与链路观测 AC

- [ ] AC-OBS-001 需求、Change、任务和验收材料记录 `product_data_collection_observability` 适用状态、affected layers、原因和验证摘要。
- [ ] AC-OBS-002 连接器作为直接 API 调用入口时，不伪造 `usage_events`；若新增管理端连接器配置 UI，则 UI 页面访问和表单提交按 Web 管理端行为事件规则采集。
- [ ] AC-OBS-003 所有后端 API 调用默认写入 `request_logs`，并能识别 `workbuddy_connector` 或等价来源、`client_request_id`、资源类型、结果和脱敏错误摘要。
- [ ] AC-OBS-004 写操作、媒体上传、批量或长耗时工具接入 `task_traces` 和 `task_trace_spans`，并能通过 `request_id` 关联。
- [ ] AC-OBS-005 日志、Trace、错误摘要和审计记录不得保存完整 prompt、完整请求体、完整响应体、Authorization、Cookie、Token、真实密钥、本机绝对路径或真实客户敏感数据。
- [ ] AC-OBS-006 验证覆盖直接 API 调用、鉴权失败、越权、dry-run 不写入、真实写入成功/失败、媒体上传成功/失败和日志脱敏。

## 安全与权限 AC

- [ ] AC-SEC-001 连接器不能绕过现有 `admin/employee` 管理端权限边界。
- [ ] AC-SEC-002 后端不信任 WorkBuddy 传入的用户身份字段作为认证或授权依据。
- [ ] AC-SEC-003 第二阶段真实写操作具备工具级 scope，scope 至少区分只读、SKU 写入、上下架、品牌/类目维护和媒体上传。
- [ ] AC-SEC-004 凭据支持轮换或可替换配置；凭据缺失、过期或 scope 不足时返回明确错误码和脱敏错误摘要。
- [ ] AC-SEC-005 删除类操作不在 MVP 范围；若后续开放，需独立需求、独立评审和强确认。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: add-workbuddy-custom-connector
source_sprint: sprint-029
evidence: []
failed_items: []
source_event: opsx.modify
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防管理端媒体上传链路回归。

- [ ] AC-XCUT-001 媒体上传工具在实现真实上传时，必须验证上传状态机或等价服务端流程覆盖 `idle -> uploading -> done/failed`，失败信息可定位到上传对象或工具结果，不能只依赖全局错误摘要。
- [ ] AC-XCUT-002 媒体上传成功后，同一会话内必须能通过业务接口或工具结果立即获得可回显的媒体 URL、object key 摘要和媒体元数据。
- [ ] AC-XCUT-003 含上传的 Change 必须从 Web Docker 用户入口 `http://localhost:3000` 或等价生产入口验证边界文件；小文件成功，超限文件返回业务错误而不是 Nginx 413。
- [ ] AC-XCUT-004 媒体验收必须同时记录脱敏 key、对象存在性、`/media/{object_key}` 或公开 URL 状态、业务错误码和用户/工具可见表现；不得只以 HTTP 200 作为通过依据。
- [ ] AC-XCUT-005 第一阶段 stdio PoC 不执行真实上传：N/A — 仅需验证 `preview_media_upload` 不写数据库、不写对象存储，并提示第二阶段上传链路验收要求。
