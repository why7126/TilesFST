## MODIFIED Requirements

### Requirement: Banner 与快捷入口
小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口；其中品牌入口 SHALL 进入品牌列表页。

#### Scenario: 快捷入口点击策略
- **WHEN** 用户点击四个快捷入口之一
- **THEN** “选瓷砖” SHALL 进入分类 Tab、筛选页或已有分类能力
- **AND** “品牌馆”或“品牌” SHALL 进入品牌列表页
- **AND** “新品榜” SHALL 进入商品列表页并带入 `section=new`
- **AND** “热销榜” SHALL 进入商品列表页并带入 `section=hot`
- **AND** 新品榜和热销榜入口 SHALL NOT 使用 `/pages/search/index?section=...` 承接
- **AND** 任一目标不可达时 SHALL 安全降级且不得出现白屏或路由错误。
