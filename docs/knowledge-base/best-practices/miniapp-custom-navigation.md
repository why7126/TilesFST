---
title: 小程序自定义导航最佳实践
purpose: 统一微信小程序自定义导航的状态栏、原生胶囊、返回兜底、页面 offset 与截图验收矩阵
content: 小程序自定义导航 best-practice
source: REQ-0053-miniapp-custom-navigation-best-practice
update_method: 小程序导航组件、设备验收矩阵或页面接入规则变化时更新
owner: 小程序负责人
status: draft
created_at: 2026-07-19 20:06:00
updated_at: 2026-07-19 20:06:00
note: 适用于后续涉及小程序自定义导航、fixed header、分享、返回或页面顶部布局的需求与 Change
---

# 小程序自定义导航最佳实践

## 适用范围

本文档用于后续新增或改造微信小程序页面时，统一自定义导航栏的实现约束与验收口径。适用场景包括：

- 首页品牌导航、普通非首页标题导航、TabBar 页面顶部导航、详情页和分享直达页。
- 涉及状态栏安全区、微信右侧原生分享 / 关闭胶囊、返回按钮、fixed header 或 sticky header 的 Change。
- 需要在 Sprint 验收报告、OpenSpec `tasks.md` 或 Change `acceptance.md` 中记录导航截图 evidence 的场景。

不适用或仅部分适用时，验收材料必须写明 N/A reason，例如：仅修改后端字段过滤、不影响小程序 UI；仅新增文档；仅修改非导航区域且不影响顶部布局。

## 导航结构

| 页面形态 | 导航规则 | 重点验收 |
|---|---|---|
| 首页形态 | 保留品牌信息表达，默认不展示左侧返回按钮 | 品牌文案稳定、状态栏避让、首屏内容不被遮挡 |
| TabBar 页面形态 | 按页面定位确认是否展示返回；默认保持 TabBar 入口语义 | 不误导用户返回层级、不遮挡 TabBar 与首屏内容 |
| 普通非首页 | 展示页面标题与返回按钮，右侧避让微信原生胶囊 | 标题单行截断、返回可用、胶囊不重叠 |
| 详情 / 分享直达 | 展示返回按钮，并提供无页面栈兜底 | 分享直达不白屏、不报错、可回首页或安全入口 |

后续页面不得重复手写互相冲突的导航结构。若确需页面专属顶部布局，必须在 Change design 和验收中说明原因。

## 状态栏与胶囊

自定义导航不得硬编码单一机型高度。实现或验收时应优先使用微信小程序可获取的窗口、状态栏和菜单按钮信息，或项目确认的兼容封装。

必须说明和验收的字段：

| 字段 | 含义 | 验收方式 |
|---|---|---|
| `status_bar_height` | 状态栏高度 | DevTools / 真机记录数值或人工摘要 |
| `navigation_content_height` | 导航内容区域高度 | 与胶囊高度、触控热区一起复核 |
| `navigation_total_height` | 状态栏 + 内容区总高度 | 页面 offset 使用同一值或等价 token |
| `native_capsule_reserve` | 右侧原生胶囊不可占用宽度 | 标题、Logo、返回和操作按钮不进入 reserve |

Fallback 规则：

- 获取状态栏高度失败时使用项目统一 fallback，不得各页面自行猜测。
- 获取胶囊矩形失败时使用项目统一 reserve 宽度和导航内容高度。
- fallback 值必须集中维护或集中说明。
- 若 fallback 参与验收，evidence 必须记录触发原因和剩余风险。

禁止事项：

- 禁止在 WXML / WXSS 中自绘模拟微信分享按钮、关闭按钮或系统胶囊。
- 禁止将标题、品牌文案、Logo、返回按钮、搜索入口或操作按钮放入原生胶囊区域。
- 非分享页面不得因右侧 reserve 出现不可点击的伪分享按钮。

## 返回兜底

统一返回策略：

```text
点击返回
  |
  +-- 有上一页页面栈：wx.navigateBack()
  |       |
  |       +-- fail：进入首页兜底
  |
  +-- 无上一页页面栈：进入首页兜底
          |
          +-- fail：wx.reLaunch() 或项目确认的安全入口
```

验收要求：

- 分享卡片、扫码、收藏入口或外部入口直达详情页时，返回按钮不得失效、报错或无反馈。
- 加载态、空状态和错误态下返回按钮仍应可用，除非页面存在明确不可中断操作。
- 返回按钮触控热区不得小于 44x44 pt 或项目等价触控标准。
- 返回行为不得破坏当前页面分享、刷新、重试或埋点语义。

## 页面 offset

当导航栏使用 fixed 或 sticky 顶部定位时，页面主体必须避让真实导航高度。推荐统一策略至少选择一种：

