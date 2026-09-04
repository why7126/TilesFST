---
created_at: 2026-08-31 09:10:00
updated_at: 2026-08-31 09:20:58
---

# 验收记录

## 验收目标

- release-propose 能声明公告、usage docs 和升级路径默认决策。
- release-prepare 能按 release.json 自动生成或校验对应产物。
- release-status 只读，不再把默认准备产物拆成发布主线之外的人工命令。
- release-publish 只写发布确认，不生成主公告、usage docs 或 upgrade plan。

## 验收结果回填

- 发布命令契约已收敛：`release-propose` 声明四类产物决策，`release-prepare` 执行计划产物生成和校验，`release-status` 只读，`release-publish` 仅确认。
- `scripts/validate-release.py` 已支持 `upgrade_plans` 声明来源并将缺失计划的主线修复指向 `/release-prepare <version>`。
- `scripts/validate-usage-docs.py` 已支持 `usage_docs.status=requested`，并将其识别为 prepare 生成动作。
- `scripts/generate-usage-docs.py` 迁移历史 usage docs 时会同步页面截图引用并清理 release-local assets。
- 验证：`python -m py_compile scripts/validate-release.py scripts/validate-release-upgrade.py scripts/generate-usage-docs.py scripts/validate-usage-docs.py` 通过；`uv run pytest tests/test_release_validation.py tests/test_release_upgrade_validation.py` 51 passed；`openspec validate converge-release-prepare-automation` 通过。
