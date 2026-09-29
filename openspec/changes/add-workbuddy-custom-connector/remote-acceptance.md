---
purpose: REQ-0132 远程协议与部署准备验收
content: 本地协议互操作、容器部署准备及未完成边界
created_at: 2026-09-11 09:12:44
updated_at: 2026-09-11 09:19:27
---

# 远程部署准备验收

## 偏差与修复

根因状态 confirmed，限定为源码可证的协议偏差：原 `server.py` 初始化固定返回 2024-11-05、未知方法统一 -32603，`http_server.py` 未检查协议版本头及媒体协商。不是对真实 WorkBuddy HTTPS 失败原因的推断。

已按 [MCP 2025-06-18 传输规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) 与 [生命周期](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle) 补齐无状态 JSON 模式、初始化版本协商、通知/客户端响应 202、GET/DELETE 405、415/406、非法版本 400、请求大小 413 及 JSON-RPC 安全错误。Pydantic 严格解析 envelope；缺 id 的通知不会执行写工具。保留已有 stdio 和工具 registry，未引入运行时 SDK 依赖。

## 证据

| 来源 | 结果 | 证明边界 |
|---|---|---|
| `tests/test_workbuddy_protocol.py` | 25 项通过，含固定官方 mcp==1.13.1 SDK | SDK 通过实际 loopback TCP/HTTP 完成 initialize、initialized 通知、list_tools、call_tool、ping；身份和业务 registry 为替身，无真实后端调用 |
| 原有 connector/hardening 测试 | 61 项通过 | 工具回归、身份隔离、撤销、权限、幂等及错误摘要的本地自动化证据 |
| Dockerfile 本地构建 | 成功，复用现有后端镜像 | 基础镜像 ID 为 sha256:2b22a610422f912e46a172592cb6111dbc0324cf85b66ca79606b4dcdfa5eced；不是产品发布镜像或生产部署确认 |
| `deploy/scripts/verify-workbuddy-remote.py` | 七类检查通过 | 实际独立 Compose：安全配置、UID 10001、health、匿名/无效凭据拒绝、卷写入及容器重启后同键阻断；空合成凭据映射，不连接业务服务 |

复跑入口与部署前置条件以 `deploy/prod/workbuddy.md` 为事实源。运行时脚本仅删除本次随机项目及合成卷，不触碰业务容器、历史本地验收卷或 WorkBuddy 配置。

## 影响与剩余项

### 扩大回归与独立失败

扩大执行 140 项首次得到 136 passed / 4 failed，其中 SDK 测试默认 Uvicorn 日志配置影响同进程 caplog；已通过 `log_config=None` 和禁用不需要的 WebSocket 适配修复隔离。最终聚焦复跑 MCP、harness、维护 Trace、类目和媒体日志测试共 116 passed、4 个既有弃用 warning。

品牌测试单独运行、不加载本次 SDK 测试，结果 22 passed / 3 failed：`test_upload_brand_logo_returns_accessible_media_url` 为 404，`test_brand_list_returns_accessible_logo_url`、`test_brand_detail_returns_accessible_logo_url` 为 429。故扩大回归不能宣称全绿；媒体失败根因 unknown，本次未修改品牌媒体业务代码或豁免断言。

独立 follow-up 建议（未自动创建 Issue）：

- 建议命令：`/bug-capture 品牌媒体 URL 回归独立运行出现 404/429`
- 类型倾向：测试隔离或媒体代理行为缺陷，根因待证据确认。
- 背景：品牌测试独立运行仍有三项失败，非 SDK 日志污染。
- 影响范围：品牌上传、列表及详情媒体 URL 验收，不扩展 MCP 协议返修。
- 复现与验收：`uv run --project src/backend python -m pytest src/backend/tests/test_admin_brands.py -q --tb=short`；确认代理预算、对象定位、测试配置边界，三项恢复且无真实存储访问。
- 来源：REQ-0132、add-workbuddy-custom-connector、sprint-029、opsx-modify 扩大回归。

### 校验与收尾

OpenSpec strict、语言、目录、观测门禁、Ruff 与 diff whitespace 校验通过。Sprint 目标列表中的空行导致校验器提前结束读取，仅移除该空行，保留全部其他需求内容。最终镜像构建无告警，镜像 ID 为 sha256:03d15259fdf037e7d06bf9294bad0ea50fa1ff1c296a0d4cdea2e7270fc164d9。

product_data_collection_observability 适用于 MCP HTTP 入口、deployment 及既有 backend_api/request_logs 链路。本次未改变 API adapter 的来源头、工具审计、业务写入 Trace，也不新增 usage_events。身份替身测试不证明真实日志落库；此前真实本地证据沿用 `local-acceptance.md`。

未修改业务 `/api/v1` 请求响应、数据库、Web、小程序或管理端页面，不需 Orval 重生成。MCP HTTP 契约已同步 API 索引和部署文档。

任务 8.1 保持未完成：真实 HTTPS 网关、证书、网络路径、WorkBuddy 原生远程工具及专用账号验收尚缺。任务 8.3 保持未完成：跨主机共享存储原子性和企业账本保留/恢复责任人尚缺；默认单实例避免声称分布式保证。静态 Bearer 映射不等于 OAuth；默认 8 MiB JSON 限制不等于大视频验收。

没有自动归档、发布或创建 follow-up Issue。当前命令只推进原 Change 内可本地完成的准备工作。
