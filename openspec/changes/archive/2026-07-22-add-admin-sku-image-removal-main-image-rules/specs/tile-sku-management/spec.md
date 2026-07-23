## MODIFIED Requirements

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；MUST NOT 通过 PUT 直接修改 `status`（使用 publish/unpublish）。PUT MUST 要求 `reference_price` 非 null（含 `0.0`）；**MUST NOT** 因 surface_finish 留空而拒绝更新。若 PUT 变更 `spec_id` 至新规格，新规格 MUST 为 `ENABLED`；若保留原 `spec_id` 且该规格已 DISABLED，MAY 允许更新非规格字段。PUT 接收图片列表时 MUST 将提交的 images 视为该 SKU 的完整图片关联事实源；被移除图片不应继续关联到该 SKU。系统 MUST 保证同一 SKU 至多一张图片为主图，并按提交后的 `sort_order` 回填图片顺序。

#### Scenario: 更新 SKU 资料

- **WHEN** PUT 合法字段且 `sku_code` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后 SKU 对象
- **AND** `updated_at` MUST 已更新
- **AND** 若含 `spec_id`，`size` MUST 同步

#### Scenario: 更新缺少参考价格被拒绝

- **WHEN** PUT 请求将 `reference_price` 置为 null 或未提供合法数值
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: 更新 SKU 图片移除关联

- **WHEN** PUT 请求提交的 images 列表不包含某张原已关联图片
- **THEN** 系统 MUST 在保存后解除该 SKU 与该图片的关联
- **AND** 再次 GET SKU 详情时 MUST NOT 返回该图片
- **AND** 系统 MUST NOT 因解除关联而物理删除 MinIO 对象文件

#### Scenario: 更新 SKU 图片主图唯一与顺序

- **WHEN** PUT 请求提交多张图片且其中一张 `is_main=true`
- **THEN** 保存后同一 SKU MUST 至多一张图片 `is_main=1`
- **AND** 再次 GET SKU 详情时主图 MUST 位于图片列表第一位
- **AND** 图片 `sort_order` MUST 可按提交后的顺序回填

#### Scenario: 更新 SKU 移除全部图片

- **WHEN** PUT 请求提交空 images 列表
- **THEN** 系统 MUST 保存该 SKU 为无图片关联状态
- **AND** 再次 GET SKU 详情时 images MUST 为空
- **AND** 素材完整度 MUST 沿用缺图片/缺主图规则

### Requirement: SKU 图片与视频上传

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。

#### Scenario: 上传 SKU 图片成功

- **WHEN** `admin` 或 `employee` 上传合法图片
- **THEN** 系统返回 object_key
- **AND** 创建/更新 SKU 时可关联图片并设置 `is_main`

#### Scenario: 非法 MIME 被拒绝

- **WHEN** 上传不允许的文件类型
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: 移除非主图图片

- **WHEN** 用户在 SKU 编辑弹窗中移除非主图图片
- **THEN** 当前主图 MUST 保持不变
- **AND** 剩余图片 MUST 重新生成连续 `sort_order`
- **AND** 保存后再次打开弹窗，被移除图片 MUST 不再出现

#### Scenario: 设置主图自动前置

- **WHEN** 用户在 SKU 编辑弹窗中点击某张非主图图片的「设为主图」
- **THEN** 该图片 MUST 立即成为唯一主图
- **AND** 该图片 MUST 移动到图片列表第一位
- **AND** 保存 payload 中该图片 MUST 为 `is_main=true` 且 `sort_order=0`

#### Scenario: 移除当前主图自动兜底

- **WHEN** 用户在 SKU 编辑弹窗中移除当前主图且移除前后一张图片存在
- **THEN** 移除前后一张图片 MUST 自动成为新主图
- **AND** 新主图 MUST 在弹窗内即时显示在图片列表第一位

#### Scenario: 移除最后位置主图自动兜底

- **WHEN** 用户移除当前主图且该主图已是移除前最后一张图片，但移除后仍有其它图片
- **THEN** 移除后列表第一张图片 MUST 自动成为新主图
- **AND** 新主图 MUST 在弹窗内即时显示在图片列表第一位

#### Scenario: 移除全部商品图片

- **WHEN** 用户移除 SKU 编辑弹窗中的最后一张商品图片
- **THEN** 图片列表 MUST 为空
- **AND** 弹窗 MUST 不再显示「主图」标签
- **AND** 「继续添加图片」入口 MUST 仍可用

#### Scenario: 图片上传状态不因移除能力回归

- **WHEN** 用户在同一 SKU 编辑弹窗会话中上传图片
- **THEN** 上传过程 MUST 体现 `idle→uploading→done/failed` 或等价状态机
- **AND** 上传成功的图片 MUST 即时回显并可继续执行「设为主图」与「移除」
- **AND** 上传失败 MUST 在上传控件或图片区域内展示错误
