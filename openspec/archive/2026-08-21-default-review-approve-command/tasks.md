---
change_id: default-review-approve-command
status: implemented
created_at: 2026-08-21 13:45:41
updated_at: 2026-08-21 13:52:00
---

# 任务清单

- [x] 更新 `/req-review` 与 `/bug-review` Skill，明确无 flag 默认 `approve`，反向结果必须显式 flag。
- [x] 同步 `AGENTS.md`、`rules/requirement-management.md`、`rules/bug-management.md`、`rules/issues-lifecycle.md` 中的正向评审命令示例。
- [x] 同步相关 Skill 的 Next、推荐顺序和最终输出示例，避免继续提示 `--approve`。
- [x] 更新 OpenSpec delta spec 与 Change trace。
- [x] 写入 `docs/spec-logs/` 治理日志并维护 `CHANGELOG.md`。
- [x] 运行治理校验、OpenSpec 校验和聚焦文档表达卫生校验。
