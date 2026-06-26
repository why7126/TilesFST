## ADDED Requirements

### Requirement: 品牌 Logo 上传进度反馈

Web 客户端 MUST 修复 `/admin/brands` 编辑品牌弹窗 Logo 更换流程中的上传反馈缺陷。用户选择新 Logo 后，系统 MUST 立即触发上传，MUST 在弹窗内展示上传进度条、百分比或等价可感知反馈，并 MUST 在上传成功后更新 Logo 预览与待保存的 `logo_object_key`。上传失败时 MUST 提供明确错误和重试入口。该修复 MUST 保持品牌管理既有功能、权限边界和 Design System 约束。

#### Scenario: 选择 Logo 后触发上传

- **GIVEN** `admin` 或 `employee` 已打开品牌编辑弹窗
- **WHEN** 用户点击「更换 Logo」并选择 JPG、PNG 或 WebP 图片
- **THEN** Web 客户端 MUST 立即触发品牌 Logo 上传流程
- **AND** 上传请求 MUST 使用既有后端授权上传接口
- **AND** MUST NOT 要求用户先保存品牌后才开始上传文件

#### Scenario: 上传过程中展示进度反馈

- **GIVEN** 用户已选择 Logo 图片
- **WHEN** 上传正在进行
- **THEN** 弹窗内 MUST 展示进度条、百分比或等价可感知上传反馈
- **AND** 进度反馈 MUST 位于 Logo 控件附近
- **AND** 上传过程中「更换 Logo」入口 SHOULD 展示上传中状态或被禁用，避免重复触发

#### Scenario: 上传成功后更新预览和保存对象 Key

- **GIVEN** 品牌 Logo 上传接口返回成功
- **WHEN** 响应包含新的 `object_key` 和可访问 URL
- **THEN** 弹窗中的 Logo 预览 MUST 更新为新图片
- **AND** 后续保存品牌时 MUST 使用新的 `logo_object_key`
- **AND** 保存后再次打开编辑弹窗 MUST 回显最新 Logo

#### Scenario: 上传失败可见且可重试

- **GIVEN** Logo 上传接口返回失败、网络异常或文件类型不合法
- **WHEN** 上传流程结束
- **THEN** 弹窗内 MUST 展示明确错误信息
- **AND** 用户 MUST 可以重新选择图片重试
- **AND** 失败时 MUST NOT 将旧 Logo 静默替换为无效预览或错误对象 Key

#### Scenario: 同一文件可重新选择

- **GIVEN** 用户已选择过某个 Logo 文件
- **WHEN** 用户再次选择同一个文件
- **THEN** Web 客户端 SHOULD 能再次触发上传或明确提示当前文件已选择
- **AND** 文件 input MUST NOT 因 value 未重置导致用户无法重试

#### Scenario: 品牌管理功能不回退

- **WHEN** 用户执行查询、重置、分页、每页显示切换、新增、编辑、启用、停用或删除品牌
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌
- **AND** `store_owner` MUST NOT 访问管理端品牌维护能力

#### Scenario: Design System 约束

- **WHEN** 修复修改品牌编辑弹窗 Logo 上传控件
- **THEN** 进度条、按钮、错误文案和预览态 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式
- **AND** MUST NOT 新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式
