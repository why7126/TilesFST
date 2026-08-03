## Why

BUG-0100 已评审通过：SKU 图片上传后系统会生成同目录 `.thumb` 缩略图对象，并且公开商品卡片、商品列表、搜索结果、品牌详情商品区等场景优先使用该缩略图 URL；但当前缩略图对象只是原图 bytes 的复制品，没有 resize、压缩或真实派生处理。

这会让“缩略图优化”名义存在、实际加载收益缺失。公开端仍可能传输接近原图体积的图片资源，同时对象存储中保存原图和同内容缩略图，增加存储、流量和移动端首屏成本。

## What Changes

- 在后端媒体链路中补齐真实缩略图生成要求：解码图片、保持比例、限制最大宽高、重编码或压缩，并保持同目录 `.thumb` key 规则。
- 明确 SKU 图片上传生成的 `.thumb` 对象不得与原图 bytes 完全一致，且大图场景下像素尺寸与体积应有效降低。
- 明确小图、透明 PNG/WebP、异常图片和缩略图生成失败的边界策略。
- 补齐历史 `.thumb` 对象审计与重生成要求，避免只修新增上传。
- 保持公开商品卡片继续优先使用后端受控 `.thumb` URL，详情大图和图片预览仍可使用原图或高清图。
- 补充回归测试要求，从“缩略图对象存在”提升到“真实轻量派生图”的行为验证。

## Rollback Plan

- 若真实缩略图生成导致 SKU 图片上传失败率异常，可回退新增缩略图生成逻辑，临时保留原图上传和 `.thumb` 缺失回退能力。
- 回退不得删除已成功生成的缩略图对象；若需重建，应通过审计/重生成脚本 dry-run 后执行。
- 若历史重生成脚本 apply 发现异常，应停止后续批次，保留 dry-run / apply 摘要，优先通过对象存在性、原图 size、缩略图 size 和失败原因对账。
- 回退期间公开端仍必须通过后端 `/media/{object_key}` 受控读取，禁止前端直连对象存储。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `object-storage`: 补充真实缩略图生成、体积/尺寸约束、历史缩略图审计与重生成、安全输出要求。
- `tile-sku-management`: 补充 SKU 图片上传后生成真实同目录缩略图、多格式边界、失败策略和测试要求。
- `miniapp-product-list-page`: 补充商品卡片缩略图必须是轻量优化图片，不得仅以对象存在性视为性能优化生效。

## Impact

- Backend / Admin API: 影响管理端 SKU 图片上传后处理链路；上传响应结构通常保持不变。若新增错误码、响应字段或接口参数，必须同步 Pydantic Schema、OpenAPI、Orval 和 `docs/03-api-index.md`。
- Object Storage / MinIO: 影响 `.thumb` 对象生成、历史审计和重生成；必须遵守单 Bucket、标准前缀、同目录 `.thumb` 和后端适配层边界。
- Dependencies / Docker: 可能新增图片处理依赖；必须同步后端依赖文件与 Docker 镜像构建验证。
- Database: 默认不要求新增表字段；历史审计/重生成脚本读取 `tile_images.object_key` 和对象存储元信息。若引入迁移记录表，必须同步 SQLite/MySQL schema 和 `docs/04-database-design.md`。
- Miniapp / Public Web: 公开商品卡片继续使用可访问 `.thumb` URL，加载性能不应回退；详情高清图不应被强制降级。
- Tests: 需要补充后端媒体处理测试、上传集成测试、历史重生成脚本测试和公开商品卡片 URL 回归测试。
