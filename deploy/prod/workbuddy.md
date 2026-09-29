---
purpose: WorkBuddy 远程 MCP 部署准备
content: 单实例安全拓扑、构建、密钥、网关契约与验收边界
created_at: 2026-09-11 09:12:44
updated_at: 2026-09-11 09:12:44
---

# WorkBuddy 远程 MCP

## 部署模型

`WorkBuddy -> 企业 HTTPS 网关 -> 127.0.0.1:8010 -> MCP -> 已有后端 API`。

独立 `compose.workbuddy.yml` 不管理业务数据库、对象存储或后端服务。默认单实例单 worker、写工具关闭、UID/GID 10001、只读根文件系统、禁用 capabilities、只读凭据目录及持久化 journal 卷。日志禁用 HTTP access log，仅保留既有脱敏工具审计并轮转。不会继承后端全局管理员 Token。

本模板面向同主机 HTTPS 网关。网关运行在其他主机时不能直接访问 loopback，需另行审核私网入口；不要直接将端口暴露到公网。容器内 `TILESFST_API_BASE_URL` 必须是可达的已有后端地址，不能误填宿主机的 localhost。

## 配置与构建

依据 `workbuddy.env.example` 在仓库外维护部署 env。`WORKBUDDY_BASE_IMAGE` 是经审核的后端镜像 digest，复用其 uv.lock 对应 Python 3.12 依赖；`WORKBUDDY_MCP_IMAGE` 是本次构建目标引用。Dockerfile 的本地默认标签只用于开发验收，不能作为发布证据。构建上下文只允许 `src/mcp/`，不会发送 env、数据卷或业务数据。

在仓库根目录设置 `WORKBUDDY_ENV_FILE` 为私有 env 文件位置后执行：

```bash
docker compose --env-file "$WORKBUDDY_ENV_FILE" -p tilesfst-workbuddy -f deploy/prod/compose.workbuddy.yml config --quiet
docker compose --env-file "$WORKBUDDY_ENV_FILE" -p tilesfst-workbuddy -f deploy/prod/compose.workbuddy.yml build
docker compose --env-file "$WORKBUDDY_ENV_FILE" -p tilesfst-workbuddy -f deploy/prod/compose.workbuddy.yml up -d --no-build --wait
```

部署变量与默认值以 `workbuddy.env.example` 为准；真实镜像发布仍需走项目 image/release 工作流。本手册不代表已经上线。

## 凭据与持久化

`WORKBUDDY_SECRET_DIR` 指向已存在的专用私有目录，其中只有 `workbuddy-credentials.json`；目录 0700、文件 0600，所有者 UID/GID 10001。映射结构、用户后端验真、scope 和撤销策略见 [远程身份与幂等](../../docs/02-deployment.md#workbuddy-远程身份与幂等)。不得挂载包含其他秘密的目录。以目录挂载便于在该目录内原子替换凭据文件；替换后仍保持属主与权限。

健康检查 `/health` 只证明进程存活，不验证映射文件可读性、后端凭据有效期、后端连通性或完整权限。上线前必须用专用凭据完成 initialize、tools/list 和只读工具调用，确认过期/撤销拒绝和账号隔离，再审批写权限。当前是静态 Bearer 映射，不支持 OAuth discovery/授权码流程；客户端若只接受 OAuth，应保留为兼容阻塞。

命名卷持久化同一主机上的幂等账本；不要执行生产 `down --volumes`。镜像更新和回滚保留同一项目名/卷，并先禁用写入、核对 pending/uncertain 记录。不能通过删账本或更换幂等键恢复未知结果。保留期限、备份访问权限、人工恢复责任人需企业确认。未验收跨主机原子 mkdir/rename/fsync 前禁止多副本；本模板不声称分布式幂等。

## 网关与协议

- `/mcp` 是无状态 Streamable HTTP JSON 端点，不创建 session，不提供服务端 SSE；GET/DELETE 返回 405。仅支持通知及客户端响应的无正文 202。
- 初始化协商 2024-11-05、2025-03-26、2025-06-18；不支持的初始化版本返回 2025-06-18。后续 `MCP-Protocol-Version` 缺失默认 2025-03-26，非法版本 400。
- 网关透传 Authorization、Content-Type、Accept、MCP-Protocol-Version，不缓存 POST。请求必须 `Content-Type: application/json` 且 Accept 包含 application/json 与 text/event-stream；不满足返回 415/406。
- 拒绝所有 Origin 请求，适用于原生客户端，不支持浏览器直接连接。不要通过网关剥离 Origin 绕过拒绝策略。无认证 401，权限拒绝 403，配置/身份服务不可用 503，限流 429。
- 网关校验域名和 TLS 证书，限制请求速率与总连接数，禁记 Authorization/请求体/完整查询串。应用不信任 forwarded headers，代理后应用限流按网关地址汇总；用户级限流由企业网关提供，不通过伪造 X-Forwarded-For 绕过。
- 默认整个 JSON 请求体上限 8 MiB，包含 Base64 约 4/3 膨胀；超限 413。网关配置同等或更小限制，后端保持自身媒体限制。当前默认不支持生产大视频上传；提高限制需同时评估容器内存、网关与后端限制。
- 工具可能包含多个串行 API 调用，网关超时需大于工具总耗时而非仅等于单次 API timeout。超时不会撤销已发出的写请求，未知结果按幂等恢复流程核对。

## 可独立复跑

```bash
uv run --project src/backend --with mcp==1.13.1 python -m pytest tests/test_workbuddy_protocol.py -q
docker build --build-arg WORKBUDDY_BASE_IMAGE=tilesfst-tilesfst-backend -f src/mcp/workbuddy/Dockerfile -t tilesfst-workbuddy:local-req0132 .
python deploy/scripts/verify-workbuddy-remote.py
```

第一条使用固定版本官方 SDK 连接真实本机 HTTP，但业务 registry/身份为测试替身。后两条使用本机现有镜像，独立随机 Compose 项目、随机 loopback 端口、空合成凭据映射、不可达后端地址；检查安全配置、拒绝访问和卷重启后去重，结束仅删除本次专属资源，不读取业务 env。

这些证据不证明真实 HTTPS 网关、WorkBuddy 原生远程工具、OAuth、跨主机存储或企业策略已验收。真实环境还需保留脱敏的初始化版本、原生工具调用结果、401/403/撤销、审计关联和 TLS 检查证据。
