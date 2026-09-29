---
created_at: '2026-09-08 18:36:57'
updated_at: '2026-09-08 18:36:57'
---

## 背景与目标

来源：`issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/requirement.md`、`acceptance.md`、`review.md`、`prototype/web/banner-fit.html`和`prototype/web/context.md`。需求已在sprint-030，优先级P1，估算M/3人天。本设计只覆盖四类图片完整适配，实施不改视频、卡片、API、DB或图片来源策略。

## 设计决策

### D1 小程序原生适配

使用目标图片节点的aspectFit和页面局部WXSS。Web影响为false，prototype/web只是小程序设计载体，不触发Web CSS Port选择。逐一覆盖展示图及缩略图分支，保留现有src、事件、懒加载和回退，不用全局image替换或修改视频共用类实现。

### D2 稳定容器与品牌文字

首页436rpx、品牌列表348rpx、品牌详情总高380rpx、详情图库现有视口比例保持。品牌头图按220rpx图片区及160rpx文字区拆分，文字不覆盖图片，沿用品牌名一行和简介两行截断。实现时将内边距和边框计入可用区域，以实际computed style确认无溢出；固定图高而非按素材宽高动态撑开，防止切图跳动。

### D3 图片消费与并行工作

本Change不改变display/thumbnail/preview选取、签名续期或对象存储链路。同Sprint的REQ-0136可能触及相同页面请求逻辑，实现前复核最新文件，仅修改图片mode及局部布局，保留其合法改动；无需求依赖强制等待其交付。避免把旧MODIFIED段覆盖同期更新，归档时复核规格合并差异。

## 冲突报告与处理（Conflict Resolution）

| 对照点 | 结论与处置 |
|---|---|
| HTML完整适配与当前aspectFill | 以局部HTML完整适配为目标，四个MODIFIED规格补充完整适配场景 |
| HTML品牌图片区/文字区与当前叠层 | 采用互不重叠分区，修改品牌信息区规格；不恢复首页及品牌列表的Banner标题遮罩 |
| HTML cqw与小程序rpx/视口 | HTML是局部比例示意，context明确实际视口/padding边界；保留原容器契约并记录实际尺寸证据，不照搬cqw数值 |
| HTML边框占据空间 | 图/文固定高度之和需按content-box可用空间核验，允许扣除边框等价误差，不改变380rpx总高；文字不得被overflow意外裁掉 |
| HTML Mock状态与实际空态/回退 | Mock仅说明稳定空间，沿用真实页面状态契约，不把示例“暂无图片”覆盖所有业务文案 |
| PNG缺失 | Partially Ready，非文档创建阻塞；Skeleton与视觉验收条件继续保留 |

## UI Contract

| 项目 | 合同 |
|---|---|
| 事实源优先级 | HTML > PNG（未导出） > context.md > acceptance.md > rules/ui-design.md > 正式规格；仅对原型覆盖的局部区域生效 |
| 页面入口 | pages/index、pages/brand-list、pages/brand-detail、pages/tile-detail；现有首页、品牌列表/详情和商品入口，权限状态不变 |
| 信息架构 | 现有导航与下方内容不重设计；四类图框保留，品牌头图内上下分区，loading/empty/error空间稳定 |
| 视觉token | 使用现有背景/文字/边框语义，禁止新增裸Hex；仅必要局部样式，共享token若必须新增需同步tokens/globals/预览及使用端 |
| 字体与层级 | 沿用当前字体和字号；品牌名一行、简介两行，不以缩小图片文字或堆叠层级掩盖可读性；图与文区域不重叠 |
| 交互状态 | 轮播切换/指示、Banner点击、图片预览、懒加载、错误回退保留；视频操作回归；小程序hover/click-outside不适用，原型选择器仅设计工具 |
| 图标与文案 | 沿用业务图标和空态；不增加原型说明、测试边缘标记或控制下拉框到产品 |
| Mock/API边界 | HTML素材及状态全部合成，无真实网络；生产页面继续使用既有公开API和媒体处理器，真实回退及Network须另行验证 |
| 权限规则 | 公开页面和素材访问沿用既有权限；不暴露内部标题、object key或未授权URL，不改管理端 |
| 最终一致性参照 | 四页面×320/375/430pt、宽/方/竖素材、正常/回退/失败/空态、长品牌信息及混排视频；验收以来源REQ的17条AC为准 |

## 验证及证据

先拆解原型并确认Skeleton，记录1440px设计核对视口与小程序DevTools/真机或等价证据；细节实现后记录图片mode、框/文字区域width/height/padding/border、overflow、背景token及层级。PNG缺口和此前本地浏览器策略拒绝不等于视觉通过，不绕过访问限制。截图返修后重新取证。静态检查优先扩充 `tests/test_miniapp_static.py` 相关断言，覆盖目标图片分支和视频隔离；若修改逻辑则补状态用例并同步TS/JS。

知识库引用：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`、`docs/knowledge-base/retrospectives/sprint-028-retrospective.md`；承接AC-XCUT-001～003的key/object/URL/render、Network脱敏及来源声明，不增加批量对象审计。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: [wechat_miniapp]
  reason: 仅图片mode和局部布局，无API/DB、请求封装、行为事件、日志、Task Trace、敏感字段或保留周期变更；不改媒体URL选择及对象策略。
  validation: 设计阶段核对来源REQ的AC-OBS-001/002，实施阶段检查diff及静态回归，证据脱敏；尚未执行产品验收。
```

参照 `docs/standards/product-data-collection-observability.md`。不改变请求、响应、错误码或Pydantic/SQLite/MySQL schema，无OpenAPI/Orval/迁移及Docker Compose输入变化。若实际范围扩大需重新声明并补门禁。

## 风险、发布与回退

窄视口长文案、边框盒模型、图片回退与共享video样式为重点风险，按对应AC取证。实现完成后按现有小程序发布流程，不在本命令发布。回退限定本Change的mode/布局/测试改动，保留其他Change和媒体来源逻辑；无数据迁移。当前无额外需求决策，Skeleton确认和真实视觉证据由实施阶段完成。
