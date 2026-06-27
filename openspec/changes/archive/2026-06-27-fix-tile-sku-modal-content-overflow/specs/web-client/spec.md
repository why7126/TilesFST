## ADDED Requirements

### Requirement: SKU 弹窗内容溢出与滚动修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的内容溢出缺陷：当表单内容高度超过视口允许的最大弹窗高度时，弹窗 MUST 保持页眉与页脚固定可见，且主体内容区 MUST 提供垂直滚动以访问全部字段与操作按钮。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: 矮视口下弹窗主体可滚动

- **WHEN** 已登录 `admin` 或 `employee` 在视口高度 ≤900px 时打开「新增SKU」或「编辑SKU」弹窗
- **THEN** 弹窗 `.modal-body`（或等价内容 wrapper）MUST 支持垂直滚动
- **AND** 用户 MUST 能滚动至 SKU 图片、SKU 视频与备注说明字段

#### Scenario: 页眉页脚固定可见

- **WHEN** 弹窗内容超出可视高度且用户滚动主体区域
- **THEN** 标题、副标题与关闭按钮 MUST 保持可见
- **AND** 「取消 / 保存草稿 / 创建SKU（或保存）」footer MUST 保持可见且可点击

#### Scenario: 弹窗尺寸约束不变

- **WHEN** 用户打开 SKU 弹窗
- **THEN** 弹窗宽度 MUST 仍为 880px（`max-width: 100%` 响应式除外）
- **AND** 弹窗 `max-height` MUST NOT 超过视口（如 `calc(100vh - 64px)`）

#### Scenario: 关闭交互不回退

- **WHEN** 用户在弹窗内滚动
- **THEN** ESC、点击遮罩、点击 × MUST 仍可正常关闭弹窗
- **AND** MUST NOT 因滚动导致意外关闭

#### Scenario: SKU 表单功能保持可用

- **WHEN** 用户在修复后的弹窗中填写并保存
- **THEN** 保存草稿、创建 SKU、编辑更新、图片/视频上传 MUST 继续可用
- **AND** MUST NOT 变更 API 请求参数或响应结构
