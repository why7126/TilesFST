## Why

当前产品发布流程已经能汇总 Sprint、REQ、BUG、Change、公告和常规门禁，但镜像构建仍主要依赖 `scripts/build-images.sh` 与本地 env 人工操作。发布范围一旦涉及数据库 schema、迁移脚本、Dockerfile、Compose、环境变量或构建脚本变化，缺少一层可追踪的镜像构建计划与产物 manifest，容易出现发布通过但下一次镜像仍沿用旧脚本、旧 tag 或旧构建输入的问题。

## What Changes

- 增加发布镜像治理门禁：发布准备需要判断 `image_required`，并在需要时引用镜像准备和构建证据。
- 定义 `/image-prepare <version>`：轻量校验 release、版本/tag、Dockerfile、Compose、构建脚本、构建 env、schema/migration 等输入，并生成 `image-build-plan.json`。
- 定义 `/image-build <version>`：基于已通过的 image build plan 复用现有构建脚本，完成镜像构建、验证、离线包导出和 `image-manifest.json` 生成。
- 定义 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build`、`/release-publish` 的门禁依赖。
- 扩展发布对象、镜像构建、部署和工作流命令治理 spec，明确敏感信息排除、hash 漂移阻断、外部构建证据边界和 AI usage hook 要求。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `product-release-management`: 发布对象与发布门禁需要纳入镜像准备、镜像构建和 manifest 一致性证据。
- `deployment-image-build`: 镜像构建能力需要拆分构建前计划与真实构建产物，新增 image build plan 与 manifest 契约。
- `deployment`: 生产部署与镜像交付需要校验镜像 tag、Compose、Dockerfile、schema/migration 等输入与发布版本一致。
- `agent-workflow-tooling`: 工作流命令族需要新增 `/image-prepare`、`/image-build` 的职责边界、依赖关系、紧凑输出和 AI usage hook。

## Impact

- 影响文件：`.agents/skills/image-prepare/SKILL.md`、`.agents/skills/image-build/SKILL.md`、`.agents/skills/release-prepare/SKILL.md`、`.agents/skills/release-publish/SKILL.md`、`rules/release.md`、`docs/08-production-image-release.md`、`releases/templates/release.json`、`scripts/validate-release.py`、新增或扩展镜像计划/manifest 校验脚本。
- 可能影响：`scripts/build-images.sh`、`scripts/build-images.env.example`、`docker-compose.prod.yml`、`docker-compose.prod.external.yml`、`.env.example`、数据库 schema / migration 校验脚本。
- 不直接影响业务 API、数据库运行模型、Web UI、小程序或管理端业务页面。
- 不需要 Orval；若实现阶段修改 API 或生成物校验逻辑，需另行说明。
- 需要补充命令级测试、发布 validator 测试、镜像 plan/manifest 安全扫描测试，以及 Docker/Compose 配置静态校验。
