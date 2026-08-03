## MODIFIED Requirements

### Requirement: 发布前校验门禁
发布流程 SHALL 在必填发布就绪检查通过前阻断发布确认；若某项不适用，必须明确标记不适用并说明理由。测试门禁失败时，发布准备流程 SHALL classify failures before reporting blockers so governance drift can be fixed at the right layer. 当发布范围涉及镜像构建、Dockerfile、Compose、构建脚本、构建 env、数据库 schema / migration、API / Orval 构建输入或离线镜像交付时，发布门禁 SHALL 纳入镜像准备和镜像构建证据。

#### Scenario: 测试失败分类
- **WHEN** release preparation runs automated tests and any test fails
- **THEN** the release preparation output SHALL classify representative failures as archived path residual, fixture/schema drift, helper payload invalid, product regression, or environment blocker
- **AND** governance-drift failures SHALL include a concrete remediation such as updating shared test helpers, archived Change path resolution, or fixture schema
- **AND** the release object SHALL NOT mark the tests gate as pass until the focused regression and relevant suite pass.

#### Scenario: 发布准备识别镜像门禁
- **WHEN** release preparation evaluates a release whose impact includes backend runtime, Web build output, Dockerfile, Compose, `.env.example`, image build script, database schema / migration, API / Orval generated client, or offline image delivery
- **THEN** the release object SHALL mark `image_required` as true or record an equivalent image-required decision
- **AND** release preparation SHALL require an `image_prepare` gate to pass or record a blocker before publish can be ready
- **AND** release preparation SHALL NOT mark `image_prepare` as pass without concrete evidence from `releases/<version>/image-build-plan.json` or an equivalent validated plan.

#### Scenario: 发布准备不自动执行真实镜像构建
- **WHEN** release preparation determines that image build is required
- **THEN** it SHALL point to `/image-prepare <version>` and, when delivery requires a built image, `/image-build <version>`
- **AND** it SHALL NOT execute the heavy image build by default unless the user explicitly invokes the image build workflow or an equivalent documented build command.

#### Scenario: 发布确认校验镜像 manifest
- **WHEN** release publish runs for a release with `image_required` true or with offline image delivery in scope
- **THEN** it SHALL require `releases/<version>/image-manifest.json` or approved external build evidence
- **AND** it SHALL verify that manifest version, image tag, source plan, and input hashes match the current release inputs
- **AND** it SHALL block publish when the manifest is missing, stale, version-mismatched, tag-mismatched, or input hashes have drifted.

#### Scenario: 镜像证据公开安全
- **WHEN** release metadata, announcement, image build plan, image manifest, or external build evidence are validated
- **THEN** validation SHALL reject secrets, raw `.env` content, database connection strings, Authorization headers, cookies, MinIO credentials, non-public operational endpoints, or real customer data.
