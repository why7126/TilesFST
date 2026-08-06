---
requirement_id: REQ-0102-sprint-goal-scope-consistency-validation
created_at: 2026-08-06 11:41:39
updated_at: 2026-08-06 11:41:39
---

# Business Flow

## 1. 当前问题流

```text
/sprint-propose 或 Workflow Sync
        |
        v
sprint.yaml 正式 Scope 已包含 REQ/BUG/Change
        |
        v
sprint.md ## 2. Scope 主表与分组表被同步
        |
        v
sprint.md ## 1. 目标编号列表仍可能漏项
        |
        v
validate-sprint-scope.py 只看 Scope 区域
        |
        v
校验通过，但人读目标列表不完整
```

## 2. 目标流程

```text
新增或同步 Sprint Scope
        |
        v
更新 sprint.yaml 机器事实源
        |
        v
刷新 sprint.md Scope 主表与分组表
        |
        v
同步或人工维护 Sprint 目标编号列表
        |
        v
运行增强 validate-sprint-scope.py
        |
        +--> 通过：Sprint 四件套可进入下一步
        |
        +--> 失败：输出缺失编号与位置，修复后重跑
```

## 3. 范围边界

| 文档 / 脚本 | 职责 |
|---|---|
| `sprint.yaml` | Sprint 正式 Scope 的机器事实源。 |
| `sprint.md ## 1. 目标` | 人读目标描述、目标编号列表和对应要点。 |
| `sprint.md ## 2. Scope` | 产品面对齐用 Scope 主表和 Workflow Sync 分组表。 |
| `validate-sprint-scope.py` | 校验机器事实源与人读 Scope / 目标编号列表一致。 |
| `/sprint-propose` | 新建或追加 Sprint Scope 时同步目标编号列表，并在结束前运行校验。 |
| Workflow Sync | 维护派生 Scope 表；目标编号列表维护策略需在实现阶段明确。 |

## 4. 与父 REQ / 相关需求差异

本需求不是业务功能需求，也不属于某个管理端 UI 体验需求的子需求。它来源于 sprint-020 复盘中的流程治理行动项，关注 Sprint 规划文档的一致性和校验闭环。

与 `REQ-0089-workflow-subdocument-status-sync` 的区别：

- `REQ-0089` 关注 REQ/BUG 文档包内状态和验收结果同步。
- `REQ-0102` 关注 Sprint 四件套中目标编号列表与正式 Scope 的一致性。

## 5. 异常与修复流

```text
校验发现目标编号缺失
        |
        v
报告：<编号> missing from sprint.md Sprint target id list
        |
        v
操作者确认该编号是否属于正式 Scope
        |
        +--> 属于：补齐目标编号列表和必要要点段落
        |
        +--> 不属于：修复 sprint.yaml / Scope 事实源
        |
        v
重跑 Workflow Sync 与 validate-sprint-scope.py
```
