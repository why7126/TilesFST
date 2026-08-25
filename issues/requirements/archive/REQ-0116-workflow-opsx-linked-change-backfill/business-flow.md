---
requirement_id: REQ-0116-workflow-opsx-linked-change-backfill
created_at: 2026-08-22 14:27:46
updated_at: 2026-08-22 14:27:46
---

# Business Flow

## 1. 当前问题流

```text
/req-opsx 或 /bug-opsx 创建 Change
        |
        v
trace.md openspec_changes[] 已写入
        |
        +--> sprint.yaml changes[] 可能由 Workflow Sync 补齐
        |
        +--> requirement.md / bug.md 仍可能只同步 status
        |
        +--> _registry.yaml related_change 仍可能滞后
        |
        v
人读入口和机器入口出现 linked Change 漂移
        |
        v
后续 /opsx-apply <REQ|BUG-id>、看板推导或评审需反查多个事实源
```

## 2. 目标流程

```text
/req-opsx 或 /bug-opsx 创建或确认 Change
        |
        v
运行 Workflow Sync --event req.opsx|bug.opsx --issue --change --sprint auto
        |
        +--> 同步 Issue trace openspec_changes[] / related_changes
        |
        +--> 同步 requirement.md 或 bug.md linked Change 可读入口
        |
        +--> 同步 _registry.yaml related_change
        |
        +--> 若 Issue 已在 Sprint scope，补齐 sprint.yaml changes[] 与 scope_estimates[].change
        |
        v
运行 focused check / dry-run
        |
        +--> 通过：后续可使用 /opsx-apply <REQ|BUG-id>
        |
        +--> 失败：报告缺失入口、字段和值，修复后重跑
```

## 3. 范围边界

| 文档 / 脚本 | 职责 |
|---|---|
| `trace.md` | Issue linked Change 的机器事实源，维护 `openspec_changes[]` 和生命周期状态。 |
| `requirement.md` / `bug.md` | 人类入口主文档，展示当前 linked Change 或明确引用 trace。 |
| `_registry.yaml` | 当前态 registry，维护 `related_change` 便于索引和看板推导。 |
| `sprint.yaml` | Sprint 机器事实源，维护正式 `changes[]` 与 `scope_estimates[].change`。 |
| `sync-workflow-status.py` | linked Change 自动回填、幂等检查与摘要输出的主要入口。 |
| `/req-opsx` / `/bug-opsx` | 创建或确认 Change，并调用 Workflow Sync；不应手工分散维护所有派生字段。 |

## 4. 与相关需求差异

与 `REQ-0089-workflow-subdocument-status-sync` 的区别：

- `REQ-0089` 关注 REQ/BUG 子文档状态、验收结果和 residual 状态同步。
- `REQ-0116` 关注 `req.opsx` / `bug.opsx` 后 linked Change 在 trace、主文档、registry 和 Sprint scope 间的一致性。

与 Sprint scope 相关治理的区别：

- Sprint scope 治理关注 `sprint.yaml` 与 `sprint.md` 四件套一致。
- 本需求关注 Issue linked Change 是否能在进入 Sprint scope 后继续被多入口追踪。

## 5. 异常与修复流

```text
focused dry-run 发现 linked Change 漂移
        |
        v
报告：Issue、Change、漂移文件、当前值、期望值
        |
        +--> 字段语义清晰：Workflow Sync 自动修复
        |
        +--> 多 Change 选择冲突：报告 blocker，要求人工确认主 linked Change 策略
        |
        +--> 历史 archive 批量漂移：仅输出 dry-run 摘要，不默认批量 apply
        |
        v
重跑 Workflow Sync 与后续 opsx.apply dry-run
```

## 6. 复盘经验吸收

最近 Sprint 复盘显示，Workflow Sync 派生块即使正确，人写说明区、主文档入口和当前态索引仍可能残留中间态或旧路径。REQ-0116 的实现应优先使用 focused summary、字段级检查和幂等修复，避免再次把 linked Change 信息分散到多个不可验证入口。
