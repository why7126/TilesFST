## 背景

REQ-0129 的事实源来自 `issues/requirements/archive/REQ-0129-miniapp-sku-detail-actionbar-compact-favorite/` 六件套和 `prototype/miniapp/actionbar-compact.html`。当前小程序商品详情页底部 actionbar 使用收藏图标加文字的纵向按钮，导致底部固定区域偏高；返回首页悬浮按钮已有 actionbar offset，需要随底部高度变化同步调整。

## 目标与非目标

**目标：**

- 收藏按钮去掉可见第二行文字，仍通过心形状态、激活色和 toast 表达收藏 / 已收藏 / 失败反馈。
- 底部 actionbar 高度变紧凑，同时保留不小于 44x44 pt 或项目等价触控热区。
- 分享主按钮保持主要视觉权重和微信原生分享能力。
- 返回首页悬浮按钮 actionbar offset 与新底部高度、安全区避让一致。
- 验收记录覆盖 320 pt、375 pt、430 pt 小程序视口和安全区表现。

**非目标：**

- 不改收藏 API、收藏数据模型、SKU 详情 API、分享 API、分享文案生成逻辑或行为事件。
- 不改收藏列表页、商品详情主体信息架构、推荐卡片、品牌卡片或媒体浏览能力。
- 不新增后台配置、主题配置、外部依赖或跨端 Design System token。

## 决策

### D1 使用既有小程序样式做局部压缩

本 Change 直接调整商品详情页既有 WXML/WXSS 结构，优先删除可见 `action-label` 文本节点或使其不渲染，并收敛 `.actions`、收藏按钮和分享按钮的高度 / padding / gap。这样可以把变更限制在详情页底部操作区，避免引入新组件或影响收藏列表等其他页面。

### D2 收藏状态由图标、颜色和 toast 承担

收藏入口保留稳定按钮热区，图标按未收藏 / 已收藏区分空心与实心或等价视觉状态；请求成功、取消成功和失败继续使用既有 toast。若平台支持可访问属性，实现可补充按钮语义说明，但不得恢复可见的“收藏 / 已收藏”第二行文字。

### D3 返回首页悬浮按钮 offset 跟随 actionbar 高度下调

商品详情页 actionbar 压缩后，同步调整 `home-floating-button` 的 `offset-actionbar` 或等价样式，使悬浮按钮仍避开底部栏和安全区，但不再保持旧高度下的过大距离。该调整仅作用于 actionbar 场景，不改变其他页面 offset 策略。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | `prototype/miniapp/actionbar-compact.html` > `prototype/miniapp/context.md` > `acceptance.md` > `rules/ui-design.md` > `openspec/specs/miniapp-sku-detail-page/spec.md`。若原型像素与小程序原生约束冲突，以触控热区、安全区和既有深色视觉为准。 |
| 页面与入口 | 微信小程序 `/pages/tile-detail/index`，覆盖首页、列表、收藏页和分享直达进入 SKU 详情后的底部操作栏。 |
| 信息架构 | 页面主体结构不变；底部固定区保留次级收藏图标按钮和“分享给客户”主按钮；返回首页悬浮按钮位于 actionbar 上方并避让安全区。 |
| 视觉 token | 延续小程序详情页深色背景、边线、品牌金主按钮和次级图标色；不得引入电商红、纯白底或裸露解释性文案。 |
| 交互状态 | 覆盖未收藏、已收藏、请求中、失败回滚、分享按钮、底部安全区和悬浮按钮避让；状态变化不得造成 actionbar 高度跳变。 |
| 图标与文案 | 收藏按钮可见区域仅保留心形或等价图标，不显示“收藏 / 已收藏”；分享按钮保留“分享给客户”。 |
| Mock/API 边界 | 使用现有 SKU 详情、收藏和分享逻辑；本 Change 不新增接口、字段、mock 数据或请求封装。 |
| 权限规则 | 沿用现有小程序公开详情页与收藏授权规则；未登录或授权失败按既有收藏失败路径处理。 |
| 一致性参照 | 对齐 REQ-0129 AC-001 至 AC-020，验收需记录 320/375/430 pt 视觉证据和实现 diff N/A 复核。 |

## 冲突处理

- 原型表达“紧凑布局策略”而非固定像素值；实现阶段可按小程序 rpx、安全区变量和现有组件结构微调。
- 若去掉文字后图标语义不足，优先补充非可见语义属性、图标状态和 toast 反馈，不恢复可见第二行文字。
- 若 actionbar 高度压缩与触控热区冲突，优先保留有效点击区域，再在 padding、gap、图标尺寸和悬浮按钮 offset 上寻找更小高度。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 本 Change 仅调整微信小程序商品详情页底部操作栏静态 UI、收藏按钮可见文案和返回首页悬浮按钮 actionbar offset；不新增或修改 API、DB、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。
  validation: /opsx-apply 阶段通过实现 diff 确认收藏 API 路径、分享 open-type、track 事件名、请求封装和数据模型未变；通过小程序静态测试与 320/375/430 pt 视觉证据确认 UI 调整生效。
```

## 风险与缓解

- 触控热区被压缩过度：实现阶段显式检查收藏按钮和分享按钮有效点击区域，不以视觉高度替代可点区域。
- 去文字后状态识别降低：使用心形形态、激活色和 toast 形成多通道反馈。
- loading 态撑高底栏：将请求中状态限制在既有按钮容器内，测试高度稳定性。
- 悬浮按钮 offset 过低或过高：用 320/375/430 pt 截图验证与安全区、推荐卡片和底部按钮的关系。

## 迁移与回滚

本 Change 为小程序局部 UI 调整，无数据迁移。若验收发现点击热区或避让异常，可回滚相关 WXML/WXSS 与 `home-floating-button` actionbar offset 改动，收藏 API 与数据不会受影响。

## 开放问题

- 无。实现阶段如微信开发者工具或真机证据不可用，需在 Change trace 标记 `blocked` 或 `follow_up`，不得写作已通过。
