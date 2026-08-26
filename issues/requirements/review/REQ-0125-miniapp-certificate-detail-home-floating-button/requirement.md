---
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
title: 小程序证书详情页新增返回首页悬浮按钮
terminal: miniapp
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P2
parent_requirement: REQ-0085-miniapp-global-home-floating-button
created_at: 2026-08-25 22:35:40
updated_at: 2026-08-26 08:32:09
related_change: update-miniapp-certificate-detail-home-floating-button
---

# REQ-0125 小程序证书详情页新增返回首页悬浮按钮

## 1. 需求背景

小程序已存在统一的 `home-floating-button` 返回首页悬浮按钮，用于帮助用户从非首页深层页面快速回到首页。当前商品详情页、品牌详情页、商品列表页、搜索结果页、分类页、品牌列表页、收藏页和证书列表页已具备该入口，但证书详情页仅有自定义导航栏返回能力，缺少明确的【返回首页】悬浮按钮。

证书详情页承载品牌资质图片、证书信息、品牌入口和分享承接。用户从证书列表、品牌详情或分享进入证书详情后，若希望回到首页继续浏览品牌、分类或推荐商品，需要依赖页面栈返回或重新进入 Tab。为保持小程序深层页面导航体验一致，本需求要求证书详情页新增返回首页悬浮按钮，并复用现有组件和位置口径。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 装修客户 | 查看证书详情后，可快速回到首页继续浏览推荐、分类和品牌入口。 |
| 设计师 | 从分享或品牌证书路径进入后，可快速回到首页切换其他资料。 |
| 门店导购 | 演示证书资质后，可一键回到首页继续介绍产品和品牌内容。 |
| 产品与测试人员 | 用统一组件和统一 offset 验收证书详情页与其他深层页面的导航一致性。 |

## 3. 范围

### 3.1 本期包含

- 小程序证书详情页 `pages/certificate-detail/index` 新增【返回首页】悬浮按钮。
- 按钮复用已有 `components/home-floating-button/` 组件，不新增页面私有按钮样式。
- 按钮位置与其他同类深层页面保持一致，默认使用 `offset="list"`。
- 点击按钮后沿用现有组件的返回首页策略：优先 `wx.switchTab` 到 `/pages/index/index`，失败时使用组件内兜底。
- 加载态、空态、错误态、分享直达等证书详情页状态下保持可返回首页。
- 保留证书详情页原有 `custom-navigation` 左上返回能力。

### 3.2 本期不包含

- 不重构证书详情页整体布局、顶部媒体区、品牌入口、分享能力或证书字段展示。
- 不调整 `home-floating-button` 组件的全局视觉、跳转逻辑、锁定策略或 offset 枚举。
- 不新增门店信息页、找砖页或其他页面的返回首页悬浮按钮覆盖范围。
- 不调整底部 TabBar、自定义导航栏或首页路由。
- 不新增后台配置、开关、埋点统计或运营报表。
- 不涉及后端 API、数据库、对象存储、Web 管理端或店主 Web。

## 4. 功能要求

### FR-001 证书详情页展示返回首页悬浮按钮

- 证书详情页 MUST 展示明确的返回首页悬浮按钮。
- 按钮 MUST 复用 `home-floating-button` 组件，避免页面私有跳转逻辑和样式分叉。
- 按钮语义 MUST 与现有组件保持一致，对用户呈现“首页”或等价首页入口含义。
- 证书详情页原有左上返回能力 MUST 保持可用，不得因新增悬浮按钮被移除或改变语义。

### FR-002 offset 位置与其他页面保持一致

- 证书详情页悬浮按钮 MUST 使用与其他非 Tab 深层内容页一致的位置口径。
- 默认实现 SHOULD 使用 `offset="list"`，与品牌详情页、商品列表页以及商品详情页无底部操作区状态保持一致。
- 按钮不得使用页面私有 offset、临时 class 或复制样式来模拟位置。
- 若后续实现发现证书详情页存在固定底部操作区，应在 OpenSpec 设计中说明是否仍保持 `list`，或按既有组件规则调整为已有 offset 枚举；不得新增未治理的 offset 值。

### FR-003 点击后返回小程序首页

- 用户点击悬浮按钮后，MUST 返回小程序首页 `/pages/index/index`。
- 返回首页策略 MUST 沿用 `home-floating-button` 现有实现，优先使用 `wx.switchTab`，失败时使用兜底跳转。
- 连续点击时 MUST 遵守组件现有导航锁定策略，避免重复跳转、页面栈异常或多次 toast。
- 返回首页失败时 SHOULD 使用组件现有失败提示，不引入证书详情页私有提示文案。

