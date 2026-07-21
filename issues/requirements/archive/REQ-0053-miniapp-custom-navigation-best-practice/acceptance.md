---
requirement_id: REQ-0053-miniapp-custom-navigation-best-practice
title: 小程序自定义导航 best-practice 沉淀验收标准
status: done
created_at: 2026-07-19 18:41:33
updated_at: 2026-07-19 21:05:25
---

# REQ-0053 小程序自定义导航 best-practice 沉淀验收标准

## 1. 文档结构 AC

- [ ] AC-STRUCT-001 后续 best-practice 文档必须包含适用范围、导航结构、状态栏与胶囊、返回兜底、页面 offset、截图验收矩阵、接入 checklist 和引用示例。
- [ ] AC-STRUCT-002 best-practice 文档必须优先沉淀到 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 或评审确认的等价长期位置。
- [ ] AC-STRUCT-003 文档必须明确其来源于 REQ-0048 自定义导航经验、REQ-0052 evidence 模板和 sprint-008 复盘行动项。
- [ ] AC-STRUCT-004 文档必须说明后续小程序 REQ、OpenSpec tasks、acceptance 和 Sprint 验收报告如何引用该实践。

## 2. 状态栏与胶囊 AC

- [ ] AC-SAFEAREA-001 文档必须要求自定义导航优先使用微信小程序窗口、状态栏和菜单按钮 API 或项目确认的兼容封装，不得硬编码单一机型高度。
- [ ] AC-SAFEAREA-002 文档必须定义状态栏高度、导航内容高度、总导航高度和右侧胶囊 reserve 的记录或验收方式。
- [ ] AC-SAFEAREA-003 文档必须定义获取状态栏或胶囊信息失败时的 fallback 策略，且 fallback 不得散落在多个页面。
- [ ] AC-CAPSULE-001 文档必须要求标题、品牌文案、Logo、返回按钮、搜索入口和操作按钮不得进入微信原生胶囊区域。
- [ ] AC-CAPSULE-002 文档必须禁止在 WXML / WXSS 中自绘模拟分享、关闭或系统胶囊。
- [ ] AC-CAPSULE-003 支持分享的页面必须继续使用微信原生分享能力，非分享页面不得出现不可点击的伪分享按钮。

## 3. 返回兜底 AC

- [ ] AC-BACK-001 文档必须要求有上一页页面栈时优先使用 `wx.navigateBack()`。
- [ ] AC-BACK-002 文档必须要求无上一页页面栈时进入明确兜底路径，默认建议返回首页。
- [ ] AC-BACK-003 文档必须要求返回兜底失败时具备二级安全入口，例如 `wx.reLaunch()` 到首页或项目确认的等价入口。
- [ ] AC-BACK-004 分享卡片、扫码、收藏入口或外部入口直达详情页时，返回按钮不得失效、报错或无反馈。
- [ ] AC-BACK-005 加载态、空状态、错误态下返回按钮仍应可用，除非页面存在明确不可中断操作。
- [ ] AC-BACK-006 返回按钮触控热区不得小于 44x44 pt 或项目等价触控标准。

## 4. 页面 offset AC

- [ ] AC-OFFSET-001 文档必须要求 fixed / sticky 导航下页面主体通过统一 spacer、CSS 变量、style 片段、class 或等价布局 token 避让导航高度。
- [ ] AC-OFFSET-002 首页首屏、搜索框、分类列表、商品列表、SKU 媒体区、收藏列表、证书列表和门店信息均必须纳入内容不遮挡验收。
- [ ] AC-OFFSET-003 加载态、骨架屏、空状态、错误态、网络失败提示、滚动容器顶部和下拉刷新区域必须纳入 offset 验收。
- [ ] AC-OFFSET-004 不同页面不得各自硬编码互相冲突的顶部 padding；若确需特殊 offset，必须在页面验收中记录原因。
- [ ] AC-OFFSET-005 320 到 430 pt 常见宽度下不得出现横向滚动、标题挤压胶囊 reserve 或首屏内容被导航遮挡。

