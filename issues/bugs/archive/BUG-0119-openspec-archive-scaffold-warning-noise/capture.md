---
bug_id: BUG-0119-openspec-archive-scaffold-warning-noise
status: done
created_at: 2026-08-06 10:05:19
updated_at: 2026-08-06 12:08:39
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

每次执行 OpenSpec 归档后，最终归档说明都会重复出现固定提示：

```text
说明：归档时 OpenSpec CLI 仍提示 proposal.md 缺少英文 ## Why / ## What Changes，项目封装脚本已标记为非阻塞 warning；项目自己的中文语言校验通过。
```

该提示对应的是上游 OpenSpec CLI 对英文脚手架标题的兼容 warning，而项目规则已明确要求 Change 文档中文优先，且不得为了消除 CLI 提示而添加英文 `## Why` / `## What Changes` 标题。

# 复现步骤

1. 准备一个符合项目中文语言规范、但不包含英文 `## Why` / `## What Changes` 标题的 OpenSpec Change。
2. 执行 `/opsx-archive <change-id>` 或底层 `scripts/archive-change.sh <change-id>`。
3. 确认 `python scripts/validate-openspec-language.py` 通过。
4. 查看归档最终输出。

# 期望 vs 实际

期望：

- 已知的 OpenSpec CLI 英文脚手架兼容 warning 由项目归档封装层吸收。
- 当该 warning 是唯一 stderr 且项目中文语言校验通过时，最终归档结论不再重复提示该固定说明。
- 真实归档错误、其他 stderr、目录结构错误或中文语言校验失败仍然正常暴露或阻断。

实际：

- 归档本身成功，中文语言校验也通过。
- 最终归档说明仍每次重复暴露同一段非阻塞 warning，容易让验收者误以为归档存在未解决问题。

# 附件

- 相关脚本：`scripts/archive-change.sh`
- 相关规则：`rules/language.md`
- 相关技能：`.agents/skills/opsx-archive/SKILL.md`
- 来源命令：`/opsx-explore`
