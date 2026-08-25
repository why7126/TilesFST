---
requirement_id: REQ-0121-miniapp-certificate-detail-brand-card-entry
title: 小程序证书详情页品牌入口复用 brand-card 验收标准
acceptance_status: passed
owner: product
source: requirement.md
created_at: 2026-08-24 15:26:47
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 功能 AC

- [ ] AC-001 证书详情页所属品牌入口复用小程序 `brand-card` 组件，不保留页面私有品牌入口 DOM/模板结构。
- [ ] AC-002 证书详情 `brand` 数据包含 `brand_logo_thumbnail_url`，且字段语义为品牌 Logo 缩略图 URL。
- [ ] AC-003 `brand-card` 在证书详情页优先消费 `brand_logo_thumbnail_url` 展示品牌 Logo。
- [ ] AC-004 品牌 Logo 缩略图缺失、为空或加载失败时，组件使用统一兜底，不展示破图，不造成品牌卡片高度跳动。
- [ ] AC-005 证书详情页品牌入口点击后跳转到对应品牌详情页或既定品牌入口，跳转参数包含稳定品牌标识。
- [ ] AC-006 品牌数据缺失、品牌不可公开或入口参数不可用时，阻止无效跳转，并按 `brand-card` 统一不可用态处理。
- [ ] AC-007 所有 `brand-card` 点击事件名统一为 `brand_card_click`，证书详情页不使用页面私有点击事件名。
- [ ] AC-008 `brand_card_click` 埋点参数包含可用的 `brandId`、`brandName`、`sourcePage`、`sourceModule`、`certificateId` 和 `requestId`。
- [ ] AC-009 埋点上报失败不阻断品牌入口跳转。
- [ ] AC-010 回归商品详情页、证书详情页和其他当前使用 `brand-card` 的页面，确认展示、跳转、不可用态和事件名一致。

## UI AC

- [ ] AC-UI-001 证书详情页品牌入口视觉与既有 `brand-card` 保持一致，不新增冲突的私有卡片样式、箭头、Logo 占位或点击反馈。
- [ ] AC-UI-002 在 320 / 375 / 430px 逻辑宽度下，品牌 Logo、品牌名称、入口提示和箭头不重叠、不横向溢出。
- [ ] AC-UI-003 品牌 Logo 容器尺寸稳定，图片加载前后不导致证书详情页品牌区域明显 layout shift。
- [ ] AC-UI-004 品牌入口有效点击区域不小于 44px 高度，满足小程序触控体验。

## 数据与媒体 AC

- [ ] AC-DATA-001 证书详情响应不得暴露对象存储原始 Key、本机路径、后台备注、内部审计字段或真实存储凭据。
- [ ] AC-DATA-002 品牌 Logo 小卡片场景不得 fallback 到原图 URL；目标缩略图缺失时使用安全占位或明确的不可用状态。
- [ ] AC-DATA-003 小程序 Network evidence 显示证书详情品牌 Logo 请求使用受控媒体 URL 或安全静态资源，资源大小符合缩略图预期。
- [ ] AC-DATA-004 小程序 render evidence 显示证书详情页品牌入口实际可见、可点击或按不可用态稳定展示。

## 小程序媒体四联验收

来源：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

| 维度 | 验收目标 | 最小证据 |
|---|---|---|
| key | 品牌 Logo 缩略图来源稳定，不暴露原始对象 Key。 | 脱敏 key hash 或字段来源摘要；若无 key 则说明 N/A。 |
| object | 缩略图对象可读且体积收益成立。 | MIME、size 摘要、缩略图/原图体积对比或生成状态。 |
| URL | 小程序使用后端受控 URL 或安全静态资源。 | URL 类型、HTTP 状态、资源大小、耗时。 |
| render | `brand-card` 在证书详情页稳定展示并可交互。 | DevTools/真机/体验版截图、录屏或人工摘要。 |

Network evidence 必须脱敏，不得记录 Authorization header、Cookie、真实 `.env`、本机绝对路径或未脱敏 object key。

## Knowledge-base 横切检查

| 标签 | 引用文档 | 将写入 AC-XCUT 条数 | 说明 |
|---|---|---:|---|
| 无匹配标签 | - | 0 | 本 REQ 为小程序展示和组件复用场景，不属于 `admin-list`、`admin-form`、`admin-modal` 或上传链路 `media-upload`。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-24 17:08:39
accepted_by: workflow-sync
source_change: update-miniapp-certificate-detail-brand-card-entry
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

