## 背景与原因

管理端 SKU、品牌、证书和 Banner 列表都是图片密集页面，运营人员在列表中只需要快速识别对象，不需要加载原图级资源。当前品牌与证书已有缩略图优先策略，但 SKU 与 Banner 列表仍直接使用原图字段，导致列表首屏、翻页和滚动加载体感较慢，也让同类管理端列表的 image adapter 口径不一致。

REQ-0098 已评审通过，要求将管理端列表资源选择收敛为“列表优先缩略图，详情/编辑/预览继续使用原图”，并同步 API 契约、OpenAPI、Orval 与测试。

## 变更内容

- 管理端 SKU 列表响应新增 `main_image_thumbnail_url`，由主图 object key 派生后端受控缩略图 URL。
- 管理端 Banner 列表响应新增 `image_thumbnail_url`，由最终 `image_object_key` 派生后端受控缩略图 URL。
- SKU 与 Banner 列表页优先使用缩略图字段，缺失或加载失败时回退原图或既有占位。
- 品牌与证书列表复核既有缩略图优先策略，补齐必要测试或验收说明。
- 详情、编辑、上传预览、放大预览和原文件查看继续使用原图或原文件。
- 同步 OpenAPI、Orval、后端测试、前端测试和管理端列表横切验收。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `tile-sku-management`: 管理端 SKU 列表响应和列表展示必须支持 `main_image_thumbnail_url` 缩略图优先策略。
- `banner-management`: 管理端 Banner 列表响应和列表展示必须支持 `image_thumbnail_url` 缩略图优先策略。

## 影响范围

- 后端：管理端 SKU / Banner 列表 Schema 与 service 映射。
- API：管理端列表响应新增向后兼容字段，需要同步 OpenAPI。
- Web 管理端：SKU / Banner 列表图片展示优先级调整，品牌 / 证书列表复核。
- Orval：需要重新生成前端 API 类型与客户端。
- 测试：需要后端 API 字段测试、前端列表渲染优先级与 fallback 测试。
- 数据库：不新增或修改 SQLite/MySQL 表结构。
- 存储：不改变上传鉴权、MinIO 单桶策略或 `/media/{object_key}` 受控读取边界。
- 小程序与店主 Web：不涉及。
