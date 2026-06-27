## ADDED Requirements

### Requirement: SKU 弹窗商品视频上传状态与即时回显修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）「商品视频」区块的上传反馈缺陷。用户选择 MP4 后，系统 MUST 立即触发授权上传，MUST 在视频区内展示 `idle → uploading → uploaded / failed` 状态与可感知进度或等价文案，MUST 在上传成功后 **同一弹窗会话内** 立即追加文件卡片（`.sku-video-card` 或等价）展示文件名与大小，MUST 在上传失败时在视频区内展示明确错误。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略；MUST NOT 回归 BUG-0011 弹窗主体滚动能力。

#### Scenario: 选择 MP4 后立即触发上传

- **GIVEN** `admin` 或 `employee` 已打开 SKU 新增或编辑弹窗并位于「商品视频」区块
- **WHEN** 用户点击「上传视频」并选择合法 MP4
- **THEN** Web 客户端 MUST 立即触发 `POST /api/v1/admin/uploads/tile-videos`
- **AND** MUST NOT 要求用户先保存 SKU 后才开始上传

#### Scenario: 上传过程中展示可感知状态

- **GIVEN** 用户已选择 MP4 文件
- **WHEN** 上传正在进行
- **THEN** 「商品视频」区块 MUST 展示上传中状态（进度条、百分比或等价文案）
- **AND** 状态 MUST 经过 `idle → uploading → uploaded / failed`
- **AND** 上传中 SHOULD 禁用「上传视频」重复触发
- **AND** 上传中 MUST 禁止提交保存（对齐 `BrandFormModal` Logo 行为）

#### Scenario: 上传成功后即时回显视频预览

- **GIVEN** 视频上传接口返回 200 且含有效 `object_key` 与可访问 `url`
- **WHEN** 上传完成且用户未关闭弹窗
- **THEN** 「商品视频」区块 MUST 立即出现视频卡片，含 **16:9 视频预览/播放器**（`<video>`，`preload="metadata"`，`controls`）
- **AND** 卡片 MUST 展示文件名与大小（或占位「—」）
- **AND** 卡片 MUST 提供「移除」入口
- **AND** 区域 SHOULD 展示简短成功提示（如「视频已添加」）

#### Scenario: 上传失败在视频区内可见且可重试

- **GIVEN** 上传失败、网络异常或非 MP4 文件
- **WHEN** 上传流程结束
- **THEN** 「商品视频」区块 MUST 进入 `failed` 状态并展示明确错误信息
- **AND** MUST NOT 仅依赖弹窗顶部 notice 作为唯一反馈
- **AND** 用户 MUST 可重新选择文件重试

#### Scenario: 支持继续添加多个视频

- **GIVEN** 已有一个视频文件卡片
- **WHEN** 用户再次上传另一个 MP4 并成功
- **THEN** 新卡片 MUST 追加到列表
- **AND** 先前卡片 MUST 保留

#### Scenario: SKU 弹窗滚动与图片能力不回退

- **WHEN** 用户在使用修复后的 SKU 弹窗
- **THEN** `.modal-body` 垂直滚动 MUST 仍可用（BUG-0011）
- **AND** SKU 图片上传与主图逻辑 MUST 无回归
- **AND** MUST NOT 变更 API 请求参数或响应结构

#### Scenario: Design System 约束

- **WHEN** 修复修改 SKU 弹窗视频上传控件
- **THEN** 进度条、按钮禁用态、错误与成功文案 MUST 使用 semantic token 或既有管理端样式
- **AND** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部色值
