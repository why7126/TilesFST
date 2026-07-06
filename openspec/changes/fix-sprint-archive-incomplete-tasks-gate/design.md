# Design

## Context

已有 `scripts/workflow_sync/collect.py` 能统计 change 的 task 进度，但它面向同步状态，不适合作为 `/sprint-archive` 前的硬阻断点。归档命令需要一个独立、可直接运行、可在 CI/手工流程中复用的 readiness gate。

## Approach

新增 `scripts/validate-sprint-archive-readiness.py`：

- 解析 `iterations/change/<sprint-id>/sprint.yaml`、`iterations/archive/<sprint-id>/sprint.yaml` 与 legacy `iterations/<sprint-id>/sprint.yaml`。
- 只检查当前 Sprint `changes[]` 范围，避免误扫其他 Sprint。
- 对每个 change 优先检查 active 路径 `openspec/changes/<id>/`，否则检查 archived 路径 `openspec/changes/archive/*-<id>/`。
- 统计 `tasks.md` 中 `- [x]` 与 `- [ ]`。
- 默认将以下情况视为 blocker：
  - change 目录缺失；
  - `tasks.md` 缺失；
  - `tasks.md` 存在未完成项。
- 支持 `--force`：仍报告 blocker，但返回 0，用于团队显式确认的例外流程。
- 支持 `--json`，方便后续自动化集成。

## Command Integration

`/sprint-archive` Step 0.5 必须运行：

```bash
python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>
```

若使用 `--change <change-id>`，对应传递给脚本：

```bash
python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id> --change <change-id>
```

默认非 0 时必须停止归档、停止 Sprint close、停止 issue promote。仅在用户显式 `--force` 并确认每个 blocker 时可继续。

## Alternatives

- 只修改命令文档：不足以防止再次遗漏。
- 把逻辑塞入 workflow sync：sync 发生在归档动作后，不适合作为前置阻断。
- 依赖 `openspec status`：无法覆盖已提前归档但 tasks 未完成的历史状态。
