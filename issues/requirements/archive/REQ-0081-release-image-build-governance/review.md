---
review_id: REV-REQ-0081-001
date: 2026-07-29
participants:
  - product
result: approved
created_at: 2026-07-29 15:16:34
updated_at: 2026-07-29 15:16:34
---

# REQ-0081 需求评审

## 评审结论

评审通过。REQ-0081 聚焦发布镜像准备与构建治理，范围清晰，明确拆分 `/image-prepare` 与 `/image-build`，并将镜像计划、镜像 manifest、版本/tag/hash 一致性、数据库变更输入和发布门禁纳入统一发布链路。

该需求不涉及 Web 管理端、店主 Web、小程序 UI 或业务 API 直接变更；后续应通过 OpenSpec Change 落地命令 Skill、发布规则、镜像计划/manifest schema、校验脚本与文档同步。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类原型或实现策略已决：N/A，本需求为发布/镜像构建命令治理。
- [x] 无与现有 REQ 重复未说明：与 REQ-0026 为扩展关系，已在 PRD 中说明。

## 条件通过项

- [ ] 后续 `/req-opsx` 生成 OpenSpec Change 时，design.md MUST 明确 `image-build-plan.json` 与 `image-manifest.json` 的最小 schema、敏感信息排除策略和 hash 漂移判定方式。
- [ ] 后续实现必须同步 `rules/release.md`、`docs/08-production-image-release.md`、发布模板与相关命令 Skill。
- [ ] 若实现新增 `/image-*` 命令 Skill，必须补充 AI usage post-command hook 和上下文预算 guardrails。

## 下一步

```text
/req-opsx REQ-0081-release-image-build-governance
```
