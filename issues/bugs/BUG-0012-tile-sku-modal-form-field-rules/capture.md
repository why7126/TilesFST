---
bug_id: BUG-0012-tile-sku-modal-form-field-rules
status: captured
recorded_at: 2026-06-27 08:56:54
severity_hint: medium
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 现象

瓷砖 SKU 新增/编辑弹窗表单字段必填规则与默认值不符合当前产品预期：

1. **表面工艺** 当前实现或验收要求为必填，产品期望改为**非必填**。
2. **参考价格（元）** 当前为选填，产品期望改为**必填**，且默认值为 **0 元**。

> 注：REQ-0006 v4 文档（`requirement.md` AC-024）原定义为「表面工艺*、参考价格选填」。本缺陷记录产品方在实现验收阶段提出的字段规则调整，后续 `/bug-complete` 需同步更新 acceptance 与 API 校验策略。

# 复现步骤

1. 以 admin 登录管理端，进入「瓷砖SKU」列表页。
2. 点击「新增SKU」打开弹窗。
3. 不填写「表面工艺」，填写其他必填项，尝试保存 — 观察是否被阻止提交。
4. 不填写「参考价格（元）」，观察是否允许保存及列表展示占位。
5. 打开新增弹窗，观察「参考价格（元）」初始值是否为空而非 `0`。
6. 对照 `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` AC-024、AC-026。

# 期望 vs 实际

| 字段 | 期望 | 实际（待确认） |
|---|---|---|
| 表面工艺 | 非必填；留空可正常保存 | 可能仍标记为必填并阻止提交 |
| 参考价格（元） | 必填；新建时默认 `0`；校验不允许空值 | 可能为选填；默认空；无价格时列表展示「—」 |
| Label | 仍为「参考价格（元）」 | — |

# 影响范围

- Web 管理端：SKU 新增/编辑弹窗表单校验与默认值。
- 后端：创建/更新 SKU 接口对 `surface_finish`、`reference_price` 的校验规则。
- 关联需求：REQ-0006-tile-sku-management（需 acceptance delta）。
- 列表展示：参考价格为 0 时应格式化为 `¥ 0.00`（非「—」）。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | 表单校验/业务规则不符合产品预期 |
| 严重程度建议 | medium |
| 可能修复面 | 前端表单 schema、后端 Pydantic 校验、REQ-0006 acceptance 同步 |
| 设计约束 | 保持 Label「参考价格（元）」；两位小数；默认 0 |

# 附件

- 暂无截图。
- 当前需求：`issues/requirements/REQ-0006-tile-sku-management/requirement.md` §字段定义
- 验收：`acceptance.md` AC-024、AC-026、AC-015
