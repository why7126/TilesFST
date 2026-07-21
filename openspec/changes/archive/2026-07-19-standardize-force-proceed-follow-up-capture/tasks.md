## 1. 技能入口约束

- [x] 1.1 定位 `.agents/skills/**/SKILL.md` 中涉及 `force-proceed`、follow-up、自动 capture 或后续 Issue 的命令入口。
- [x] 1.2 为相关技能补充统一门禁：`force-proceed` 默认不得自动创建 follow-up REQ/BUG。
- [x] 1.3 明确只有用户当前命令显式授权时，才可调用 `/req-capture`、`/bug-capture` 或 `/capture` 落盘。

## 2. 标准 Capture 文案

- [x] 2.1 在相关技能中定义 follow-up capture 文案最低字段：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令。
- [x] 2.2 确保未落盘 follow-up 输出明确包含“未自动创建 Issue”提示。
- [x] 2.3 为多个 follow-up 事项定义逐条输出规则，保证每条都能独立用于后续 capture。

## 3. 校验与测试

- [x] 3.1 补充或更新脚本校验，检查相关技能是否保留 force-proceed follow-up 门禁与标准文案字段。
- [x] 3.2 补充测试或示例 fixture，覆盖未授权 `force-proceed` 不创建 Issue 的路径。
- [x] 3.3 补充测试或示例 fixture，覆盖显式授权自动 capture 时必须运行对应 Workflow Sync 的路径。

## 4. 验证

- [x] 4.1 运行 OpenSpec 校验，确认 delta spec 格式和场景可解析。
- [x] 4.2 运行相关 Python 或脚本测试。
- [x] 4.3 复核 git diff，确认未修改业务 API、数据库、Web、小程序或生成物。

## 归档验证摘要

- 归档时间：2026-07-19 17:23:45
- 归档路径：`openspec/changes/archive/2026-07-19-standardize-force-proceed-follow-up-capture/`
- 验证命令与结果：
  - `openspec archive "standardize-force-proceed-follow-up-capture" -y`：成功，`agent-workflow-tooling` 新增 2 条 Requirement。
  - `python scripts/sync-workflow-status.py --event opsx.archive --change standardize-force-proceed-follow-up-capture --sprint auto`：成功，Sprint scope skipped，Updated 0，Errors 0。
  - `python scripts/promote-issues-for-archive.py --change standardize-force-proceed-follow-up-capture --reason "/opsx-archive standardize-force-proceed-follow-up-capture"`：成功，无 eligible Issue。
  - `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.archive --change standardize-force-proceed-follow-up-capture --json`：成功，`usage_mode: actual`，`warning_count: 0`。
  - `openspec validate --specs --strict`：成功，32 passed，0 failed。
- 验收结论：归档完成；正式规格 `openspec/specs/agent-workflow-tooling/spec.md` 已包含 `Force-proceed follow-up Issue 默认不自动落盘` 与 `Follow-up capture 文案标准化`。
- 关联 Issue / Sprint 状态：无关联 REQ/BUG；无 Sprint scope。
