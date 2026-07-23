## Context

`REQ-0066-admin-sku-image-removal-main-image-rules` 已评审通过，目标是补齐管理端 SKU 编辑弹窗中商品图片的移除与主图规则。现有 `tile-sku-management` spec 已有多图、主图唯一、PUT 更新图片关联、SKU 图片上传等基础能力；前端 `TileSkuFormModal` 当前可添加图片并设置 `is_main`，后端 `_normalize_images()` 已能保证主图唯一，但产品层尚未定义“设主图前置”和“移除当前主图兜底”。

本 change 不进入业务代码实现，只提供 OpenSpec 变更事实源。实现必须等待该 Change 纳入 Sprint 后通过 `/opsx-apply` 执行。

## Goals / Non-Goals

**Goals:**

- 在 SKU 编辑弹窗支持移除任意商品图片。
- 让主图在前端展示顺序和保存 payload 中始终位于第一位。
- 让移除当前主图时自动选择新主图，避免仍有图片时变成缺主图。
- 保持现有 SKU 更新 API 与数据表结构不扩散。
- 把 `admin-modal`、`media-upload` best-practice 横切验收带入实现任务。

**Non-Goals:**

- 不做图片拖拽排序、批量删除或图片裁剪。
- 不新增上传接口、不改变上传大小/MIME 限制、不改变 MinIO 前缀策略。
- 不做对象存储物理删除或孤儿文件清理。
- 不调整小程序、店主端或 Web 展示端的图片展示规则。

## Decisions

### D1. 实现策略：state-normalize

采用 `state-normalize` 策略：复用现有 SKU 弹窗 DOM/CSS 与上传链路，只补齐前端图片数组状态算法。相比重做组件或引入拖拽排序，该策略风险更小，能直接满足 REQ-0066 的主图前置和兜底规则。

算法建议：

```text
setMain(index):
  selected = images[index]
  rest = images without selected
  normalize([selected(is_main=true), ...rest(is_main=false)])

removeImage(index):
  removing = images[index]
  nextCandidate = images[index + 1]
  remaining = images without index
  if remaining empty: return []
  if removing.is_main:
    newMain = nextCandidate if exists else remaining[0]
    return normalize([newMain(is_main=true), ...remaining without newMain])
  return normalize(remaining with existing main preserved)

normalize(images):
  ensure at most one is_main
  if any is_main: move it to index 0
  recompute sort_order = index
```

### D2. API 与数据语义保持不变

继续使用 `PUT /api/v1/admin/tile-skus/{id}` 提交 images 全量列表。被移除图片不出现在 payload 中，后端 `replace_images()` 解除该 SKU 与图片的关联。默认不新增 API、不改 Pydantic 字段、不改 SQLite/MySQL schema。

### D3. 对象存储不物理删除

移除图片只解除 SKU 关联，不删除 MinIO 对象。原因是现有媒体对象可能被其它运营位或未来能力复用，物理删除需要独立媒体治理设计和审计策略。

### D4. Conflict Resolution

原型与验收优先级：

```text
prototype/web/admin-sku-image-removal-main-image-rules.html
> prototype/web/admin-sku-image-removal-main-image-rules-context.md
> acceptance.md
> requirement.md
> rules/ui-design.md
> openspec/specs/tile-sku-management/spec.md
```

冲突结论：

- 既有 spec 已允许图片/视频上传和主图标记；REQ-0066 不改变上传能力，只补充图片编辑规则。
- 既有 spec 的“主图唯一”继续保留；本 change 增加“主图第一”和“移除主图兜底”。
- `admin-media-upload-chain` 中 Docker 边界文件验收仅在实现触及上传链路时强制；若仅改移除与 payload 重排，可标记 N/A 并说明未改变上传链路。
- `TileSkuFormModal` 是 admin-modal 正例，必须继续避免 `modal-card` 与 `sku-modal-card` 双类并存。

## Risks / Trade-offs

- **[Risk] 前端状态与后端 normalize 规则不一致** → 通过组件测试和必要的后端回归测试同时验证 `is_main` 唯一、主图第一、`sort_order` 连续。
- **[Risk] 运营误删图片** → 本期可先提供清晰移除入口和可访问名称；是否增加二次确认由实现评估，但不得阻塞基础移除能力。
- **[Risk] 被移除对象文件残留** → 本 change 明确不做物理删除；后续如需清理孤儿媒体，应单独创建媒体治理 REQ/Change。
- **[Risk] 弹窗宽度或矮视口滚动回归** → acceptance 包含 `admin-modal` 横切 AC，apply 阶段必须验收 computed width 和矮视口滚动。

## Migration Plan

无需数据库迁移。部署时只需发布 Web 管理端前端变更；如实现不改变 API contract，则无需 OpenAPI/Orval。若实现发现需要调整 images 请求/响应字段，必须先补充 API 文档、OpenAPI、Orval 和测试。

## Open Questions

无阻塞项。二次确认是否启用可在实现阶段按 UX 复杂度决定，但验收不强制。
