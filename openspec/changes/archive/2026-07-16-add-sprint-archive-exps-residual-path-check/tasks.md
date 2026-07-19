## 1. 残留检查脚本

- [x] 1.1 新增 `scripts/check-archived-path-residuals.py` 或等价模块，支持 `--sprint <sprint-id>`、`--json` 与摘要输出。
- [x] 1.2 复用或抽取 Sprint/Change 路径解析 helper，解析 `iterations/change|archive/<sprint-id>/` 与 `openspec/changes/archive/<date>-<change-id>/`。
- [x] 1.3 以 `sprint.yaml` 的 `requirements[]`、`bugs[]`、`changes[]` 定位检查范围，默认排除生成物、构建产物、无关历史归档和依赖目录。
- [x] 1.4 报告每条残留的类型、文件路径、行号、旧路径、建议新路径，并在无残留时输出检查文件数和命中数摘要。

## 2. Sprint archive 集成

- [x] 2.1 更新 `.agents/skills/sprint-archive/SKILL.md`，在 close/sync/promote 后加入路径残留检查步骤。
- [x] 2.2 在 `/sprint-archive` 成功报告中加入 residual path check 摘要，发现残留时不得静默输出闭环成功。
- [x] 2.3 确保检查失败时给出可执行重试命令和修复建议，不手工编辑 workflow-sync marker blocks。

## 3. Sprint exps / Fact Sheet 集成

- [x] 3.1 更新 `.agents/skills/sprint-exps/SKILL.md`，在 Fact Sheet 后、写入复盘前运行路径残留检查。
- [x] 3.2 扩展 `scripts/generate-sprint-fact-sheet.py` 或复盘输入处理，将 residual path warning 暴露为 warnings / evidence_hints。
- [x] 3.3 确保复盘文档不把旧路径作为新的证据链接写入，并在 Experience Analysis Report 中展示残留风险。

## 4. 测试与验证

- [x] 4.1 增加脚本单元测试，覆盖无残留、Sprint `change/` 路径残留、active Change 路径残留、归档 Change 日期路径解析。
- [x] 4.2 增加命令级或脚本级回归测试，验证检查范围只来自 Sprint scope，避免扫描无关 archive 和 generated 文件。
- [x] 4.3 运行 `openspec validate add-sprint-archive-exps-residual-path-check --strict`。
- [x] 4.4 运行相关 pytest 或脚本校验，至少覆盖新增残留检查脚本与 Fact Sheet 集成。