- 导航组件提供 spacer，占位高度等于真实导航高度。
- 导航组件向页面暴露 CSS 变量、style 片段或等价布局 token。
- 页面根容器通过统一 class、mixin 或 utility 使用导航高度。

必须纳入内容不遮挡验收的区域：

- 首页首屏、搜索框、分类列表、商品列表、SKU 媒体区、收藏列表、证书列表和门店信息。
- 加载态、骨架屏、空状态、错误态和网络失败提示。
- 下拉刷新区域、滚动容器顶部和横向窄屏内容。

不同页面不得各自硬编码互相冲突的顶部 padding。确需特殊 offset 时，必须在页面验收中记录原因。

## 页面接入 checklist

- [ ] 页面是否需要自定义导航；若豁免，已写明 N/A reason。
- [ ] 页面形态已识别：首页、TabBar、普通非首页、详情 / 分享直达。
- [ ] 标题固定或动态均可单行截断，不挤压胶囊 reserve。
- [ ] 返回按钮展示规则、页面栈兜底和首页兜底均已验收。
- [ ] 页面首屏、加载态、空状态和错误态不被导航栏遮挡。
- [ ] 原生分享页面保留分享路径和关键参数。
- [ ] DevTools 与真机 evidence 按截图矩阵记录。

## 截图验收矩阵

| 维度 | 建议覆盖 | 结论字段 |
|---|---|---|
| 页面 | 首页、搜索、分类、商品列表、商品详情、收藏、证书、门店信息 | 首屏内容不被遮挡 |
| 入口 | 首页跳转、TabBar 切换、列表进入详情、分享直达详情、异常参数直达 | 返回路径与兜底路径可用 |
| DevTools 视口 | 320 pt、375 pt、430 pt | 标题、返回、胶囊 reserve 不重叠 |
| 真机类型 | iPhone 刘海屏、iPhone 非刘海屏、Android 常见机型 | 状态栏、安全区、胶囊和触控真实可用 |
| 页面状态 | 正常、加载、空状态、错误态、网络失败、长标题 | 无横向滚动，状态页不被遮挡 |

每条 evidence 至少记录：

```yaml
target: REQ/Bug/Change ID
page_path: pages/tile-detail/index?sku_id=...
entry: share_direct | tabbar | list_to_detail | home_jump
viewport: 320pt | 375pt | 430pt | device
source: devtools | real_device | static_test | not_applicable
status: required | passed | failed | blocked | not_applicable | follow_up
artifact_ref: screenshots/... | videos/... | manual-summary
conclusion:
  status_bar: pass | fail | blocked | not_applicable
  capsule_reserve: pass | fail | blocked | not_applicable
  back_fallback: pass | fail | blocked | not_applicable
  content_offset: pass | fail | blocked | not_applicable
remaining_risk:
```

## DevTools 与真机边界

本文档复用 `docs/standards/miniapp-device-evidence-template.md` 的 evidence 状态与字段。

- DevTools evidence 不等同于真机验收。
- 没有真机记录时不得写作真机通过。
- 无法执行真机验证时，必须标记 `blocked` 或 `follow_up` 并说明原因。
- `not_applicable` 必须写明 N/A reason。
- `failed` 必须记录失败表现、影响页面和后续处理建议。
- `follow_up` 必须记录剩余风险和后续承接方式。

## 安全边界

截图、录屏、报告和人工摘要必须使用仓库相对路径或稳定 artifact 引用。不得记录：

- 本机绝对路径。
- token、Cookie、Authorization header。
- `.env` 内容、真实密钥、数据库 DSN、MinIO 凭据。
- 真实客户数据、未脱敏手机号、地址或个人隐私。
- 大段日志、完整构建输出或无法复核的口头描述。

若截图包含敏感信息，必须脱敏或记录不可公开原因。

## 引用示例

REQ `acceptance.md`：

```markdown
- [ ] 自定义导航相关页面已按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 完成状态栏、胶囊、返回兜底、页面 offset 和截图矩阵验收。
```

OpenSpec `tasks.md`：

```markdown
- [ ] 按小程序自定义导航 best-practice 记录 DevTools 320/375/430 pt evidence；真机不可用时标记 blocked 或 follow_up。
```

Sprint `acceptance-report.md`：

```markdown
自定义导航 evidence 摘要：DevTools 375 pt passed；真机 Android blocked，原因为设备暂不可用，已承接 follow_up。
```

## 追溯

- `REQ-0053-miniapp-custom-navigation-best-practice`
- `openspec/changes/add-miniapp-custom-navigation-best-practice/`
- `REQ-0048-miniapp-global-custom-navigation-bar`
- `REQ-0052-miniapp-device-evidence-template`
- `docs/standards/miniapp-device-evidence-template.md`
- `docs/knowledge-base/retrospectives/sprint-008-retrospective.md`
