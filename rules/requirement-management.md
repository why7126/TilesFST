---
purpose: 需求（REQ）生命周期、状态机、目录与评审门禁
source: 项目团队 + AI v2 定稿
update_method: 命令族变更时同步更新
---

# 需求管理规范

## 1. 目录

```text
issues/requirements/
├── _registry.yaml
└── REQ-NNNN-slug/
    ├── capture.md
    ├── requirement.md
    ├── user-stories.md
    ├── business-flow.md
    ├── acceptance.md
    ├── trace.md
    ├── review.md
    └── prototype/{web,admin,miniapp}/
```

禁止在 `docs/product/`、`docs/prd/` 存放业务需求（见 `rules/document-governance.md`）。

## 2. 状态机

| status | 含义 |
|--------|------|
| `captured` | 已记录（capture.md） |
| `exploring` | 已探讨，未落 PRD |
| `draft` | 仅有 requirement.md |
| `enriching` | 六件套补齐中 |
| `pending_review` | 文档齐，待评审 |
| `approved` | **评审通过**（可 req-opsx、可进 Sprint） |
| `rejected` | 不做 |
| `deferred` | 延后 |
| `in_sprint` | 已纳入迭代 |
| `done` | 已交付验收 |

**事实源**：`trace.md` 的 `status`；`requirement.md` frontmatter **MUST** 同步。

## 3. 命令与阶段

| 命令 | 允许 status（入口） | 产出 |
|------|---------------------|------|
| `/req-capture` | — | capture.md、trace 壳 |
| `/req-explore` | captured, exploring | 默认无文件 |
| `/req-generate` | captured, exploring | requirement.md → draft |
| `/req-complete` | draft, enriching | 六件套 → pending_review |
| `/req-review` | pending_review | review.md → approved/rejected/deferred |
| `/req-opsx` | **approved** | openspec/changes/* |

## 4. 门禁

- `/req-opsx`：**仅** `approved`
- `/sprint-propose`、`/sprint-apply`：**仅** `approved` 或 `in_sprint`
- 旧命令 `/requirement-to-opsx` 已删除 → `/req-opsx`

## 5. Readiness（req-opsx / req-complete）

| 级别 | 条件 |
|------|------|
| Ready | requirement + user-stories + business-flow + acceptance + trace 齐全 |
| Partially Ready | 缺 prototype 或非阻塞项 |
| Not Ready | 缺 requirement 或 acceptance |

## 6. trace.md 最小字段

```yaml
requirement_id: REQ-NNNN-slug
status: captured
priority: P1
lifecycle:
  captured: null
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
openspec_changes: []
related_requirements: []
```

每次命令结束追加 `## 变更记录`。

## 7. 参考命令

`.cursor/commands/req-*.md`
