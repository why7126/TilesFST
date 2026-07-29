## Context

`REQ-0078-certificate-multiple-images-main-image` 已评审通过，来源于 `REQ-0038-brand-certificate-management` 的能力增强。现有 `brand-certificate-management` spec 已定义单个证书文件、证书上传预览、管理端列表、弹窗、通用组件和横切 UI 验收。本 Change 将单文件图片能力扩展为多张图片与唯一主图，同时兼容既有 PDF/文档占位和旧单文件证书数据。

当前约束：

- 上传必须经过后端鉴权、MIME/大小校验和 MinIO/S3 兼容对象存储适配层。
- 管理端 UI 必须遵守“工业石材 · 暗色旗舰风”、semantic token、admin-list、admin-modal 和 media-upload best-practices。
- API/Schema 变化必须同步 OpenAPI、Orval、API 文档和测试。
- 真实实现必须等纳入 Sprint 后通过 `/opsx-apply` 执行；本 Change 仅提供规格和任务。

## Goals / Non-Goals

**Goals:**

- 为品牌证书维护多张图片，并保证同一证书只有一张主图。
- 支持第一张成功上传图片默认主图、手动设置主图、删除主图后的兜底主图。
- 让证书列表、证书摘要和默认预览入口优先使用主图缩略图。
- 兼容旧单文件证书数据，避免上线后已有证书列表或编辑弹窗空白。
- 明确数据库、API、Orval、上传、安全和测试同步边界。

**Non-Goals:**

- 不实现店主 Web 或微信小程序证书详情多图浏览。
- 不新增证书审批、OCR、电子签章、真伪校验或证书与 SKU 绑定。
- 不物理删除对象存储文件；删除图片只解除业务关联。
- 不改变 SKU 图片、品牌 Logo、Banner 等其他媒体场景的主图规则。

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| 文档包 | requirement、user-stories、business-flow、acceptance、trace、review、prototype/web 均存在 |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-list、admin-modal、media-upload |
| Change type | update |

## Impact Analysis

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: true
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - brand-certificate-management
```

## Conflict Report

优先级：HTML > PNG > prototype-context.md > acceptance.md > ui-design.md > openspec/specs。

| 来源 | 内容 | 决议 |
|---|---|---|
| `prototype/web/certificate-multiple-images-main-image.html` | 静态原型示例中 `.certificate-modal-card` 宽度为 880px | 不作为宽度变更依据；该 HTML 用于多图状态与布局语义验收 |
| `prototype/web/prototype-context.md` | 要求 computed width 与设计批准宽度一致 | 与现有 spec 对齐，继续使用 REQ-0038 已批准的 760px |
| `acceptance.md` AC-XCUT-006 | 要求弹窗 Computed width 与设计批准宽度一致 | 设计批准宽度解释为现有 `brand-certificate-management` spec 的 760px |
| `openspec/specs/brand-certificate-management/spec.md` | “品牌证书新增编辑弹窗”要求宽 760px | 保留，不因本 Change 扩宽弹窗 |

Conflict Resolution: 最终实现必须保持新增/编辑证书弹窗 Computed width 为 760px；若多图区内容较多，应通过局部换行、滚动和更紧凑的图片卡片解决，而不是扩大弹窗宽度。

## Decisions

### D1. UI 策略采用 DS / existing-components，而非 CSS Port

原因：`REQ-0078` 的 prototype HTML 是状态和验收语义参考，不是新的视觉皮肤来源。品牌证书页面已有 spec 与组件化要求，继续复用现有页面容器、通用证书展示方法、上传状态机、FixedAdminToast 和 AdminConfirmModal，可降低 admin CSS cascade 回归风险。

替代方案：

- CSS Port：会把静态原型中的 880px 宽度和裸 CSS 细节带入实现，容易与现有 760px 弹窗 spec 冲突。
- 全新上传组件：可能扩大范围；如确需抽象，必须保持上传 API 和 toast 仍由页面容器控制。

### D2. 数据模型优先使用证书图片关联表

建议新增或等价实现 `brand_certificate_images`，字段至少包含 `certificate_id`、`file_key`、`file_url` 或受控读取引用、`file_name`、`mime_type`、`file_size`、`is_main`、`sort_order`、`created_at`、`updated_at`。旧 `brand_certificates` 单文件字段保留兼容读取，迁移或保存后逐步转换为图片记录。

理由：多图、排序、唯一主图和删除关联更适合子表表达；避免把图片数组塞入单字段导致查询、校验和迁移困难。

### D3. PDF/文档类证书首期沿用单文件兼容

本 Change 的多图能力以图片为主。PDF/文档类证书继续展示既有 PDF/文件占位；如某证书同时存在图片列表和 PDF 单文件，则管理端列表缩略图优先使用主图图片，预览入口默认从主图开始，PDF 可作为兼容文件入口保留或由设计阶段选择互斥。实现前必须在 API Schema 中明确互斥/并存策略。

### D4. 主图规则由前后端双重保证

前端负责交互即时反馈：第一张成功上传图片默认主图、设置主图前置、删除主图兜底。后端负责最终契约：有图片时必须且只能有一张 `is_main=true`；拒绝多主图、无主图异常 payload 或不属于当前上传链路的文件引用。

### D5. 删除图片只解除业务关联

删除图片从证书图片列表移除并保存后，不应立即物理删除对象存储文件。后续若需要孤儿文件回收，应另建媒体治理或对象存储清理 Change。

## Risks / Trade-offs

- [Risk] 旧单文件证书与新图片表并存导致列表缩略图逻辑分叉 → Mitigation: 在 Service 层统一组装 `images`、`main_image` 和 legacy file fallback。
- [Risk] 弹窗多图区域挤压字段或底部按钮 → Mitigation: 保持 760px 宽度，使用换行/局部滚动，并验收矮视口 body scroll。
- [Risk] API contract 变化导致 Orval 和测试夹具漂移 → Mitigation: tasks 明确 OpenAPI、Orval、docs、pytest/Vitest 同步。
- [Risk] 上传成功但同会话列表不回显 → Mitigation: 复用 media-upload best-practice，覆盖即时回显测试。
- [Risk] 主图唯一性只在前端保证 → Mitigation: 后端保存时二次校验并增加集成测试。

## Migration Plan

1. 新增或等价实现证书图片存储结构。
2. 查询证书详情和列表时，为旧单文件记录生成兼容展示模型。
3. 保存新多图证书时写入图片列表、主图和排序。
4. 若需要迁移历史图片证书，可将原图片文件映射为 `sort_order=0`、`is_main=true` 的图片记录；PDF/文档保留 legacy 字段或按设计确认策略处理。
5. 回滚时保留 legacy 单文件字段读取能力，新增图片表不影响旧字段展示。

## Open Questions

- PDF/文档类证书与图片列表最终采用互斥还是并存？本设计建议兼容读取，保存策略在 apply 前确认。
- 单证书图片数量上限是否固定为 9？本设计沿用 REQ 默认值，实施前需同步前后端校验和文案。
- 是否需要一次性迁移全部历史图片证书，还是 lazy fallback 到首次编辑保存时转换？
