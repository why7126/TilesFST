## ADDED Requirements

### Requirement: 品牌列表搜索路径
品牌列表页 SHALL 支持在当前品牌列表页按品牌名称、品牌简称和品牌英文名过滤，并 SHALL 保持品牌卡片、品牌详情入口和品牌类目入口不回归。搜索态 SHALL 隐藏品牌 Banner 轮播和品牌 Hero 兜底，清空关键词后 SHALL 恢复完整品牌列表和 Banner 展示。

#### Scenario: 品牌关键词查找
- **WHEN** 用户在品牌列表页输入或提交品牌关键词
- **THEN** 页面 SHALL 请求公开品牌列表并携带 `keyword`
- **AND** 后端 SHALL 仅在品牌字段内匹配品牌名称、品牌简称和品牌英文名
- **AND** 搜索结果 SHALL 保持品牌列表页卡片布局、品牌卡片点击、品牌详情跳转和品牌类目入口行为
- **AND** 页面 SHALL 隐藏 Banner 轮播和品牌 Hero 兜底
- **AND** 空结果 SHALL 说明当前为品牌范围无结果，并提供调整关键词或清空当前搜索的路径。

#### Scenario: 品牌搜索清空
- **WHEN** 用户清空品牌列表页关键词
- **THEN** 页面 SHALL 重新请求不带 `keyword` 的公开品牌列表
- **AND** 页面 SHALL 恢复完整品牌列表、Banner 轮播或品牌 Hero 兜底
- **AND** 搜索入口 SHALL NOT 替代品牌卡片主点击区域。
