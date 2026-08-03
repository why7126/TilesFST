---
bug_id: BUG-0110-miniapp-card-banner-thumbnail-usage
acceptance_status: passed
created_at: 2026-08-03 08:22:59
updated_at: 2026-08-03 20:52:16
related_requirement: null
related_bug: BUG-0100-thumbnail-size-equals-original
source_change: fix-miniapp-card-banner-thumbnail-usage
source_sprint: sprint-018
---

# 验收标准

## 回归用例

### AC-001 商品卡片优先使用缩略图

- 前置条件：商品数据存在主图缩略图 URL。
- 操作：打开小程序商品列表、搜索结果页、分类商品列表等商品卡片场景。
- 期望：商品卡片图片请求或渲染字段优先使用缩略图 URL。

### AC-002 品牌卡片优先使用缩略图

- 前置条件：品牌数据存在 Logo 或主图缩略图 URL。
- 操作：打开小程序品牌列表页或其他品牌卡片展示场景。
- 期望：品牌卡片图片请求或渲染字段优先使用缩略图 URL。

### AC-003 证书卡片优先使用缩略图

- 前置条件：证书数据存在图片缩略图 URL。
- 操作：打开小程序证书列表页或其他证书卡片展示场景。
- 期望：证书卡片图片请求或渲染字段优先使用缩略图 URL。

### AC-004 Banner 使用符合性能策略的展示图

- 前置条件：首页或相关页面存在 Banner 图片数据。
- 操作：打开包含 Banner 的小程序页面。
- 期望：Banner 优先使用缩略图或符合性能策略的展示图；若产品定义 Banner 必须使用特定尺寸图，应明确字段和降级策略。

### AC-005 缩略图缺失时按降级策略展示

- 前置条件：构造缩略图 URL 缺失、为空或加载失败的数据。
- 操作：打开商品卡片、品牌卡片、证书卡片和 Banner 场景。
- 期望：页面按明确顺序降级到原图或占位图，不出现空白、报错或页面阻塞。

### AC-006 不影响详情与预览体验

- 前置条件：卡片图片可点击进入详情或触发图片预览。
- 操作：点击商品、品牌、证书或 Banner 关联入口。
- 期望：跳转、详情页展示和图片预览策略不受缩略图字段修复影响；需要原图的场景仍可使用原图。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-miniapp-card-banner-thumbnail-usage
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

