---
purpose: 原型驱动 UI 验收标准
content: 带 prototype 的 UI Change 的 UI Contract、Skeleton、截图、computed style、Mock/API 和一致性验收清单
source: /spec-study apply ProjectMoonBox 治理学习改写
update_method: UI 原型验收、Design System 或 opsx 门禁变化时更新
created_at: 2026-08-10 23:28:57
updated_at: 2026-08-10 23:28:57
---

# 原型驱动 UI 验收标准

本标准适用于任何包含 `prototype/`、`prototype_refs`、`AC-PROTOTYPE-*`、UI Skeleton 或明确引用既有页面视觉的 UI Change。目标是把“像不像原型”前置为可执行合同、可截图证据和可复核样式检查。

## 1. UI Contract

`/req-opsx` MUST 在 Change `design.md` 写入 UI Contract。缺少 UI Contract 时，`/opsx-apply` 只能补齐合同和 Skeleton，不得把 UI 实现标记完成。

| 项 | 必填内容 |
|---|---|
| 事实源优先级 | `prototype.html`、PNG/截图、`context.md`、`acceptance.md`、`rules/ui-design.md`、既有页面的排序和冲突处理 |
| 页面与入口 | 路由、导航入口、默认落点、登录态/权限态差异 |
| 信息架构 | 顶部区、侧边栏、主内容、浮层、弹窗、列表、卡片、空态和错误态 |
| 视觉 token | 字体、字号、行高、semantic token、边框、间距、圆角、阴影、层级和滚动规则 |
| 交互状态 | hover、active、focus、disabled、loading、click outside、展开/收起、键盘可达性 |
| 图标与文案 | 相同功能统一图标/文案，不同功能保持差异，用户可见文案产品化 |
| Mock/API 边界 | Mock 区域、真实 API 区域、后续接入计划、生产风险和验收非目标 |
| 权限规则 | 菜单、按钮、危险操作、店主端/管理端入口等按角色显示的规则 |
| 一致性参照 | 需要对齐的店主端、管理端、小程序或既有页面，以及逐项 checklist |

## 2. Skeleton 首轮确认

带 prototype 的 UI Change MUST 先完成 Skeleton，再进入细节实现。Skeleton 至少覆盖：

- 页面壳、布局区域、导航结构、菜单、弹窗/浮层容器和主要状态容器。
- 关键元素的稳定选择器、可测状态和占位数据边界。
- 1440px 桌面首屏截图或等价视觉证据，证明布局、密度和层级方向正确。

Skeleton 证据未通过时，不得继续关闭细节实现任务。

## 3. 视觉截图门禁

`/opsx-apply` 和 `/opsx-modify` 完成 UI 任务前 MUST 记录 1440px 桌面视口证据。若页面存在关键交互，还 MUST 记录对应交互状态。小程序 UI Change 需记录微信开发者工具截图、真机截图或等价证据。

| 场景 | 必查内容 |
|---|---|
| 默认首屏 | 页面标题、导航、主要区域、间距、对齐、滚动边界、文本溢出 |
| 管理端侧边栏 | 展开、收起、active 态、分组、品牌区、用户触发器 |
| 店主端商品区 | 搜索、筛选、商品卡、材质图、分页、价格与 CTA |
| 弹窗/浮层 | 宽高、层级、背景区分、边框、滚动、底部操作 |
| 小程序页面 | 自定义导航、列表密度、卡片角标、图片加载态、低端机可读性 |
| 响应式 | 原型或验收要求的低视口、移动端或横向滚动场景 |

任意 UI 返修会使相关旧截图 stale；必须重新取证并更新 Change `trace.md`。

## 4. Computed Style

对原型差异风险高或验收反馈已指出的视觉点，MUST 使用浏览器 computed style、Playwright 断言、微信开发者工具证据或等价工具记录关键属性。

| 类别 | 示例属性 |
|---|---|
| 字体层级 | `font-family`、`font-size`、`font-weight`、`line-height` |
| 尺寸间距 | `width`、`height`、`padding`、`margin`、`gap`、`min/max-*` |
| 颜色边框 | semantic token、`color`、`background-color`、`border-color`、`border-width` |
| 层级定位 | `position`、`z-index`、`overflow`、`transform` |
| 交互状态 | hover/active/open/collapsed 状态下的样式变化 |

computed style 证据可以记录在 Change `trace.md`、验收日志或测试输出中，但必须能定位到页面、选择器、视口和结论。

## 5. Mock/API 边界

带 UI 的 Change 必须声明数据边界：

- 使用 Mock 数据时，明确 Mock 字段、Mock 来源和不代表真实 API 已完成。
- 使用真实 API 时，明确接口来源、权限、错误态和空态。
- 如果本 Change 不接入真实数据，必须把真实数据接入作为非目标或后续建议，避免验收误判。

## 6. 归档门禁

`/opsx-archive` 前 MUST 复核 linked REQ 与 Change 的 UI Contract、Skeleton、截图、computed style、Mock/API 边界和最终实现一致。缺证据、证据 stale、Mock/API 边界未声明或最终一致性 checklist 未完成时，归档应阻断。
