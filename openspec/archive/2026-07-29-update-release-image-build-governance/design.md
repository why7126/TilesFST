## Context

项目已有三段式产品发布命令族和脚本化镜像构建入口。`/release-prepare` 当前关注 OpenSpec、测试、Orval、Docker Compose、数据库、env、产品版本和公告安全；`scripts/build-images.sh` 关注实际镜像构建、镜像基础验证和离线 tar 导出。两者之间缺少稳定的“构建输入计划”和“构建产物 manifest”事实源。

REQ-0081 要解决的是发布证据与镜像交付证据脱节：当数据库、Dockerfile、Compose、构建脚本或 env 示例变化后，发布流程必须能判断是否需要镜像、镜像构建使用了哪些输入、这些输入是否在发布前发生漂移。

## Goals / Non-Goals

**Goals:**

- 将镜像准备和镜像构建纳入发布门禁。
- 拆分 `/image-prepare` 与 `/image-build`：前者轻量校验和生成计划，后者执行重构建和产物导出。
- 让 `release.json`、`image-build-plan.json`、`image-manifest.json` 形成可追踪链路。
- 对版本/tag/input hash 漂移、manifest 缺失和敏感信息泄露建立阻断规则。
- 复用现有 `scripts/build-images.sh`、Dockerfile、Compose 与发布目录，不引入新的顶层目录。

**Non-Goals:**

- 不实现 CI/CD 自动发布流水线。
- 不自动推送远程镜像仓库。
- 不改变 `PRODUCT_VERSION` 作为用户可见产品版本号事实源。
- 不新增后端业务 API、数据库业务表或 Web/小程序 UI。
- 不把真实 `.env`、数据库连接串、密钥或不可公开运维地址写入发布或镜像产物。

## Decisions

### D1. `/image-prepare` 与 `/image-build` 分离

`/image-prepare` 只做轻量、可频繁执行的构建前契约检查，输出 `releases/<version>/image-build-plan.json`。它可以在 Docker 不可用时完成大部分静态校验，并把缺少 Docker、缺少 env 或版本不一致记录为 blocker。

`/image-build` 是重命令，读取有效 plan 后再执行真实构建。它不得自行猜测版本、tag、build args 或输出目录，避免再次引入“本地旧 env 覆盖发布事实”的风险。

### D2. release gates 引用镜像证据而不吞并真实构建

`/release-prepare` 负责判断 `image_required` 和镜像门禁状态，必要时要求 `/image-prepare` 通过，但不默认自动执行真实 `/image-build`。真实构建依赖 Docker、buildx、网络和基础镜像源，适合独立命令承载。`/release-publish` 在 `image_required=true` 或发布目标包含离线镜像包时，必须校验 manifest 或受控外部构建证据。

### D3. 输入 hash 是过期判定的核心

`image-build-plan.json` 记录 Dockerfile、Compose、构建脚本、构建 env 示例、Nginx 配置、schema、migration、release.json 等输入文件 hash。`image-manifest.json` 继承并确认这些 hash。发布确认阶段重新计算当前输入 hash；若 manifest 生成后输入漂移，则镜像证据失效。

### D4. 构建 env 摘要必须脱敏

image plan 可以记录构建 env 文件路径和非敏感变量摘要，例如 image tag、platform、镜像仓库名、是否导出 tar。不得记录真实 `.env` 内容、数据库连接串、密钥、Authorization header、Cookie 或真实客户数据。安全扫描应覆盖 release、plan、manifest 和公告。

### D5. 外部构建证据可存在但必须有边界

当本地 Docker/网络不可用或镜像由外部构建系统完成时，发布流程可以接受人工外部构建证据，但必须记录证据来源、版本、image tag、平台、tarball 或镜像 digest、sha256、校验方式、负责人确认和风险说明。外部证据不得绕过公开安全扫描和版本一致性校验。

## Risks / Trade-offs

- 镜像门禁增加发布步骤 → 通过 `/image-prepare` 轻量化，只有需要交付镜像时才执行 `/image-build`。
- input hash 列表过宽会造成频繁重建 → 首版只纳入 release、Dockerfile、Compose、构建脚本、构建 env 示例、Nginx 配置、schema、migration 等稳定输入；实现阶段可用设计说明扩展。
- 外部构建证据质量不一 → 以受控 schema 记录来源、sha256、校验命令和风险，发布确认仍要阻断敏感信息和版本不一致。
- 当前 active change `unify-image-version-env` 已完成但未归档 → 本 Change 需复用其 `TILESFST_IMAGE_TAG` 统一 tag 思路，避免重复定义变量语义。

## Migration Plan

1. 扩展发布模板和 validator，支持 `image_required`、`image_prepare`、`image_build` 及 plan/manifest 引用。
2. 新增 `/image-prepare` Skill 与 plan validator，先覆盖静态输入校验。
3. 新增 `/image-build` Skill 与 manifest validator，复用 `scripts/build-images.sh`。
4. 更新 release prepare/publish Skill，使发布流程消费镜像证据。
5. 更新发布和生产镜像构建文档。
6. 补充测试覆盖 plan/manifest 最小合法 payload、敏感信息扫描、hash 漂移和版本不一致阻断。

## Open Questions

- `image-build-plan.json` 中 `scripts/build-images.env` 缺失时，是允许生成 blocked plan，还是直接阻断不写 plan。
- 首版是否需要支持外部构建 manifest 导入命令，还是只允许手工写入受控证据字段。
- 是否需要把 `image_required` 判定脚本独立为 `scripts/validate-image-build-inputs.py`，供 release 与 image 命令共同调用。
