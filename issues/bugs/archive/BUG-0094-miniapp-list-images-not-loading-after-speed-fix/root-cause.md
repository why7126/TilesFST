---
bug_id: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
status: done
created_at: 2026-07-31 12:51:42
updated_at: 2026-07-31 21:32:14
---

# 直接原因

商品列表图片加载优化后，生产环境首页和商品列表接口返回的 `cover_image` 已确认均为 `/media/thumbnails/...` 缩略图地址。用户在真机上进一步确认，异常图片请求集中在 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。

因此当前直接原因应收敛为：公开商品列表中的部分主图仍引用 `tiles/pending` 上传路径，`BUG-0092` 的缩略图优先策略又将其转换为 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。该缩略图路径在真机请求中异常，最终触发商品卡片“暂无图片”兜底。

# 根本原因

`BUG-0092` 的性能修复把“列表使用轻量图片资源”作为目标，但没有对 `tiles/pending` 这类未绑定 tile_id 的商品图片 key 建立明确的公开列表契约：

- 列表接口统一返回 `/media/thumbnails/...`，这是生产环境已确认事实。
- 真机异常请求证明图片请求已经发出，且异常路径均落在 `/media/thumbnails/default/tiles/pending/`。
- 商品图片上传接口在未传 `tile_id` 时会生成 `images/default/tiles/pending/<uuid>.<ext>`；列表缩略图转换会进一步生成 `thumbnails/default/tiles/pending/<uuid>.<ext>`。
- 公开 SKU 主图如果长期保留 pending key，列表缩略图策略必须保证 pending key 有可访问缩略图，或在列表接口回退到可展示原图 URL。
- 商品卡片失败兜底把“请求失败”和“确实无主图”都展示为“暂无图片”，缺少可见的错误区分和可排障信号。

# 触发条件

1. 小程序访问首页、商品列表、搜索结果、品牌详情商品区等复用商品卡片的页面。
2. 后端列表接口返回的 `cover_image` 为 `/media/thumbnails/...`。
3. 公开 SKU 主图 object key 仍处于 `images/default/tiles/pending/<uuid>.jpg` 形态，或列表接口未对 pending key 做保护。
4. 后端缩略图转换生成 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
5. 真机请求该缩略图 URL 异常后，小程序商品卡片进入“暂无图片”兜底状态。

# 分类

- 类型：regression / media-url-contract / data-consistency
- 层级：后端公开列表图片 URL 策略、商品主图 object key 生命周期、缩略图路径生成、小程序商品卡片兜底
- 直接影响端：微信小程序
- 关联后端：`/api/v1/miniapp/home`、`/api/v1/miniapp/products`、`/media/{object_key}`
- 数据风险：中，公开 SKU 主图可能仍引用 `tiles/pending` 上传路径
- 回归风险：高，来源于 `BUG-0092` 的图片加载性能修复

# 已确认结论

- 已确认：生产环境 `/api/v1/miniapp/home` 与 `/api/v1/miniapp/products` 返回的 `cover_image` 均为 `/media/thumbnails/...`。
- 已确认：真机异常请求路径为 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- 已确认：商品图片上传在未传 `tile_id` 时会生成 `images/default/tiles/pending/<uuid>.<ext>`。
- 已确认：生产数据库公开 SKU 主图 `tile_images.object_key` 仍存在 `images/default/tiles/pending/<uuid>.jpg`。
- 已确认：对应 pending 原图对象存在，但 thumbnail 对象不存在。
- 已确认：修复策略为补齐缩略图；缩略图存储路径应与原图路径保持一致，仅通过文件名差异区分缩略图；同时必须补全历史缩略图。

## 修复策略边界

| 事项 | 结论 | 说明 |
|---|---|---|
| 生产 DB pending 主图 | 存在 | 公开 SKU 主图仍有 `images/default/tiles/pending/<uuid>.jpg`。 |
| 对象存储状态 | 原图存在，thumbnail 不存在 | 当前无图由缩略图对象缺失触发，不是原图缺失。 |
| 缩略图存储约定 | 与原图同目录，仅文件名不同 | 不采用独立 `thumbnails/` 前缀作为最终策略。 |
| 历史数据 | 必须回填历史缩略图 | 需要覆盖既有公开 SKU 主图，避免只修新增上传。 |

AI 可辅助项：

- 后续在 OpenSpec Change 中设计缩略图文件命名规则、生成/回填脚本、列表 URL 生成逻辑和测试用例。
- 在本地或测试环境复现 pending 原图存在但 thumbnail 缺失时的列表无图问题。
- 设计审计脚本，输出历史主图缩略图缺失清单和回填结果。
