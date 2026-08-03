## 上下文

REQ-0088 已建立 `releases/vX.Y.Z/usage-docs/`、manifest、按需生成/跳过决策和发布门禁。REQ-0094 在此基础上要求把“发布事实源”和“文档站源目录”拆开：`releases/` 继续承担审计快照，`mintlify/` 承担站点浏览、多版本导航、`latest` 指针和共享截图资产。

当前目录规范不允许随意新增一级目录，因此新增 `mintlify/` 必须随 OpenSpec Change 同步目录边界、部署规则和校验脚本。该 Change 同时涉及 Docker Compose，可选启动 Mintlify 文档站服务，必须遵守端口和环境变量治理。

## 目标 / 非目标

**目标：**

- 定义 `mintlify/` 为公开文档站源目录，支持 `mintlify/docs/vX.Y.Z/`、`mintlify/docs/latest/`、`mintlify/releases/vX.Y.Z/` 和 `mintlify/assets/screenshots/`。
- 让 `releases/vX.Y.Z/usage-docs/` 继续作为全量文档快照和 manifest 事实源。
- 通过 manifest 追踪页面、截图引用、hash、来源、覆盖、站点目标路径和同步状态。
- 支持跨版本按内容 hash 复用系统截图，同时避免版本语义失真。
- 通过 Docker Compose 可选 profile 启动 Mintlify 文档站服务。
- 更新规则、文档、技能、脚本和测试，确保目录、发布、安全、部署门禁一致。

**非目标：**

- 不实现真实 Mintlify 账号、DNS、Cloudflare、Vercel 或生产外部托管配置。
- 不删除既有 `releases/vX.Y.Z/usage-docs/` 快照。
- 不把 `mintlify/` 作为 release 的唯一事实源。
- 不新增后端 API、数据库表、Web 管理端入口或小程序入口。
- 不让默认 `docker compose up` 无条件启动 Mintlify 服务。

## 决策

### D1：`releases/` 保持事实源，`mintlify/` 作为站点投影源

`releases/vX.Y.Z/usage-docs/` 保留全量 MDX 和 manifest，便于发布审计与历史回溯。`mintlify/docs/vX.Y.Z/` 从 release 快照同步或投影生成，适配 Mintlify 路径、导航和站点资产。

备选方案是把所有 usage docs 迁出 `releases/`，但这会削弱发布证据链；或者继续只使用 `releases/mint.json`，但多版本站点结构会越来越别扭。

### D2：截图集中到 `mintlify/assets/screenshots/`

release manifest 记录截图引用、hash、来源和覆盖页面，截图文件默认集中到 `mintlify/assets/screenshots/`，按内容 hash 去重。跨版本复用截图必须记录 `first_used_in`、`used_by_versions` 和 `reuse_reason`。

这样可以减少 release 目录大体积资产膨胀，同时保留可验证引用。风险是共享截图误用于不适合的版本，因此 validator 必须检查复用依据。

### D3：Mintlify Compose 服务使用可选 profile

新增 Compose 服务必须通过 `docs-site` 或等价 profile 启动。默认 `docker compose up` 仍只服务业务系统，避免文档站成为 backend / web / minio 的运行前置条件。

宿主机端口使用 `.env.example` 变量，例如 `HOST_PORT_MINTLIFY_DOCS`；新增服务、端口、volume、environment 和 command 必须有邻近注释。

### D4：发布门禁显式区分外部托管与 Compose 内服务

生产可选择外部 Mintlify、静态托管、反向代理或 Compose 内文档站服务。未确认时 `/release-prepare` 记录 blocker 或待确认项。若 Compose / Dockerfile / 文档站服务进入发布范围，必须触发 Docker Compose 验证，并按发布规范评估 `/image-prepare` 与 `/image-build` 证据。

## 风险 / 权衡

- `mintlify/` 新增一级目录扩大目录边界 → 必须更新 `rules/directory-structure.md`、AGENTS 和目录校验脚本。
- 共享截图节省体积但可能误导历史版本 → manifest 必须记录复用依据，validator 对语义变化缺证据时阻断或告警。
- Docker Compose 文档站服务可能引入端口冲突 → 遵守宿主机端口可变策略，使用 `.env.example` 变量。
- 真实 Mintlify CLI / 镜像依赖可能需要网络 → 实现阶段应区分本地 preview、静态校验和外部托管证据，网络不可用时记录 blocker 或替代校验。

## 迁移计划

1. 更新目录和发布规则，允许 `mintlify/` 并明确提交边界。
2. 新增 `mintlify/` 基础结构和站点 manifest / `mint.json`。
3. 将已有 release usage docs 以受控方式投影到 `mintlify/docs/<version>/`，截图迁移到共享资产目录。
4. 扩展 usage docs 生成、更新、校验脚本和 release gate。
5. 增加 Docker Compose `docs-site` profile、端口变量和部署说明。
6. 补充测试和校验命令。

回滚策略：保留 `releases/vX.Y.Z/usage-docs/` 事实源不变；若 `mintlify/` 投影或 Compose 服务失败，可禁用 `docs-site` profile 并继续使用 release 快照与外部托管证据。

## 冲突处理

本 REQ 无 UI prototype。验收优先级为 `acceptance.md`、`requirement.md`、既有 specs 和规则文档。与 REQ-0088 可能冲突的“截图必须位于 release usage docs 目录”要求，由本 Change 通过 MODIFIED spec 调整为“release manifest 记录截图引用，截图资产可位于 `mintlify/assets/screenshots/`”。
