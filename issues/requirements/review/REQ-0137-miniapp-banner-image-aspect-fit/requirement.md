---
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
title: 小程序 Banner 图片统一完整适配展示
terminal: miniapp
version: v1
status: in_sprint
owner: product
source: capture.md
related_change: fix-miniapp-banner-image-aspect-fit
priority: P1
parent_requirement: null
created_at: '2026-09-07 22:53:01'
updated_at: 2026-09-08 18:38:04
---

# 小程序 Banner 图片统一完整适配展示

## 1. 背景与目标

小程序 Banner 和详情大图承载品牌视觉、宣传文字与瓷砖主体。现有填充裁切方式在素材与容器比例不一致时可能裁掉边缘内容，影响用户查看完整信息。

本需求统一四类大图位的展示规则：图片等比完整显示，允许留白，保持容器和页面布局稳定。“100% 显示”指完整展示当前加载图片的画面范围，不代表按原始像素大小显示，也不要求下载原图或恢复图片源中已经裁掉的内容。

现状依据为四个页面 `index.wxml` 的只读检查：首页、品牌列表和品牌详情的展示图及缩略图回退分支使用 `aspectFill`；商品详情顶部媒体图片也使用 `aspectFill`。这些是代码证据，不代表已完成 DevTools、真机或线上验证。

## 2. 目标用户

- 店主及协助选型人员：通过大图向客户展示瓷砖主体和品牌资料。
- 选购客户：浏览品牌与商品，完整识别图片中的文字、纹理和边缘信息。

## 3. 范围

### 3.1 包含范围

| 页面 | 目标图片位 | 定位入口 |
|---|---|---|
| 首页 | Banner 轮播的展示图及缩略图回退 | `src/miniapp/pages/index/index.wxml` |
| 品牌列表 | Banner 轮播的展示图及缩略图回退 | `src/miniapp/pages/brand-list/index.wxml` |
| 品牌详情 | 品牌头图及缩略图回退 | `src/miniapp/pages/brand-detail/index.wxml` |
| 商品详情 | 顶部媒体轮播中的图片项及其图片回退 | `src/miniapp/pages/tile-detail/index.wxml` |

### 3.2 不包含范围

- 视频本体、视频封面、播放比例和全屏播放策略。
- 商品推荐图、商品卡片缩略图、证书图、品牌圆形 Logo 等非 Banner 图片。
- 图片预览能力重设计、页面信息架构调整、统一四类容器为同一高度。
- API 字段、数据库、媒体对象 key、图片派生生成、URL 选择和对象存储策略变更。
- Web 店主端、企业管理端、上传配置或素材管理能力变更。

## 4. 功能要求

### FR-001 四类图片统一等比完整适配

目标图片在既有容器内等比缩放并居中，完整露出图片画面，允许上下或左右留白；不得拉伸、裁切或通过放大、位移重新隐藏边缘。实现采用 `aspectFit` 或能证明等效完整适配的方式，展示图和缩略图回退分支执行同一规则。

### FR-002 容器高度与加载过程稳定

保留各页面现有容器尺寸契约，不随每张图片的宽高动态改变轮播或头图高度。加载前后、切换不同比例图片和加载失败时，周围内容不应新增跳动、横向溢出或重叠。图片为空或失败时沿用既有占位和回退行为。

### FR-003 留白与品牌文字可读

留白沿用页面或容器的背景语义，与现有暗色设计协调。品牌详情保留品牌名称、英文名称和描述信息，在原头图总高内划分独立图片区与文字区，避免两者互相遮挡；图片区等比完整适配，文字区沿用既有截断规则。局部尺寸方案见 business-flow.md，不以裁切图片解决可读性问题。

### FR-004 保持既有交互与媒体边界

Banner 跳转、轮播切换和指示状态、图片预览、懒加载和错误回退继续按既有契约工作。商品详情图片与视频共用轮播区域时，图片适配变更不得影响视频尺寸、封面和播放操作。不得对页面全部 image 节点或共享媒体样式进行无差别修改。

