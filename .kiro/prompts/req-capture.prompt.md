---
description: 需求记录 - 轻量 capture，防遗忘，分配 REQ-ID；支持一次输入多条并按需拆分
---

**Input**：一句话描述，或粘贴会议/反馈原文。用户可能在一条消息中描述**多个**独立需求。

可选：`--priority P0|P1|P2`、`--parent REQ-xxxx`（单条或对子需求 refinement 时使用）

**Output**：每条需求 → `issues/requirements/REQ-NNNN-slug/capture.md` + `trace.md` 最小壳；更新 `_registry.yaml`。

**禁止**：创建 `requirement.md`、写 `src/`、写 `openspec/`。

---

## Steps

1. 读 `rules/requirement-management.md`、`issues/requirements/_registry.yaml`
2. **评估并拆分**（见下节）— 先判断应创建 1 个还是 N 个 REQ
3. 为每条 REQ 分配 `REQ-NNNN-kebab-slug`（`next_id` 连续递增）
4. 创建目录与 `capture.md`、`trace.md`；更新 `_registry.yaml`
5. 向用户输出 **Capture 摘要**（单条简短说明；多条用表格）

---

## Multi-REQ 评估（MUST）

执行前 MUST 解析用户输入，决定 **合并为 1 条** 还是 **拆分为多条** REQ。

### 应拆分为独立 REQ（任一满足即拆）

| 维度 | 示例 |
|------|------|
| **不同业务能力** | 用户管理 vs SKU 管理 vs 登录体验 |
| **不同模块/端** | 管理端 vs 店主端 vs 小程序 |
| **独立优先级** | 一条 P0 核心能力，另一条 P2 体验优化 |
| **独立 OpenSpec Change** | 预期会生成不同的 `add-*` / `fix-*`，无法共用一个 PRD |
| **独立验收闭环** | 用户故事与 acceptance 无法写在同一份 requirement 内而不混淆 |
| **用户显式枚举** | 分号、换行、编号列表、会议议题多条并列 |

### 保持为单条 REQ（全部满足时可合并）

- 同一功能域的**一个交付单元**（如「SKU 列表 + 新增弹窗」同属 tile-sku-management）
- 多条描述是同一能力的不同细节，将在同一份 `requirement.md` 内展开
- 属于对**已有 REQ 的小幅 refinement** → 优先 `--parent REQ-xxxx` 或走原 REQ 更新，**而非**新建 peer REQ（除非团队明确要求新编号）

### 拆分 vs 父需求

| 情况 | 做法 |
|------|------|
| 全新、独立能力 | 新 REQ-ID |
| 已有 REQ 的体验增强/策略补充 | 新 REQ + `parent_requirement: REQ-xxxx`，或评估是否应合并进原 REQ capture |
| 实为缺陷 | **不要** req-capture → 引导 `/bug-capture` |

### 拆分执行规则

- 每条需求 **MUST** 有独立目录与 REQ-ID；**禁止**建「总 REQ + 子 bullet」 umbrella 记录
- slug 按**最小可交付能力**命名
- 未拆分时，在回复中 **一句话说明** 为何不拆

---

## capture.md 模板

```markdown
---
req_id: REQ-0008-example
status: captured
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
recorded_by: product
source: 会议|反馈|竞品
priority_hint: P1
parent_requirement:
---

# 一句话
…

# 原始描述
…

# 待澄清
- [ ] …

# 探索结论
（/req-explore 后人工确认写入）
```

## Capture 摘要（回复用户）

单条：REQ-ID、标题、priority、路径。

多条：

| REQ ID | 标题 | 优先级 | 拆分理由 |
|--------|------|--------|----------|
| REQ-0009 | … | P1 | 独立模块，与用户管理无关 |

## Next

每条：`/req-explore REQ-xxxx` → `/req-generate REQ-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对**本次创建的每一条** REQ 依次执行：

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event req.capture --req "$req" --sprint auto || exit 1
done
```

- 每条命令 exit code **MUST** 为 `0`
- 向用户打印 **Workflow Sync Report**（多条时可打印最后一次完整报告，并注明共 N 条）
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`)
