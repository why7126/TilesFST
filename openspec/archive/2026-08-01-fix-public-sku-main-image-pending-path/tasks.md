## 1. Implementation

- [x] 1.1 增加后端媒体对象正式化逻辑，将 `images/default/tiles/pending/...` 图片复制到 SKU 正式图片目录，并生成或复制对应同目录缩略图。
- [x] 1.2 在 SKU 创建成功获得 `tile_id` 后，对提交的 pending 图片执行正式化，再写入或更新 `tile_images.object_key` / `url`。
- [x] 1.3 在 SKU 编辑保存图片列表时，对新增或仍处于 pending 的图片执行正式化，保持图片顺序、主图唯一和移除关联语义不变。
- [x] 1.4 在 SKU 发布流程增加 pending 主图兜底门禁：发布后公开主图不得位于 `images/default/tiles/pending/...`；迁移失败时阻止发布或回滚。
- [x] 1.5 增加存量公开 SKU pending 主图迁移脚本，支持 dry-run、apply、幂等、limit、对象缺失统计、缩略图处理和安全摘要。
- [x] 1.6 保持对象操作通过后端对象存储适配层，禁止前端直连对象存储、禁止信任前端目标 key、禁止使用用户原始文件名。
- [x] 1.7 如新增错误码、响应字段、接口参数或数据库字段，同步 Pydantic Schema、OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md`、SQLite/MySQL schema 和 `.env.example`（按实际影响）。

## 2. Tests

- [x] 2.1 补充后端 pytest：新建 SKU 时上传 pending 主图并保存后，`tile_images.object_key` 进入正式 SKU 目录，`/media/{object_key}` 可读。
- [x] 2.2 补充后端 pytest：编辑已有 SKU 新增 pending 图片后，保存结果不保留 pending key，主图唯一和排序不回退。
- [x] 2.3 补充后端 pytest：发布 SKU 时若主图仍在 pending，系统完成正式化；正式化失败时发布失败且状态/数据库引用不产生半成功。
- [x] 2.4 补充对象存储适配测试：原图复制、缩略图复制或生成、目标 key 冲突、源对象缺失和 MIME/扩展名保留。
- [x] 2.5 补充迁移脚本测试：dry-run 不写对象/数据库，apply 可重入，输出总数、成功、失败、缺失、冲突和失败原因摘要。
- [x] 2.6 补充公开端数据测试：小程序商品列表、搜索结果、品牌详情商品 Tab 或首页商品卡片返回的主图/缩略图 URL 不再派生 pending 目录。
- [x] 2.7 保留或更新现有上传前缀测试，确认新建前上传仍可使用 pending 暂存目录。

## 3. Documentation

- [x] 3.1 如对象 key 策略、迁移脚本或 pending 清理边界变化，同步 `docs/07-object-storage-strategy.md` 与 `rules/object-storage.md`。
- [x] 3.2 如媒体上传/缩略图处理流程变化，同步 `docs/06-video-asset-management.md` 或相关媒体说明（若适用图片段）。
- [x] 3.3 如 API、DB、错误码或环境变量发生变化，同步对应 docs、standards 和 `.env.example`；若无变化，在 trace 中记录不适用原因。
- [x] 3.4 根据修复价值评估是否新增 `docs/knowledge-base/incidents/` 或 best-practice 条目，至少在 archive 前记录是否适用。

## 4. Validation

- [x] 4.1 运行相关后端 pytest。
- [x] 4.2 运行迁移脚本 dry-run，确认输出不泄露密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。
- [x] 4.3 如 API 契约变化，运行 OpenAPI / Orval 生成与相关前端测试。
- [x] 4.4 运行 `openspec validate fix-public-sku-main-image-pending-path --strict`。
- [x] 4.5 在 apply 前确认 BUG-0099 已纳入 Sprint；未纳入时不得执行 `/opsx-apply`。
