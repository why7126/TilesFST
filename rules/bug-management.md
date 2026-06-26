---
purpose: 缺陷（BUG）生命周期、状态机、目录与评审门禁
source: 项目团队 + AI v2 定稿
update_method: 命令族变更时同步更新
---

# 缺陷管理规范

## 1. 目录

```text
issues/bugs/
├── _registry.yaml
└── BUG-NNNN-slug/
    ├── capture.md
    ├── bug.md
    ├── root-cause.md
    ├── workaround.md
    ├── acceptance.md
    ├── trace.md
    ├── review.md
    ├── logs/
    └── screenshots/
```

禁止在 `docs/bugs/` 存放缺陷记录。

## 2. 状态机

| status | 含义 |
|--------|------|
| `captured` | 已记录 |
| `exploring` | 复现/影响分析中 |
| `draft` | 仅有 bug.md |
| `enriching` | 缺陷包补齐中 |
| `pending_review` | 待评审 |
| `approved` | **确认修复**（可 bug-opsx、可进 Sprint） |
| `rejected` | 非缺陷/误报 |
| `wont_fix` | 不修 |
| `deferred` | 延后 |
| `in_sprint` | 已纳入迭代 |
| `done` | 已修复验收 |

## 3. 命令与阶段

| 命令 | 产出 |
|------|------|
| `/bug-capture` | capture.md、trace 壳 |
| `/bug-explore` | 默认无文件 |
| `/bug-generate` | bug.md |
| `/bug-complete` | root-cause、workaround、acceptance、trace |
| `/bug-review` | review.md、status |
| `/bug-opsx` | openspec/changes/fix-* |

## 4. 门禁

- `/bug-opsx`：**仅** `approved`
- Sprint：**P0 BUG** 优先于功能 REQ；纳入须 `approved` 或 `in_sprint`
- 旧命令 `/bug-to-change` 已删除 → `/bug-opsx`

## 5. 严重等级

```text
blocker | critical | high | medium | low
```

## 6. 知识沉淀

修复后若有复用价值，可更新 `docs/knowledge-base/incidents/`（由 bug-opsx tasks 提醒）。

## 7. 父需求反向追溯

BUG 的 `related_requirement` 不只是单向引用。若 `related_requirement` 非空，AI 在以下阶段 MUST 同步更新父需求 `issues/requirements/<REQ-ID>/trace.md` 的 `## 关联缺陷` 索引表：

- `/bug-complete` 或 `/bug-review` 确认父需求后。
- `/bug-opsx` 创建或确认修复 Change 后。
- BUG 纳入 Sprint、完成 `/opsx-apply`、完成 `/opsx-archive` 或状态变化后。

父需求 trace 中只记录索引级信息：`BUG`、`严重等级`、`状态`、`关联 Change`、`说明`。MUST NOT 在需求 trace 中复制 BUG 复现步骤、根因全文、日志或截图。

`trace.md` 的 `lifecycle` 与 `## 变更记录` 中所有时间记录 MUST 遵守 `rules/document-governance.md` 的秒级格式：`YYYY-MM-DD HH:mm:ss`（默认 `Asia/Shanghai`）。

## 8. 参考命令

`.cursor/commands/bug-*.md`
