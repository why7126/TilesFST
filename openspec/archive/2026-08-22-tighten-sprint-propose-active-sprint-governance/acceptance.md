---
created_at: 2026-08-22 14:12:50
updated_at: 2026-08-22 14:12:50
acceptance_status: passed
---

# 验收

- `rules/iterations-lifecycle.md` 明确未指定 Sprint、指定 Sprint、新建 Sprint、容量超限和归档冻结规则。
- `.agents/skills/sprint-propose/SKILL.md` 明确运行 Sprint 选择门禁和失败引导。
- `scripts/validate-sprint-selection.py` 能识别无 active、单 active、多个 active、跳号创建和第三个 active Sprint 场景。
- OpenSpec、目录结构、上下文预算和聚焦测试通过。

## 验收结果回填

- 结果：passed。
- 证据：新增脚本当前仓库检查通过；聚焦 pytest 7 passed；上下文预算、OpenSpec 语言、目录结构和目标 Change 校验通过；文档表达卫生脚本退出码为 0，存在 5 条既有规范句式 warning。
