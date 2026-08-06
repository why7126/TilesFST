# deployment-image-build Specification

## Purpose
TBD - created by archiving change add-image-build-script-env. Update Purpose after archive.
## Requirements
### Requirement: 镜像构建脚本化入口
系统 SHALL 提供一个位于 `scripts/` 的 shell 脚本，用于从 env 文件读取配置并构建后端与 Web 生产镜像。镜像构建工作流 SHALL 在真实构建前依赖一个已生成且未过期的镜像构建计划，避免直接从本地旧 env 或人工猜测的 tag 执行发布镜像构建。

#### Scenario: 使用默认 env 文件构建镜像
- **WHEN** 操作人员执行镜像构建脚本且默认 env 文件存在
- **THEN** 系统 MUST 读取默认 env 文件中的镜像名、版本 tag、平台和构建参数，并构建后端与 Web 镜像

#### Scenario: 使用指定 env 文件构建镜像
- **WHEN** 操作人员执行镜像构建脚本并传入 env 文件路径
- **THEN** 系统 MUST 使用传入的 env 文件覆盖默认配置来源

#### Scenario: 镜像构建必须基于构建计划
- **WHEN** `/image-build <version>` is executed
- **THEN** the workflow SHALL read `releases/<version>/image-build-plan.json`
- **AND** it SHALL refuse to build release images when the plan is missing, blocked, version-mismatched, or stale
- **AND** it SHALL NOT infer release version, image tag, build args, release dir, or tar name solely from ad-hoc local environment values.

### Requirement: 构建配置示例
系统 SHALL 提供一个可提交的 env 示例文件，说明镜像构建所需变量的用途、默认值含义和安全边界。构建配置示例 MUST 将 `IMAGE_BUILD_TAG` 作为常规发版路径下唯一必须修改的版本号输入，离线交付输出目录与离线镜像包文件名 MUST 可由 `IMAGE_BUILD_TAG` 和 `IMAGE_BUILD_PLATFORM` 默认推导；仅特殊路径或命名场景才需要显式覆盖。

#### Scenario: 复制示例配置
- **WHEN** 操作人员需要准备镜像构建配置
- **THEN** 系统 MUST 提供可复制的 env 示例，且示例不得包含真实密钥、真实客户数据或敏感生产地址

#### Scenario: 常规发版只填写一次构建版本
- **WHEN** 操作人员复制 `scripts/build-images.env.example` 准备常规镜像构建
- **THEN** 示例 MUST 只要求操作人员修改 `IMAGE_BUILD_TAG` 表达版本号
- **AND** `IMAGE_BUILD_RELEASE_DIR` MUST 默认推导为与 `IMAGE_BUILD_TAG` 一致的 release 目录
- **AND** `IMAGE_BUILD_TAR_NAME` MUST 默认推导为包含 `IMAGE_BUILD_TAG` 与 `IMAGE_BUILD_PLATFORM` 的离线包文件名

### Requirement: 镜像验证与离线包导出
镜像构建脚本 SHALL 在构建后执行基础验证，并 SHALL 支持按 env 配置导出 gzip 离线镜像包与 sha256 校验文件。镜像构建工作流 SHALL 在成功构建后生成镜像 manifest，用于发布确认阶段校验产物与输入快照的一致性。

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
- **AND** the manifest SHALL record enough evidence for release publish to detect stale images after Dockerfile, build script, schema, migration, Compose, or release input changes.

#### Scenario: 发布前校验离线包 checksum 一致性
- **WHEN** `/release-publish <version>` or `python scripts/validate-image-build.py validate-manifest --release <version>` validates an image-required release
- **THEN** the workflow MUST verify that the manifest tarball path exists
- **AND** it MUST verify that the tarball `.sha256` sidecar exists
- **AND** it MUST verify that the sidecar sha256 equals the manifest tarball sha256
- **AND** it MUST compute the actual tarball sha256 and verify it equals the manifest tarball sha256
- **AND** it MUST block publish when any of these checks fail.

#### Scenario: 构建环境阻断不伪造成功
- **WHEN** Docker, buildx, network access, base image pull, dependency installation, image validation, tar export, or checksum generation fails
- **THEN** `/image-build` SHALL classify and record the blocker
- **AND** it SHALL NOT write pass evidence or a successful manifest for the failed build.

### Requirement: 镜像构建计划
系统 SHALL 为每个需要镜像治理的产品版本生成镜像构建计划，作为真实构建前的机器可读事实源。

#### Scenario: 生成构建计划
- **WHEN** `/image-prepare <version>` is executed for a release
- **THEN** the workflow SHALL create or update `releases/<version>/image-build-plan.json`
- **AND** the plan SHALL include version, image_required, image_tag, source_scope, build_env summary, input_files, input_hashes, database_impact, required_commands, and blockers
- **AND** the plan SHALL include release, Dockerfile, Compose, image build script, image build env example, Nginx config, schema, and migration inputs when applicable.

#### Scenario: 构建计划脱敏
- **WHEN** `image-build-plan.json` is written or validated
- **THEN** it SHALL NOT contain raw `.env` content, database URLs, passwords, access keys, secret keys, Authorization headers, cookies, local-only sensitive paths, or real customer data.

#### Scenario: 发布输入变更后拒绝旧镜像证据
- **GIVEN** `image-build-plan.json` and `image-manifest.json` were generated for a release
- **WHEN** release stable inputs such as announcement, scope, image tag, Dockerfile, Compose, build script, schema, migration, or database documentation change
- **THEN** manifest validation MUST report input hash drift
- **AND** release publish MUST require rerunning `/image-prepare <version>` and `/image-build <version>` before confirmation.

