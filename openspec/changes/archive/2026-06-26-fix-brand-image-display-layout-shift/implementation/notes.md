---
purpose: fix-brand-image-display-layout-shift 实现备注
status: proposed
created_at: 2026-06-25 22:28:15
---

# 实现备注

本文件用于 `/opsx-apply fix-brand-image-display-layout-shift` 阶段记录实现取舍。

## 初始约束

- 不新增数据库字段。
- 不绕过后端授权访问对象存储。
- 若 API schema 变化，必须同步 OpenAPI、Orval 与 API 文档。
- Web UI 修改不得新增裸 Hex。

## 待实现阶段确认

- `/media/{object_key}` 是采用后端代理、签名 URL，还是环境区分方案。
- 是否将管理端通知抽象成共享 toast 组件。
- 是否需要同步 `docs/06-video-asset-management.md` 或 `docs/03-api-index.md`。
