---
purpose: WorkBuddy 本地隔离验收运行手册
content: 独立 Compose、真实 stdio 写操作、对象存储和日志证据、持久化与清理边界
source: REQ-0132 / add-workbuddy-custom-connector
created_at: 2026-09-08 08:58:00
updated_at: 2026-09-08 09:12:12
---

# WorkBuddy 隔离验收

## 执行

前提：Docker Compose 可用，本机已有 `tilesfst-tilesfst-backend` 后端依赖镜像及 `minio/minio:latest`。后端依赖镜像应与 `src/backend/uv.lock` 一致；缺少镜像时按项目 Dockerfile 构建，不把业务容器作为测试服务。验收会只读挂载当前后端及 MCP 源码。

在仓库根目录运行：

```bash
python deploy/scripts/verify-workbuddy-local.py
```

脚本创建随机 `wb-req0132-` 前缀 Compose 项目，不接受外部业务 URL，不读取根 `.env`，不发布宿主机端口。后端、MinIO 和验收驱动只在独立 internal 网络通信；SQLite、MinIO、临时目录与幂等账本使用专属命名卷。不会复用 `tilesfst-backend`、已有数据库或对象存储。

应用签名密钥、测试管理员密码和 MinIO 密码在内存中随机生成，通过已有环境变量注入测试容器。MCP 子进程启动前剥离管理员密码与 MinIO 密钥，只持有后端 API Token。脚本不保存凭据、不打印原始 Compose 输出或完整业务响应。测试源代码只读挂载，Python 缓存目录与宿主机隔离；验收驱动只读挂载 SQLite 以核对证据，MCP 子进程自身仍只调用鉴权后端 API。

## 覆盖

- 每次工具调用新建 stdio 子进程，执行 initialize、通知、tools/list、tools/call；不作为 WorkBuddy App 原生证据。
- 通过管理 API 准备一个合成规格；登录与规格创建是前置步骤，不计为 MCP 能力。品牌、类目、SKU 和媒体写入全部经 MCP。
- SKU 创建、编辑、上架、下架；品牌与类目创建、编辑、启用、停用；四类媒体上传。
- 五种只读工具、六种预览工具；预览前后核对业务表计数、SKU 字段/状态与对象列表。
- 确认缺失、输入错误、scope 不足、非法凭据拒绝；后端超限失败后同键禁止重试。
- 并发四个真实 stdio 进程同键创建，数据库只产生一条 SKU；新进程、容器重启后重复键仍不重写。
- MinIO stat 与后端媒体 URL 返回长度一致；重启后数据库、媒体对象和幂等账本仍可用。
- `client_request_id -> request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans` 实际落库核对，扫描测试敏感标记，无伪造 WorkBuddy usage_events。

媒体上限仅在该测试环境设为 1 MiB，测试恰好上限和上限加一字节。原图使用合成 PNG，视频使用 MP4 文件类型头的传输夹具；这证明上传、存储和读取链路，不证明视频播放、转码、所有媒体编码或生产 500 MiB 文件性能。扩展名、MIME、无路径文件名、非空合法 Base64 在 MCP 侧检查，后端继续负责权限、用途和实际大小限制；不宣称已验证文件内容嗅探。

按当前 REQ 的全部真实写操作要求，SKU、媒体、品牌与类目维护均验证 Task Trace。品牌/类目在后端路由增加仅针对连接器来源的观测依赖，沿用服务端鉴权身份和 TaskTraceService，观测失败不覆盖业务结果；不增加后端数据库访问工具。

## 幂等恢复与保留

账本中的 pending/uncertain 不是可安全重试的证明。人工先用 operation_ref、client_request_id、请求日志和业务对象核对结果：已生效则保留原账本并查询现状；无法确认则停止重试。不得直接删除预约、改为 completed 或自动换键。需重新执行时必须先确认原操作未生效并由负责人批准新的业务操作。

本地脚本实际验证超限失败后的同键阻断、重复操作查询恢复及容器重启。没有自动清理期限；正式部署的保留时长、责任人和跨主机共享目录恢复演练仍需企业验收，不能用单机命名卷证明跨主机或断电保证。

正常结束或测试失败都会移除该项目容器和网络，保留专属数据卷以便复核。控制台输出 project 标识，用它精确筛选 `com.docker.compose.project` 标签，仅在证据已确认不再需要后删除这四个测试卷；禁止使用全局 prune。凭据未保存，保留卷用于离线证据核对，不等同于可直接恢复登录的常驻环境；再次运行会创建全新项目。

## 证明边界

这是本地 Docker、SQLite、真实 MinIO 与手动 stdio 协议驱动的集成验收。不是 WorkBuddy 原生远程连接器、HTTPS 网关、企业多用户部署、MySQL、多主机共享存储或线上验收。整体 REQ 仍需这些部署证据及人工验收确认。
