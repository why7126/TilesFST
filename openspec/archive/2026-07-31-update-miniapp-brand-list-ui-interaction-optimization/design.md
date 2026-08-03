## Context

REQ-0086 来源于已评审需求 `REQ-0086-miniapp-brand-list-ui-interaction-optimization`，父需求为 `REQ-0060-brand-list-page`，并承接 `REQ-0083-miniapp-brand-list-category-summary` 已完成的品牌单卡片、商品数量和末级类目汇总能力。

当前正式 spec `miniapp-brand-list-page` 已包含品牌列表页入口、顶部品牌轮播、每行一个品牌的信息行、公开品牌过滤、商品数量与末级类目口径、品牌/类目点击和小程序导航设备验收。本 Change 不重做品牌列表页基础能力，而是将用户提供的新版设计稿转化为更明确的 UI 与交互契约。

## Goals / Non-Goals

**Goals:**

- 在小程序品牌列表页落地新版暗色旗舰风视觉结构。
- 明确顶部导航、微信胶囊 reserve、品牌 Hero、品牌矩阵标题、单品牌卡片和底部 TabBar 的验收口径。
- 明确品牌卡片上行和下行类目标签是两个独立触控区域。
- 明确类目标签跳转依赖 `brandId` 与 `categoryId`，并约束事件冒泡。
- 把小程序自定义导航 best practice 与 sprint-014 小程序列表类复盘经验写入实现和验收任务。

**Non-Goals:**

- 不改管理端品牌维护、Logo 上传、排序配置或权限能力。
- 不改品牌详情页内部结构。
- 不重构商品列表页自身视觉。
- 不调整类目层级、命名、绑定或后台排序规则。
- 不新增品牌搜索、筛选、收藏、询价或下单流程。
- 不新增数据库表或对象存储策略。

## Decisions

### D1. 原型优先级采用 HTML-first

本 Change 的 UI 验收优先级为：

```text
prototype/miniapp/prototype.html
> 用户提供截图 / 后续导出的 prototype.png
> prototype/miniapp/context.md
> acceptance.md
> rules/ui-design.md
> openspec/specs/miniapp-brand-list-page/spec.md
```

原因：用户已提供可运行 HTML 原型和 390pt 截图，HTML 能表达具体层级、间距、点击区域和类目自动换行；截图适合作为视觉一致性参考。`rules/ui-design.md` 提供整体暗色旗舰风，但不应覆盖本 REQ 的页面级原型。

### D2. Hero 与既有品牌轮播能力保持兼容

实现时可以将新版 Hero 作为品牌轮播的视觉呈现，也可以作为品牌列表页顶部品牌氛围区；但不得破坏现有品牌列表页轮播数据、跳转、安全降级和图片安全要求。

如果后续实现选择替换轮播视觉，必须保留轮播能力的用户可感知行为或在任务输出中说明等价关系。若数据为空或图片失败，仍需展示品牌化兜底，不得白屏或破图。

### D3. 品牌卡片采用上下分区，不再做左右挤压

品牌卡片上行展示 Logo / 首字母、品牌名、商品数量和进入指示，作为品牌详情入口。下行通过分隔线和类目胶囊承载类目入口，不再展示“全部类目 · 点击查看该品牌下的类目商品”等说明文案；品牌矩阵标题右侧也不再展示“按类目快速识别”提示。

原因：REQ-0083 已暴露品牌信息与类目集合同时展示时的扫读压力。上下分区能减少类目数量较多时对品牌名称和商品数量的挤压，也能把“进入品牌详情”和“进入类目商品列表”两个动作讲清楚。

验收返修确认类目胶囊字体不应过弱：品牌名称为 `32rpx` 时，类目胶囊使用 `30rpx`，即比品牌名称小 `2rpx`。

### D4. 类目标签完整展示并独立点击

类目标签必须完整展示并自动换行，不使用“等 N 类”隐藏类目。每个类目标签单独绑定点击事件，携带 `brandId` 与 `categoryId` 跳转商品列表页，并阻止触发品牌详情入口。

若当前接口只返回类目名称，应扩展品牌列表公开接口，使 `leafCategories[]` 返回 `categoryId` 与 `categoryName`。字段变化必须同步 OpenAPI、Orval、小程序调用类型、接口文档和测试。

### D5. 小程序验收必须覆盖导航、胶囊和安全区

品牌列表页属于 TabBar 页面，同时又存在自定义导航与可能的返回入口。实现与验收必须参考 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，覆盖 320/375/390/430 pt DevTools 视口；真机不可用时只允许写 `blocked` 或 `follow_up`。

## Conflict Resolution

| 冲突点 | 解析 |
|---|---|
| 正式 spec 中 requirement 标题仍含“双列品牌卡片列表”但正文已要求单行品牌信息 | 不在本 Change 直接修改正式 spec 文件；delta 新增“新版 UI 与交互分区” requirement，并在后续归档时由 OpenSpec 合并语义。 |
| REQ-0083 原型文案曾写“轮播图保持现有品牌页能力，本需求只调整下方品牌列表” | REQ-0086 允许新版 Hero 强化品牌页首屏，但必须兼容既有轮播能力，不得破坏数据与跳转。 |
| UI 规范建议卡片圆角接近直角，而附件原型为较大圆角 | 本页面以附件 HTML/截图为高优先级视觉源，允许小程序品牌卡片使用 16px 左右圆角；后续实现需在 acceptance 中按产品确认等价。 |
| 类目集合很多时完整展示会拉高卡片 | 按 REQ-0086 选择完整展示和自然滚动，避免隐藏可点击入口；性能和首屏高度通过小程序静态测试与视口验收控制。 |

## Risks / Trade-offs

- 类目标签依赖 `categoryId`，当前接口可能缺字段 → 在任务中设置 API 契约检查，缺失时同步后端 Schema、OpenAPI、Orval 和测试。
- 类目过多导致页面变长 → 允许卡片高度自然增长，并通过页面滚动与底部 TabBar 避让验收兜底。
- Hero 与轮播边界容易误改 → tasks 中要求保留轮播能力回归和图片安全验收。
- 小程序 `.ts` / `.js` 双入口可能漂移 → tasks 中要求同步运行入口或按项目既有机制生成。
- 真机 evidence 可能不可用 → 不阻塞 OpenSpec 创建，但 apply/验收输出不得把 DevTools 通过写成真机通过。

## Knowledge Base References

- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- `docs/knowledge-base/retrospectives/sprint-014-retrospective.md`
