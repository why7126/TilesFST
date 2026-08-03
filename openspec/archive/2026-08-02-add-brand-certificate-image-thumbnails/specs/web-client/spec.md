## MODIFIED Requirements

### Requirement: 品牌 Logo 展示与提示布局修复

Web 客户端 MUST 修复 `/admin/brands` 品牌 Logo 展示失败与状态提示导致页面上下波动的问题。品牌列表和品牌编辑弹窗 MUST 使用后端返回的可访问媒体 URL 正常展示/回显 Logo；品牌列表和小图预览 SHOULD 优先使用后端受控真实缩略图，放大预览 SHOULD 使用原图或原始受控 URL；品牌页自动消失状态提示 MUST NOT 通过插入普通文档流节点推挤页面主体。修复 MUST 保持品牌查询、分页、新增、编辑、启用、停用、删除等既有功能可用，并 MUST 遵守 Design System 语义样式约束。

#### Scenario: 品牌列表展示已上传 Logo
- **GIVEN** 品牌记录存在可访问 `logo_url`、`thumbnail_url` 或等价预览 URL
- **WHEN** `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 品牌列 MUST 展示已上传 Logo 图片
- **AND** 品牌列小图 SHOULD 优先使用缩略图
- **AND** 无 Logo 的品牌 MUST 保持首字/缩写占位
- **AND** 图片加载失败时 MUST 保持稳定单元格尺寸和空态，不得造成表格布局跳动。

#### Scenario: 品牌编辑弹窗回显 Logo
- **GIVEN** 品牌记录存在可访问 Logo URL
- **WHEN** 用户点击「编辑」打开品牌弹窗
- **THEN** 「品牌Logo」区域 MUST 展示当前 Logo 预览
- **AND** 小预览 SHOULD 优先展示缩略图
- **AND** 更换 Logo 后预览 MUST 即时更新
- **AND** 保存后再次打开弹窗 MUST 回显最新 Logo。

#### Scenario: 品牌缩略图回退
- **GIVEN** 品牌 Logo 原图存在但缩略图缺失、损坏或不可读
- **WHEN** Web 客户端展示品牌列表或品牌编辑小预览
- **THEN** 客户端 MUST 回退原图或首字占位
- **AND** MUST NOT 显示浏览器破图、空字符串、`null`、`undefined` 或接口字段名
- **AND** 回退提示 MUST NOT 推挤页面主体布局。

#### Scenario: 品牌状态变更提示不推挤页面
- **WHEN** 用户在 `/admin/brands` 执行启用或停用品牌
- **THEN** 系统 SHOULD 展示成功或失败提示
- **AND** 提示出现和消失 MUST NOT 改变 page-header、指标卡、筛选区、表格或分页区域的纵向位置
- **AND** 提示 MUST 使用固定 toast、稳定提示槽或等价不推挤主体内容的方式。

#### Scenario: Design System 约束
- **WHEN** 修复修改 Web UI 样式
- **THEN** 新增或修改样式 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式
- **AND** MUST NOT 新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式。

### Requirement: 品牌 Logo 上传进度反馈

Web 客户端 MUST 修复 `/admin/brands` 编辑品牌弹窗 Logo 更换流程中的上传反馈缺陷。用户选择新 Logo 后，系统 MUST 立即触发上传，MUST 在弹窗内展示上传进度条、百分比或等价可感知反馈，并 MUST 在上传成功后更新 Logo 预览与待保存的 `logo_object_key`。上传成功后预览 SHOULD 使用后端返回的缩略图或等价小图 URL；上传失败时 MUST 提供明确错误和重试入口。该修复 MUST 保持品牌管理既有功能、权限边界和 Design System 约束。

#### Scenario: 选择 Logo 后触发上传
- **GIVEN** `admin` 或 `employee` 已打开品牌编辑弹窗
- **WHEN** 用户点击「更换 Logo」并选择 JPG、PNG 或 WebP 图片
- **THEN** Web 客户端 MUST 立即触发品牌 Logo 上传流程
- **AND** 上传请求 MUST 使用既有后端授权上传接口
- **AND** MUST NOT 要求用户先保存品牌后才开始上传文件。

#### Scenario: 上传过程中展示进度反馈
- **GIVEN** 用户已选择 Logo 图片
- **WHEN** 上传正在进行
- **THEN** 弹窗内 MUST 展示进度条、百分比或等价可感知上传反馈
- **AND** 进度反馈 MUST 位于 Logo 控件附近
- **AND** 上传过程中「更换 Logo」入口 SHOULD 展示上传中状态或被禁用，避免重复触发。

#### Scenario: 上传成功后更新预览和保存对象 Key
- **GIVEN** 品牌 Logo 上传接口返回成功
- **WHEN** 响应包含新的 `object_key`、可访问 URL 和可用缩略图引用
- **THEN** 弹窗中的 Logo 预览 MUST 更新为新图片或其缩略图
- **AND** 后续保存品牌时 MUST 使用新的 `logo_object_key`
- **AND** 保存后再次打开编辑弹窗 MUST 回显最新 Logo。

#### Scenario: 上传失败可见且可重试
- **GIVEN** Logo 上传接口返回失败、网络异常或文件类型不合法
- **WHEN** 上传流程结束
- **THEN** 弹窗内 MUST 展示明确错误信息
- **AND** 用户 MUST 可以重新选择图片重试
- **AND** 失败时 MUST NOT 将旧 Logo 静默替换为无效预览或错误对象 Key。
