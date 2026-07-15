## Why

当前品牌主数据仅维护品牌名称、Logo 与介绍，无法结构化管理质量体系、检测报告、绿色建材、荣誉资质等品牌证书，也无法支撑证书有效期治理和店主端可展示数据。REQ-0038 已评审通过，需要新增独立的管理端品牌证书能力，并让证书文件走既有后端鉴权与 MinIO 单桶上传链路。

## What Changes

- 新增管理端“品牌证书”一级页面，支持跨品牌查询、指标概览、筛选、分页、预览、编辑、显示/隐藏和删除。
- 新增品牌证书数据模型与管理 API，建立 `brand 1:N brand_certificate` 关系，并由服务端返回有效状态。
- 新增证书文件上传、回显和受控读取要求，支持 JPG、PNG、WebP、PDF，单文件最大 20MB。
- 新增证书权限点、审计记录、软删除、同品牌名称唯一性和删除品牌前证书约束。
- 新增管理端 UI 验收门禁，覆盖列表一致性、弹窗 CSS 层叠、媒体上传链路和原型冲突处理。
- 首版不实现店主端证书展示页面、审批流、OCR、批量操作、导出、多语言和 SKU 证书绑定。

## Capabilities

### New Capabilities

- `brand-certificate-management`: 管理端品牌证书主数据、API、数据模型、文件上传、展示控制、权限审计和 UI 验收能力。

### Modified Capabilities

无。该能力依赖 `brand-management` 的品牌主数据与 `object-storage` 的单桶上传/受控读取要求，但不修改既有 spec 的规范行为。

## Impact

- 影响后端：新增品牌证书模块、Schema、Repository、Service、Router、权限点、错误码和审计写入。
- 影响数据库：新增 `brand_certificates` 表或等价 schema / migration，并同步 SQLite/MySQL 初始化与文档。
- 影响 API：新增 `/api/v1/admin/brand-certificates` 及 show/hide/delete 等接口，需同步 OpenAPI、Orval、API 文档和集成测试。
- 影响 Web 管理端：新增 `/admin/brand-certificates` 页面、导航入口、品牌列表快捷入口、证书弹窗、上传控件和预览交互。
- 影响对象存储：证书文件必须经后端授权写入 MinIO 单桶，不允许前端直连未授权对象存储。
- 影响测试与验收：需要补充 pytest、Vitest/Testing Library、OpenSpec 校验、Docker Web `:3000` 上传边界验证和原型/DS 横切验收。
- 不影响小程序首版实现；店主端展示页面只保留数据基础，不在本 Change 实现。
