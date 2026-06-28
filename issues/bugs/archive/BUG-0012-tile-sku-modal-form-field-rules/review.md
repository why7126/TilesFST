---
bug_id: BUG-0012-tile-sku-modal-form-field-rules
review_id: REV-BUG-0012-001
status: approved
reviewed_at: 2026-06-27 11:43:36
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0012-tile-sku-modal-form-field-rules` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0012-tile-sku-modal-form-field-rules
```

建议修复 Change：

```text
fix-tile-sku-modal-form-field-rules
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 给出稳定复现路径（表面工艺拦截、参考价格可空、默认非 0）；`root-cause.md` 已定位前后端校验、schema、publish 策略及 REQ-0006 v4 与 UAT 规则偏差。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断登录/列表/草稿保存，但影响运营录入体验与 UAT 验收对齐。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-012 覆盖表面工艺非必填、参考价格必填默认 0、上架策略、API/Orval、REQ delta 及关联 BUG 不回退。 |
| 是否需 hotfix 路径 | 不需要 | 非 P0、非安全/数据损坏；可通过常规 `fix-*` Change 修复。 |

## 3. 批准理由

1. UAT 产品规则变更清晰：表面工艺改非必填、参考价格改必填且默认 0，与当前实现及 REQ-0006 v4 旧文档差异明确。
2. `root-cause.md` §5 已在 complete 阶段锁定产品决策（含上架不拦空工艺），消除修复歧义。
3. 修复面可界定：前端 `TileSkuFormModal`、后端 `tile_sku_admin_service`、publish 策略、REQ acceptance delta；无需 DB migration。
4. 有临时 workaround（填占位工艺/手动补价），但不符合产品预期，需正式 fix。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-sku-modal-form-field-rules` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 前端：去掉表面工艺 `*` 与校验；参考价格加 `*`、新建默认 `0`、空值拦截。
2. 后端：移除 surface_finish 必填校验；reference_price 必填（含 `0.0`）；调整 `publish_sku` 表面工艺检查。
3. 同步 REQ-0006 `requirement.md` 字段定义与 `acceptance.md` AC-024、AC-015。
4. 运行 Orval；更新 `TileSkuFormModal` 与 `test_admin_tile_skus` 测试。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0012-tile-sku-modal-form-field-rules` 创建 `fix-tile-sku-modal-form-field-rules`。
2. 建议与 BUG-0010 等同批纳入 Sprint（SKU 弹窗/表单类，优先级低于已修复的 BUG-0011）。
3. 修复完成后按 `acceptance.md` 验收，再 `/opsx-archive`。
