## ADDED Requirements

### Requirement: 品牌管理 UI 一致性修复

Web 客户端 MUST 修复 `/admin/brands` 品牌管理页的 UI 一致性缺陷，使品牌列表分页与用户管理页分页保持一致，并使新增/编辑品牌弹窗的 Logo 选择文件控件与管理端表单和图片上传控件风格保持一致。修复 MUST NOT 修改品牌 API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: 品牌列表分页对齐用户管理页

- **WHEN** 管理员或运营人员分别访问 `/admin/brands` 与 `/admin/users`
- **THEN** 两个页面底部分页区域的布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 保持一致
- **AND** 品牌页 MUST NOT 使用与用户管理页割裂的 `page-left` / `brand-pagination-right` 主视觉结构

#### Scenario: 品牌分页功能不回退

- **WHEN** 用户在品牌列表页执行上一页、下一页或每页显示切换
- **THEN** 分页功能 MUST 继续可用
- **AND** 每页显示切换 MUST 将页码重置为 1

#### Scenario: 品牌跳页能力一致呈现

- **WHEN** 品牌列表保留跳页输入能力
- **THEN** 跳页输入 MUST 作为统一分页布局的可选扩展呈现
- **AND** MUST NOT 破坏与用户管理页分页的主视觉一致性

#### Scenario: 品牌 Logo 文件选择控件对齐管理端表单

- **WHEN** 用户打开新增或编辑品牌弹窗
- **THEN** 「品牌Logo」文件选择控件 MUST 与弹窗内输入框、按钮和用户管理弹窗头像上传控件保持一致的视觉层级
- **AND** 文件选择入口 MUST 使用明确按钮或可访问 label
- **AND** MUST NOT 展示浏览器默认 file input 皮相

#### Scenario: Logo 空态和预览态

- **WHEN** 品牌 Logo 尚未上传
- **THEN** 控件 MUST 展示统一空态说明和上传入口
- **WHEN** 品牌 Logo 已上传
- **THEN** 控件 MUST 展示 Logo 预览、文件更换入口和帮助文案
- **AND** MUST NOT 挤压弹窗布局或破坏头尾固定结构

#### Scenario: 品牌管理功能保持可用

- **WHEN** 用户执行查询、重置、分页、新增品牌、编辑品牌、上传 Logo 或保存品牌
- **THEN** 原有功能 MUST 保持可用
- **AND** 前端 MUST 继续使用既有品牌 API 与 Logo 上传 API