### FR-004 页面状态下保持可用

- 证书详情正常加载完成时，悬浮按钮 MUST 可见且可点击。
- 证书详情加载中、接口失败、证书不存在、证书隐藏、图片失败或分享直达无页面栈时，按钮 SHOULD 仍作为回首页恢复路径保留。
- 若页面出现不可交互的全屏遮罩、系统文件预览或原生图片预览，悬浮按钮展示与点击以小程序原生能力为准，不额外改造全屏场景。
- 按钮展示不得影响图片预览入口、品牌入口和页面滚动；证书信息字段被按钮覆盖可接受，页面不为证书信息卡新增右侧避让。

### FR-005 不影响既有证书详情能力

- 新增悬浮按钮不得改变证书详情数据加载、错误处理、分享路径、品牌入口、证书图片展示或文件预览逻辑。
- 证书详情页不得因为新增按钮引入 API 请求、数据库字段或后端权限判断变化。
- 若页面已接入 `brand-card`，悬浮按钮不得遮挡品牌卡片点击区域或造成触控冲突。
- 后续实现应同步维护 `.ts` 与 `.js` 版本，避免小程序构建时出现逻辑漂移。

## 5. UI / UE 约束

- 按钮视觉 MUST 使用现有 `home-floating-button` 组件视觉，包括图标、文案、尺寸、按压态和禁用/忙碌态。
- 按钮位置 MUST 与其他页面保持一致，默认 `offset="list"`。
- 在 320 到 430 pt 常见小程序手机宽度下，按钮不得遮挡证书主图、品牌入口卡片、错误态按钮或底部安全区；证书信息字段允许被悬浮按钮局部覆盖。
- 页面滚动时按钮 SHOULD 保持固定悬浮位置，符合既有组件表现。
- 按钮层级应足以被用户发现，但不得压过图片预览、品牌入口等核心操作。
- 不新增证书详情页专属悬浮按钮颜色、阴影、圆角或文案。

## 6. 数据、接口与测试影响

| 范围 | 影响 |
|---|---|
| 微信小程序 | 影响 `pages/certificate-detail/index` 页面组件声明与 WXML 挂载。 |
| 组件 | 复用 `components/home-floating-button/`，不改变组件契约。 |
| 后端 API | 不涉及。 |
| SQLite / MySQL | 不涉及。 |
| 对象存储 / 媒体 | 不涉及。 |
| Web / 管理端 | 不涉及。 |
| Orval | 不需要。 |
| Docker Compose | 不需要。 |
| 测试 | 后续实现应补充或更新小程序静态检查，覆盖证书详情页组件声明、WXML 引用和 `.ts` / `.js` 同步。 |

## 7. 关联需求

| 需求 | 关系 | 说明 |
|---|---|---|
| `REQ-0085-miniapp-global-home-floating-button` | parent | 已定义小程序非首页页面返回首页悬浮按钮的统一能力。 |
| `REQ-0080-miniapp-certificate-detail-page` | related | 证书详情页基础能力。 |
| `REQ-0121-miniapp-certificate-detail-brand-card-entry` | related | 证书详情页品牌入口复用组件，新增悬浮按钮需避免遮挡品牌卡片。 |

## 8. 风险与待确认

| 风险 / 待确认 | 说明 |
|---|---|
| 内容遮挡 | 证书详情页主图、品牌卡片和错误态按钮位置需在实现验收中确认不被遮挡；证书信息字段允许被悬浮按钮局部覆盖。 |
| 页面状态覆盖 | 加载失败、空态、分享直达等状态是否全部展示按钮，需要在 `/req-complete` 的验收用例中细化。 |
| 其他缺口页面 | 门店信息页、找砖页等页面是否也需要显式悬浮按钮不纳入本需求；如需推进应单独 capture。 |

## 9. 状态块

```yaml
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
status: in_sprint
terminal: miniapp
version: v1
source: capture.md
priority: P2
parent_requirement: REQ-0085-miniapp-global-home-floating-button
lifecycle_stage: review
iteration: sprint-026
openspec_changes:
  - change_id: update-miniapp-certificate-detail-home-floating-button
    type: update
    status: applied
scope_summary: 小程序证书详情页复用 home-floating-button 新增返回首页悬浮按钮，offset 位置与其他深层内容页保持一致，默认使用 list
excluded_scope:
  - 证书详情页整体重构
  - home-floating-button 组件契约调整
  - 其他页面覆盖范围扩展
  - 后端 API、数据库、对象存储或 Web 端改造
next: /opsx-apply REQ-0125-miniapp-certificate-detail-home-floating-button
```
