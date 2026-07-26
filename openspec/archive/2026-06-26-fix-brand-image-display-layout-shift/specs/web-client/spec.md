## ADDED Requirements

### Requirement: 品牌 Logo 展示与提示布局修复

Web 客户端 MUST 修复 `/admin/brands` 品牌 Logo 展示失败与状态提示导致页面上下波动的问题。品牌列表和品牌编辑弹窗 MUST 使用后端返回的可访问媒体 URL 正常展示/回显 Logo；品牌页自动消失状态提示 MUST NOT 通过插入普通文档流节点推挤页面主体。修复 MUST 保持品牌查询、分页、新增、编辑、启用、停用、删除等既有功能可用，并 MUST 遵守 Design System 语义样式约束。

#### Scenario: 品牌列表展示已上传 Logo

- **GIVEN** 品牌记录存在可访问 `logo_url` 或等价预览 URL
- **WHEN** `admin` 或 `employee` 访问 `/admin/brands`
- **THEN** 品牌列 MUST 展示已上传 Logo 图片
- **AND** 无 Logo 的品牌 MUST 保持首字/缩写占位
- **AND** 图片加载失败时 MUST 保持稳定单元格尺寸和空态，不得造成表格布局跳动

#### Scenario: 品牌编辑弹窗回显 Logo

- **GIVEN** 品牌记录存在可访问 Logo URL
- **WHEN** 用户点击「编辑」打开品牌弹窗
- **THEN** 「品牌Logo」区域 MUST 展示当前 Logo 预览
- **AND** 更换 Logo 后预览 MUST 即时更新
- **AND** 保存后再次打开弹窗 MUST 回显最新 Logo

#### Scenario: 品牌状态变更提示不推挤页面

- **WHEN** 用户在 `/admin/brands` 执行启用或停用品牌
- **THEN** 系统 SHOULD 展示成功或失败提示
- **AND** 提示出现和消失 MUST NOT 改变 page-header、指标卡、筛选区、表格或分页区域的纵向位置
- **AND** 提示 MUST 使用固定 toast、稳定提示槽或等价不推挤主体内容的方式

#### Scenario: 品牌创建更新删除提示不推挤页面

- **WHEN** 用户创建、更新或删除品牌并触发提示
- **THEN** 提示出现和消失 MUST NOT 造成页面主体上下位移
- **AND** 弹窗内表单错误 MAY 使用 inline 错误文案
- **AND** inline 错误文案 MUST NOT 影响列表页主体稳定性

#### Scenario: 品牌管理功能不回退

- **WHEN** 用户执行查询、重置、分页、每页显示切换、新增、编辑、启用、停用或删除品牌
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌
- **AND** `store_owner` MUST NOT 访问管理端品牌维护能力

#### Scenario: Design System 约束

- **WHEN** 修复修改 Web UI 样式
- **THEN** 新增或修改样式 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式
- **AND** MUST NOT 新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式
