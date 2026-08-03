---
requirement_id: REQ-0089-workflow-subdocument-status-sync
title: REQ/BUG 子文档状态同步与验收结果回填机制 - 业务流程
status: done
created_at: 2026-08-01 09:52:35
updated_at: 2026-08-01 11:46:26
---

# 业务流程

## 1. 当前问题流

```text
req/bug generate
  │
  ├─ 写 requirement.md / bug.md: status=draft
  │
  ▼
review / opsx / sprint / archive
  │
  ├─ Workflow Sync 更新 trace.md、registry、Sprint 派生块
  │
  └─ 子文档状态不一定同步
        │
        ▼
archive 后打开文档
  │
  ├─ trace.md: done / archived
  ├─ requirement.md 或 bug.md: 早期非闭环状态
  └─ acceptance.md: 早期评审状态，验收结果未回填
```

## 2. 目标状态流

```text
状态变化命令
  │
  ├─ req.review / bug.review
  ├─ req.opsx / bug.opsx
  ├─ opsx.apply
  ├─ opsx.archive
  └─ sprint.archive
        │
        ▼
Workflow Sync / shared status sync
  │
  ├─ 更新 trace.md 当前主状态
  ├─ 更新 registry
  ├─ 刷新 Sprint 派生块
  ├─ 同步 requirement.md / bug.md 人类入口状态
  ├─ 回填 acceptance.md 验收结果
  └─ 输出子文档同步摘要
        │
        ▼
Drift check
  │
  ├─ pass → 可继续 review / archive / close
  └─ fail → 输出文件、字段、旧值、建议命令
```

## 3. 历史治理流程

```text
scan archive
  │
  ▼
classify residuals
  │
  ├─ safe-to-sync
  ├─ needs-human-review
  ├─ missing-trace-or-evidence
  └─ acceptance-result-missing
        │
        ▼
dry-run report
        │
        ▼
human confirmation
        │
        ├─ apply safe fixes
        └─ record waiver / leave follow-up
        │
        ▼
check again
```

## 4. 与现有流程差异

| 现有流程 | 目标流程 |
|---|---|
| `trace.md` 是主要同步对象，子文档多为被动 residual 补救。 | `trace.md` 继续做事实源，子文档作为派生读物在状态变化后主动同步。 |
| `acceptance.md` 多数只表达验收标准。 | `acceptance.md` 或等价文档同时能表达验收结论和证据。 |
| archive promote 时才容易发现子文档非闭环状态。 | review/apply/archive/close 均可通过 check 及早发现漂移。 |
| 历史修复容易变成一次性人工批改。 | 历史修复必须 dry-run、分类、确认、apply、复查。 |

## 5. 非 UI 判定

本 REQ 是流程治理需求，不新增管理端列表、表单、弹窗或媒体上传交互；因此不生成 prototype，不写 UI 横切 AC。
