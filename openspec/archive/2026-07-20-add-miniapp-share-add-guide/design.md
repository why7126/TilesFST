## Context

`REQ-0061-miniapp-share-add-guide` 已评审通过，目标是在微信小程序进入场景提示用户通过右上角系统入口添加到“我的小程序”，降低下次找回成本。现有 `miniapp-home` 已定义首页品牌导航、首屏内容和原生系统按钮边界；`miniapp-global-custom-navigation-bar` 已定义状态栏、微信原生胶囊、fixed header offset 和禁止手绘系统胶囊；`miniapp-device-evidence-template` 已定义 DevTools / 真机 evidence 边界。

本 Change 新增小程序端轻量引导能力，不修改微信原生菜单，不新增 API / DB / Orval，不提供后台配置。实现阶段必须继续遵守 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。

## Goals / Non-Goals

**Goals:**

- 在用户进入小程序时展示“添加到我的小程序”含义明确的轻量引导语。
- 引导语与右上角微信原生菜单 / 分享入口形成视觉关联，但不得覆盖或模拟系统胶囊。
- 用户可以手工关闭引导语；关闭后至少当前会话内不再展示。
- 在首页、分享进入、扫码进入、加载/错误/空状态等场景下安全降级，不阻断主功能。
- 为后续实现提供可测试的 DevTools / 真机 evidence 要求。

**Non-Goals:**

- 不修改微信右上角原生菜单、分享、关闭或添加到我的小程序的系统行为。
- 不手绘微信系统分享按钮、更多按钮、关闭按钮或胶囊。
- 不新增后端配置接口、数据库字段、后台管理页或 Orval 生成物。
- 不引入营销弹窗、优惠券、用户画像定向或活动运营卡片。
- 不直接实现代码；实现由后续 `/opsx-apply` 或 Sprint apply 承接。

## Decisions

### D1 引导语作为小程序本地 UI 状态

实现阶段应优先在 `src/miniapp` 内新增共享引导组件或首页局部组件，以小程序本地状态控制展示/隐藏。关闭状态优先使用小程序本地存储或会话内状态，不依赖服务端。

备选方案：服务端配置或后台开关。当前需求默认不需要运营配置，使用服务端会扩大 API、DB、Orval 和管理端范围，因此不纳入本 Change。

### D2 位置计算复用导航安全区与胶囊 reserve

引导语位置应基于微信菜单按钮信息、状态栏高度或项目统一 fallback 计算，避免硬编码单一机型。引导语可以位于胶囊左下方或相邻安全区域，但容器、箭头和关闭入口不得进入原生胶囊 reserve。

备选方案：固定 CSS top/right。该方案容易在 320 pt、刘海屏、Android 胶囊差异下错位，因此只允许作为集中 fallback，不允许各页面散落硬编码。

### D3 关闭策略保守落地

评审接受“至少当前会话内不再展示”为默认底线。若实现阶段选择当天或长期不再展示，必须在 tasks/acceptance 记录具体策略，并验证再次进入行为。

备选方案：严格每次进入都展示。该方案与“允许用户手工关闭”存在体验冲突，除非产品再次确认，否则不作为默认实现策略。

### D4 设备验收分层

后续实现必须记录 DevTools 320、375、430 pt evidence。真机 evidence 作为高风险交互推荐项；若环境不可用，必须标记 `blocked` 或 `follow_up`，不得写作真机通过。

备选方案：只用静态测试。静态测试可检查伪胶囊、自绘系统按钮和文件接入，但不能证明真实胶囊、安全区、触控和真机布局，因此不能替代设备验收。

## Conflict Resolution

原型优先级按 `HTML > PNG > context > acceptance > ui-design.md > openspec/specs` 执行。本 REQ 只有 `prototype/miniapp/prototype.html` 和 `context.md`，无 PNG Golden Reference。

- `prototype.html` 展示气泡在原生胶囊左下方，是位置意图而非强制像素实现。
- `context.md` 明确“安全降级时可不展示气泡”，优先于“每次进入必须强制展示”的字面理解。
- `acceptance.md` 明确关闭后至少当前会话不再展示；实现不得让用户关闭后同一会话反复出现。
- `miniapp-global-custom-navigation-bar` 的胶囊 reserve 和禁止手绘系统胶囊规则优先于任何装饰箭头或提示气泡视觉。

## Risks / Trade-offs

- [风险] 胶囊位置在不同设备上不一致，提示气泡可能遮挡系统入口。 → [缓解] 使用菜单按钮信息或集中 fallback，并强制 DevTools 320/375/430 pt evidence。
- [风险] 每次进入展示可能造成打扰。 → [缓解] 手工关闭后至少当前会话不再展示，长期策略在实现验收中记录。
- [风险] 静态测试被误写成真机验收通过。 → [缓解] 引用 `miniapp-device-evidence-template`，缺少真机时必须写 `blocked` 或 `follow_up`。
- [风险] 后续埋点诉求扩大 API / DB 范围。 → [缓解] 本 Change 默认不新增服务端能力；若需要服务端埋点，另行变更并同步文档和测试。

## Migration Plan

1. 在后续实现阶段新增或接入小程序引导组件。
2. 接入首页进入场景，必要时扩展到全局页面入口，但必须保证非首页不遮挡。
3. 增加关闭状态控制和本地状态降级。
4. 补充静态测试与设备 evidence。
5. 若发现必须新增 API / DB / Orval，停止实现并补充对应 OpenSpec、docs 和测试计划。

回滚策略：移除或禁用引导组件入口，保留现有首页、导航、分享和返回能力不变。

## Open Questions

- 关闭状态最终采用当前会话、当天还是长期记忆？
- 引导是否只在首页展示，还是分享/扫码进入非首页也展示？
- 是否需要后续独立 REQ 承接引导展示/关闭埋点？
