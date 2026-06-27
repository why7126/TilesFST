---
name: /bug-capture
id: bug-capture
category: Workflow
description: 缺陷记录 - 轻量 capture，分配 BUG-ID；支持一次输入多条并按需拆分
---

**Input**：现象描述、复现步骤、环境（可选截图路径）。用户可能在一条消息中描述**多个**独立缺陷。

Flags：`--severity blocker|critical|high|medium|low`（单条时；拆分时按每条单独评估）

**Output**：每条缺陷 → `issues/bugs/BUG-NNNN-slug/capture.md` + `trace.md`；更新 `_registry.yaml`

**禁止**：`bug.md`、`src/`、`openspec/`

---

## Steps

1. 读 `rules/bug-management.md`、`issues/bugs/_registry.yaml`
2. **评估并拆分**（见下节）— 先判断应创建 1 个还是 N 个 BUG
3. 为每条 BUG 分配 `BUG-NNNN-kebab-slug`（`next_id` 连续递增）
4. 创建目录、`capture.md`、`trace.md` 最小壳；更新 `_registry.yaml`
5. 向用户输出 **Capture 摘要**（单条简短说明；多条用表格）

---

## Multi-BUG 评估（MUST）

执行前 MUST 解析用户输入，决定 **合并为 1 条** 还是 **拆分为多条** BUG。

### 应拆分为独立 BUG（任一满足即拆）

| 维度 | 示例 |
|------|------|
| **不同界面/层级** | 列表页 vs 弹窗 vs API/后端 vs 部署环境 |
| **不同缺陷类型** | UI 一致性 vs 滚动/溢出 vs 校验规则 vs 功能不可用 |
| **不同修复面** | 前端样式 vs 后端校验 vs 需独立 `fix-*` Change |
| **独立严重度** | 一条 blocker/high，另一条 medium/low |
| **独立交付优先级** | 一条可随当前 Sprint，另一条可延后 |
| **用户显式枚举** | 分号、换行、编号列表、「另外」「还有」等多条并列描述 |

### 保持为单条 BUG（全部满足时可合并）

- 同一页面/同一弹窗，**一次修复**可闭环
- 多条现象是**同一根因**的不同表现，复现与验收不可分
- 拆分会导致完全重复的复现步骤与 acceptance

### 拆分执行规则

- 每条缺陷 **MUST** 有独立目录与 BUG-ID；**禁止**建「总 BUG + 子 bullet」 umbrella 记录
- slug 按**最小可修复单元**命名（如 `tile-sku-list-ui-inconsistency`、`tile-sku-modal-content-overflow`）
- 同属一父需求时，各条 `related_requirement` 填同一 REQ；存在因果链时用 `related_bug` 互引
- 未拆分时，在回复中 **一句话说明** 为何不拆

---

## capture.md 模板

```markdown
---
bug_id: BUG-0001-example
status: captured
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
severity_hint: high
environment: local|docker|prod
related_requirement:
related_bug:
---

# 现象
…

# 复现步骤
1. …

# 期望 vs 实际
…

# 附件
screenshots/…  logs/…
```

## Capture 摘要（回复用户）

单条：BUG-ID、标题、severity、路径。

多条：

| BUG ID | 标题 | 严重度 | 拆分理由 |
|--------|------|--------|----------|
| BUG-0009 | … | medium | 列表 UI，与用户管理页对齐 |

## Next

每条：`/bug-explore BUG-xxxx` → `/bug-generate BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对**本次创建的每一条** BUG 依次执行：

```bash
for bug in BUG-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event bug.capture --bug "$bug" --sprint auto || exit 1
done
```

- 每条命令 exit code **MUST** 为 `0`
- 向用户打印 **Workflow Sync Report**（多条时可打印最后一次完整报告，并注明共 N 条）
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`)
