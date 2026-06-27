---
description: 智能收集 - 自动区分需求与缺陷，按需拆分并分别走 req-capture / bug-capture 落盘
---

**Input**：用户不确定是需求还是 BUG 时的原始描述；可粘贴会议/反馈/工单原文。一条消息中可能同时包含**多个**需求、**多个**缺陷，或**混合**两者。

可选：`--priority P0|P1|P2`（仅作用于被判定为 REQ 的条目）、`--severity blocker|critical|high|medium|low`（仅作用于被判定为 BUG 的条目）、`--parent REQ-xxxx`

**Output**：

1. **分类分析表**（类型判定 + 拆分理由）
2. 每条 REQ → `issues/requirements/REQ-NNNN-slug/capture.md` + `trace.md`
3. 每条 BUG → `issues/bugs/BUG-NNNN-slug/capture.md` + `trace.md`
4. 更新对应 `_registry.yaml`

**禁止**：创建 `requirement.md` / `bug.md`、写 `src/`、写 `openspec/`。

**定位**：当用户**已知**类型时，仍应直接使用 `/req-capture` 或 `/bug-capture`；`/capture` 用于**类型未决**或**混合输入**场景。

---

## Steps

1. 读 `rules/requirement-management.md`、`rules/bug-management.md`、`issues/requirements/_registry.yaml`、`issues/bugs/_registry.yaml`
2. **解析并分类**（见下节）— 先拆条目，再判定每条为 REQ 或 BUG
3. 对 REQ 条目应用 `/req-capture` 的 Multi-REQ 拆分规则；对 BUG 条目应用 `/bug-capture` 的 Multi-BUG 拆分规则
4. 分配 ID、创建目录与 capture + trace、更新 registry
5. 向用户输出 **分类分析表** + **Capture 摘要**（REQ / BUG 分表）

---

## 需求 vs 缺陷 分类（MUST）

对每条候选条目，按下列标准判定。**有疑问时优先按现象判断**：已有能力/规范下的偏差 → BUG；尚未交付的新能力/流程 → REQ。

### 判定为 BUG（缺陷）

| 信号 | 示例 |
|------|------|
| **已有功能异常** | 登录失败、上传无进度、保存后数据丢失 |
| **与既有规范/参照不一致** | 列表分页与用户管理页不一致；弹窗副标题样式与品牌弹窗不符 |
| **回归** | 修复 A 后 B 又坏了；重启服务后行为变化 |
| **期望 vs 实际** | 用户能描述「应该怎样」且系统**本应**已满足（PRD/原型/同类页面已对齐） |
| **环境/部署问题** | Docker 下 MinIO 未生效、端口冲突导致不可用 |
| **文案/交互明显错误** | 按钮点了没反应、校验规则与业务不符 |

### 判定为 REQ（需求）

| 信号 | 示例 |
|------|------|
| **新能力/新页面** | 新增瓷砖规格管理页、新增 Banner 模块 |
| **能力扩展** | SKU 支持批量导入、侧边栏可收起 |
| **流程/策略变更** | 登录记住密码、品牌停用需二次确认 |
| **竞品/反馈驱动的新功能** | 参照 SoulKing 做版本号展示 |
| **尚无交付基线** | 用户描述的是「想要有 X」，而非「X 坏了」 |
| **体验优化（非修复）** | 首页改版、新增筛选维度（非对齐既有规范） |

### 边界与歧义

| 情况 | 做法 |
|------|------|
| 「新增 X 页，且现有 Y 页样式不对」 | 拆成 REQ（新页）+ BUG（Y 页样式） |
| 新功能验收未通过、与 PRD/原型不符 | BUG（fix-*），`related_requirement` 指向对应 REQ |
| 对已有 REQ 的范围补充（非缺陷） | REQ + `parent_requirement` |
| 同一页面多条 UI 问题、不同修复面 | 多条 BUG（见 bug-capture 拆分规则） |
| 无法从描述判断 | 在分类表中标注 **待澄清**，capture.md「待澄清」列出，默认倾向 REQ 若描述为「希望/需要/新增」 |

### 分类输出（回复用户，执行落盘前）

先输出 **分类分析表**：

| # | 摘要 | 判定 | 理由 |
|---|------|------|------|
| 1 | … | REQ | 新页面，尚无交付基线 |
| 2 | … | BUG | 与品牌弹窗样式不一致，属既有规范偏差 |

若混合类型，说明将分别创建 REQ 与 BUG 目录。

---

## 拆分规则（MUST）

分类完成后，**分别**套用既有命令的拆分逻辑：

- **REQ 条目** → 遵循 `/req-capture` **Multi-REQ 评估**（不同模块/端、独立 Change、独立验收等 → 多条 REQ）
- **BUG 条目** → 遵循 `/bug-capture` **Multi-BUG 评估**（不同界面/类型/修复面/严重度等 → 多条 BUG）

**禁止** umbrella 记录；每条 MUST 独立 ID 与目录。

---

## capture.md 附加约定

经 `/capture` 创建的记录，在 frontmatter 增加：

```yaml
captured_via: capture
classification_rationale: 一句话说明为何判为 REQ 或 BUG
```

REQ 仍用 req-capture 模板；BUG 仍用 bug-capture 模板；在正文末尾可加：

```markdown
# 分类说明（/capture）
…
```

---

## REQ capture.md 模板

（同 `/req-capture`，含 `captured_via` / `classification_rationale`）

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
captured_via: capture
classification_rationale: …
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

## BUG capture.md 模板

（同 `/bug-capture`，含 `captured_via` / `classification_rationale`）

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
captured_via: capture
classification_rationale: …
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

---

## Capture 摘要（回复用户）

1. **分类分析表**（见上）
2. **REQ 表**（若有）：

| REQ ID | 标题 | 优先级 | 拆分/分类理由 |
|--------|------|--------|---------------|

3. **BUG 表**（若有）：

| BUG ID | 标题 | 严重度 | 拆分/分类理由 |
|--------|------|--------|---------------|

4. 若全部为单一类型，可提示用户下次直接使用 `/req-capture` 或 `/bug-capture`。

## Next

- REQ：`/req-explore REQ-xxxx` → `/req-generate REQ-xxxx`
- BUG：`/bug-explore BUG-xxxx` → `/bug-generate BUG-xxxx`

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md`.对**本次创建的每一条** REQ 与 BUG **分别**执行：

```bash
for req in REQ-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event req.capture --req "$req" --sprint auto || exit 1
done
for bug in BUG-xxxx-slug ...; do
  python scripts/sync-workflow-status.py --event bug.capture --bug "$bug" --sprint auto || exit 1
done
```

- 每条命令 exit code **MUST** 为 `0`
- 向用户打印 **Workflow Sync Report**（混合类型时注明 REQ N 条 + BUG M 条）
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`)
