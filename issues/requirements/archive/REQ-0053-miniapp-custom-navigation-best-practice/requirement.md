---
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
title: 小程序自定义导航 best-practice 沉淀
terminal: miniapp
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
created_at: 2026-07-19 18:09:25
updated_at: 2026-07-19 21:05:25
---

# REQ-0053 小程序自定义导航 best-practice 沉淀

## 1. 需求背景

`REQ-0048-miniapp-global-custom-navigation-bar` 已完成小程序全局自定义导航栏能力，覆盖首页品牌导航、非首页返回、状态栏避让、微信原生胶囊避让和页面内容不被 fixed header 遮挡等关键要求。后续小程序还会持续新增或调整分类、商品列表、详情、收藏、证书、门店信息等页面，如果只依赖单次实现经验，容易出现以下问题：

- 新页面重复手写导航栏或页面顶部 padding，导致状态栏、胶囊和内容 offset 策略不一致。
- 从分享卡片、扫码、外部入口直达详情页时，返回按钮没有页面栈兜底。
- DevTools 预览通过后，未区分真机安全区、微信版本和不同视口下的实际表现。
- 验收截图散落在 Change tasks、acceptance 或 Sprint 报告中，无法复用为后续页面接入 checklist。

本需求用于将小程序自定义导航栏的实现与验收经验沉淀为可复用 best-practice，明确状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵，供后续小程序页面、OpenSpec Change 和验收报告引用。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 小程序开发 | 新增或调整页面时能按统一导航规则接入，避免重复手写状态栏、胶囊 reserve、返回兜底和内容 offset。 |
| 测试 / 验收人员 | 能按固定截图矩阵验证首页、非首页、详情页、异常态和不同视口，不把 DevTools 通过误写成真机通过。 |
| 产品 / 需求负责人 | 能判断后续页面是否满足自定义导航体验和验收证据要求，减少发布前才发现顶部遮挡或返回失效。 |
| AI / Codex Agent | 在后续 `/req-complete`、`/req-opsx`、`/opsx-apply` 中引用同一 best-practice，避免生成互相冲突的页面级规则。 |

## 3. 需求目标

- 沉淀一份小程序自定义导航 best-practice，覆盖实现规则、页面接入规则和验收矩阵。
- 明确状态栏与微信原生胶囊数据来源、降级值和布局约束。
- 明确返回按钮在有页面栈、无页面栈、分享直达和异常态下的兜底策略。
- 明确页面内容 offset 的统一策略，避免 fixed header 遮挡首屏内容、加载态、空状态和滚动区域。
- 明确截图验收矩阵，与 `REQ-0052-miniapp-device-evidence-template` 的 evidence 字段联动。
- 将该 best-practice 作为后续小程序导航相关需求和 Change 的引用事实源，而不是重复分散在多个需求中。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| best-practice 文档 | 形成小程序自定义导航栏的长期实践文档，建议沉淀到 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。 |
| 状态栏规则 | 明确状态栏高度、安全区、胶囊位置和异常降级值的读取与使用原则。 |
| 胶囊避让规则 | 明确右侧微信原生分享 / 关闭胶囊不可占用区域，禁止自绘伪系统胶囊。 |
| 返回兜底规则 | 明确有页面栈、无页面栈、分享直达、错误态和加载态的返回行为。 |
| 页面 offset 规则 | 明确 fixed / sticky 导航下页面主体、骨架屏、空状态、错误态和滚动区如何避让导航栏高度。 |
| 截图验收矩阵 | 明确页面、设备、视口、状态和结论字段，复用 REQ-0052 的 evidence 记录方式。 |
| 引用方式 | 明确后续 REQ、OpenSpec Change、tasks、acceptance 和 Sprint 验收报告如何引用该 best-practice。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新增小程序业务页面 | 本需求只沉淀实践，不新增首页、分类、列表、详情、收藏、证书或门店信息页面。 |
| 重构导航组件 | 本需求不直接修改 `src/miniapp/components/custom-navigation/`，如需重构须在后续 OpenSpec Change 中明确。 |
| 自动化截图工具链 | 本需求不新增小程序自动化截图、真机云测或 DevTools 控制工具。 |
| 回填全部历史截图 | 可引用历史问题作为案例，但不强制补录所有历史 DevTools/真机 evidence。 |
| 修改 API / DB / Orval | 本需求不新增后端接口、数据库字段或 Web API 生成物。 |
| 修改 Docker Compose / MinIO | 本需求不影响部署、对象存储、环境变量或运行时数据。 |

## 5. 功能要求

### FR-001 best-practice 文档结构

后续 best-practice 文档 MUST 至少包含以下章节：

