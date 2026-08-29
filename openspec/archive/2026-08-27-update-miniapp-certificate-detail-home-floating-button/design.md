## 上下文

REQ-0125 已完成评审并纳入 `sprint-026`。当前小程序已存在 `components/home-floating-button/`，并已在多个非首页深层页面复用；证书详情页 `pages/certificate-detail/index` 已具备 `custom-navigation`、证书媒体区、证书信息、品牌入口、错误态和分享能力，但尚未声明并挂载返回首页悬浮按钮。

本 Change 属于小程序 UI 导航一致性更新。它不引入新业务能力，也不改变证书详情 API、品牌证书数据模型、对象存储读取策略或全局返回首页组件契约。

## 目标与非目标

**目标：**

- 在证书详情页接入既有 `home-floating-button`，默认传入 `offset="list"`。
- 保持证书详情页原有自定义导航左上返回能力、页面数据加载、媒体预览、品牌入口和分享路径不变。
- 覆盖正常态、加载态、错误态、证书不可查看、分享直达和快速重复点击的回首页路径。
- 在实现阶段补充静态检查和 DevTools 320 / 375 / 430 pt evidence。

**非目标：**

- 不调整 `home-floating-button` 的视觉、跳转、导航锁、offset 枚举或失败提示。
- 不新增页面私有悬浮按钮样式、私有 offset 或私有跳转逻辑。
- 不扩展门店信息页、找砖页或其他页面的返回首页覆盖范围。
- 不变更后端 API、数据库、对象存储、Web 管理端、店主 Web、Orval 或 Docker Compose。

## 设计决策

### D1 复用全局返回首页悬浮按钮

实现阶段 SHALL 在 `pages/certificate-detail/index.json` 声明 `home-floating-button`，并在 `index.wxml` 挂载组件。页面不实现独立点击处理器，不复制 `wx.switchTab` / `wx.reLaunch` 兜底逻辑。

选择依据：

- 全局组件已经承接首页路径、导航锁、失败兜底和忙碌态。
- 复用组件可以避免证书详情页与其他深层页面在按钮文案、触控反馈和失败路径上分叉。

备选方案：

- 页面私有按钮和私有跳转逻辑：拒绝，违反 REQ-0125 的组件复用和一致性要求。

### D2 固定使用 `offset="list"`

证书详情页后续实现 SHALL 默认挂载为 `<home-floating-button offset="list" />` 或等价语义。若实现阶段发现证书详情页存在固定底部操作区，仍应优先说明为何 `list` 能满足核心内容可用；不得新增私有 offset 值。证书信息字段被悬浮按钮局部覆盖可接受，页面不为证书信息卡新增右侧避让。

选择依据：

- 证书详情页没有底部固定购物、询价或预览操作条，页面形态更接近品牌详情页、商品列表页和商品详情页无底部操作区状态。
- `offset="list"` 是既有组件枚举，能维持页面间位置口径。

### D3 `.ts` 与 `.js` 同步维护

后续实现 SHALL 同步维护 `index.ts` 与 `index.js`，避免小程序构建、上传或运行入口使用不同源文件时出现漂移。若实现只需修改 JSON/WXML，也 SHALL 通过静态检查确认 TS/JS 无行为分叉。

### D4 验收证据前置

本 Change 的实现不要求新增完整视觉原型，但必须记录小程序 UI 证据。DevTools 320 / 375 / 430 pt evidence SHALL 覆盖标题、原生胶囊 reserve、内容 offset、品牌入口同宽、证书信息非避让排版和悬浮按钮位置一致结论。证书信息字段被按钮局部覆盖可接受；真机证据不可用时 SHALL 标记 `blocked` 或 `follow_up`。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | `prototype/miniapp/prototype-context.md` > `acceptance.md` > `requirement.md` > `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` > `rules/ui-design.md` > 已归档 OpenSpec specs。 |
| 页面与入口 | 页面为 `src/miniapp/pages/certificate-detail/index`；入口包括证书列表、品牌详情证书区域和微信分享直达。 |
| 信息架构 | 保持 `custom-navigation(title="证书详情")`、证书媒体区、证书信息、品牌入口、错误/空态；新增 `home-floating-button(offset="list")` 为页面级悬浮入口。 |
| 视觉 token | 复用 `home-floating-button` 的既有尺寸、图标、文案、圆角、阴影、按压态和 busy 态；不新增证书详情页私有颜色、阴影、圆角或文案。 |
| 交互状态 | 覆盖正常态、加载态、错误态、证书不可查看、分享直达、快速重复点击和导航失败兜底；导航锁释放沿用组件现有策略。 |
| 图标与文案 | 返回首页入口使用组件既有图标与“首页”或等价首页语义；左上返回保持“返回上一页 / 无页面栈兜底首页”语义。 |
| Mock/API 边界 | 不新增 Mock 或真实 API；证书详情数据、品牌入口数据、媒体 URL 和分享数据沿用既有证书详情能力。 |
| 权限规则 | 公开小程序页面能力；不可公开、隐藏、删除或非法证书继续走既有错误/不可查看状态。 |
| 一致性参照 | 与商品详情页、品牌详情页、商品列表页等已接入 `home-floating-button` 的深层页面对齐；与 `miniapp-custom-navigation` best practice 对齐。 |

## 风险与取舍

- 内容遮挡风险 → 通过 `offset="list"`、320 / 375 / 430 pt evidence 和错误态/品牌入口状态覆盖验收；证书信息字段局部覆盖为验收允许项。
- 分享直达无页面栈风险 → 同时验证自定义导航左上返回兜底和悬浮按钮回首页路径。
- 重复点击导航锁残留风险 → 复用组件现有导航锁，并在测试与人工 evidence 中覆盖首次点击、再次进入和快速重复点击。
- TS/JS 漂移风险 → 通过静态检查或等价脚本覆盖 `.ts` 与 `.js` 同步。

## 迁移与回滚

实现为小程序页面级组件声明和 WXML 挂载。若上线后发现遮挡或导航异常，可回滚证书详情页的组件声明和 WXML 引用；不需要数据库回滚、API 回滚或 Orval 重新生成。

## 未决问题

无。
