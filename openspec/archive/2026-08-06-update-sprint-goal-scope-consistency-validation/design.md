## 上下文

`sprint.yaml` 是 Sprint 正式范围的机器事实源，Workflow Sync 会将范围派生到 `sprint.md` 的 `## 2. Scope` 主表和分组表。`sprint.md ## 1. 目标` 下的「Sprint 目标编号列表」仍是人读摘要，当前不属于 Workflow Sync marker block。

`sprint-020` 暴露了一个漂移：Scope 已包含 `REQ-0100`，但目标编号列表未列出。由于现有 `validate-sprint-scope.py` 只检查 Scope 区域，该遗漏在 `/sprint-propose` 收尾校验中不会失败。

## 目标与非目标

目标：

- 让 Sprint Scope 校验覆盖目标编号列表，发现正式范围中已纳入但目标列表遗漏的 REQ/BUG/必要 Change。
- 保持 `sprint.yaml` 作为事实源，校验只报告漂移，不用目标列表反向覆盖机器范围。
- 让 `/sprint-propose` 在追加 Scope 时同步人读目标列表，并把增强校验作为完成门禁。
- 用脚本级测试固定 `sprint-020` / `REQ-0100` 漏列复现场景。

非目标：

- 不自动重写 `## 1. 目标` 的自然语言段落。
- 不批量修复所有历史 Sprint 文档。
- 不修改 API、数据库、Web、小程序、管理端运行时代码、Orval 或 Docker。

## 决策

### D1 目标编号列表解析只读取目标章节的显式列表

实现应从 `sprint.md` 中定位 `## 1. 目标`，再定位「Sprint 目标编号列表：」后连续的 Markdown bullet 列表。解析范围在第一个非列表块或下一个标题前结束。

理由：

- 可以避免把 `## 2. Scope` 主表、Workflow Sync 分组表、依赖树或关联文档中的编号误当成目标列表证据。
- 保持人读列表格式简单，不引入新的 marker block。

备选方案：

- 让 Workflow Sync 自动生成整个目标列表。该方案幂等性更强，但更容易覆盖人工目标说明和要点段落，本变更优先用校验兜底，允许后续再评估自动维护。

### D2 REQ/BUG 必须出现，纯 Change 按策略校验

目标编号列表必须覆盖 `sprint.yaml.requirements` 与 `sprint.yaml.bugs`。对于 `sprint.yaml.changes`：

- 若 Change 已通过关联 REQ/BUG 表达，可以不强制重复出现 Change ID。
- 若 Change 是纯 Change，且不属于任何 REQ/BUG，则必须出现在目标编号列表。

理由：

- 避免列表冗余，同时确保纯治理 Change 不被隐藏。
- 与现有 Sprint 目标列表中同时列 BUG 与 Change 的格式兼容。

### D3 缺失项报告必须可操作

校验失败时输出具体 Sprint、缺失 ID 和缺失位置，例如：

```text
REQ-0100-mintlify-docs-site-ia-content-experience missing from sprint.md Sprint target id list
```

理由：

- `/sprint-propose` 和人工复核都需要直接知道补哪一项。
- 多项缺失时分条输出，便于一次修复。

### D4 与 Workflow Sync 的边界

Workflow Sync 继续维护 `## 2. Scope` 主表与分组 marker block。目标编号列表不在 marker block 内，`/sprint-propose` 负责在创建或追加范围时维护；增强后的 `validate-sprint-scope.py` 负责最终兜底。

如果后续改为 Workflow Sync 自动维护目标编号列表，应新增独立设计并保证不覆盖自然语言目标段落。

## 风险与权衡

| 风险 | 缓解 |
|---|---|
| 历史 Sprint 目标列表格式不一致导致解析失败 | 失败信息区分“列表缺失/格式异常”和“编号缺失”，先报告再人工修复。 |
| 纯 Change 归属判断不准确 | 优先使用 `sprint.yaml` 与现有 Scope 派生数据；无法关联 REQ/BUG 的 Change 按纯 Change 处理。 |
| `/sprint-propose` 手工更新目标列表仍可能漏项 | 最终必须运行增强校验，失败则不得完成命令。 |
| 校验误读后续章节编号 | 解析范围严格限制在目标编号列表连续 bullet 块。 |

## 迁移计划

1. 增强 `validate-sprint-scope.py` 解析与校验目标编号列表。
2. 更新 `/sprint-propose` 与 Workflow Sync 技能规则，明确目标列表维护和校验边界。
3. 增加测试覆盖缺失、通过、短编号等价和纯 Change 策略。
4. 用 `sprint-021 --item REQ-0102` 验证新增范围通过；用 `sprint-020 --item REQ-0100...` 验证历史遗漏可失败。

## 开放问题

无阻塞开放问题。后续如要把目标编号列表纳入 Workflow Sync 自动维护，应另行评估幂等更新策略。
