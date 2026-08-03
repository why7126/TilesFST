---
req_id: REQ-0081-release-image-build-governance
status: done
created_at: 2026-07-29 10:00:08
updated_at: 2026-07-29 18:35:04
recorded_by: product
source: 发布流程探索
priority_hint: P1
parent_requirement:
---

# 一句话

建立发布镜像准备与构建治理，明确 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build`、`/release-publish` 的依赖关系、门禁和产物，避免数据库、Dockerfile、Compose 或构建脚本变更后下次镜像仍沿用旧脚本或旧配置。

# 原始描述

发布时，如果涉及镜像重构修改，例如数据库变更、Dockerfile 变更、Compose 变更、`.env.example` 变更或镜像构建脚本变更，需要解决发布与镜像构建之间的治理问题，避免下次构建镜像时仍使用原来的脚本或配置。

探索中形成的初步方向：

- `/image-prepare` 和 `/image-build` 分成两个命令更合适。
- `/image-prepare` 负责轻量的构建前契约校验：版本、tag、release scope、Dockerfile、Compose、构建 env、数据库 schema / migration、回滚证据等输入一致性。
- `/image-build` 负责真实构建、验证、导出镜像包和 sha256，并生成镜像 manifest。
- 五个命令存在依赖关系：`/release-propose` → `/release-prepare` → `/image-prepare` → `/image-build` → `/release-publish`。
- 镜像相关步骤应作为发布门禁的一部分，但真实构建较重，不应默认塞进 `/release-prepare` 自动执行。

# 待澄清

- [ ] `image_required` 的判定规则：哪些影响范围必须触发 `/image-prepare`，哪些必须进一步触发 `/image-build`。
- [ ] `image-build-plan.json` 与 `image-manifest.json` 的字段结构、存放路径和校验策略。
- [ ] `/release-prepare` 是否只检查 image plan，还是在镜像影响明确时自动调用 `/image-prepare`。
- [ ] `/release-publish` 对镜像 manifest 的强制条件：版本、tag、脚本 hash、Dockerfile hash、schema / migration hash 与当前发布输入如何比对。
- [ ] Docker/网络不可用时，发布流程应如何记录 blocker、是否允许人工提供外部构建证据。

# 探索结论

本需求暂保持为单条 REQ：镜像准备、镜像构建与发布命令依赖属于同一套发布治理能力，后续通过 `/req-explore` 与 `/req-generate` 展开为 PRD、命令边界、门禁和验收标准。
