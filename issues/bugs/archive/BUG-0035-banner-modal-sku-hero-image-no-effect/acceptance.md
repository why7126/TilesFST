---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
status: pending_review
created_at: 2026-06-28 16:17:35
updated_at: 2026-06-28 16:17:35
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0016 **AC-031**，并使 SKU 详情 Banner 可通过 SKU 主图来源完成创建/编辑；不得回归自定义上传及其他 `jump_type` 弹窗行为。

## AC-001 选择 SKU 后 MUST 默认预览 SKU 主图（对齐 REQ AC-031）

**Given** 管理员已登录 `/admin/banners`，打开新增 Banner 弹窗  
**When** 将跳转类型设为「SKU 详情」并选择一条 **有主图** 的 SKU  
**Then** `image_source` MUST 为 `sku_main_image`  
**And** Banner 图片预览区 MUST 显示该 SKU 主图  
**And** 表单 MUST 持有非空 `image_object_key`（与后端 SKU 主图 key 一致）

## AC-002 点击「使用 SKU 主图」MUST 回填预览与 key

**Given** 弹窗已选 SKU 详情 + 有效 SKU，当前 Banner 图为空或来自自定义上传  
**When** 点击「使用 SKU 主图」  
**Then** 预览区 MUST 更新为 SKU 主图  
**And** `image_source` MUST 为 `sku_main_image`  
**And** `sku_gallery_asset_id` MUST 为 `null`  
**And** MUST NOT 静默无响应

## AC-003 SKU 无主图时 MUST 明确提示

**Given** 选择的 SKU `has_main_image=false`（或详情无 `is_main` 图）  
**When** 点击「使用 SKU 主图」或选择该 SKU 触发自动回填  
**Then** MUST 展示 inline 错误（如「该 SKU 无主图，请自定义上传」）  
**And** MUST NOT 清空已有合法自定义上传图（编辑模式）除非用户显式切换

## AC-004 保存 SKU 详情 Banner MUST 成功

**Given** 已通过 AC-001/002 回填 SKU 主图  
**When** 填写其余必填项并点击「保存 Banner」  
**Then** MUST 成功创建/更新（HTTP 200）  
**And** 响应 `image_source=sku_main_image`，`image_object_key` 与 SKU 主图一致  
**And** MUST NOT 出现「请配置 Banner 图片」或后端 `BANNER_JUMP_TARGET_INVALID`（30052）

## AC-005 编辑模式 MUST 可重新应用 SKU 主图

**Given** 编辑一条 `jump_type=SKU_DETAIL` 的 Banner，当前图为自定义上传  
**When** 点击「使用 SKU 主图」  
**Then** 预览 MUST 切换为关联 SKU 主图  
**And** 保存后 `image_source` MUST 更新为 `sku_main_image`

## AC-006 自定义上传 MUST 保持可用（回归）

**Given** 跳转类型为 SKU 详情  
**When** 用户通过「自定义上传」选择图片并上传成功  
**Then** MUST 正常预览与保存（`image_source=custom_upload`）  
**And** MUST NOT 因本次修复破坏 `uploadBannerImage` 流程

## AC-007 其他 jump_type MUST 不受影响（回归）

**Given** 跳转类型为外部链接、专题页或无跳转  
**When** 打开弹窗并操作 Banner 图片区  
**Then** MUST NOT 展示「使用 SKU 主图」按钮（SKU 详情以外）  
**And** 原有上传/校验行为 MUST 与修复前一致

## AC-008 修复范围 SHOULD 优先前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** 首选方案 MUST NOT 变更 SQLite schema  
**And** 若仅前端调用 `fetchTileSku`，MUST NOT 需要 Orval 重新生成  
**And** 若扩展列表 API 字段，MUST 同步 OpenAPI + Orval + `docs/03-api-index.md`

## AC-009 测试 SHOULD 补齐

**Given** 进入 `fix-banner-modal-sku-hero-image`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 Vitest：mock 列表 `images: []`、详情含主图 `object_key`，断言选择 SKU / 点击按钮后 `imageKey` 被设置  
**And** MAY 在 Change `trace.md` 记录手工验收截图

## AC-010 与 BUG-0031–0036 MUST 可独立验收

**Given** 本 BUG 与同弹窗 UI 类缺陷可能同 Sprint  
**When** 分别或合并提交 fix Change  
**Then** 本 AC 集合 MUST 可独立验收，不依赖上传按钮文案（BUG-0032）等 UI 修复  
**And** 合并 Change 时 MUST 仍满足 AC-001～AC-007
