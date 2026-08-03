## 1. Implementation

- [x] 1.1 在后端媒体模块封装真实缩略图生成 helper，支持 JPG、PNG、WebP 解码、等比缩小、禁止放大小图、重编码和 size/尺寸结果返回。
- [x] 1.2 更新 SKU 图片上传链路，使传入 `thumbnail_key` 时写入真实缩略图 bytes，而不是复制原图 bytes。
- [x] 1.3 明确并实现原图上传成功但缩略图生成失败时的策略，保证不会产生原图不可访问或数据库引用半成功。
- [x] 1.4 更新历史商品卡片图片审计/回填脚本：dry-run 识别疑似无效缩略图，apply 重生成 `.thumb` 对象并保持幂等。
- [x] 1.5 保持同目录 `.thumb` key 规则、单 Bucket 策略、后端对象存储适配层和 `/media/{object_key}` 受控读取边界。
- [x] 1.6 如新增图片处理依赖，同步后端依赖文件、Docker 镜像构建输入和部署说明。
- [x] 1.7 如新增错误码、接口字段、数据库字段或环境变量，同步 Pydantic Schema、OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md`、`.env.example` 和相关 tests；若无变化，在 trace 中记录不适用。

## 2. Tests

- [x] 2.1 补充后端媒体单元测试：大图生成缩略图后像素尺寸小于原图或不超过目标最大宽高，bytes 不等于原图。
- [x] 2.2 补充后端媒体测试：缩略图 size 通常小于原图，异常增大场景按约定保护或告警。
- [x] 2.3 补充格式测试：JPG、PNG、WebP、横图、竖图、大图、小图、透明图和异常图片输入。
- [x] 2.4 补充上传接口或集成测试：管理端 SKU 图片上传后对象存储中原图和 `.thumb` 均存在，且 `.thumb` 不是原图复制品。
- [x] 2.5 补充历史脚本测试：dry-run 不写对象，apply 可重入，覆盖对象缺失、已合格缩略图跳过、同 size/同 bytes 重生成和失败原因摘要。
- [x] 2.6 补充公开商品卡片数据回归测试：小程序首页、商品列表、搜索结果或品牌详情商品区继续返回可访问 `.thumb` URL。
- [x] 2.7 保留现有缩略图 key、缺失回退、媒体缓存和视频 Range 测试，避免性能修复引入无图或媒体读取回归。

## 3. Documentation

- [x] 3.1 同步 `docs/07-object-storage-strategy.md` 中 SKU 缩略图生成策略、历史重生成和同目录 `.thumb` 约定。
- [x] 3.2 如新增图片处理依赖或 Docker 构建要求，同步 `docs/02-deployment.md`、`docs/08-production-image-release.md` 或镜像构建计划相关说明。
- [x] 3.3 如 API/Orval/DB/.env 无变化，在 Change trace 或实施记录中明确说明不适用原因。
- [x] 3.4 修复后评估是否新增 `docs/knowledge-base/incidents/` 条目，沉淀“缩略图对象存在不等于性能优化生效”的媒体链路经验。

## 4. Validation

- [x] 4.1 运行相关后端 pytest：媒体存储、上传、SKU 图片、历史脚本和公开商品卡片数据测试。
- [x] 4.2 运行历史缩略图审计 dry-run，确认输出不泄露密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。
- [x] 4.3 如 API 契约变化，运行 OpenAPI / Orval 生成与相关前端测试。
- [x] 4.4 如新增依赖，运行 Docker 或生产镜像构建相关验证。
- [x] 4.5 运行 `openspec validate fix-media-thumbnail-generation --strict`。
- [x] 4.6 在 apply 前确认 BUG-0100 已纳入 Sprint；未纳入时不得执行 `/opsx-apply`。

## 归档验证摘要

- 归档时间：2026-08-01 08:19:38
- 归档路径：`openspec/archive/2026-08-01-fix-media-thumbnail-generation/`
- 关联 BUG：`BUG-0100-thumbnail-size-equals-original`
- 关联 Sprint：`sprint-016`
- 任务状态：24/24 completed。
- Spec 同步：MODIFIED `object-storage` / `tile-sku-management` / `miniapp-product-list-page`，目标正式 spec 中均存在同名 Requirement。
- 文档同步：已同步 `docs/07-object-storage-strategy.md`、`docs/02-deployment.md`、`docs/08-production-image-release.md`，并新增 `docs/knowledge-base/incidents/media-thumbnail-copy-regression.md`。
- API/DB/Orval/.env：无接口字段、错误码、数据库结构、Pydantic Schema、环境变量变化，不需要同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md` 或 `.env.example`。
- 验证命令与结果：14 个直接相关 pytest 通过；历史审计 dry-run 输出安全；后端 Docker build 与容器内 Pillow 导入验证通过；`openspec validate fix-media-thumbnail-generation --strict` 通过。
- 验收结论：BUG-0100 缩略图复制原图的问题已修复，新增上传与历史 `.thumb` 审计/再生成链路达到验收要求。
- Issue 状态：`BUG-0100-thumbnail-size-equals-original` 已同步为 `done`，物理路径为 `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/`。
- Sprint 状态：`sprint-016` 范围内该 Change 已 archived，等待 Sprint 总归档关闭。
