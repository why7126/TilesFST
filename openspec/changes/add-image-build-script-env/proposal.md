## Why

当前生产镜像包构建步骤分散在部署文档中，需要人工复制多段 `docker buildx`、`docker save` 与校验命令，容易出现镜像 tag、平台、输出目录不一致。将镜像构建收敛为 `sh` 脚本 + env 配置，可以降低离线交付和重复构建的操作风险。

## What Changes

- 新增镜像构建脚本入口，支持从 env 文件读取镜像名、版本 tag、平台、builder、输出目录和是否导出离线包。
- 新增镜像构建 env 示例文件，所有可调参数带注释，避免在命令中硬编码交付参数。
- 更新部署文档中的生产镜像构建说明，优先使用脚本化流程，保留手工命令作为排障参考。
- 不引入接口、数据库、权限、上传存储或业务行为变化。

## Capabilities

### New Capabilities

- `deployment-image-build`: 生产镜像构建、验证与离线包导出的脚本化运维能力。

### Modified Capabilities

- 无。

## Impact

- 影响文件：`scripts/` 下新增构建脚本与 env 示例，`docs/02-deployment.md`、`docs/08-production-image-release.md` 同步说明。
- 影响系统：Docker 镜像构建与离线交付流程。
- 不影响 API、数据库、Web 运行时代码、小程序、管理端权限或 Orval 生成物。
