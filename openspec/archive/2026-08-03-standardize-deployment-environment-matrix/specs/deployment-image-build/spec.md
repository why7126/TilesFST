## MODIFIED Requirements

### Requirement: 镜像构建计划

系统 SHALL 为每个需要镜像治理的产品版本生成镜像构建计划，作为真实构建前的机器可读事实源。若发布范围涉及 `deploy/` 目录、部署 Compose、部署脚本或环境化 env 示例，镜像构建计划 MUST 将这些文件作为部署输入纳入 `input_files` 与 `input_hashes`，或记录明确不适用理由。

#### Scenario: 生成构建计划

- **WHEN** `/image-prepare <version>` is executed for a release
- **THEN** the workflow SHALL create or update `releases/<version>/image-build-plan.json`
- **AND** the plan SHALL include version, image_required, image_tag, source_scope, build_env summary, input_files, input_hashes, database_impact, required_commands, and blockers
- **AND** the plan SHALL include release, Dockerfile, Compose, image build script, image build env example, Nginx config, schema, and migration inputs when applicable.

#### Scenario: 部署目录输入纳入构建计划

- **WHEN** `/image-prepare <version>` detects deploy directory, deployment Compose, deployment script, or environment example changes in release scope
- **THEN** the plan SHALL include applicable `deploy/**/*.yml`, `deploy/**/*.env.example`, and `deploy/scripts/*` files
- **AND** the plan SHALL include hashes for those deploy inputs
- **AND** the plan SHALL record a blocker or rationale when legacy root Compose paths and deploy Compose paths conflict.

#### Scenario: 构建计划脱敏

- **WHEN** `image-build-plan.json` is written or validated
- **THEN** it SHALL NOT contain raw `.env` content, database URLs, passwords, access keys, secret keys, Authorization headers, cookies, local-only sensitive paths, or real customer data.

### Requirement: 镜像验证与离线包导出

镜像构建脚本 SHALL 在构建后执行基础验证，并 SHALL 支持按 env 配置导出 gzip 离线镜像包与 sha256 校验文件。镜像构建工作流 SHALL 在成功构建后生成镜像 manifest，用于发布确认阶段校验产物与输入快照的一致性。若构建或发布验证使用 `deploy/` 下 Compose、脚本或 env 示例，manifest MUST 记录这些部署输入。

#### Scenario: 构建后验证镜像

- **WHEN** 后端与 Web 镜像构建完成
- **THEN** 系统 MUST 验证镜像目标平台，并执行后端依赖导入检查与 Web Nginx 配置检查

#### Scenario: 导出离线包

- **WHEN** env 配置启用离线包导出
- **THEN** 系统 MUST 将后端与 Web 镜像导出为一个 gzip 压缩包，并生成对应的 sha256 校验文件

#### Scenario: 生成镜像 manifest

- **WHEN** `/image-build <version>` successfully builds and validates release images
- **THEN** the workflow SHALL create or update `releases/<version>/image-manifest.json`
- **AND** the manifest SHALL include version, image_tag, built_at, platform, backend_image, web_image, tarball, input_hashes, validation, and source_plan
- **AND** the manifest SHALL record enough evidence for release publish to detect stale images after Dockerfile, build script, schema, migration, Compose, deploy directory, deploy script, environment example, or release input changes.

#### Scenario: 部署输入漂移使 manifest 过期

- **WHEN** applicable deploy Compose, deploy script, or deploy env example inputs drift after `image-manifest.json` is generated
- **THEN** release publish SHALL reject the stale manifest or record a blocker
- **AND** it SHALL recommend rerunning `/image-prepare` and `/image-build` when image evidence is required.

#### Scenario: 构建环境阻断不伪造成功

- **WHEN** Docker, buildx, network access, base image pull, dependency installation, image validation, tar export, or checksum generation fails
- **THEN** `/image-build` SHALL classify and record the blocker
- **AND** it SHALL NOT write pass evidence or a successful manifest for the failed build.
