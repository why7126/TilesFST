## Why

`REQ-0038-brand-certificate-management` 已交付品牌证书管理，但当前证书文件以单文件方式维护，无法覆盖证书封面、内页、检测明细页和附页等多页图片场景。`REQ-0078-certificate-multiple-images-main-image` 已评审通过，需要把品牌证书从单图/单文件展示增强为多图上传、主图设置和主图缩略图展示。

## What Changes

- 管理端品牌证书新增/编辑弹窗支持为同一证书维护多张图片。
- 证书图片列表支持唯一主图、默认主图、设置主图、删除主图后的兜底主图规则。
- 管理端证书列表和默认预览入口优先使用主图缩略图。
- 后端 API、Schema 和数据模型扩展或兼容证书图片数组，并保持旧单文件证书数据可读。
- 上传链路继续走后端鉴权、MIME/大小校验和对象存储适配层，禁止前端直连未授权对象存储。
- 横切 UI 验收继续覆盖 admin-list、admin-modal、media-upload best-practices。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `brand-certificate-management`: 扩展品牌证书数据模型、管理端创建/更新 API、文件上传/预览、页面、弹窗、通用组件和横切 UI 验收，支持多张图片与主图规则。

## Impact

- Backend: 品牌证书 API、Schema、Service、Repository、数据兼容逻辑。
- Web/Admin: `/admin/brand-certificates` 列表缩略图、新增/编辑弹窗、多图上传卡片、主图状态与回填。
- Database: 可能新增 `brand_certificate_images` 关联表或等价结构，并补充 SQLite/MySQL schema/migration 文档。
- Storage/Media: 继续使用 MinIO/S3 单桶与后端上传适配层；删除图片默认解除业务关联，不物理删除对象。
- API/Orval: 若请求/响应契约变化，必须同步 OpenAPI、Orval 生成物和 API 文档。
- Tests: 后端集成测试、前端组件测试、上传边界和旧数据兼容回归。
- Miniapp/Web catalog: 本 Change 不直接实现公开端多图浏览，仅保留主图和图片顺序数据结构供后续消费。