### FR-005 保持图片消费策略

继续消费各图片位现有展示图、缩略图和占位来源，不因完整显示要求回退下载原图，不新增请求字段或图片变体。完整适配只约束端侧渲染；素材源本身的裁切或清晰度问题不在本需求中修复。

## 5. UI 与技术约束

- 遵循 `rules/ui-design.md`，复用现有页面样式和设计系统语义；新增或调整背景不得散落裸 Hex，不扩大为全站主题整改。
- 不同图片比例使用同一完整适配规则；宽图、方图、竖图及带边缘文字的图片均纳入视觉核对。
- 局部原型见 `prototype/web/banner-fit.html`，适用边界见同目录 `context.md`；后续实现需遵守 UI Contract、Skeleton、视觉和样式证据要求。
- 若实现涉及小程序逻辑，保持 TypeScript 与实际运行 JavaScript 同步；具体文件和测试在 Change 中确定。

## 6. 后续验证要求

- 静态检查覆盖四类图片位及展示图、缩略图回退分支，证明目标图片完整适配且视频、Logo、证书和商品卡片未被误改。
- 在 320、375、430 pt 等价逻辑宽度下，使用宽图、方图、竖图和带边缘文字的素材核对完整性、留白、文字可读性和溢出情况。
- 覆盖加载中、加载失败、空数据、轮播切换、图片与视频混排，并回归 Banner 点击与图片预览。
- 后续补充小程序聚焦静态测试及 DevTools 或真机视觉证据；记录证据来源、页面、宽度、素材比例和执行时间。静态测试通过不等同视觉验收，DevTools 证据不等同真机或线上通过。

## 7. 关联需求

| 对象 | 关系 |
|---|---|
| `REQ-0106-admin-banner-title-hidden` | 保持有图 Banner 不展示标题遮罩，品牌详情信息区不属于恢复 Banner 标题 |
| `REQ-0118-unified-web-miniapp-image-variant-consumption-matrix` | 延续既有图片变体消费矩阵，仅调整渲染适配，不改变 URL 或变体选择 |
| `BUG-0148-miniapp-product-list-card-image-fit` | 相邻展示问题；其 Change 明确排除 Banner、品牌图和商品详情轮播，本需求独立闭环 |

BUG 边界依据见 `openspec/changes/fix-miniapp-product-grid-image-fit/proposal.md` 的不变范围。关联对象不构成本需求已评审或已纳入 Sprint 的依据。

## 8. 评审方案

本需求按 capture 中的明确范围收敛“所有 Banner”为上述四类大图位；保留品牌文字信息，以完整图片和文字同时可读为约束；视频继续排除且不自动创建后续需求。本次通过方案文档评审，不代表已完成视觉验收。需求完善采用原头图 380rpx 总高内划分 220rpx 图片区和 160rpx 文字区的局部方案，保留品牌字段与既有截断规则，按本次评审方案进入后续设计与验收。

## 9. 状态块

```yaml
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
status: approved
terminal: miniapp
version: v1
priority: P1
parent_requirement: null
iteration: null
openspec_changes:
  - fix-miniapp-banner-image-aspect-fit
  - change_id: fix-miniapp-banner-image-aspect-fit
    type: update
    status: proposed
product_data_collection_observability:
  applicability: not_applicable
  affected_layers:
    - wechat_miniapp
  reason: 仅调整小程序四类大图位的图片显示模式、留白和容器适配，不改变 API、数据库、请求日志、行为事件、Task Trace 或 Web/小程序/App 请求封装；图片 URL、变体选择和既有错误回退链路保持原契约。
  validation: PRD 阶段已只读核对 capture、四页面 WXML 和相邻 BUG 的范围；未实现代码、未执行静态测试或视觉验收。实现阶段需复核差异范围并完成聚焦测试和渲染证据，若涉及采集或请求链路则重新声明适用性。
api_change: false
db_change: false
web_change: false
admin_change: false
miniapp_change: true
orval_required: false
docker_compose_validation_required: false
```
