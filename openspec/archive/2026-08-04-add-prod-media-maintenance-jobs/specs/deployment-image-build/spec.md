## MODIFIED Requirements

### Requirement: 镜像构建计划

系统 SHALL 为每个需要镜像治理的产品版本生成镜像构建计划，作为真实构建前的机器可读事实源。若发布范围涉及 `deploy/` 目录、部署 Compose、部署脚本或环境化 env 示例，镜像构建计划 MUST 将这些文件作为部署输入纳入 `input_files` 与 `input_hashes`，或记录明确不适用理由。若发布范围新增或修改生产媒体维护镜像、maintenance service、Dockerfile COPY、维护命令入口或相关 env 示例，镜像构建计划 MUST 将这些维护作业输入纳入追踪。

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

#### Scenario: 维护作业镜像输入纳入构建计划

- **WHEN** 发布范围新增或修改 `tilesfst-maintenance` service、维护镜像、后端 Dockerfile COPY、维护 CLI 或生产维护 env 示例
- **THEN** image build plan MUST include those files in input_files and input_hashes
- **AND** MUST record whether the maintenance image shares backend image tag or uses a dedicated image tag
- **AND** MUST record blockers when maintenance commands are only available through untracked local bind mounts.
