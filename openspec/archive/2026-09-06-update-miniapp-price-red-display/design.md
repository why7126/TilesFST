---
change_id: update-miniapp-price-red-display
requirement_id: REQ-0133-miniapp-price-red-display
created_at: 2026-09-05 22:22:41
updated_at: 2026-09-05 22:24:54
---

## 上下文与目标

来源为 `issues/requirements/archive/REQ-0133-miniapp-price-red-display/` 六件套和局部原型，已纳入sprint-029。实现统一价格强调与无价状态，保持价格内容、业务规则、公开权限和布局。无API、数据库或媒体变更。

## 设计决策

### D1 小程序语义色与局部样式调整

采用现有WXSS和共享Design Token策略，不迁移Web CSS、不重建页面。新增独立价格语义色，首选候选#F87171；由共享token单一事实源向小程序暴露统一映射，保持既有品牌金值和Web产品样式。实施前核实当前token生成链，优先复用既有同步机制；仅新增必要映射，不扩展整套主题系统。

备选方案为各页面直接替换色值，实现简单但容易遗漏独立价格节点和无价文案，且造成重复常量，因此不采用。复用error/hotSale颜色会耦合不同语义，也不采用。

### D2 展示状态统一

统一得出valid、empty、unavailable或等价状态；可公开查看且符合现有价格格式的正数金额为valid。空值、零、非正、无法识别、旧无价文案均不使用金额强调；不可查看状态优先于缓存金额。金额保留原price_display，不重新格式化或计算，不增加后端字段。

现有归一化逻辑分散在共享卡片、详情和收藏。实现提取或复用最小展示helper，分别接入共享卡片、详情主价格、同系列/同品牌推荐和收藏，保持TS/JS同步。保留原无价与错误文案处理，状态helper只决定价格视觉，不引入新业务定价规则。

### D3 组件范围与并发改动

只调整价格节点的状态与样式；BUG-0148对grid图框及aspectFit的改动为既有工作成果，不覆盖或回滚。优先处理缺陷项，再合入价格变更；相关静态回归覆盖图片适配未退化。

## UI Contract

| 契约项 | 约定 |
|---|---|
| 事实源 | 价格状态和颜色采用REQ局部HTML > PNG（待导出）> context > acceptance > ui-design > 正式spec；其他结构由现有小程序实现决定 |
| 页面入口 | 首页新品/热门/全部产品，商品列表，品牌详情商品Tab，搜索SKU，详情主价格及推荐，收藏 |
| 信息架构 | 不改变导航、媒体、卡片布局、列表密度、收藏及分享操作；只拆分必要金额与辅助文本节点 |
| 视觉token | 独立price红色候选#F87171，brand.gold不变；辅助与占位色中性；字体、间距与尺寸沿用当前页面 |
| 交互状态 | valid/empty/unavailable及有效↔无价、有效→失效更新；loading/error沿用原页面；不新增产品状态切换按钮 |
| 图标文案 | 无新图标；保留参考价格、门店确认说明及既有无价/失效文案；货币符号与金额同色，独立单位辅助色 |
| Mock/API边界 | REQ HTML仅合成数据；实现沿用原API和本机收藏，不引入Mock到运行代码；原型不能证明真实接口已验收 |
| 权限 | 保持公开商品可见规则，失效收藏不把历史金额当有效报价，不新增权限检查接口 |
| 可读性 | 实际背景对比度≥4.5:1，覆盖透明度、长金额和小字号；320/375/430移动宽度及1440预览 |
| Skeleton | 先接入稳定价格状态容器并取得首轮确认及1440证据，再关闭细节任务；合同已定义，Skeleton待实施 |
| 样式证据 | 记录页面、选择器、视口、color、background-color、opacity、font-size/weight和line-height；金额、辅助、无价分别取证 |
| 最终参照 | 逐项回扣REQ acceptance的页面矩阵与AC-PROTOTYPE-001至004；布局和BUG-0148成果不得回退 |

## 冲突处理

- 既有rules/ui-design.md描述品牌金用于价格；本需求明确小程序有效金额红色，实施同步端侧适用说明，Web/管理端保留原语义。正式design-system并无小程序价格必须金色的条目，采用ADDED Requirements补充，不删除Web token规则。
- 原型具有较大字号和演示控制按钮，只是局部状态示意；保留现有产品字号布局，演示按钮不进入产品。完整页面布局不受局部原型重定义。
- PNG尚未导出且未完成渲染确认，readiness为partially_ready；允许创建Change，不能据此勾选视觉验收任务。

## 验证与观测

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 仅价格展示状态、WXSS、token及必要规范变更，不新增API、DB、请求日志、行为事件、Task Trace或Web/小程序/App请求封装；无新增采集、存储和保留周期。
  validation: 通过差异检查确认接口、schema、track事件与请求封装未改动，执行REQ的AC-OBS-001至003及价格状态回归；Orval和Docker Compose为N/A。
```

规范引用：`docs/standards/product-data-collection-observability.md`、`docs/standards/prototype-ui-acceptance.md`。知识库引用：`docs/knowledge-base/README.md`、`docs/knowledge-base/retrospectives/sprint-028-retrospective.md`；无管理端/上传标签，不引入AC-XCUT。复盘经验用于分清静态、Mock、DevTools及真机证据。

## 风险与回滚

缓存金额残留通过unavailable优先和状态切换测试处理；小字号红色可读性通过实际样式及对比度证据处理；共享token外溢通过其他端差异审查处理。回滚仅撤销本Change的价格helper接入、token引用和规范适用说明，保留BUG-0148图片适配，不回滚数据库或对象存储。无数据迁移。上线沿用小程序既有发布流程，本Change不执行发布。

## 后续确认

最终价格色值、PNG和Skeleton/视觉证据在实施阶段确认，未完成时不得关闭相应任务或归档。
