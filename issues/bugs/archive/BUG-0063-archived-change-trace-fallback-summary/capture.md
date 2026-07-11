---
bug_id: BUG-0063-archived-change-trace-fallback-summary
status: archived
created_at: 2026-07-11 13:21:59
updated_at: 2026-07-11 20:13:04
severity_hint: high
environment: local
related_requirement:
related_bug:
---

# 现象

归档后的 OpenSpec Change 可能缺失 `trace.md`，且归档校验没有要求 `proposal.md`、`design.md`、`tasks.md` 至少保留归档验证摘要。缺失 trace 时，归档包无法提供明确的验证结论、测试摘要、关联 Issue/Sprint 状态和归档证据，降低归档可追溯性。

# 复现步骤

1. 准备一个已进入归档流程或已归档到 `openspec/changes/archive/` 的 Change。
2. 删除或缺失该 Change 的 `trace.md`。
3. 确保 `proposal.md`、`design.md`、`tasks.md` 中也没有归档验证摘要，例如测试结果、验收结论、归档时间、关联 Issue/Sprint 状态。
4. 执行归档校验或检查归档包完整性。

# 期望 vs 实际

- 期望：归档校验应检查 archived Change 是否缺失 `trace.md`；若缺失，至少要求 `proposal.md`、`design.md`、`tasks.md` 任一或全部按规则保留归档验证摘要，确保归档证据可追溯。
- 实际：当前归档校验未覆盖该兜底规则，可能接受既没有 `trace.md`、也没有归档验证摘要的 archived Change。

# 附件

- 用户反馈：检查 archived Change 是否缺失 `trace.md`，缺失时要求 `proposal/design/tasks` 至少有归档验证摘要。
