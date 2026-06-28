---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
review_id: REV-BUG-0035-001
status: approved
reviewed_at: 2026-06-28 16:18:44
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0035-banner-modal-sku-hero-image-no-effect` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0035-banner-modal-sku-hero-image-no-effect
```

建议修复 Change：

```text
fix-banner-modal-sku-hero-image
```

或与 BUG-0031–0036 合并为 `fix-banner-modal-ui`（本项 AC-031 功能验收 MUST 独立通过）。

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位列表 API `images[]` 为空 → `mainImageKey` 恒 null → 静默跳过；与 `tile_sku_admin_service.list_skus` / `BannerFormModal` 代码一致。 |
| 严重等级合理 | 通过 | `high` 合理；SKU 详情 Banner 无法以主图来源完成创建，功能阻断，非纯 UI。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖 REQ AC-031、按钮回填、无主图提示、保存成功、编辑模式、自定义上传与其他 jump_type 无回归。 |
| 是否需 hotfix 路径 | 不需要 | 非安全/数据损坏；可用 workaround（自定义上传）继续运营；常规 `fix-*` Change 即可，优先随 sprint-003 REQ-0016 收尾。 |

## 3. 批准理由

1. 根因清晰：前后端契约假设错误（列表 vs 详情 media 载荷），修复方案明确（`fetchTileSku` 或列表增加 `main_image_object_key`）。
2. 与 REQ-0016 AC-031、OpenSpec SKU 详情变体直接冲突，必须在 `add-banner-management` 归档前修复或另建 fix change。
3. 后端 Banner 保存校验已就绪，修复面以前端为主，风险可控。
4. workaround 已文档化；静默失败路径 MUST 在修复中补充用户提示。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-sku-hero-image` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 选择 SKU / 点击「使用 SKU 主图」时，通过 `fetchTileSku(id)` 获取含 `images[]` 的详情并写入 `imageKey` / `imageUrl`。
2. SKU 无主图或解析失败时 `setError` 明确提示，禁止静默跳过。
3. SHOULD 补充 `BannerFormModal` Vitest（列表无 images、详情有主图）。
4. 若选后端方案扩展列表字段，MUST 同步 OpenAPI + Orval。
5. MUST NOT 削弱 `_validate_sku_image` 后端校验。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0035-banner-modal-sku-hero-image-no-effect` 创建 OpenSpec change。
2. 评估与 BUG-0031–0036 合并为 `fix-banner-modal-ui`；合并时 AC-001～AC-007 仍须独立验收。
3. 修复完成后 `/opsx-apply` → 按 AC-001/AC-004 手工验证 SKU 详情 Banner 创建 → `/opsx-archive`。
