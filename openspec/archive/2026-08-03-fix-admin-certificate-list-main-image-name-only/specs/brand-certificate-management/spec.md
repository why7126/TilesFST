## MODIFIED Requirements

### Requirement: 管理端品牌证书页面

系统 MUST 在管理端提供 `/admin/brand-certificates` 页面。页面 MUST 作为独立一级品牌证书管理页，左侧导航 MUST 独立高亮“品牌证书”，并 MUST 提供指标概览、即时筛选、证书列表、分页、新增/编辑弹窗、预览、显示/隐藏和删除入口。页面 MUST 不展示品牌摘要栏或品牌详情面包屑。证书列表中的证书字段 MUST 仅展示证书主图和证书名称；当无主图或主图不可读时 MUST 展示稳定占位并保持证书名称可读。证书列表的证书字段 MUST NOT 展示图片名称、文件名称、对象 key、原始 URL、上传控件内部文案或文件就绪文案。

#### Scenario: 打开品牌证书页面

- **WHEN** 管理端用户访问 `/admin/brand-certificates`
- **THEN** 左侧导航 MUST 高亮“品牌证书”
- **AND** 页面 MUST 展示标题、说明、新增证书按钮、四个指标卡、筛选区、列表和分页
- **AND** 页面 MUST NOT 展示品牌摘要栏

#### Scenario: 品牌快捷入口筛选

- **WHEN** 用户从品牌列表页点击某品牌的证书快捷入口
- **THEN** 系统 MUST 跳转到 `/admin/brand-certificates?brand_id={brand_id}`
- **AND** 品牌证书页 MUST 自动应用所属品牌筛选

#### Scenario: 筛选即时生效

- **WHEN** 用户输入关键词或改变下拉筛选
- **THEN** 关键词 MUST 在 300ms 防抖后生效
- **AND** 下拉筛选 MUST 立即生效
- **AND** 当前页 MUST 重置为第 1 页
- **AND** 筛选条件 MUST 同步到 URL Query

#### Scenario: 分页结构

- **WHEN** 页面展示分页
- **THEN** 左侧 MUST 显示 `共 x 个证书`
- **AND** 右侧 MUST 显示上一页、页码、下一页和每页显示 20/50/100 条

#### Scenario: 证书列表字段隐藏文件名噪音

- **GIVEN** 品牌证书列表项包含证书主图、证书名称、图片文件名、证书文件名、对象 key 或原始 URL
- **WHEN** 管理端用户查看 `/admin/brand-certificates` 列表
- **THEN** 证书字段 MUST 展示证书主图和证书名称
- **AND** 证书字段 MUST NOT 展示图片名称、文件名称、对象 key、原始 URL、上传组件内部文案或文件就绪文案
- **AND** 列表排序、筛选、分页和编辑入口 MUST 保持可用

#### Scenario: 证书列表无主图占位

- **GIVEN** 品牌证书列表项没有可展示主图
- **WHEN** 管理端用户查看证书字段
- **THEN** 页面 MUST 展示稳定占位
- **AND** 证书名称 MUST 仍清晰可读
- **AND** 页面 MUST NOT 使用图片文件名、证书文件名、对象 key 或原始 URL 替代证书名称
