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

## 7. 需求 ↔ BUG 反向关联

当 BUG 文档中的 `related_requirement` 指向某个需求时，该需求的 `trace.md` MUST 维护索引级 `## 关联缺陷` 章节。该章节只记录缺陷索引，不重复 BUG 全文。

推荐格式：

```markdown
## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0003-brand-image-display-layout-shift | high | done | fix-brand-image-display-layout-shift | 品牌 Logo 展示与提示布局修复 |
```

同步时机：

- BUG 创建或完善后确定 `related_requirement` 时，MUST 在父需求 `trace.md` 增加或更新对应行。
- BUG 进入 Sprint、完成 `/opsx-apply`、完成 `/opsx-archive` 或状态变化时，MUST 同步更新父需求 `trace.md` 中该 BUG 的 `状态` 与 `关联 Change`。
- 若 BUG 的 `related_requirement` 为 `null`，不得强行写入需求 trace；除非后续评审明确补齐父需求。

`lifecycle` 与 `## 变更记录` 中所有时间记录 MUST 遵守 `rules/document-governance.md` 的秒级格式：`YYYY-MM-DD HH:mm:ss`（默认 `Asia/Shanghai`）。

## 8. 参考命令

`.cursor/commands/req-*.md`
