---
req_id: REQ-0012-object-storage-key-layout
status: captured
created_at: 2026-06-27 22:15:10
updated_at: 2026-06-27 22:15:10
recorded_by: product
source: 技术优化
priority_hint: P1
parent_requirement:
---

# 一句话

优化 MinIO 对象存储前缀与 Object Key 生成规则：用语义前缀（images/videos/files/audios）替代 original/，简化 Key 层级并保留 default 多租户段。

# 原始描述

优化存储对象的前缀以及 Object Key 生成规则：

- **前缀**：`images`、`videos`、`files`、`audios` 等，不使用 `original/`
- **resource_type**：如 `user/avatars`、`brands/logos`、`tiles/{tile_id}` 等
- **Key 形态**：`{prefix}/default/{resource_type}/{uuid}.{ext}`
- **保留** `default` 多租户预设段
- **去掉** `{YYYY}/{MM}` 日期分片（分得过细，不利于检索）

# 待澄清

- [ ] 历史 `object_key` 迁移策略（DB + MinIO 存量对象）
- [ ] 读取层是否需兼容旧 Key 格式过渡期
- [ ] `audios/`、`files/` 首期是否仅规范预留、无上传入口

# 探索结论

（/req-generate 已纳入 requirement.md）
