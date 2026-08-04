## 实施任务

- [x] 1. 维护命令入口
  - [x] 1.1 设计后端 maintenance CLI / registry，首批覆盖 object key 迁移、品牌证书缩略图回填、SKU pending 主图正式化和二次审计。
  - [x] 1.2 将维护任务接入后端配置、数据库 session、对象存储适配层，移除仅 SQLite 或本地 MinIO 的生产 apply 假设。
  - [x] 1.3 为所有写任务实现 dry-run/apply、limit/batch、幂等 skipped、失败原因统计和重试候选。
  - [x] 1.4 增加脱敏输出，阻止 `.env`、数据库连接串、对象存储密钥、Authorization header、Cookie、本机绝对路径和真实客户敏感数据进入日志或 JSON 摘要。

- [x] 2. Docker 与部署
  - [x] 2.1 明确维护镜像策略，优先新增 `tilesfst-maintenance` service 或等价受控维护入口。
  - [x] 2.2 若复用 backend 镜像，证明不改变 `tilesfst-backend` 在线服务 CMD、端口和健康检查语义。
  - [x] 2.3 更新 `deploy/prod/compose.tencent-cos.yml`、生产 env 示例和必要注释，说明维护作业入口、安全边界和真实 env 禁止提交。
  - [x] 2.4 保留根目录生产 Compose 兼容说明，不把它作为新的唯一生产事实源。

- [x] 3. 备份、回滚与验收摘要
  - [x] 3.1 在维护命令和文档中提示 MySQL 快照与对象存储 bucket/prefix 快照前置条件。
  - [x] 3.2 为 apply 后输出二次审计摘要，覆盖 key、object、URL、thumbnail benefit、render 或 N/A / blocked 原因。
  - [x] 3.3 将 fail / blocked 摘要整理为可支撑 `/bug-capture` 的字段。

- [x] 4. 文档与发布治理同步
  - [x] 4.1 更新 `docs/02-deployment.md`、`deploy/prod/README.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md`。
  - [x] 4.2 更新 `rules/media.md`、`rules/object-storage.md`、`rules/environment.md` 中维护作业、脱敏输出和 env 示例边界。
  - [x] 4.3 若新增维护镜像、Compose service、Dockerfile COPY 或 env 示例，更新 `/image-prepare` 输入追踪或记录不适用理由。

- [x] 5. 测试与校验
  - [x] 5.1 补充后端测试：dry-run 不写、apply 幂等、失败原因统计、脱敏输出扫描、provider fake。
  - [x] 5.2 补充部署校验：Compose config、env 示例安全、生产 SQLite 阻断、维护 service 不泄密。
  - [x] 5.3 运行相关 pytest、目录结构校验、OpenSpec 语言校验和 OpenSpec validate。
  - [x] 5.4 若影响镜像治理，运行或说明 `/image-prepare`、Docker Compose config 与镜像输入 hash 验证。

## 验收任务

- [x] 6. 验收记录
  - [x] 6.1 记录 Requirement AC-001 至 AC-015 的通过、失败、blocked 或 N/A 结果。
  - [x] 6.2 回填 REQ-0097 acceptance 的生产维护作业证据入口或受控验证摘要。
  - [x] 6.3 若生产真实执行不在本 Sprint 发生，明确记录 release-gate / external evidence 状态，避免普通未勾项误读。

## 验收返修记录

- [x] 2026-08-04 20:28:00 `/opsx-modify`：同步 `deploy/scripts/media-maintenance.sh` 作为生产媒体维护作业包装入口，默认 `prod mysql-tencent-cos object-key-audit` 只读审计，保留 `--apply --confirm-backup` 备份门禁，并补充脚本语法与默认安全行为测试。
