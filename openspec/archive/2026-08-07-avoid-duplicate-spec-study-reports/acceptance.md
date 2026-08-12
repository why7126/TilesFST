---
created_at: 2026-08-07 11:22:49
updated_at: 2026-08-07 11:54:47
change_id: avoid-duplicate-spec-study-reports
acceptance_status: passed
---

# 验收记录

## 验收要点

- [x] `/spec-study` 明确同一次学习应用流程只生成一份 `YYYYMMDDhhmmss-study-xxx.md`。
- [x] `/spec-study` 明确不得额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`。
- [x] `/spec-study` 学习报告明确禁止本机绝对路径，并要求使用仓库相对路径或脱敏占位符。
- [x] 学习阶段候选内容不得另起第二份正式 study 报告。
- [x] 同一流程已有 study 报告时，后续补充必须更新同一文件。
- [x] 治理校验通过。