## 5. 页面接入 checklist AC

- [ ] AC-CHECK-001 checklist 必须要求识别页面是否需要自定义导航；若豁免，必须写明 N/A reason。
- [ ] AC-CHECK-002 checklist 必须区分首页形态、TabBar 页面形态、普通非首页形态和详情 / 分享直达形态。
- [ ] AC-CHECK-003 checklist 必须要求标题固定、动态、单行截断和胶囊 reserve 挤压风险可验收。
- [ ] AC-CHECK-004 checklist 必须要求返回按钮展示、页面栈兜底和首页兜底均可验收。
- [ ] AC-CHECK-005 checklist 必须要求页面是否支持原生分享、分享路径和关键参数保留均可验收。

## 6. 截图验收矩阵 AC

- [ ] AC-MATRIX-001 矩阵必须覆盖首页、搜索、分类、商品列表、商品详情、收藏、证书和门店信息。
- [ ] AC-MATRIX-002 矩阵必须覆盖首页跳转、TabBar 切换、列表进入详情、分享直达详情和异常参数直达。
- [ ] AC-MATRIX-003 矩阵必须覆盖 DevTools 320 pt、375 pt、430 pt 视口。
- [ ] AC-MATRIX-004 矩阵必须建议覆盖 iPhone 刘海屏、iPhone 非刘海屏和 Android 常见机型；无法执行时必须标记 blocked 或 follow_up。
- [ ] AC-MATRIX-005 矩阵必须覆盖正常、加载、空状态、错误态、网络失败和长标题。
- [ ] AC-MATRIX-006 矩阵结论必须能记录状态栏不遮挡、胶囊不重叠、返回可用、首屏内容不被遮挡和无横向滚动。
- [ ] AC-MATRIX-007 每条 evidence 必须支持截图或录屏引用、执行环境、结论、阻塞项和剩余风险。
- [ ] AC-MATRIX-008 DevTools evidence 与真机 evidence 必须分层记录；没有真机记录时不得写作真机通过。

## 7. 范围与安全 AC

- [ ] AC-SCOPE-001 本需求不新增或修改小程序业务页面。
- [ ] AC-SCOPE-002 本需求不直接重构 `src/miniapp/components/custom-navigation/`；如需修改源码，必须在后续 OpenSpec Change 中明确。
- [ ] AC-SCOPE-003 本需求不新增小程序自动化截图、真机云测或 DevTools 控制工具。
- [ ] AC-SCOPE-004 本需求不强制回填全部历史截图或验收记录。
- [ ] AC-SCOPE-005 本需求不修改 API、数据库、Orval、Docker Compose、MinIO 或环境变量。
- [ ] AC-SAFE-001 截图、录屏或报告引用必须使用仓库相对路径或稳定 artifact 引用，不得记录本机绝对路径、密钥、token、Cookie、`.env` 内容或真实客户隐私。

## 8. 引用与流程 AC

- [ ] AC-REF-001 REQ `acceptance.md`、OpenSpec `tasks.md`、OpenSpec `acceptance.md` 或 `trace.md`、Sprint `acceptance-report.md` 均可引用该 best-practice。
- [ ] AC-REF-002 后续小程序导航、fixed header、分享、返回或页面顶部布局相关 Change 必须检查该 best-practice 是否仍适用。
- [ ] AC-REF-003 若实践已过期，后续 Change 必须同步更新 best-practice 或记录豁免原因。
- [ ] AC-REF-004 Sprint acceptance-report 只应记录矩阵摘要、结论、blocked 和 follow_up，不复制完整证据表。

## 横切 AC（knowledge-base）

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| 无匹配标签 | 本 REQ 为微信小程序导航 best-practice 与验收矩阵治理，不命中管理端列表、表单、弹窗或媒体上传横切标签 | 0 |

最近复盘参考：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md`。与本 REQ 相关的复发预防点为小程序自定义导航建立独立 best-practice，统一状态栏、胶囊避让、返回兜底、页面 offset 和 320/375/430 pt 设备验收矩阵，避免自动化通过被误写成真实设备验收完成。
