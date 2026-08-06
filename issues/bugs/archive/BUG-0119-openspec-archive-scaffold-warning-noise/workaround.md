---
bug_id: BUG-0119-openspec-archive-scaffold-warning-noise
title: OpenSpec 归档反复暴露英文脚手架兼容 warning 临时规避
created_at: 2026-08-06 10:27:26
updated_at: 2026-08-06 10:27:26
---

# 临时规避方案

在正式修复前，执行 `/opsx-archive <change-id>` 后需要人工区分该提示是否属于已知非阻塞兼容 warning。

可按以下方式判断：

1. 确认 OpenSpec 归档命令本身成功退出。
2. 确认 `python scripts/validate-openspec-language.py` 通过。
3. 确认 stderr 或最终说明中只有 `proposal.md` 缺少英文 `## Why` / `## What Changes` 相关提示。
4. 若以上条件全部满足，可将该提示视为已知兼容噪音，不需要为了消除它修改 Change 文档标题。

# 风险与限制

- 人工判断容易让验收者误把非阻塞 warning 当作未解决问题。
- 若 stderr 中混入其他未知内容，人工筛选可能遗漏真实风险。
- 该规避不能减少每次归档输出中的重复噪音，也无法替代自动化脚本的稳定过滤。

# 是否可不修

不建议长期不修。

理由：该问题不阻塞归档，但会持续降低 `/opsx-archive` 输出的可信度，并可能诱导操作者违反项目中文语言规范去迎合上游 CLI 英文脚手架提示。
