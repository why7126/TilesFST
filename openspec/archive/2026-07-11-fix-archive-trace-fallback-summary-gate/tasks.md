# Tasks

## 1. Readiness Gate

- [x] 1.1 扩展 `scripts/validate-sprint-archive-readiness.py` 的 Change readiness 数据模型，记录 `trace_exists`、fallback summary 状态、承载文件与缺失项。
- [x] 1.2 为 archived Change 增加 `trace.md` 存在性检查，并在报告中展示状态。
- [x] 1.3 实现 `proposal.md`、`design.md`、`tasks.md` 的 `## 归档验证摘要` 识别与必备信息项校验。
- [x] 1.4 对缺失 `trace.md` 且无完整兜底摘要的 archived Change 输出 blocker 并返回非零退出码。

## 2. Workflow Documentation

- [x] 2.1 更新 `.agents/skills/source-command-opsx-archive/SKILL.md`，明确缺失 `trace.md` 时必须补充标准化归档验证摘要。
- [x] 2.2 更新 `.agents/skills/source-command-sprint-archive/SKILL.md`，明确 readiness gate 覆盖 trace / fallback summary 检查。
- [x] 2.3 在报告或帮助文本中说明 active Change 与 archived Change 的检查语义差异。

## 3. Regression Tests

- [x] 3.1 新增或更新测试：archived Change 存在 `trace.md` 时通过。
- [x] 3.2 新增或更新测试：archived Change 缺失 `trace.md` 但存在完整 fallback summary 时通过并报告承载文件。
- [x] 3.3 新增或更新测试：archived Change 缺失 `trace.md` 且无 fallback summary 时失败并输出 blocker。
- [x] 3.4 新增或更新测试：fallback summary 缺少验证命令、验收结论、Issue/Sprint 状态或归档证据时列出缺失项。

## 4. Validation

- [x] 4.1 运行相关 pytest 或脚本级测试。
- [x] 4.2 运行 `python scripts/validate-sprint-archive-readiness.py --sprint <fixture>` 覆盖通过与失败路径。
- [x] 4.3 运行 `openspec validate fix-archive-trace-fallback-summary-gate --strict`。
- [x] 4.4 评估是否需要将归档证据门禁经验沉淀到 `docs/knowledge-base/incidents/`。

## 实现记录

- `scripts/validate-sprint-archive-readiness.py` 已区分 active / archived Change；archived Change 缺失 `trace.md` 时要求完整 `## 归档验证摘要`。
- 已运行 `uv run pytest tests/test_sprint_archive_readiness.py`。
- 已运行 `openspec validate fix-archive-trace-fallback-summary-gate --strict`。
- 本次经验已沉淀到归档技能说明与脚本测试，暂不新增 incident 文档。
