## 设计目标

本 Change 只调整管理端图片密集列表的资源选择与响应契约，不改变媒体上传、缩略图生成、数据库结构或公开端展示逻辑。实现应复用已有同目录缩略图派生能力与后端受控 `/media/{object_key}` 读取链路。

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - tile-sku-management
    - banner-management
```

## D1 UI 策略

选择 **Design System / 既有页面适配策略**，不做 CSS Port，也不引入新视觉资产。

理由：

- REQ-0098 的 prototype/web 仅表达资源选择策略，不是完整 Golden 页面。
- SKU、品牌、证书、Banner 列表已有页面结构和样式，本 Change 不应重做列表视觉。
- 需求重点是 image adapter 字段优先级、fallback 和行高稳定性，应通过局部 helper 或页面内展示模型收敛。

## D2 后端响应字段

SKU 列表：

- 在管理端 SKU 列表项 Schema 增加 `main_image_thumbnail_url: str | None`。
- 当 `main_image_url` 或主图 object key 可解析时，后端派生同目录缩略图 URL。
- 当无主图、object key 无法安全解析或缩略图策略不适用时，字段返回 `null`，保留 `main_image_url`。

Banner 列表：

- 在管理端 Banner 列表项 Schema 增加 `image_thumbnail_url: str | None`。
- 该字段必须基于最终 `image_object_key` 派生，不能改用跳转目标的其它图片。
- 字段新增保持向后兼容，不改变 `image_url`、`image_object_key`、`image_source` 语义。

## D3 前端展示策略

前端列表图片使用以下优先级：

```text
thumbnail URL -> original URL -> existing fallback
```

SKU 列表优先 `main_image_thumbnail_url`，回退 `main_image_url`。Banner 列表优先 `image_thumbnail_url`，回退 `image_url`。品牌和证书列表复核已有 `logo_thumbnail_url`、`thumbnail_url` 优先策略，不重复引入新字段。

图片加载失败时应避免浏览器默认破图，可通过已有 fallback class、onError 状态或业务 helper 展示原图 / 占位。不得因为图片资源切换改变表格行高、sticky action column、分页或筛选布局。

## D4 API / Orval 同步

新增响应字段属于管理端 API 契约变化，必须：

- 更新 Pydantic Schema。
- 重新导出 OpenAPI。
- 运行 Orval 生成前端客户端与类型。
- 避免手写与后端重复的接口类型。
- 用 diff/stat 复核生成物，不在评审输出中展开 generated 全文。

## D5 原型冲突处理

优先级按 `HTML > context.md > acceptance.md > rules/ui-design.md > openspec/specs`。

冲突结论：

- `prototype/web/admin-media-list-thumbnails.html` 只表达缩略图优先和原图 fallback 的信息架构，不要求复制其 CSS 或 DOM。
- `prototype/web/context.md` 明确“不作为最终视觉稿”，要求沿用现有列表布局。
- acceptance 与 prototype 一致：列表优先缩略图，详情 / 编辑 / 预览使用原图。
- 现有 `banner-management` 已要求 Banner 列表缩略图完整预览，本 Change 补充响应字段和资源优先级，不改变完整预览要求。

## D6 知识库横切要求

后续 `/opsx-apply` 必须引用并落实：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-019-retrospective.md`

验收必须覆盖：

- 管理端列表分页、筛选、toast、confirm 和操作列布局不回归。
- 媒体类 URL/render 证据能证明列表使用缩略图，详情或预览仍可访问原图。
- 不新增 `window.confirm`。

## D7 风险与边界

- 缩略图对象缺失不应阻塞列表接口；字段可为空，由前端 fallback。
- 本 Change 不强制执行历史媒体批量补齐；若发现存量缩略图缺失严重，可后续单独创建媒体维护需求。
- 不新增数据库字段，避免把可派生 URL 固化到业务表。
