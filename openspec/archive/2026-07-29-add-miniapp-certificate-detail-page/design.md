## Context

REQ-0080 已在 `issues/requirements/archive/REQ-0080-miniapp-certificate-detail-page/` 完成评审并通过。当前小程序已具备证书列表页 `pages/certificates/index`，公开列表 API 为 `GET /api/v1/miniapp/certificates`，列表卡片当前直接进行图片预览或 PDF 打开。管理端品牌证书能力已经提供证书主数据、多图上传、主图设置、旧单文件兼容和公开展示控制。

本变更要把证书列表从“聚合列表 + 文件预览”扩展为“列表进入详情页 + 详情页内浏览/预览/分享”。它同时影响后端公开证书查询契约、小程序路由与页面、对象存储 URL 安全、小程序自定义导航 evidence 和测试，因此需要 design.md 固化跨模块决策。

## Goals / Non-Goals

**Goals:**

- 新增小程序证书详情页，支持证书列表、品牌详情证书区域和微信分享进入。
- 提供或扩展公开证书详情接口，返回证书公开字段、图片组/主图、旧单文件兼容、品牌入口和分享信息。
- 将证书列表卡片主点击调整为进入详情页；详情页内再执行图片预览或 PDF 受控打开。
- 复用商品详情页的大媒体区、品牌入口、分享、骨架屏和错误态设计语义，但保留证书字段语义。
- 严格过滤隐藏、软删除和不可公开品牌证书，不暴露内部字段、对象 Key 或未授权 URL。
- 按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 验收详情页分享直达、返回兜底、胶囊 reserve 和页面 offset。

**Non-Goals:**

- 不新增管理端证书维护能力，不调整证书上传、编辑、显示/隐藏、删除或主图设置交互。
- 不实现证书真伪校验、OCR、电子签章、防伪查询或证书审批。
- 不引入收藏、推荐、购物车、购买、支付、库存、优惠券、询价或价格展示。
- 不强制建立证书与 SKU 的绑定关系；若商品详情页后续需要展示证书入口，另行建 REQ/Change。

## Decisions

### D1. 使用既有 `miniapp-certificate-list-page` capability 承载详情页扩展

证书详情页是证书列表页的下钻能力，依赖同一公开证书数据域和展示控制规则，因此不新增独立 capability。Delta spec 在 `miniapp-certificate-list-page` 下新增详情页、详情 API、分享、导航和埋点要求，并修改证书文件预览要求。

备选方案是新增 `miniapp-certificate-detail-page` capability。该方案会让列表点击、公开过滤、文件预览和详情接口拆散到两个 capability，增加归档后读者追踪成本，因此本次不采用。

### D2. 新增详情接口优先于复用列表接口拼装详情

详情页建议使用 `GET /api/v1/miniapp/certificates/{certificateId}` 或等价详情接口一次返回首屏所需字段。列表接口保持分页摘要用途，避免小程序端用列表项字段拼装详情后遗漏多图、主图、说明、分享和旧单文件兼容。

如果实现阶段确认现有列表接口已返回足够字段，也必须在 Change apply 中证明其满足详情页 AC；否则新增详情接口并同步 OpenAPI、Orval 或小程序服务层、API 文档和后端集成测试。

### D3. 列表主点击进入详情页，预览动作下沉到详情页

当前 `pages/certificates/index` 的卡片点击直接预览文件。REQ-0080 要求用户能看到单证书完整信息和分享路径，因此主点击必须改为进入详情页；详情页提供“预览文件/打开文件”操作。这样保留文件预览能力，同时给证书信息、品牌入口和分享留出稳定承载页。

### D4. 详情页 UI 复用商品详情页结构，不复用商品业务能力

证书详情页使用商品详情页的大媒体区、信息分区、品牌入口、分享和错误态作为体验参考；但明确不显示收藏、推荐、价格、SKU 编码、购物和询价。设计优先级为：

```text
prototype/miniapp/certificate-detail.html
> prototype/miniapp/prototype-context.md
> acceptance.md
> docs/knowledge-base/best-practices/miniapp-custom-navigation.md
> rules/ui-design.md
> openspec/specs
```

### D5. 公开过滤和 URL 安全由后端兜底

小程序端只做展示和降级，不能作为唯一安全边界。详情接口必须过滤隐藏、软删除、所属品牌不可公开的证书，并只返回后端控制的可读 URL 或签名 URL。响应不得包含后台备注、审计字段、内部用户字段、对象存储原始 Key、本机路径、Authorization header、Cookie、密钥或 `.env` 内容。

## Conflict Resolution

- HTML 原型与 acceptance 均要求顶部大媒体区。若最终小程序实现因机型或自定义导航高度调整尺寸，仍必须保持“首屏主视觉优先，不用小卡片包裹媒体”的体验，而不是照抄 HTML 像素。
- 证书列表旧 spec 允许“点击图片证书缩略图、卡片主区域或查看入口”直接预览。本 Change 修改为列表主区域进入详情页；文件预览入口迁移到详情页内。
- 商品详情页 spec 中收藏、推荐、价格、SKU 字段不适用于证书详情页；本 Change 明确不引入这些业务能力。
- PNG Golden Reference 尚未导出，不阻塞 Change 创建；实现验收以 HTML、context、acceptance 和 DevTools evidence 为准。

## Risks / Trade-offs

- [详情接口字段不足] → 在 tasks 中要求先梳理现有证书列表响应与管理端证书数据字段，若不足则新增详情接口和 Schema。
- [列表点击行为改变影响用户快速预览] → 详情页首屏提供明确预览/打开文件操作，并保留图片原生预览和 PDF 受控打开。
- [多图与旧单文件兼容复杂] → 后端详情响应同时提供 `images` 与 `file` 兼容结构，前端按主图、多图、PDF、未知类型分别降级。
- [分享直达无页面栈导致返回失效] → 按 miniapp-custom-navigation best-practice 实现返回兜底并留存 evidence。
- [真机验收资源不可用] → acceptance 允许标记 blocked 或 follow_up，但不得写作真机通过。

## Migration Plan

1. 新增或扩展后端公开证书详情服务和路由，保持旧证书列表 API 兼容。
2. 新增小程序 `pages/certificate-detail/index` 并注册路由。
3. 修改证书列表页卡片主点击为 `wx.navigateTo` 到详情页；详情页内提供图片预览/PDF 打开。
4. 增加品牌详情证书区域进入详情页的路径（若当前品牌详情证书区域存在）。
5. 增加分享路径与 `onShareAppMessage`。
6. 补充测试、OpenAPI/Orval 或小程序服务层契约、文档和 evidence。

Rollback：保留证书列表接口与列表页本身兼容；若详情页上线异常，可临时恢复列表卡片直接预览行为并隐藏详情页入口，但不得绕过后端公开过滤。

## Open Questions

- 详情接口是否新增独立路径，还是复用已有证书列表服务内部 repository 查询能力暴露详情路由。
- 品牌详情页证书区域当前是否已渲染证书卡片；若未实现，本 Change 是否只预留详情路由能力。
- PDF 打开失败时采用复制受控 URL、`wx.openDocument` 失败提示，还是两者组合。
