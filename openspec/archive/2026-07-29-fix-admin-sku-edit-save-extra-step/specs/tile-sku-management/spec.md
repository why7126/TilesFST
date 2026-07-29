## MODIFIED Requirements

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；MUST NOT 通过 PUT 直接修改 `status`（使用 publish/unpublish）。PUT MUST 要求 `reference_price` 非 null（含 `0.0`）；**MUST NOT** 因 surface_finish 留空而拒绝更新。若 PUT 变更 `spec_id` 至新规格，新规格 MUST 为 `ENABLED`；若保留原 `spec_id` 且该规格已 DISABLED，MAY 允许更新非规格字段。PUT 接收图片列表时 MUST 将提交的 images 视为该 SKU 的完整图片关联事实源；被移除图片不应继续关联到该 SKU。系统 MUST 保证同一 SKU 至多一张图片为主图，并按提交后的 `sort_order` 回填图片顺序。管理端 SKU 表单在创建、保存草稿或编辑成功后 MUST 直接关闭并刷新列表，MUST NOT 在弹窗内额外展示任务追踪反馈。

#### Scenario: 更新 SKU 资料

- **WHEN** PUT 合法字段且 `sku_code` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后 SKU 对象
- **AND** `updated_at` MUST 已更新
- **AND** 若含 `spec_id`，`size` MUST 同步

#### Scenario: 编辑弹窗保存成功直接关闭

- **WHEN** 管理端 SKU 编辑弹窗提交合法修改且更新接口返回成功
- **THEN** 弹窗 MUST 直接关闭
- **AND** 管理端 MUST 刷新 SKU 列表
- **AND** 弹窗内 MUST NOT 显示“SKU 已更新”任务追踪 feedback 或复制追踪 ID 入口

#### Scenario: 新增弹窗创建成功直接关闭

- **WHEN** 管理端 SKU 新增弹窗提交合法创建或保存草稿且接口返回成功
- **THEN** 弹窗 MUST 直接关闭
- **AND** 管理端 MUST 刷新 SKU 列表
- **AND** 弹窗内 MUST NOT 显示任务追踪 feedback 或复制追踪 ID 入口

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
