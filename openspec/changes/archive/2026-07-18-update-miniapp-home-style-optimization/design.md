## Context

`REQ-0043` 是 `REQ-0041-miniapp-home` 的 refinement。现有正式 spec 已定义小程序首页、首页聚合、Banner/快捷入口、搜索/详情、分享咨询、热销统计、原型范围和运行入口质量门禁。本 Change 不重建小程序首页基础能力，而是在现有能力上明确新的视觉结构、瀑布流承接和未完成页安全降级。

原型输入位于 `issues/requirements/archive/REQ-0043-miniapp-home-style-optimization/prototype/miniapp/`，其中 `prototype.html` 是可执行布局参考，`context.md` 记录原型策略。需求已纳入 `sprint-008`，但实现前仍必须先完成本 OpenSpec Change。

## Goals / Non-Goals

**Goals:**

- 让首页符合深色品牌展厅风格，强化菲尚特瓷砖品牌识别。
- 将首页快捷入口稳定为“选瓷砖、品牌馆、新品榜、热销榜”。
- 在热销推荐下新增全部产品双列瀑布流，支持分页、去重和失败重试。
- 保证收藏、证书、品牌馆、新品榜/热销榜独立页等未完成能力安全降级，不出现白屏或路由错误。
- 补充首页交互事件，支持后续判断收藏、证书和榜单能力优先级。

**Non-Goals:**

- 不新增收藏持久化 API、收藏列表、收藏统计或用户维度收藏状态。
- 不新增完整证书聚合页、证书详情页或公开证书 API。
- 不新增品牌馆独立页、品牌详情页、新品榜独立页或热销榜独立页。
- 不新增快捷入口后台配置能力。
- 不新增订单、库存、新增、编辑、上下架、客户管理等后台入口。
- 不强制切换全局 `navigationStyle: custom`；若实现阶段选择自定义导航，必须额外处理状态栏、胶囊、安全区和机型适配。

## Decisions

### D1. Change 类型：update

`openspec/specs/miniapp-home/spec.md` 已存在首页首期能力，`product-usage-logging` 已存在小程序详情访问、分享、咨询事件。本 Change 修改既有能力要求并增加新场景，因此使用 `update-miniapp-home-style-optimization`，不创建新的 capability。

### D2. 原型优先级与冲突处理

冲突优先级采用：

```text
prototype.html
  > prototype.png（用户附件，若后续落盘）
  > prototype/miniapp/context.md
  > acceptance.md
  > rules/ui-design.md
  > openspec/specs
```

Conflict Resolution：

- `prototype.html` 中模拟微信状态栏和胶囊按钮的 DOM 只作为视觉参考，不得在真实小程序页面复刻系统控件。
- `REQ-0041` 旧快捷入口“按空间、按规格、按风格、按颜色或全部分类”被 REQ-0043 的“四入口”替代。
- `REQ-0041` 要求收藏能力不进入本期；REQ-0043 允许心形作为非持久化视觉反馈或建设中提示，但不得承诺或实现收藏持久化。
- `REQ-0041` 原底部 TabBar 可含“我的”；REQ-0043 目标文案调整为：首页、分类、找砖、收藏、证书。收藏和证书未完整实现时必须安全降级。

### D3. 数据复用优先

实现阶段优先复用现有首页聚合、Banner 和 `/api/v1/miniapp/products` 公开商品列表。全部产品瀑布流若需要 `has_more`，优先由前端基于 `total/page/page_size` 推导；只有现有响应无法稳定判断时才扩展 API，并同步 OpenAPI、Orval、docs 和 tests。

### D4. 小程序样式策略

小程序端可以在 `.wxss` 中使用 REQ 明确的品牌色值作为小程序页面局部样式事实源。Web Design System 的 semantic token 规则不直接约束原生小程序 `.wxss`，但视觉语义必须与 `rules/ui-design.md` 中的“工业石材 · 暗色旗舰风”一致。

### D5. 埋点不阻断主流程

首页搜索、快捷入口、商品点击、瀑布流加载、加载失败、收藏视觉点击和证书 Tab 点击均作为 usage event 或前端预留事件处理。埋点失败不得阻断浏览、跳转、分页或降级提示。

## Risks / Trade-offs

- [Risk] REQ-0043 与 REQ-0041 修改同一首页文件，容易出现范围重叠或回归 → Mitigation: tasks 先确认 REQ-0041 当前实现和 BUG-0065 运行入口修复状态，再按模块分层改动。
- [Risk] 原型视觉中模拟系统胶囊，真实小程序复刻会和微信原生导航冲突 → Mitigation: Header 禁止模拟系统状态栏、分享按钮、关闭按钮和胶囊；如使用自定义导航，需单独处理安全区。
- [Risk] 瀑布流分页可能重复触发并发请求或重复商品 → Mitigation: 状态机必须包含 `loading/finished/retry`，并按 `product_id` 去重。
- [Risk] 收藏和证书入口被误解为完整能力 → Mitigation: spec 明确只允许视觉反馈、建设中提示或占位页，不新增持久化/API/聚合页。
- [Risk] 新增事件字段过宽 → Mitigation: 事件只允许商品 ID、入口标识、页面标识、client type 和时间上下文，禁止聊天内容、Authorization、Cookie、手机号等敏感信息。

## Migration Plan

1. 在 `/opsx-apply` 中先确认当前小程序实际运行入口与 `REQ-0041` 首页实现状态。
2. 按首页模块逐步替换视觉和结构，保留已有公开接口和详情跳转。
3. 增加瀑布流状态机与降级状态，补齐测试。
4. 增加或预留 usage event 字典与客户端上报，埋点失败不阻断主流程。
5. 若 API 需要扩展，补齐 OpenAPI、Orval、docs 和后端测试。

## Open Questions

- 是否在本 Change 中落盘用户附件 `prototype.png` 作为 Golden Reference？当前 trace 记录为建议，若需要视觉验收截图可在 apply 阶段补入。
- `/api/v1/miniapp/products` 当前响应是否已足以推导 `has_more`？实现阶段以代码和测试确认。
