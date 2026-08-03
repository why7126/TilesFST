## 背景

当前 `releases/vX.Y.Z/usage-docs/` 已能作为版本化产品使用文档快照，但它同时承担 Mintlify 站点源目录职责时，会让多版本导航、`latest` 指针、截图资产和站点部署边界逐渐混入发布证据目录。REQ-0094 已评审通过，要求新增面向 Mintlify 的站点源目录，并保留 release 快照作为事实源。

## 变更内容

- 新增受治理的 `mintlify/` 文档站源目录，用于承载 Mintlify 配置、多版本站点页面、公告投影和共享截图资产。
- 保留 `releases/vX.Y.Z/usage-docs/` 作为版本产品文档事实源和快照，默认不再直接存放大体积系统截图。
- 扩展 usage docs manifest，记录站点目标路径、截图引用、截图 hash、截图来源、覆盖页面、同步时间和共享复用依据。
- 支持从 release 快照同步或投影到 `mintlify/docs/vX.Y.Z/`、`mintlify/docs/latest/` 和 `mintlify/releases/vX.Y.Z/`。
- 支持 `mintlify/assets/screenshots/` 按内容 hash 集中管理可复用截图资产。
- 支持 Docker Compose 通过 `docs-site` 或等价 profile 启动 Mintlify 文档站服务，并通过 `.env.example` 维护宿主机端口变量。
- 同步目录结构、发布治理、部署文档、环境变量、端口规范、usage docs 技能和校验脚本。

## 能力

### 新增能力

无。该 Change 扩展既有产品发布和部署能力。

### 修改能力

- `product-release-management`：扩展版本化产品使用文档能力，增加 `mintlify/` 站点源目录、release 快照到站点投影、共享截图资产、站点 manifest 和发布门禁。
- `deployment`：扩展 Docker Compose 部署能力，增加可选 Mintlify 文档站服务 profile、端口变量、部署文档和发布镜像门禁要求。

## 影响

- 文档与规则：`AGENTS.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`rules/release.md`、`rules/environment.md`、`rules/port-management.md`、`docs/02-deployment.md`、`releases/README.md`。
- 发布与文档脚本：usage docs 生成、更新、校验脚本；release prepare / publish 校验；目录结构校验。
- Docker / Compose：新增可选 Mintlify 服务 profile、端口变量和部署验证。
- 测试：目录结构、usage docs manifest、站点投影、截图复用、敏感信息扫描、Compose profile 和发布门禁测试。
- 不影响：后端 API、数据库、Web 管理端业务 UI、小程序、Orval。
