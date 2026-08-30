---
created_at: 2026-08-30 12:45:20
updated_at: 2026-08-30 12:55:22
acceptance_status: passed
---

# 验收

## 验收要点

- 脚本可阻断开发证据冒充生产通过。
- 脚本可阻断 DevTools Network 冒充体验版或真机通过。
- 脚本可阻断生产发布目标中未重新判定的 `production_only_pending`。
- `opsx-archive`、`sprint-archive`、`release-status` 和 `release-publish` 入口已接入或引用该门禁。
- 未修改业务 `src/` 代码。

## 验收结果回填

```yaml
acceptance_status: passed
source_change: enforce-environment-tiered-evidence-gates
accepted_at: 2026-08-30 12:55:22
evidence:
  - "新增 validate-environment-tiered-evidence.py CLI 和 environment_tiered_evidence.py 复用模块。"
  - "validate-archive-evidence.py、validate-sprint-archive-readiness.py 和 validate-release.py 已接入同一门禁。"
  - "opsx-archive、sprint-archive、release-status、release-publish Skill 和规则文档已同步脚本入口。"
  - "聚焦测试覆盖开发证据冒充生产、Network passed 缺 evidence、production_only_pending 生产发布重判。"
failed_items: []
waived_items:
  - "API / DB / Web / 小程序 / 管理端 / Orval / Docker Compose 不适用：本变更只修改治理脚本、规则和命令技能。"
known_unrelated:
  - "tests/test_release_validation.py 全文件存在 3 个 usage-docs screenshot fixture 旧失败，与本门禁无关。"
```
