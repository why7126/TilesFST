---
created_at: 2026-07-22 09:24:00
updated_at: 2026-07-22 09:24:00
---

# banner-management Specification Delta

## ADDED Requirements

### Requirement: 管理端 Banner 图片预览

Web 管理端 Banner 管理页面 MUST 在列表缩略图与新建/编辑弹窗中提供可用于运营确认的 Banner 图片预览。预览 MUST 优先保证图片主体与关键信息完整可识别，MUST 避免因固定容器、裁切型 `object-fit`、父容器 overflow 或表格/弹窗高度限制导致关键文字、Logo 或主体内容被裁掉。预览背景、边框、占位和空白区域 MUST 使用管理端 Design System semantic token。该要求 MUST NOT 改变 Banner API、数据库表结构、对象存储策略或展示端真实投放裁切策略。

#### Scenario: 列表缩略图完整预览

- **WHEN** 管理端用户访问 `/admin/banners` 列表
- **AND** 列表项存在 Banner 图片
- **THEN** 图片缩略图 MUST 完整呈现图片主体
- **AND** MUST NOT 裁掉关键文字、Logo 或主体内容
- **AND** 图片加载或比例变化 MUST NOT 改变表格行高、分页、筛选或操作按钮布局。

#### Scenario: 弹窗图片完整预览

- **WHEN** 管理端用户新建或编辑 Banner
- **AND** 弹窗中展示已选图片或上传后的图片
- **THEN** 弹窗预览 MUST 完整呈现当前图片
- **AND** 上传后预览与编辑回显 MUST 使用一致展示策略
- **AND** MUST NOT 遮挡表单字段、上传控件、弹窗滚动区域或底部保存按钮。

#### Scenario: 多比例和多来源图片预览

- **WHEN** Banner 图片为横幅图、方图、竖图或超宽图
- **OR** 图片来源为自定义上传图、品牌 Logo、SKU 主图或 SKU 图库图
- **THEN** 管理端预览 MUST 使用一致且可预期的适配策略
- **AND** MUST 避免明显拉伸、压扁或比例失真
- **AND** MUST 保留图片主体可识别性。

#### Scenario: 修复范围不影响业务配置

- **WHEN** 管理端用户在修复后的 Banner 弹窗中保存配置
- **THEN** Banner 新建、编辑、保存、上线、下线、排序和跳转类型配置 MUST 保持既有行为
- **AND** API 请求与响应契约 MUST 不因本预览修复发生变化。
