---
title: 用户故事
purpose: REQ-0012 对象存储 Key 布局优化相关用户故事
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:17:37
updated_at: 2026-06-27 22:17:37
note: REQ-0012-object-storage-key-layout
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 平台后端开发 | P1 | 是 |
| US-002 | 管理端运营 / 管理员 | P1 | 是 |
| US-003 | 运维 / 发布负责人 | P1 | 是 |

---

## US-001 开发使用语义清晰的 Object Key 规则

**作为** 平台后端开发，  
**我希望** 上传生成的 Object Key 使用 `images`/`videos`/`files` 等语义前缀，且形态为 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`，  
**以便** 在 MinIO Console、日志与文档中快速理解对象类型，且后续扩展多租户时不改结构。

### 验收要点

- `build_object_key()` 不再插入 `{YYYY}/{MM}`。
- 新上传 MUST NOT 使用 `original/` 前缀。
- `resource_type` 遵循领域路径（如 `user/avatars`、`brands/logos`、`tiles/{id}`）。
- `MINIO_PREFIX_*` 与代码生成逻辑一致，避免硬编码。

### 关联功能

- FR-001、FR-002、FR-003、FR-005、FR-007

---

## US-002 管理员上传媒体后 URL 仍可用

**作为** 管理端管理员，  
**我希望** 上传头像、品牌 Logo、SKU 图片/视频后，列表与编辑页仍能正常预览，  
**以便** 日常运营不受 Key 规则变更影响。

### 验收要点

- 四个上传 API 响应仍为 `{ object_key, url }`，前端无需改调用方式。
- 迁移完成后，历史已保存的 Logo/头像/SKU 媒体 MUST 可访问（无 404）。
- MIME、大小限制行为与变更前一致。

### 关联功能

- FR-004、FR-006

---

## US-003 运维可安全迁移存量 object_key

**作为** 运维或发布负责人，  
**我希望** 有一次性迁移脚本（支持 dry-run），将 DB 与 MinIO 中旧 Key 迁至新规则，  
**以便** 发版后环境一致、无孤儿对象或断链 URL。

### 验收要点

- 脚本 dry-run 输出待迁移条目数与示例 Key 映射。
- `--apply` 后 SQLite 四类 `object_key` 字段与 MinIO 对象一致。
- 迁移 MUST NOT 删除仍被 DB 引用的有效对象。
- runbook 说明回滚或备份建议。

### 关联功能

- FR-006、FR-007

---

## Out of Scope（本期不做）

| 角色 | 说明 |
|---|---|
| 店主端用户 | 无新上传；仅消费 `/media` URL |
| 小程序用户 | 不涉及 |
| 内容运营（音频/文档） | `files/`、`audios/` 仅规范预留，无上传入口 |