- 适用范围：哪些页面和 Change 需要引用该实践。
- 导航结构：首页与非首页的职责差异。
- 状态栏与胶囊：数据来源、布局计算、降级值和禁止事项。
- 返回兜底：页面栈返回、首页兜底、分享直达和异常态规则。
- 页面 offset：导航 spacer、padding、滚动容器和状态页避让策略。
- 截图验收矩阵：设备、视口、页面、状态、截图引用、结论和剩余风险。
- 接入 checklist：新增页面或改造页面时的必查项。
- 引用示例：REQ、OpenSpec tasks、acceptance 和 Sprint report 中如何引用。

### FR-002 状态栏与安全区规则

best-practice MUST 明确小程序自定义导航栏不应硬编码单一机型高度。实践文档 SHOULD 要求优先使用微信小程序可获取的窗口、状态栏和菜单按钮数据，例如 `wx.getWindowInfo()`、`wx.getSystemInfoSync()`、`wx.getMenuButtonBoundingClientRect()` 或项目确认的兼容封装。

文档 MUST 要求记录降级策略：

- 获取状态栏高度失败时使用项目统一 fallback。
- 获取胶囊矩形失败时使用项目统一 reserve 宽度和导航内容高度。
- fallback 值必须集中维护或集中说明，不得散落到多个页面。
- 状态栏高度、导航内容高度、总导航高度和右侧 reserve 宽度必须能被验收或人工复核。

### FR-003 微信原生胶囊避让规则

best-practice MUST 明确：

- 自定义导航栏右侧必须为微信原生分享 / 关闭胶囊预留不可占用区域。
- 标题、品牌文案、Logo、返回按钮、搜索入口和操作按钮不得进入胶囊区域。
- 不得在 WXML / WXSS 中自绘模拟分享、关闭或系统胶囊。
- 支持分享的页面继续使用微信原生分享能力，分享路径和参数由页面级配置负责。
- 非分享页面不得因右侧 reserve 出现不可点击的伪分享按钮。

### FR-004 返回兜底规则

best-practice MUST 明确统一返回策略：

- 有上一页页面栈时，优先使用 `wx.navigateBack()` 返回上一页。
- 无上一页页面栈时，必须进入明确兜底路径，默认建议回首页。
- 兜底路径失败时，应有二级兜底，例如 `wx.reLaunch()` 到首页或项目确认的安全入口。
- 从分享卡片、扫码、收藏入口或外部入口直达详情页时，返回按钮不得失效、报错或停留无反馈。
- 加载态、空状态、错误态下返回按钮仍应可用，除非有明确不可中断操作。
- 返回按钮触控热区不得小于 44x44 pt 或项目等价触控标准。

### FR-005 页面 offset 与 fixed header 避让规则

best-practice MUST 明确页面内容的顶部 offset 不应由各页面视觉猜测。实践文档 SHOULD 推荐以下任一统一策略：

- 导航组件提供 spacer，占位高度等于真实导航高度。
- 导航组件向页面暴露 CSS 变量、style 片段或等价布局 token。
- 页面根容器通过统一 class / mixin / utility 使用导航高度。

文档 MUST 要求以下内容均避让导航栏：

- 首页首屏、搜索框、分类列表、商品列表、SKU 媒体区、收藏列表、证书列表和门店信息。
- 加载态、骨架屏、空状态、错误态和网络失败提示。
- 下拉刷新区域、滚动容器顶部和横向窄屏内容。

不同页面不得各自硬编码互相冲突的顶部 padding；如确需页面特殊 offset，MUST 在页面验收中说明原因。

### FR-006 页面接入 checklist

best-practice MUST 提供新增或改造小程序页面时的 checklist，至少包括：

- 页面是否需要自定义导航栏，若豁免必须写明原因。
- 页面是首页形态、TabBar 页面形态、普通非首页形态还是详情/分享直达形态。
- 标题是否固定、动态、单行截断，是否会挤压胶囊 reserve。
- 返回按钮是否展示，是否有页面栈兜底和首页兜底。
- 页面首屏和所有状态页是否被导航栏遮挡。
- 页面是否支持原生分享，分享路径和参数是否保留。
- DevTools 与真机 evidence 是否按矩阵记录。

### FR-007 截图验收矩阵

best-practice MUST 定义截图验收矩阵，并与 `REQ-0052-miniapp-device-evidence-template` 兼容。

矩阵 SHOULD 覆盖：

