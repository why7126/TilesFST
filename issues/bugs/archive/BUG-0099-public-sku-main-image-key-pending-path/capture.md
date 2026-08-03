---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
created_at: 2026-08-01 07:12:45
updated_at: 2026-08-01 08:06:26
severity_hint: high
environment: backend-media
related_requirement: null
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 公开商品主图已经属于已发布/已绑定商品素材，但对象 key 仍大量保留在 images/default/tiles/pending/... 暂存路径，偏离已交付媒体对象生命周期和商品目录化存储预期，属于已有能力行为偏差，因此判定为 BUG。
---

# 现象

大多数公开商品主图的对象 key 仍在 `images/default/tiles/pending/...` 路径下。`pending` 看起来像上传暂存目录，但公开商品图片正常应在商品自己的稳定目录中，而不是长期停留在 pending 路径。

# 复现步骤

1. 打开管理端或后端数据源，查看已公开商品的主图记录。
2. 检查主图 URL 或对象存储 key。
3. 观察多数公开商品主图是否仍使用 `images/default/tiles/pending/...`。
4. 对比商品发布、保存或设为主图后是否有迁移到商品专属目录的动作。

# 期望 vs 实际

- 期望：商品图片在完成绑定、保存或发布后，应落在可追溯到对应商品的稳定目录中；`pending` 仅作为未绑定上传的暂存区，不应成为公开商品主图的长期路径。
- 实际：大量公开商品主图仍使用 `images/default/tiles/pending/...`，导致对象生命周期、目录语义和后续清理策略不清晰。

# 影响范围

- 后端媒体上传、商品图片绑定、主图设置和发布流程。
- MinIO 对象 key 规划、对象生命周期管理和后续清理任务。
- 店主 Web 展示端、微信小程序商品列表/详情页的公开图片 URL。
- 可能涉及历史数据迁移或存量对象 key 修复。

# 初步线索

- 需要确认 `pending` 是否原本用于上传前/未绑定素材的暂存目录。
- 需要检查商品图片保存、设为主图、公开发布时是否缺少对象迁移或 key 重写。
- 需评估已公开存量图片是否需要迁移脚本，并保证旧 URL 在迁移期间不失效。
- 修复时应遵守 MinIO 单桶 + 前缀策略，上传仍需经过后端鉴权和对象存储适配层。

# 建议验收或复现要点

- [ ] 新上传并绑定到商品的主图不再长期保留在 `images/default/tiles/pending/...`。
- [ ] 已公开商品主图 key 能定位到商品自身目录或明确的已绑定媒体目录。
- [ ] `pending` 目录仅保留未绑定、未发布或可过期清理的临时对象。
- [ ] 存量公开商品主图完成安全迁移或提供兼容策略，迁移后图片仍可访问。
- [ ] 店主 Web 展示端与微信小程序商品主图访问不回退。
- [ ] 对象迁移、保存和发布流程补充测试，覆盖主图 key、公开 URL 和 pending 清理边界。

# 附件

- 暂无。
