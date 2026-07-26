## Context

REQ-0064 已评审通过，目标是在微信小程序首页、SKU 详情页、商品列表页和品牌详情页形成一致的页面级微信分享契约。当前代码与规格中已有部分 `onShareAppMessage` 能力，但朋友圈分享、商品列表分享、分享直达、query 参数保留、设备 evidence 和运行 `.js` / `.ts` 一致性没有统一规格。

本 Change 只定义和实现小程序端页面级分享配置，不写后台分享文案配置、不新增海报或短链、不新增 API / DB。分享图复用现有页面数据中的公开安全 URL 或本地兜底资源。

相关知识库：

- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- `docs/knowledge-base/retrospectives/sprint-009-retrospective.md`

## Goals / Non-Goals

**Goals:**

- 四个目标页面支持分享给微信朋友和分享到朋友圈。
- 首页、SKU 详情、商品列表、品牌详情的分享标题、路径、query 参数和分享图兜底可验收。
- 商品列表页保留搜索、分类、品牌和榜单上下文。
- 分享直达继续满足自定义导航、原生胶囊避让、返回兜底和页面 offset。
- 分享埋点失败不阻断用户分享。
- 静态测试或等价验收覆盖实际运行 `.js` 与维护源码 `.ts` 的分享配置一致性。

**Non-Goals:**

- 不生成分享海报、品牌海报或朋友圈图片海报。
- 不新增后台分享标题、分享图或渠道策略配置。
- 不做裂变活动、短链系统、外部 H5 落地页或微信群差异化文案。
- 默认不新增 API、数据库表或字段。
- 不自绘微信分享按钮、关闭按钮或系统胶囊。

## Decisions

### D1. 使用页面级微信原生分享能力

各页面通过 `onShareAppMessage` 承接微信朋友分享，通过 `onShareTimeline` 承接朋友圈分享。这样符合微信小程序平台能力，也避免新增自绘分享面板。

替代方案：自定义分享按钮或分享面板。拒绝原因是 REQ-0064 明确不新增可见分享面板，并要求优先使用微信原生入口。

### D2. 每个页面本地构建分享上下文

首页使用门店 / 品牌名称或兜底标题；SKU 详情使用 SKU 分享标题、SKU 名称、品牌名称和主图；商品列表使用当前列表标题和 query 上下文；品牌详情使用品牌名称和 `brandId`。分享上下文构建应集中在页面内小函数或局部 helper，减少 `onShareAppMessage` 与 `onShareTimeline` 重复。

替代方案：新增后端分享配置接口。拒绝原因是本期不需要后台配置，也会扩大 API、DB 和管理端范围。

### D3. 商品列表 query 采用白名单保留

商品列表分享只保留 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section`、`sourcePage` 等已知上下文，并对中文分类名和搜索词编码。避免复制整个 query 或 raw payload，降低敏感信息和不可解析参数风险。

替代方案：直接序列化页面 `data`。拒绝原因是页面状态包含分页、计数、requestId 等不稳定字段，且不利于长期验收。

### D4. 埋点 best-effort

分享触发应记录页面、渠道和关键业务 ID，但埋点失败必须吞掉错误并继续返回微信分享对象。这与现有小程序服务中“埋点失败不阻断用户浏览、分享或咨询”的策略一致。

### D5. 设备 evidence 前置

实现阶段需要在 tasks 中加入 DevTools 320 / 375 / 430 pt 或等价静态视口验证，并明确真机不可用时的 `blocked` / `follow_up` 状态。不能把静态测试或 DevTools 预览写作真机通过。

## Conflict Resolution

本 REQ 的 prototype 仅有 `prototype/miniapp/context.md`，没有 HTML 或 PNG。优先级为：

```text
prototype/miniapp/context.md > acceptance.md > ui-design.md > openspec/specs
```

结论：

- 不新增 HTML / PNG 原型是有意选择，因为微信原生分享无法由静态 HTML 准确表达。
- 页面可见 UI 不新增自绘分享面板或系统胶囊，验收以真实小程序页面、DevTools 或真机 evidence 为准。
- 若后续产品要求分享海报或自定义分享面板，必须另行 capture 或扩展 Change。

## Risks / Trade-offs

- [Risk] 朋友圈分享字段能力与微信基础库版本存在限制 → Mitigation: 实现阶段按微信平台实际能力降级，并在验收记录中说明字段差异。
- [Risk] `.ts` 修改后 `.js` 运行入口未同步 → Mitigation: tasks 要求静态测试检查目标页面 `.js` 与 `.ts` 均包含分享配置。
- [Risk] 商品列表上下文过多导致分享 URL 难维护 → Mitigation: 使用白名单 query，只保留业务可恢复参数。
- [Risk] 无法执行真机验收 → Mitigation: evidence 使用 `blocked` 或 `follow_up`，不得写作真机通过。

## Migration Plan

1. 在四个目标页面补齐或统一微信朋友分享与朋友圈分享配置。
2. 补充商品列表分享路径构建和 query 编码。
3. 补充分享埋点和非阻断兜底。
4. 更新小程序静态测试或等价验收，覆盖分享函数、路径参数和 `.js` / `.ts` 一致性。
5. 记录 DevTools / 真机 / blocked / follow_up evidence 结论。

Rollback：本 Change 默认不改 API / DB，可通过回退小程序页面分享配置与相关测试回滚。

## Open Questions

- 微信朋友圈分享图在当前基础库和目标环境中的展示规则是否需要人工验收确认。
- 真机 evidence 是否能在本 Sprint 内执行，或需要标记 follow_up。
