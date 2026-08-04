## 上下文

REQ-0097 已评审通过，需求目标是在生产服务器内通过 Docker Compose 一次性容器安全执行媒体历史维护任务。当前生产推荐入口是 `deploy/prod/compose.tencent-cos.yml`，生产结构化数据使用外部 MySQL，媒体对象使用腾讯云 COS 或等价 S3 兼容对象存储。根目录 `docker-compose.prod.external.yml` 只保留兼容价值。

现有维护脚本包括对象 Key 迁移、品牌证书缩略图回填和 SKU pending 主图正式化等方向，但它们位于根目录 `scripts/`，生产后端镜像默认不包含这些脚本；部分脚本仍偏 SQLite 或本地路径假设。直接在开发机下载生产 `.env` 后运行脚本存在密钥泄露、误连环境和不可审计写操作风险。

## 目标与非目标

目标：

- 提供受控生产维护入口，优先通过 `deploy/prod/compose.tencent-cos.yml` 一次性容器执行。
- 明确维护镜像策略，优先 `tilesfst-maintenance` service / 镜像，备选为 backend 镜像内受控命令。
- 维护任务支持 MySQL、腾讯云 COS / S3 兼容 provider、dry-run/apply、limit/batch、幂等和脱敏输出。
- 维护作业必须输出媒体四联或五联验收摘要，并保留备份、回滚和二次审计路径。
- 部署、Dockerfile、env 示例、镜像构建计划、文档和测试同步进入后续实现任务。

非目标：

- 不执行真实生产维护任务。
- 不新增用户可见 UI，不新增对外 API。
- 不新增视频转码、多清晰度、PDF 首页渲染或 OCR 能力。
- 不自动删除历史媒体对象；清理类动作需要单独审批或后续 Change。
- 不提交真实 `.env`、数据库备份、对象导出、客户数据或生产私有 URL。

## 决策

### D1 生产入口以 deploy/prod 矩阵为主

维护命令以 `deploy/prod/compose.tencent-cos.yml` 为主入口，文档中可说明 `docker-compose.prod.external.yml` 是兼容入口。这样能继承 REQ-0093 的部署矩阵事实源，避免继续把生产能力散落在根目录 Compose。

备选方案是继续只在根目录 `docker-compose.prod.external.yml` 增加维护命令。该方案对历史用户更直接，但会扩大新旧生产入口漂移，因此不作为主路径。

### D2 优先新增 tilesfst-maintenance service

维护作业优先通过专用 `tilesfst-maintenance` service 或镜像执行。该 service 可以复用后端镜像基础层、依赖和配置，但 command 应指向维护 CLI，避免影响在线 `tilesfst-backend` 的启动命令、端口和健康检查。

备选方案是直接在 `tilesfst-backend` 上 `docker compose run --rm tilesfst-backend uv run ...`。该方式实现成本低，但容易把在线服务镜像和一次性维护命令混在一起；若采用，必须证明镜像内有受控命令入口且不改变在线服务语义。

### D3 维护脚本复用后端配置和适配层

维护脚本应进入后端 package 或受控 maintenance package，复用 `app.core.config`、数据库 session、Repository/Service 和 `app.modules.media.storage`。脚本不得直接硬编码 SQLite 路径、本地 MinIO 默认值或 provider-specific SDK 细节。

对象 copy/remove/put/stat 必须通过对象存储适配层或清晰的 provider 分支执行；若某 provider 不支持一致性语义，apply 必须阻断或降级为只读审计。

### D4 所有写任务必须 dry-run/apply 分离

dry-run 是默认安全模式，不写数据库、不写对象存储、不删除对象。apply 必须显式参数触发，并要求执行前已完成 MySQL 快照和对象存储 bucket / prefix 快照。

输出只允许统计、脱敏对象标识、错误码、失败原因和建议动作，不输出 raw `.env`、数据库连接串、access key、secret key、Authorization header、Cookie、本机绝对路径或真实客户敏感数据。

### D5 验收使用媒体四联/五联

维护作业输出必须可转化为媒体四联或五联验收摘要。历史迁移和缩略图回填默认覆盖 key、object、URL、thumbnail benefit、render；不涉及小程序或端侧渲染时必须记录 N/A 或 blocked 原因，而不是删除维度。

## 风险与权衡

| 风险 | 缓解 |
|---|---|
| 维护镜像把脚本纳入生产后扩大镜像输入面 | 纳入 image plan / manifest 输入追踪，Dockerfile COPY 和 Compose service 变更必须进入发布证据。 |
| MySQL 与 SQLite 查询差异导致生产 apply 错误 | 使用 SQLAlchemy session / repository，测试覆盖 MySQL 等价 SQL 或至少 provider fake + SQL 方言边界。 |
| COS 与 MinIO copy/remove 语义不完全一致 | 对 provider 能力做显式检查；不满足时阻断 apply，仅允许 dry-run 或审计。 |
| 输出摘要包含敏感值 | 增加脱敏测试，脚本失败摘要只输出变量名、对象脱敏标识和错误码。 |
| 大批量维护任务运行过久或部分失败 | 支持 limit/batch、幂等 skipped、失败原因统计和重试候选。 |
| 临时挂载 scripts/ 绕过发布治理 | 文档明确只读审计可作为应急；apply 必须来自受控镜像或经后续审批。 |

## 迁移计划

1. 在后端内定义 maintenance 命令入口与任务 registry，首批覆盖 object key 迁移、品牌证书缩略图回填、SKU pending 主图正式化和二次审计。
2. 改造脚本为生产 provider 适配、dry-run/apply 分离、limit/batch、幂等和脱敏输出。
3. 更新 `deploy/prod/compose.tencent-cos.yml`，按决策新增 `tilesfst-maintenance` 或明确 backend 受控命令入口。
4. 同步 `deploy/prod/*.env.example`、`.env.example`、`docs/02-deployment.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md`、`rules/media.md`、`rules/object-storage.md`。
5. 补充 tests 覆盖 dry-run 不写、apply 幂等、敏感输出扫描、provider fake、Compose config 和镜像输入追踪。
6. 生产执行前由运维完成 MySQL 快照和对象存储 bucket / prefix 快照；失败回滚优先恢复快照。

## 待确认

- 首批维护任务是否全部进入同一个 maintenance CLI，还是按任务拆分多个子命令。
- `tilesfst-maintenance` 是否独立镜像 tag，或与 backend 镜像共 tag 但不同 command。
- 生产执行报告的事实源位置：release 证据、运维系统外部证据，或后续新增受控文档入口。
