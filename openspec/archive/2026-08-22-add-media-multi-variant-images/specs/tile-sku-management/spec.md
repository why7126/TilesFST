## MODIFIED Requirements

### Requirement: 管理端 SKU 列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页、关键词、品牌、类目、状态和素材完整度筛选，并保持既有排序、权限、错误响应、加载态、空态、失败态和行操作行为。管理端 SKU 列表项存在主图时，响应 MUST 提供 `main_image_thumbnail_url`、`main_image_display_url`、`main_image_original_url` 或等价多规格字段，并保留 `main_image_url` 兼容语义。管理端 SKU 列表图片展示 MUST 优先使用 `thumbnail` 规格，详情、编辑、上传预览和放大预览场景 SHOULD 使用 `display` 或 `original` 规格。

#### Scenario: SKU 列表返回主图多规格 URL

- **GIVEN** SKU 列表项存在主图对象
- **WHEN** 管理端请求 `GET /api/v1/admin/tile-skus`
- **THEN** 响应项 MUST 包含主图 `thumbnail` URL
- **AND** 响应项 SHOULD 包含主图 `display` URL 与 `original` URL 或等价语义字段
- **AND** 响应项 MUST 保留旧字段兼容或说明替代关系
- **AND** 响应 MUST NOT 暴露未授权对象存储地址、bucket 名称、access key、secret key 或原始 object key。

#### Scenario: SKU 列表主图规格 fallback

- **GIVEN** SKU 列表项存在原图但 `thumbnail` 不可用
- **WHEN** 管理端渲染 SKU 列表图片
- **THEN** 页面 MUST 按统一 fallback 顺序回退到 `display`、原图或无图占位
- **AND** 页面 MUST NOT 显示浏览器默认破图
- **AND** 表格行高、分页、筛选和操作列布局 MUST 保持稳定。

### Requirement: 管理端 SKU 创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。请求 MUST 接受 SKU 基础字段、图片列表、视频列表和 `save_mode`。当请求包含图片时，系统 MUST 通过媒体服务或对象存储适配层保留 `original`，并生成或调度生成 `thumbnail` 与 `display`。创建响应 SHOULD 返回图片多规格 URL 或可在后续 GET 中稳定获得多规格 URL。

#### Scenario: 创建 SKU 图片生成多规格资源

- **WHEN** 管理端创建 SKU 并提交合法图片
- **THEN** 系统 MUST 保留图片 `original`
- **AND** 系统 MUST 生成或调度生成 `thumbnail` 与 `display`
- **AND** 创建或后续详情响应 SHOULD 返回多规格 URL 语义
- **AND** 生成失败 MUST 有可诊断错误摘要或 warning，不得暴露内部路径或存储凭据。

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；提交图片列表时，系统 MUST 保持图片多规格资源与 SKU 关联一致。管理端 SKU 表单在上传、编辑或保存后 MUST 能同会话回显媒体入口，并 SHOULD 展示可理解的派生生成状态或 fallback。

#### Scenario: 更新 SKU 图片保持多规格关联

- **WHEN** PUT 请求提交图片列表
- **THEN** 保存后同一 SKU 的图片关联 MUST 能追溯到对应 `thumbnail`、`display`、`original`
- **AND** 被移除图片不应继续关联到该 SKU
- **AND** 系统 MUST NOT 因解除关联而物理删除 MinIO / 对象存储对象
- **AND** 再次 GET SKU 详情时 MUST 返回稳定的多规格 URL 或明确 fallback。
