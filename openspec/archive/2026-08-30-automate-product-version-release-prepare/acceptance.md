---
title: PRODUCT_VERSION 发布准备自动同步验收
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 23:00:41
---

# Acceptance

## 验收标准

- `/release-prepare <version>` 在校验前自动同步 Web 与小程序中存在的 `PRODUCT_VERSION` 源。
- Release metadata 自动记录 product version sync 证据。
- 公告中可由 release metadata 推导的版本状态自动刷新，不需要人工编辑。
- `/release-publish` 不修改版本源。
- `/image-prepare` 在版本源不一致时阻断并要求先运行 `/release-prepare <version>`。

## 验收结果

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 22:41:57
accepted_by: Codex / spec-opt
evidence:
  - "脚本编译：python -m py_compile scripts/validate-release.py scripts/validate-image-build.py 通过。"
  - "聚焦测试：PRODUCT_VERSION 自动同步、image-prepare mismatch blocker、publish mismatch、release-status remediation、image input candidates 共 5 passed。"
  - "v1.2.2 release prepare、publish、status 校验通过。"
  - "v1.2.2 image plan 与 manifest 校验通过。"
  - "OpenSpec、目录结构、上下文预算、Sprint scope、Workflow Sync 与 AI Usage hook 校验通过。"
pending_items: []
failed_items: []
notes: 纯治理 Change；不修改 API、DB、Web、小程序业务实现、管理端、Orval 或 Docker Compose。
```
