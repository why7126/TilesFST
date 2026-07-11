---
requirement_id: REQ-0033-acceptance-report-summary-ac-reference
title: acceptance-report 拆分最终验收摘要与原始 AC 引用 - 业务流程
status: archived
created_at: 2026-07-11 16:03:39
updated_at: 2026-07-11 20:13:04
---

# 业务流程

## 1. 当前问题流程

```text
Sprint apply / opsx archive
        |
        v
Change tasks 与 archive 状态陆续完成
        |
        v
/sprint-archive readiness gate 通过
        |
        v
acceptance-report.md 写入最终归档检查
        |
        v
同一正文继续保留大量原始 AC `- [ ]`
        |
        v
读者误判：未勾选 AC = Sprint 未完成？
```

## 2. 目标流程

```text
Sprint apply / opsx archive
        |
        v
/sprint-archive readiness gate
        |
        +-- FAIL --> 阻断归档，记录阻断项
        |
        +-- PASS --> 更新最终验收摘要
                      |
                      v
              写入最终归档检查
                      |
                      v
              原始 AC 作为引用/追溯区
                      |
                      v
              人工 sign-off 单独记录
```

## 3. 文档结构流

```text
acceptance-report.md
├── 验收概况
├── 最终验收摘要
│   ├── 验收结论
│   ├── readiness gate
│   ├── Change archived / applied / proposed
│   ├── tasks 完成计数
│   └── Sprint status / lifecycle_stage
├── 人工 sign-off 记录
│   ├── 验收人
│   ├── 验收完成时间
│   └── 遗留复核项
└── 原始 AC 引用
    ├── REQ/BUG 来源 acceptance.md
    ├── issue / Change 状态摘要
    └── 必要 AC 摘录或链接
```

## 4. 与父 REQ 差异

本需求无直接父 REQ。它属于 Sprint 文档治理和 Workflow Sync 质量改进，不新增业务模块，也不改变 REQ/BUG 原始 `acceptance.md` 的写法。

## 5. 状态语义

| 状态 | 事实源 | 用途 |
|---|---|---|
| Sprint 是否可关闭 | readiness gate、Change archive、tasks 完成数、`sprint.yaml` | 最终验收摘要与归档判断 |
| AC 是否逐条 sign-off | 人工 QA 或验收人记录 | 原始 AC 引用和人工 sign-off |
| 历史 AC 是否未勾选 | 旧模板或旧报告正文 | 追溯参考，不自动覆盖归档事实 |
| Workflow 派生状态 | `scripts/sync-workflow-status.py` | 刷新状态行和派生 note |

## 6. 异常与边界

| 场景 | 处理 |
|---|---|
| readiness gate 失败 | 不关闭 Sprint；最终摘要记录阻断项。 |
| Change 未全部 archived | 最终摘要展示 applied/proposed 数量，Sprint 不进入 completed/archive。 |
| 原始 AC 存在未勾选项但 readiness gate 通过 | 标注为待人工 sign-off 或历史追溯，不自动回退 Sprint 状态。 |
| 人工验收发现真实阻断 | 必须在最终摘要中记录阻断，并停止归档或通过 BUG/REQ 进入后续流程。 |
| 历史报告格式不一致 | 默认不批量迁移，后续主动更新时按新结构整理。 |
