## Why

BUG-0094 指出微信小程序首页、商品列表、搜索结果和品牌详情商品列表中的商品卡片图片在加载优化后大面积显示“暂无图片”。真机网络证据显示失败请求集中在 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`；生产已确认公开 SKU 主图仍存在 `images/default/tiles/pending/<uuid>.jpg`，原图对象存在但对应缩略图对象不存在。

该问题来自 `BUG-0092` 缩略图优先策略与历史 pending 主图数据之间的契约缺口。列表接口不能返回不可访问的缩略图 URL；缩略图生成、同路径命名、历史回填和审计需要成为明确规格。

## What Changes

- 为商品主图缩略图定义同目录、文件名差异化的对象 key 规则，不再把 `thumbnails/default/tiles/pending/<uuid>.<ext>` 作为最终缩略图策略。
- 新增或调整 SKU 图片上传/保存链路，确保新主图在原图对象存在后生成对应列表缩略图。
- 提供历史缩略图回填能力，覆盖既有公开 SKU 主图，尤其是 `images/default/tiles/pending/<uuid>.<ext>`。
- 调整小程序首页和商品列表接口的 `cover_image` 生成策略，优先返回可访问的同路径缩略图，缺失时安全回退到原主图或占位。
- 补充商品卡片图片审计输出，定位公开 SKU、pending 主图、原图缺失和缩略图缺失。
- 补充后端与小程序回归测试，保留懒加载和列表图片性能优化。

## Capabilities

### New Capabilities

- 无新增业务能力。

### Modified Capabilities

- `object-storage`: 列表缩略图对象 key 规则调整为与原图同目录、文件名差异区分，并要求生成、回填和缺失回退。
- `tile-sku-management`: SKU 图片上传和主图关联链路必须保证主图缩略图可生成和可回填。
- `miniapp-product-list-page`: 商品列表、搜索结果和品牌商品列表的商品卡片 `cover_image` 必须返回可访问图片 URL。
- `miniapp-home`: 首页新品、热销和全部产品商品卡片必须复用同一可访问缩略图策略。

## Impact

- 影响范围：微信小程序商品卡片图片展示、后端公开列表 `cover_image` 生成、SKU 主图缩略图生成/回填、对象存储图片 key 约定。
- API：响应字段结构不变，`cover_image` URL 语义变为“可访问的列表图优先”。若 OpenAPI 描述包含 URL 语义，需要同步文档。
- 数据库：不新增表结构；可能需要只读扫描并基于对象存储补齐历史缩略图对象。
- Web 管理端：上传/保存 SKU 图片链路可能受影响，但页面交互不应改变。
- 小程序：商品卡片图片恢复展示，懒加载和失败兜底保持。
- Orval：如仅调整 URL 生成逻辑且 Schema 不变则不需要；若同步 OpenAPI 描述则按项目 API 流程重新生成。
- Docker Compose：不强制要求；可用本地/测试对象存储完成回填与媒体读取验证。

## Rollback Plan

若同路径缩略图生成或回填导致列表图片异常，可临时回退公开列表 `cover_image` 到原主图 URL，并保留商品卡片懒加载以控制请求量；回填脚本必须支持 dry-run 与失败清单，实际写入仅新增缩略图对象，不删除原图、不修改业务表结构。若需要撤销对象存储新增缩略图，应依据回填报告按对象 key 清单清理，不能批量删除原图目录。
