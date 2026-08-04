## 背景与动机

生产部署已经进入 `deploy/prod/compose.tencent-cos.yml` + 外部 MySQL + 腾讯云 COS 的部署矩阵治理阶段，但媒体历史维护任务仍缺少正式的生产执行入口。现有脚本分散在仓库根目录 `scripts/`，生产后端镜像默认只复制 `src/backend/app/`，且部分脚本仍带有 SQLite 或本地 MinIO 假设，不能直接安全 apply 到生产 MySQL + COS。

本变更为 REQ-0097 创建受控的生产媒体维护作业能力，确保对象 Key 迁移、缩略图回填、SKU pending 主图正式化和二次审计可以通过 Docker Compose 一次性容器执行，并具备 dry-run/apply、分批、幂等、备份回滚、脱敏输出和媒体四联/五联验收摘要。

## 变更内容

- 新增生产媒体维护作业能力，定义 Compose 执行入口、镜像策略、命令形态和安全门禁。
- 修改部署规范，要求生产部署矩阵支持受控 maintenance service 或 backend 受控命令入口，并明确根目录生产 Compose 仅作为兼容入口。
- 修改对象存储规范，要求历史媒体维护脚本支持生产 MySQL、腾讯云 COS / S3 兼容 provider、dry-run/apply、分批幂等和脱敏输出。
- 修改媒体五联 / 四联验收规范，要求历史媒体维护作业输出 key、object、URL、thumbnail benefit、render 或 N/A / blocked 摘要。
- 修改镜像构建治理规范，要求新增维护镜像、Dockerfile COPY、Compose service 或部署 env 示例时纳入 image plan / manifest 输入追踪。
- 不直接执行生产维护任务，不写真实生产 `.env`、备份、对象导出或客户数据。

## 能力范围

### 新增能力

- `prod-media-maintenance-jobs`: 生产 Docker Compose 环境下的媒体历史维护作业入口、执行门禁、备份回滚和审计输出。

### 修改能力

- `deployment`: 增加生产维护作业 Compose/service/env 安全边界。
- `object-storage`: 增加历史对象迁移、缩略图回填和审计脚本的生产 provider 适配要求。
- `media-acceptance-template`: 增加维护作业对媒体四联/五联验收摘要的输出要求。
- `deployment-image-build`: 增加 maintenance 镜像、Compose service 和部署输入的镜像治理要求。

## 影响范围

```yaml
impact:
  backend: true
  web: false
  miniapp: false
  admin: false
  database: false
  storage: true
  api: false
  deployment: true
  tests: true
```

- 后端：需要提供受控维护命令入口或 maintenance package，复用配置、数据库 session 与对象存储适配层。
- 部署：可能新增 `tilesfst-maintenance` service、维护命令示例和 deploy env 示例说明。
- 对象存储：历史对象 copy/remove/put/stat 必须适配腾讯云 COS、MinIO 和 S3 兼容 provider。
- 镜像治理：维护镜像或 Dockerfile 输入变更必须进入 image plan / manifest。
- 测试：需要覆盖 dry-run 不写、apply 幂等、脱敏输出、provider fake 和 Compose config。
