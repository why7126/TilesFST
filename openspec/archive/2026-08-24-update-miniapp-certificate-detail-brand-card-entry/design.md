# 设计说明

## 上下文

REQ-0121 已评审通过并纳入 `sprint-025`。当前小程序已有 `brand-card` 组件规范，媒体多规格能力也已定义品牌 Logo 小图场景应使用 `thumbnail`。本 Change 聚焦证书详情页所属品牌入口的落地收敛：页面容器负责加载证书详情和传入品牌数据，`brand-card` 负责展示、跳转、不可用态和埋点。

关联事实源：

- `issues/requirements/archive/REQ-0121-miniapp-certificate-detail-brand-card-entry/requirement.md`
- `issues/requirements/archive/REQ-0121-miniapp-certificate-detail-brand-card-entry/acceptance.md`
- `issues/requirements/archive/REQ-0121-miniapp-certificate-detail-brand-card-entry/prototype/miniapp/prototype-context.md`
- `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`
- `docs/standards/prototype-ui-acceptance.md`

## 目标与非目标

目标：

- 证书详情页品牌入口复用 `brand-card`。
- 证书详情 `brand` 数据补齐 `brand_logo_thumbnail_url`。
- 普通品牌 Logo 展示优先使用缩略图，并提供安全占位，不请求原图作为性能通过 fallback。
- 点击跳转和埋点统一为 `brand_card_click`。
- 后续 `/opsx-apply` 可用 API、组件、静态测试和小程序媒体证据闭环。

非目标：

- 不重做证书详情页整体信息架构、媒体区、分享能力或证书字段展示。
- 不新增品牌主页、品牌商品列表、证书列表或商品详情页新能力。
- 不新增数据库表或通用图片派生能力。
- 不改管理端品牌证书维护页、上传弹窗或 Web UI。

## 关键决策

### D1 复用 brand-card 而不是页面私有品牌入口

证书详情页只负责从证书详情响应中取出 `brand` 数据，并转换为 `brand-card` 入参。组件继续负责 Logo、名称、入口提示、不可用态和点击逻辑。

理由：`brand-card` 已承载 SKU 详情页等品牌入口规则，复用可避免 Logo fallback、跳转和埋点分叉。

替代方案：在证书详情页内联品牌入口。该方案实现更快，但会重复已有组件规则，并增加后续多页面埋点和媒体字段维护成本，因此不采用。

### D2 brand_logo_thumbnail_url 由接口或适配层显式提供

实现阶段优先让证书详情 `brand` 数据显式包含 `brand_logo_thumbnail_url`。若后端已有同名或等价字段，应直接透出；若缺失，需要补齐 Schema、OpenAPI、Orval 或小程序服务类型。

理由：小程序端不应拼接对象存储 URL，也不应从原图字段推断缩略图路径。

替代方案：小程序端用 `brand_logo_url` 自行替换后缀或路径。该方案违反媒体 URL 受控边界，且无法稳定适配直出、签名或 CDN 预留，因此不采用。

### D3 事件名统一为 brand_card_click

证书详情页不定义页面私有点击事件名，而是通过 `brand-card` 上报 `brand_card_click`。事件参数带 `sourcePage=certificate_detail`、`sourceModule=brand_entry` 和 `certificateId` 等可用上下文。

理由：产品使用行为日志规范已支持 `brand_card_click`，统一事件名可减少字典漂移和分析口径分叉。

替代方案：新增 `certificate_detail_brand_click`。该方案表达精确，但会引入同一组件多事件名，后续分析需要合并，因此不采用。

### D4 原型冲突处理

事实源优先级：

```text
REQ-0121 prototype/miniapp/prototype-context.md
> REQ-0121 acceptance.md
> REQ-0054 brand-card 原型上下文
> REQ-0080 certificate-detail 原型上下文
> rules/ui-design.md
> openspec/specs
```

本 Change 是局部组件复用，不需要新建完整 HTML 原型。若既有证书详情页页面结构与本 context 冲突，保留证书详情页整体结构，只替换 `BrandEntry` 区域为 `brand-card`；不得顺手重构顶部媒体区、底部操作栏或证书字段。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | 以 REQ-0121 `prototype/miniapp/prototype-context.md` 与 `acceptance.md` 为局部品牌入口事实源；既有证书详情页原型只作为页面位置参照。 |
| 页面与入口 | 小程序证书详情页 `CertificateDetailPage` 的 `BrandEntry` 区域。 |
| 信息架构 | `BrandEntry -> brand-card -> brand-logo / brand-name / brand-hint / entry affordance`。 |
| 视觉 token | 继续沿用 `brand-card` 深色卡片、品牌金强调、固定 Logo 容器和近直角视觉，不新增私有视觉语言。 |
| 交互状态 | 覆盖 normal、thumbnail-missing、image-failed、long-name、unavailable；点击热区不小于 44px。 |
| 图标与文案 | 使用 `brand-card` 既有入口提示和箭头语义，不新增证书详情页私有箭头或提示文案。 |
| Mock/API 边界 | 本 Change 应接入真实证书详情数据；如局部开发需 Mock，必须标注 Mock 不代表 API 已补齐。 |
| 权限规则 | 仅展示公开证书所属的公开品牌；品牌不可公开或入口不可用时不产生无效跳转。 |
| 一致性参照 | 回归商品详情页与证书详情页的 `brand-card` 展示、跳转、不可用态和埋点。 |

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 证书详情接口无品牌缩略图字段，导致小程序继续使用原图。 | 实现阶段先定位证书详情 DTO / Schema，补齐 `brand_logo_thumbnail_url` 并加后端测试。 |
| 修改 `brand-card` 入参影响 SKU 详情页等既有调用方。 | 保持新增字段可选，新增回归测试覆盖既有调用方。 |
| 埋点字典缺少证书详情上下文参数。 | 使用已登记 `brand_card_click`，仅传入允许字段，缺失上下文为空，不阻断跳转。 |
| 小程序 `.ts` 与 `.js` 运行入口不同步。 | 任务要求同步源与运行入口，并通过静态测试或项目认可同步方式验证。 |
| 媒体验收只看字段存在，未证明端上实际消费缩略图。 | 按小程序媒体四联记录 key/object/URL/render 与 Network evidence。 |

## 验证策略

- 后端：证书详情响应字段测试，确认 `brand.brand_logo_thumbnail_url` 存在且不暴露对象存储原始 Key。
- 小程序：静态测试或等价检查，确认证书详情页使用 `brand-card`，不保留页面私有品牌入口结构。
- 埋点：静态测试或单元测试确认点击事件名为 `brand_card_click`，参数含品牌与证书上下文。
- 媒体：小程序 Network/render evidence 证明品牌 Logo 普通展示使用缩略图或安全占位。
- 回归：商品详情页等既有 `brand-card` 调用方展示和点击不回退。

