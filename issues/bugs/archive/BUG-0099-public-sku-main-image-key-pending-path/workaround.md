---
bug_id: BUG-0099-public-sku-main-image-key-pending-path
status: done
created_at: 2026-08-01 07:25:02
updated_at: 2026-08-01 08:06:26
---

# 临时规避方案

## 当前可用规避

在正式修复前，不建议启用任何自动清理 `images/default/tiles/pending/` 的对象生命周期任务或脚本。

若必须降低新增数据风险，可采用人工操作规避：

1. 先创建并保存 SKU，使其获得稳定 `tile_id`。
2. 再进入编辑模式上传商品图片，让上传接口携带 `tile_id`。
3. 保存并设置主图。
4. 发布 SKU 前检查主图对象 key 不在 `images/default/tiles/pending/`。

## 存量数据规避

对已公开商品：

- 可先运行只读审计，统计公开商品主图位于 pending 的数量。
- 不建议手工直接改数据库 key，除非已经确认对象存储中目标 key 存在且公开 URL 可访问。
- 不建议只复制原图而不处理缩略图，否则公开商品卡片可能仍访问缺失的 `.thumb` 对象。

## 限制

以上规避方案依赖人工流程，不能从根本上保证后续新建 SKU 不再产生 pending 主图。根治仍需要在后端 SKU 保存/发布链路中补齐对象正式化逻辑，并提供存量迁移方案。
