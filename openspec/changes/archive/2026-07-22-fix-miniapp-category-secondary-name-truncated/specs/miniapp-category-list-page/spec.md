## MODIFIED Requirements

### Requirement: 一级与二级分类展示

分类页 SHALL 以左侧一级分类导航和右侧二级分类宫格展示两级启用分类，使用户可以快速定位目标品类；二级分类名称 SHALL 在主流小程序视口中保持可辨识，超过 4 个字时不得因过早省略导致用户无法判断分类含义。

#### Scenario: 二级分类宫格

- **WHEN** 当前一级分类存在二级分类
- **THEN** 右侧区域 SHALL 展示当前一级分类名称
- **AND** 二级分类 SHALL 按三列宫格展示
- **AND** 每个二级分类 SHALL 展示分类名称
- **AND** 4 字以内二级分类名称 SHALL 正常显示且布局不得回退
- **AND** 5-8 字二级分类名称 SHALL 可被用户完整识别或以业务可接受方式清晰展示
- **AND** 超过 8 字二级分类名称 SHALL 不遮挡相邻分类、商品列表、导航栏或其他操作区
- **AND** 二级分类名称 SHALL NOT 在超过 4 个字时仅展示前 4 个字并以 `...` 省略导致含义不可辨识
- **AND** 页面 SHALL NOT 展示二级分类商品数量、简介、价格或运营 Banner。

#### Scenario: 二级分类长名称移动可用性

- **WHEN** 团队在微信开发者工具、iOS 真机、Android 真机或 320 到 430 pt 宽度范围验收分类页
- **THEN** 二级分类长名称 SHALL 保持可辨识
- **AND** 二级分类卡片 SHALL 不发生文本重叠、横向滚动、点击热区错位或底部 TabBar 遮挡
- **AND** 点击长名称二级分类 SHALL 进入对应二级分类商品列表
- **AND** 跳转参数中的 `categoryId`、`categoryName`、`categoryLevel=secondary` 和 `sourcePage=category` SHALL 与当前二级分类一致。
