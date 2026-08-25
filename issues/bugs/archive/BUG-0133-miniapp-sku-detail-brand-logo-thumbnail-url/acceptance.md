---
bug_id: BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
acceptance_status: passed
created_at: 2026-08-22 21:05:41
updated_at: 2026-08-25 14:51:36
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | 商品详情接口响应中 `brand.brand_logo_thumbnail_url` 可用，且与 `brand_logo_url` 原图字段区分 | passed |
| AC-002 | 小程序商品详情页品牌卡优先使用 `brand_logo_thumbnail_url` 展示品牌 Logo | passed |
| AC-003 | 缩略图缺失时品牌卡不直接加载过大的 Logo 原图，采用占位或受控降级策略 | passed |
| AC-004 | 微信小程序 DevTools Network 证据覆盖品牌 Logo URL、Size、Time 与缓存状态 | passed |
| AC-005 | 品牌列表、品牌详情、商品详情三个入口的品牌 Logo 缩略图消费策略保持一致 | passed |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url |
| 标题 | 小程序商品详情页品牌卡缺少 brand_logo_thumbnail_url 导致加载原图 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 媒体 URL |
| 复现入口 | 微信小程序商品详情页品牌卡 |
| 受影响端 | miniapp / backend / storage |
| 环境 | miniapp-devtools / local |
| 媒体类型 | logo / thumbnail / image |
| 业务资源 | 脱敏品牌 Logo 资源 |
| 修复前实际结果 | 商品详情页品牌卡缺少 `brand_logo_thumbnail_url`，存在直接请求 `brand_logo_url` 原图的风险 |
| 修复后期望结果 | 商品详情接口返回品牌 Logo 缩略图 URL，品牌卡普通展示优先请求缩略图；缺缩略图时不直接拉大体积原图 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | passed | 代码路径 `same_directory_thumbnail_object_key(record.brand_logo_object_key)` 从品牌 Logo 原图 key 派生同目录 `.thumb` key；测试样本原图 URL `/media/logos/fst.webp` 对应缩略图 URL `/media/logos/fst.thumb.webp` | 若历史对象实际缺失，需补充对象存储回填或保留占位策略 |
| object | passed | 用户提供 DevTools Headers 证据：`content-type=image/png`、`content-length=85880`，Network 列表 Size `86.2 kB`；请求为品牌 Logo `.thumb.png` 缩略图资源 | 若其他历史对象实际缺失，需补充对象存储回填或保留占位策略 |
| URL | passed | `uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share` 断言 `/api/v1/miniapp/skus/1` 返回 `brand.brand_logo_thumbnail_url=/media/logos/fst.thumb.webp` 且 `brand_logo_url=/media/logos/fst.webp` | 若环境中 `/media/logos/fst.thumb.webp` 404/403，需修复媒体代理或历史缩略图对象 |
| render | passed | 用户提供 DevTools Network 证据显示品牌卡实际请求 `http://127.0.0.1:8000/media/images/default/brands/logos/93cee425-393f-4937-9510-f0a0231a4ea4.thumb.png`，状态 `200 OK`，`x-media-fallback: 0`，列表中对应 PNG 行 Size `86.2 kB`、Time `134 ms`，Timing 总耗时 `135.74 ms` | 若其他商品样本未命中缩略图，需回到媒体对象补齐或保持占位策略 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦商品详情页品牌 Logo 展示消费，不直接修改上传入口 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | passed | DevTools Headers 证据显示请求经本地后端 `127.0.0.1:8000/media/...thumb.png` 受控读取，`server: uvicorn`，`x-media-fallback: 0`，未直连对象存储 endpoint |
| 历史对象与审计 | n/a | 本次不新增历史对象回填脚本；缩略图缺失时 SKU 详情品牌卡关闭原图兜底并展示占位，历史回填可作为独立治理项评估 |
| 小程序 evidence | passed | 用户提供 3 张 DevTools Network 截图，覆盖 Headers、Timing 和 Network 列表：状态 200、Size 86.2 kB、Time 134 ms、总耗时 135.74 ms、缓存头 `cache-control: public, max-age=604800, stale-while-revalidate=86400` |

## 验收数据建议

- 至少选择 1 个品牌 Logo 原图体积较大的商品详情页样本。
- 记录修复前后 `brand.brand_logo_url` 与 `brand.brand_logo_thumbnail_url` 的接口字段差异。
- 记录品牌 Logo 请求 URL、Size、Time、Waterfall 和缓存状态。
- 记录缩略图 object 的 MIME、大小、扩展名和权限结论。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 21:44:56
accepted_by: user
source_change: fix-miniapp-sku-detail-brand-logo-thumbnail-url
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

