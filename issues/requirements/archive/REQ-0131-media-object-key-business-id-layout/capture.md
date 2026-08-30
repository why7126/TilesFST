---
req_id: REQ-0131-media-object-key-business-id-layout
status: done
created_at: 2026-08-29 19:15:09
updated_at: 2026-08-29 23:24:36
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0012-object-storage-key-layout
---

# 一句话

统一媒体对象 Key 按业务对象 id 分目录，并补齐旧媒体兼容、迁移、审计与文档规范。

# 原始描述

用户希望所有媒体都按对象 id 建目录，并将该策略落地成文档和规范。

# 背景与关联

- 关联父需求：`REQ-0012-object-storage-key-layout`
- 关联能力：对象存储 Key 规范、媒体上传、媒体受控读取、图片派生图、生产媒体维护任务
- 当前现状：SKU 图片和 SKU 视频已按 `tile_id` 或 `pending` 目录组织；品牌 Logo、品牌证书、Banner、头像等媒体主要按资源类型目录与 uuid 文件名组织
- 变更目标：统一各类媒体的业务对象 id 目录规则，明确上传前 pending、保存后 formalize、旧 key 兼容、迁移和验收要求
- 影响范围：后端上传接口、媒体 key 生成、对象存储维护脚本、数据库媒体引用、Web 管理端、小程序媒体展示、发布和运维文档

# 待澄清

- [ ] “对象 id”是否统一定义为业务表主键，例如 `brand_id`、`certificate_id`、`banner_id`、`user_id`、`tile_id`
- [ ] 上传发生在业务对象创建前时，是否统一使用 `pending` 目录并在保存后 formalize 到业务 id 目录
- [ ] 存量媒体是否仅保持旧 key 兼容，还是需要提供受控迁移到新目录的生产作业
- [ ] 旧对象迁移后是否需要保留旧 key 一段时间，以及清理窗口、回滚责任和备份要求
- [ ] 是否要求所有图片派生对象 `.thumb.webp` / `.display.webp` 与原图同步迁移并同目录保存
- [ ] 是否需要同步 OpenAPI / Orval 字段说明，明确客户端不得拼接对象存储路径，只能消费后端返回 URL
- [ ] 产品数据采集与链路观测规范适用层级需在后续 PRD/Change 中确认，尤其是上传 Task Trace、请求日志、维护任务摘要和迁移审计

# 建议验收要点

- [ ] 对象 Key 策略矩阵覆盖头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片、品牌证书 PDF/文档，以及后续新增媒体类型。
- [ ] 每类媒体明确业务 id 目录、pending 目录、正式化触发时机、派生图目录、文件前缀、受控 URL 和旧 key 兼容策略。
- [ ] 新上传媒体按业务对象 id 目录生成或 formalize，前端和小程序不得自行拼接 object key、bucket、endpoint 或 raw URL。
- [ ] 存量媒体迁移必须支持 dry-run、apply、二次审计、幂等复跑、失败分类、备份与回滚说明。
- [ ] 旧版本媒体显示不得因 key 策略调整而中断；旧 key 在数据库引用和对象存储中仍可被 `/media/{object_key}` 或等价受控 URL 读取。
- [ ] 文档同步覆盖 `rules/object-storage.md`、`rules/media.md`、`docs/07-object-storage-strategy.md`、媒体维护 runbook、OpenSpec object-storage/media specs 和发布验收模板。

# 探索结论

前置探索结论：当前系统显示链路主要读取数据库已保存的完整 `object_key` / `file_key` / `logo_object_key`，再通过后端 `/media/{object_key}` 受控读取；仅修改新上传 Key 规则通常不会影响旧媒体显示。若迁移旧对象或改为按业务 id 推导路径，必须同步迁移数据库引用、原图、缩略图、展示图，并保留旧 key 兼容与回滚路径。
