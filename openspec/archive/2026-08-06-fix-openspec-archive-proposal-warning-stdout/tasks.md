---
change_id: fix-openspec-archive-proposal-warning-stdout
status: applied
created_at: 2026-08-06 13:45:35
updated_at: 2026-08-06 13:55:08
---

# 任务

- [x] 1. 复核 `scripts/archive-change.sh` 当前 stdout/stderr 捕获与输出路径，定位 proposal scaffold warning 透传点。
- [x] 2. 实现已知 proposal scaffold warning 块的精确吸收逻辑，覆盖 stdout 与既有 stderr 兼容路径。
- [x] 3. 保留未知 stdout/stderr 与失败路径诊断，确保 OpenSpec CLI 非零退出仍返回失败。
- [x] 4. 补充或更新脚本级回归测试，覆盖 AC-001 至 AC-005。
- [x] 5. 运行 `python scripts/validate-openspec-language.py`、相关 pytest 与目录结构校验。
- [x] 6. 复核是否需要更新长期文档；若无需更新，在归档验收中记录不适用原因。
- [x] 7. 如该问题修复经验可复用，评估是否沉淀到 `docs/knowledge-base/incidents/`。
