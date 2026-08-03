## MODIFIED Requirements

### Requirement: 微信小程序品牌主页信息区
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。品牌主页信息区的小图展示 SHOULD 优先使用后端受控真实缩略图；大图预览、分享图或需要高清资源的入口 MAY 使用原图或等价安全引用。

#### Scenario: 品牌主页加载公开信息
- **WHEN** 用户通过 `brandId` 访问品牌主页/详情页
- **THEN** 小程序 SHALL 加载该品牌的公开信息
- **AND** 页面上半部分 SHALL 展示品牌图片或 Logo、品牌名称和品牌介绍
- **AND** 品牌图片或 Logo 小图 SHOULD 优先使用缩略图
- **AND** 响应 SHALL NOT 暴露后台内部字段、对象存储原始 key、内部备注、Authorization header、Cookie 或敏感配置。

#### Scenario: 品牌信息降级
- **WHEN** 品牌主图缩略图缺失、Logo 缩略图缺失、原图缺失、图片加载失败或品牌介绍为空
- **THEN** 小程序 SHALL 使用统一占位、回退到可用图片、隐藏区域或展示简短兜底文案
- **AND** 页面 SHALL NOT 展示破图、异常空字段或错误字段名。

#### Scenario: 品牌不可访问
- **WHEN** `brandId` 缺失、非法、品牌不存在、品牌禁用、品牌下架或品牌不可公开
- **THEN** 小程序 SHALL 展示可恢复错误态
- **AND** 页面 SHALL 提供返回或回首页能力
- **AND** 页面 SHALL NOT 白屏。

### Requirement: 品牌主页证书 Tab
证书 Tab SHALL 展示当前品牌关联且可公开的证书列表，并过滤不可展示证书和内部字段。证书 Tab 图片小图 SHOULD 优先使用后端受控真实缩略图；图片预览或证书详情 SHALL 使用原图、原文件或等价安全引用。

#### Scenario: 当前品牌证书列表
- **WHEN** 用户查看品牌主页证书 Tab
- **THEN** 小程序 SHALL 仅展示当前品牌关联且可公开的证书
- **AND** 证书项 SHALL 展示证书图片缩略图、证书名称、证书类型和必要有效状态
- **AND** 证书响应 SHALL NOT 暴露后台内部字段、审计字段、内部备注、对象存储原始 key、Authorization header、Cookie 或敏感配置。

#### Scenario: 证书预览或详情
- **WHEN** 用户点击可公开证书项
- **THEN** 小程序 SHALL 支持预览证书图片或进入证书详情
- **AND** 证书文件 SHALL 使用受控读取 URL 或等价安全引用
- **AND** 图片预览 SHALL 使用原图或原始受控 URL
- **AND** 证书加载失败 SHALL 展示稳定错误提示。

#### Scenario: 当前品牌无证书
- **WHEN** 当前品牌没有可公开证书
- **THEN** 证书 Tab SHALL 展示品牌上下文空态
- **AND** 页面 SHALL NOT 展示其他品牌证书。
