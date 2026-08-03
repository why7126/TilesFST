## Context

BUG-0099 指出公开 SKU 主图仍大量位于 `images/default/tiles/pending/...`。根因是媒体上传链路和 SKU 业务绑定链路之间缺少对象生命周期闭环：新建 SKU 前上传图片时没有 `tile_id`，上传接口使用 `tiles/pending`；创建/编辑 SKU 时直接保存前端提交的 `object_key`；发布 SKU 时只改状态，不处理对象迁移。

正式规格中，`tile-sku-management` 已要求 SKU 图片经后端授权上传、多图主图、缩略图生成和历史缩略图回填；`object-storage` 已要求单桶标准前缀、受控读取和同目录缩略图。当前 Change 在这些能力上补齐 pending 主图正式化和存量迁移约束。

## Goals / Non-Goals

**Goals:**

- 新建 SKU 时，先上传到 pending 的图片在绑定成功后进入 SKU 正式图片目录。
- 编辑已有 SKU 新增图片时，保存后不留下 pending 图片关联。
- 发布 SKU 后，公开主图不得位于 pending 路径。
- 存量公开 SKU pending 主图可通过安全、幂等的迁移脚本修复。
- 原图和同目录缩略图保持一致迁移或可重建，公开端图片访问不回退。
- 对象操作继续通过后端对象存储适配层，保持 MinIO / S3 兼容边界。

**Non-Goals:**

- 不引入前端直传对象存储。
- 不新增多 Bucket 策略。
- 不改变 SKU 图片数量、主图排序、删除关联语义。
- 不新增视频转码、图片多清晰度或复杂媒体处理能力。
- 不改变小程序 UI 结构；只保证返回的图片 URL 可访问且不继续派生 pending。

## Decisions

### D1. 正式目录以 SKU 维度组织

绑定后的 SKU 图片对象 key SHOULD 使用可追溯到 SKU 的正式目录，例如：

```text
images/default/tiles/{tile_id}/<uuid>.<ext>
images/default/tiles/{tile_id}/<uuid>.thumb.<ext>
```

`pending` 只保留未绑定、未发布或可过期清理的临时对象。实现可复用原始文件名中的 uuid 和扩展名，但不得使用用户原始文件名，也不得信任前端提交目标路径。

### D2. 对象正式化放在后端业务保存/发布链路

推荐在 SKU 创建成功获得 `tile_id` 后，对提交的 pending 图片执行正式化：复制原图到正式 key、复制或生成同目录缩略图、更新 `tile_images` 引用，再返回 SKU 详情。编辑已有 SKU 时也应对提交图片进行同类处理。

发布阶段应作为兜底门禁：若主图仍在 pending，应尝试正式化；正式化失败时阻止发布或回滚，避免公开商品引用 pending 主图。

### D3. 对象复制与数据库更新需要可回滚

对象复制、缩略图复制/生成和数据库引用更新不能产生半成功状态。实现应优先保证：

- 对象复制失败时不更新数据库引用。
- 数据库更新失败时不删除原 pending 对象。
- 发布失败返回明确错误，并保持发布前状态。
- 迁移脚本输出原 key / 新 key 对账摘要，但不得输出密钥、本机绝对路径、Authorization header、Cookie 或 `.env` 内容。

### D4. 存量迁移脚本必须 dry-run 优先且可重入

迁移脚本应默认 dry-run，统计公开 SKU 中 pending 主图数量、原图缺失数量、缩略图缺失数量、目标 key 冲突数量和预期更新数量。apply 模式执行前应复用相同筛选条件，并做到重复执行不会重复复制或破坏已迁移数据。

### D5. 公开端不承担修复职责

小程序与店主 Web 继续通过后端公开接口和 `/media/{object_key}` 读取媒体。公开端不应通过字符串替换 pending URL 来“猜测”正式 key；正式化与兼容 fallback 应在后端数据和媒体读取层完成。

## Risks / Trade-offs

- [Risk] 对象复制成功但数据库更新失败。  
  Mitigation: 保留 pending 原对象，不删除源对象；数据库更新放在事务边界内，失败时不改变 SKU 发布状态。
- [Risk] 存量迁移目标 key 与已有对象冲突。  
  Mitigation: 目标 key 生成使用随机 uuid 或冲突检测；dry-run 输出冲突数量。
- [Risk] 缩略图遗漏导致商品列表加载失败。  
  Mitigation: 迁移原图时同步复制/生成 `.thumb`；公开列表继续保留缩略图缺失 fallback。
- [Risk] API 错误码或响应结构变化引发 Orval drift。  
  Mitigation: 若新增错误码或字段，任务明确同步 OpenAPI / Orval / docs / tests。

## Migration Plan

1. 增加后端媒体对象正式化 helper，支持 pending 图片复制到 SKU 正式目录，并处理同目录缩略图。
2. 在 SKU 创建、编辑和发布兜底路径中调用正式化逻辑。
3. 增加存量迁移脚本，先 dry-run 后 apply，输出统计摘要。
4. 更新后端测试、公开端数据测试和迁移脚本测试。
5. 如接口契约、错误码或 DB schema 有变化，同步 docs、OpenAPI、Orval、SQLite/MySQL schema 与测试。

## Open Questions

- 目标正式 key 是否沿用 pending 原 uuid，还是统一生成新 uuid；实现阶段需以避免冲突和可追溯为优先。
- 迁移后是否删除 pending 源对象；默认不删除，待验证生命周期策略稳定后再另行设计清理。
