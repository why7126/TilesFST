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

## 7. 参考命令

`.cursor/commands/bug-*.md`