| 维度 | 建议项 |
|---|---|
| 页面 | 首页、搜索、分类、商品列表、商品详情、收藏、证书、门店信息。 |
| 入口 | 首页跳转、TabBar 切换、列表进入详情、分享直达详情、异常参数直达。 |
| 视口 | DevTools 320 pt、375 pt、430 pt。 |
| 真机 | iPhone 刘海屏、iPhone 非刘海屏、Android 常见机型。 |
| 页面状态 | 正常、加载、空状态、错误态、网络失败、长标题。 |
| 结论 | 状态栏不遮挡、胶囊不重叠、返回可用、首屏内容不被遮挡、无横向滚动。 |

矩阵中的每条证据 MUST 能记录截图或录屏引用、执行环境、结论、阻塞项和剩余风险；不能执行真机验证时 MUST 标记 `blocked` 或 `follow_up`，不得写作通过。

### FR-008 引用与复用规则

后续小程序相关 REQ 或 OpenSpec Change SHOULD 在以下位置引用该 best-practice：

- `requirement.md` 的 UI / UE 约束或技术影响章节。
- `acceptance.md` 的测试与验证章节。
- OpenSpec `tasks.md` 的 DevTools / 真机验收任务。
- OpenSpec `acceptance.md` 或 `trace.md` 的 evidence 摘要。
- Sprint `acceptance-report.md` 的设备验收结果或 follow-up 风险。

如果后续 Change 修改自定义导航组件、页面顶部布局、分享入口、返回行为或 fixed header，MUST 检查本 best-practice 是否仍适用；若实践已过期，MUST 同步更新文档或记录豁免原因。

### FR-009 历史经验与案例边界

best-practice SHOULD 引用 `REQ-0048`、`REQ-0050`、`REQ-0052` 或相关 Sprint 复盘作为经验来源，但不得复制大段历史需求内容。

历史截图和验收残留可作为案例，不强制本需求回填所有历史 evidence。若需要补录历史截图，应作为独立任务处理，避免混入本需求的交付闭环。

## 6. UI / UE 约束

本需求不直接交付新的小程序页面，但 best-practice MUST 体现以下 UI / UE 约束：

- 自定义导航栏必须延续当前小程序深色品牌风格，不引入与首页冲突的新主题。
- 首页可保留品牌双行表达，非首页应优先保障页面标题、返回和胶囊避让。
- 非首页动态标题应单行截断，不得挤压右侧胶囊 reserve。
- 返回按钮应使用清晰左箭头或项目统一图标，并具备足够触控热区。
- 导航层级应高于页面内容，但不得遮挡微信原生胶囊。
- 320 到 430 pt 常见宽度下不应出现标题、返回按钮、胶囊 reserve 或首屏内容重叠。
- 截图验收应覆盖正常态、加载态、空状态、错误态和分享直达态。

## 7. 依赖与实施顺序

| 依赖 | 说明 |
|---|---|
| `REQ-0048-miniapp-global-custom-navigation-bar` | 自定义导航栏能力和验收标准来源。 |
| `REQ-0050-miniapp-brand-header-page-title-rules` | 首页双行品牌文案与非首页标题规则参考。 |
| `REQ-0052-miniapp-device-evidence-template` | 截图、DevTools、真机、blocked、follow_up 和 evidence 字段参考。 |
| `rules/document-governance.md` | best-practice 文档 frontmatter、时间和长期文档治理规则。 |
| `rules/directory-structure.md` | 文档沉淀位置和 issues / docs / OpenSpec 边界。 |
| `src/miniapp/components/custom-navigation/` | 现有实现经验来源；本需求不直接修改。 |

建议实施顺序：

1. 确认 best-practice 最终沉淀位置，优先 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。
2. 提炼状态栏、胶囊、返回兜底、页面 offset 和截图矩阵规则。
3. 补齐用户故事、业务流程和验收标准。
4. 评审通过后创建 OpenSpec Change，实现文档和必要流程引用。
5. 后续小程序页面或导航相关 Change 默认引用该 best-practice。

**建议 OpenSpec change 命名**：`add-miniapp-custom-navigation-best-practice`。

## 8. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0048 小程序全局自定义导航栏 | 父需求；能力实现和核心验收来源。 |
| REQ-0050 小程序 brand-header 页面标题规则 | 页面标题、首页/非首页差异和返回按钮规则参考。 |
| REQ-0052 小程序 DevTools/真机验收 evidence 模板 | 截图验收矩阵和设备 evidence 字段参考。 |
| `src/miniapp/components/custom-navigation/` | 现有实现经验来源；后续 Change 可决定是否调整实现或仅沉淀文档。 |

## 9. 状态

```yaml
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
priority: P1
status: done
iteration: sprint-009
owner: product
parent_requirement: REQ-0048-miniapp-global-custom-navigation-bar
openspec_change: add-miniapp-custom-navigation-best-practice
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期 best-practice 服务对象
api_change: false
database_change: false
upload_change: false
orval_required: false
docker_compose_required: false
```
