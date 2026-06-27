---
description: 已评审缺陷 → OpenSpec fix-* Change（CLI）；原 /bug-to-change
---

将 **`approved`** 的 `issues/bugs/BUG-*` 转为 `openspec/changes/fix-*/`。默认 **fix-***；不写 `src/`。

**Input**：`BUG-xxxx`

| Flag | 含义 |
|------|------|
| `--hotfix` | 命名/任务强调紧急发布 |
| `--change-name <id>` | 指定 fix-* id |

---

## Step 0 — 读取

```text
AGENTS.md
rules/bug-management.md
rules/testing.md
rules/api.md
openspec/project.md
```

BUG 目录：bug.md、root-cause.md、workaround.md、acceptance.md、trace.md、logs/、screenshots/

```bash
openspec list --json
```

---

## Step 0.5 — 评审门禁（MUST — 无例外）

`trace.md` `status ∈ { approved, in_sprint, done }` 否则 **立即停止** → `/bug-review BUG-xxxx --approve`。

未评审 **不得** `/bug-opsx`、**不得**写入 Sprint 正式规划（见 `rules/bug-management.md` §4.1）。

---

## Step 1 — Bug Readiness

Ready / Partially Ready / Not Ready。Not Ready → `/bug-complete`，停止。

---

## Step 2 — 分析

- 现象、复现、影响（Bug Analysis Report）
- 根因分类、严重等级
- 关联 REQ/Change（若有）

---

## Step 3 — 创建 fix-* Change

```bash
openspec new change "fix-<area>-<topic>"
```

命名示例：`fix-minio-upload-timeout`、`fix-admin-login-redirect`

---

## Step 4 — Artifacts

按 CLI 生成 proposal（含 Rollback Plan）、design（根因+修复方案+测试）、specs（MODIFIED/ADDED）、tasks（**含回归测试**）。

proposal **Why** 链接 `BUG-xxxx`。

---

## Step 5 — 追溯

更新 BUG `trace.md`：

```yaml
openspec_changes:
  - change_id: fix-…
    type: fix
    status: proposed
```

tasks 末项提醒：`docs/knowledge-base/incidents/`（若适用）

---

## Step 6 — 输出

```text
## Bug → OpenSpec 完成
**BUG:** …
**Change:** fix-…
**Next:** /opsx-apply fix-…
```

---

## Guardrails

- 仅 approved
- 默认 fix-*，非 add
- 不跳过 CLI
- 不写 src

## 参考

- `.cursor/commands/req-opsx.md`（结构对照）
- `.cursor/commands/opsx-apply.md`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event bug.opsx --bug <BUG-id> --change <change-id> --sprint auto
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
