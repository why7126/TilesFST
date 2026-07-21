---
change_id: fix-miniapp-sku-detail-video-url
type: fix
status: proposed
created_at: 2026-07-20 08:20:58
updated_at: 2026-07-20 22:42:13
source_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
source_requirement: REQ-0044-miniapp-sku-detail-page
---

# Test Plan - fix-miniapp-sku-detail-video-url

## 自动化测试

| 范围 | 命令 | 目的 |
|---|---|---|
| 后端 SKU 详情 | `uv run pytest tests/test_miniapp_home.py -k miniapp_sku_detail` | 覆盖详情接口、媒体 URL、商品参数顺序、收藏和埋点 |
| 小程序静态 | `uv run pytest tests/test_miniapp_static.py -k sku_detail` | 覆盖详情页 WXML/TS/JS 视频节点、poster、内容顺序和事件绑定 |
| 媒体安全回归 | `uv run pytest tests/test_miniapp_home.py -k media` | 如测试名称调整，覆盖安全媒体 URL 和 object key 语义 |
| 媒体访问兜底 | `uv run pytest tests/test_media_storage.py` | 覆盖 `/media/{object_key}` 对旧图片 key 的兼容映射 |

## 手工验收

1. 准备包含图片和视频的已发布 SKU。
2. 确认数据库中视频记录 `object_key` 为对象 key，`file_name` 为原始文件名或显示名。
3. 确认数据库中图片记录存在 `object_key`；如 `url` 为历史 `original/default/...` 路径，接口响应仍应返回当前 `/media/{object_key}`。
4. 请求 `GET /api/v1/miniapp/skus/{sku_id}`，确认图片和视频 `media[].url` 均为 `/media/...` 或完整安全 URL，且视频 URL 不使用原始上传文件名。
5. 在微信开发者工具或真机进入 SKU 详情页。
6. 切换到视频项，验证未播放态不显示商品主图覆盖；验证播放、暂停、错误提示和离开页面暂停。
7. 验证页面内容顺序为“商品信息 >> 品牌信息 >> 商品参数”，商品信息仅展示商品名称和商品价格。
8. 验证商品参数顺序为“SKU 编码 >> 类目 >> 规格 >> 主色系 >> 表面工艺”。

## 不需要执行

- 不需要 Docker Compose 全量验证，除非实现阶段改动服务启动、环境变量、MinIO 配置或跨容器访问。
- 不需要 Orval，前提是仅修正既有响应字段来源且 OpenAPI schema 不变。
