---
purpose: REQ-0132 本地隔离验收证据
content: 合成数据真实写入、媒体、幂等持久化、日志链路及证明边界
source: opsx.modify / deploy/scripts/verify-workbuddy-local.py
created_at: 2026-09-08 09:04:21
updated_at: 2026-09-08 09:12:12
---

# 本地隔离验收

## 环境与来源

2026-09-08，最终独立 Docker Compose 项目 `wb-req0132-c9bec905`（前一整轮通过项目为 `wb-req0132-714af3e4`）。FastAPI 使用当前后端源码，MCP 使用当前运行时代码，依赖镜像 `tilesfst-tilesfst-backend`，镜像摘要 `sha256:e4523e21227a6bdac28ffd244908396fccceaad4f7891f20236e9ff6f9253193`。SQLite、MinIO、临时文件和幂等账本均使用专属命名卷。internal 网络无宿主机端口，不读取业务 env 或现有业务数据。

执行入口：`python deploy/scripts/verify-workbuddy-local.py`。脚本是独立验收驱动，不是 WorkBuddy App；所有能力调用通过真实 stdio initialize / tools/list / tools/call，后端与存储不使用 TestClient 或 Mock。登录与一个规格创建通过鉴权管理 API 准备，仅为测试前置条件；数据库读取及 MinIO stat 仅由验收驱动执行，未为 MCP 增加直连权限。

## 实际结果

| 验收面 | 结果与证明 |
|---|---|
| 受控写入 | SKU 创建、编辑、上架、下架；品牌/类目创建、编辑、启用、停用全部成功，返回实际业务 ID/状态 |
| 只读与预览 | 五种只读、六种预览成功；预览前后业务记录数、SKU 字段/状态、对象列表不变 |
| 权限和输入 | 无确认、非法参数、缺 scope、非法凭据均拒绝；非法媒体元数据/空 Base64 拒绝前不调用后端 |
| 媒体存储 | SKU 图片、视频、品牌 Logo、品牌证书四类上传，MinIO stat 与后端媒体 URL 返回长度一致 |
| 大小边界 | 测试环境上限 1 MiB：四类目标恰好上限通过，上限加一字节拒绝；非法 MIME 拒绝 |
| 幂等 | 四个 stdio 进程同键并发只有一次真实创建；数据库恰有一条 SKU；新进程重复、异参冲突和后端失败后的同键重试均阻断 |
| 持久化 | 重启后端和 MinIO，并重建验收/MCP 进程后，原键不重复写入，SKU 和媒体仍存在 |
| 日志链路 | 写入/查询阶段 44 条最终调用关联请求、重启阶段 2 条请求落库；每条实际管理写请求均有 Trace 与 spans，Trace 关联服务端 request_id |
| 脱敏 | stderr 和落库日志扫描测试凭据及敏感标记未出现；未伪造 workbuddy_connector usage_events |

写入/查询阶段 671 次断言通过，重启阶段 31 次断言通过，共 702 次断言。断言含重复协议/脱敏检查，不等同于 702 个独立测试用例。脚本正常结束并移除本项目容器与网络，保留四个专属证据卷；现有业务容器未修改。

项目 Python 聚焦回归：`uv run --project src/backend python -m pytest src/backend/tests/test_workbuddy_maintenance_trace.py src/backend/tests/test_admin_brands.py src/backend/tests/test_admin_tile_categories.py tests/test_workbuddy_connector.py tests/test_workbuddy_hardening.py tests/test_workbuddy_acceptance_harness.py -q`，115 passed，4 条既有框架弃用提示。品牌/类目 9 个 OpenAPI 路径与现有 Web OpenAPI 文件结构比较无变化，无需 Orval。最终 MCP 子进程环境剥离测试管理员密码与 MinIO 密钥，仅保留 API Token；专门回归确认这一隔离，最终真实容器复验仍为 671 + 31 次断言通过。

验证收尾：项目 Python Ruff、OpenSpec strict、语言、目录、Agent 上下文预算、Sprint scope、产品数据采集/链路观测门禁及聚焦 diff 空白检查通过。根因脚本退出 0，但因无 linked BUG 自动检查 N/A，根因以本报告代码与实测证据为准。验收驱动测试原先生成 deploy/scripts 字节码目录，已清除自身生成的缓存并调整测试加载方式，目录校验复跑通过。结束时 Docker 容器清单与原有业务容器/端口一致。

## 根因与返修

| 问题 | 根因状态与证据 | 本轮处置 |
|---|---|---|
| 下架目标契约不一致 | confirmed：真实调用 DISABLED 返回 invalid_arguments；MCP schema 仅 PUBLISHED/DRAFT，而后端 unpublish 返回 DISABLED | 新增 DISABLED 正式目标，DRAFT 仅保留旧下架别名；预览显示实际目标，补回归 |
| 无扩展名仍上传成功 | confirmed：早期边界夹具 filename=boundary 的真实上传成功；连接器无扩展名检查 | 添加前置文件名、MIME/扩展名和非空 Base64 校验，预览提示元数据风险；不宣称完成文件内容嗅探 |
| 品牌/类目缺少 Trace | confirmed：隔离 SQLite 查询确认八种维护请求各 1 条 request_log、0 条关联 Trace；路由原先无 TaskTraceService 接入 | 仅对连接器来源增加后端观测依赖；成功、失败、权限与观测降级测试通过；验收脚本强制检查全部管理写请求 |
| 间歇 stdio EOFError | unknown：复跑出现过子进程启动退出；当次未获得足够堆栈证据确认根因 | 串行回归后复跑通过；独立 Python 缓存目录避免读取宿主机字节码，最终整轮通过，不把缓存竞争写成已确认根因 |

初次后端回归命令误用系统 pytest，因系统环境缺 Pillow 收集失败；改用项目 Python 的 `python -m pytest` 后全部通过。该问题属于验收运行环境，不是业务回归。

## 未证明事项

- 本轮不是 WorkBuddy 原生工具面板或 HTTPS 远程调用，不覆盖真实用户确认交互、企业凭据部署及远程协议兼容。
- 单机命名卷不证明跨主机共享目录、断电持久性或多实例部署保证；企业账本保留周期与恢复责任人仍待确认。
- 视频为 MP4 类型头传输夹具，图片为合成 PNG；不证明播放、转码、全部 MIME/编码组合、文件内容嗅探、生产大文件性能或 MySQL 行为。
- 扩展名拒绝证据来自 MCP 前置校验，不冒充后端直连接口的独立扩展名校验覆盖。
- 整体 REQ 保持 pending，不自动归档。运行手册和恢复边界见 `deploy/local/workbuddy-acceptance.md`。

product_data_collection_observability：适用 backend_api、request_logs、task_traces、task_trace_spans、connector_audit、deployment、object_storage_indirect。实际 SQLite 关联和 MinIO 对象已验证；usage_events 为直接 API 入口 N/A，确认未伪造；无 Web/小程序 UI 变化；无数据库 schema 变更。品牌/类目观测仅为原验收目标补齐，不改变业务权限和 HTTP 契约。
