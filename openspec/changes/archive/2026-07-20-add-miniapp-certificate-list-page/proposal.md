## Why

小程序底部 TabBar 已包含「证书」，但当前页面仍是建设中占位，用户无法集中查看企业可公开展示的品牌资质、检测报告和环保认证。REQ-0057 已评审通过，需要将证书 Tab 升级为公开证书聚合列表页，复用管理端证书主数据与展示控制，增强选砖过程中的品牌信任。

## What Changes

- 新增小程序公开证书列表页能力，覆盖 `pages/certificates/index` 的真实列表、搜索筛选、加载更多、空/错状态和证书预览。
- 新增公开证书列表 API 或等价后端能力，仅返回未删除、前台展示且所属品牌允许公开的证书。
- 证书卡片展示证书名称、所属品牌、类型、编号或发证机构、有效期/有效状态、图片缩略图或 PDF 占位。
- 证书文件预览必须使用后端受控 URL 或等价安全引用，不暴露 MinIO 原始对象 Key 或内部字段。
- 小程序验收必须覆盖全局自定义导航、胶囊 reserve、页面 offset、320/375/430 pt 视口和真机 evidence 状态。
- 不包含管理端证书新增、编辑、上传、显示/隐藏、删除、证书详情页、OCR、电子签章或证书真伪校验。

## Capabilities

### New Capabilities

- `miniapp-certificate-list-page`: 小程序公开证书聚合列表页，支持公开证书读取、列表展示、搜索筛选、分页加载、文件预览、异常状态、导航视口验收和行为埋点。

### Modified Capabilities

- 无。

## Impact

- 影响端：微信小程序、后端 API、OpenAPI / Orval、测试。
- 可能涉及源码：
  - `src/miniapp/pages/certificates/*`
  - `src/miniapp/services/api.*`
  - `src/miniapp/app.json` 或等价页面/TabBar 配置
  - `src/backend/app/api/v1/miniapp.py`
  - `src/backend/app/services/miniapp_home_service.py` 或新增 miniapp certificate service
  - `src/backend/app/repositories/brand_certificate_repository.py` 或等价公开查询方法
  - `src/backend/app/schemas/miniapp_home.py` 或新增 miniapp certificate schema
- API：新增或复用 `GET /api/v1/miniapp/certificates`；必须使用统一响应 envelope。
- 数据库：原则上复用 `brand_certificates` 和 `brands`，不新增表；如实现发现需新增索引或字段，必须同步 schema、数据库文档和测试。
- 对象存储：不新增上传能力；文件读取必须继续遵守 MinIO 单桶和后端受控 URL 策略。
- 管理端：无功能变更。
- Orval：若新增或修改后端 API，必须同步 OpenAPI / Orval。
- 测试：补充后端公开 API 测试、小程序静态/页面状态测试、文件预览降级测试和设备/视口 evidence。
