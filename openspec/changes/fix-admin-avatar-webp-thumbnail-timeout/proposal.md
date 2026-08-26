---
change_id: fix-admin-avatar-webp-thumbnail-timeout
source_bug: BUG-0142-admin-avatar-upload-storage-put-slow
sprint: sprint-026
created_at: 2026-08-25 22:25:47
updated_at: 2026-08-25 22:25:47
---

# 修复管理端 WebP 头像缩略图生成长尾

## 背景

BUG-0142 记录了管理端上传 127KB 级 WebP 头像时，`POST /api/v1/admin/uploads` 返回 200 但等待约 31.74 秒的问题。阶段级证据已经确认主要慢点不是对象存储写入，而是头像派生图的 `thumbnail_generate` 阶段：同一次请求中 `original_put_object=151ms`、`thumbnail_generate=28464ms`、`thumbnail_put_object=87ms`。

当前头像上传链路在接口响应前同步完成原图写入、thumbnail 生成、thumbnail 写入以及 display 派生处理。对特定 WebP 样本，thumbnail 生成出现 28 秒级长尾，会直接阻塞管理端头像上传体验，也会让外层累计 span 被误读为对象存储 put 变慢。

## 变更内容

- 收敛管理端头像 WebP thumbnail 生成长尾，确保 127KB 级问题样本不再出现 30 秒级接口等待。
- 明确头像上传对 thumbnail / display 派生图生成的性能边界、降级策略和可观测要求。
- 保持原图、thumbnail、display 三规格对象 key、受控 `/media/{object_key}` 读取和对象存储适配层边界不变。
- 继续复用已补齐的上传阶段级 Task Trace spans，将验收重点落到 `thumbnail_generate` 阶段耗时和媒体四联证据。
- 不改变数据库结构；默认不新增上传响应字段，不触发 Orval。

## 能力范围

### 新增能力

无。

### 修改能力

- `admin-profile-page`：补充头像上传性能与慢派生图降级要求。
- `media-multi-variant-images`：补充支持图片派生图生成的性能边界与失败可观测要求。

## 回滚计划

- 若修复引入图片派生图质量、对象 key 或受控读取回归，回滚头像上传缩略图生成策略到变更前实现。
- 回滚后必须保留阶段级 Task Trace spans，不得移除 REQ-0123 已建立的阶段可观测能力。
- 回滚验证至少覆盖：头像原图可上传、`/media/{object_key}` 可读、旧头像不被错误覆盖、错误响应不泄露对象存储内部信息。

## 影响

- 后端：影响头像上传派生图生成路径和媒体服务测试。
- API：默认不改变 `POST /api/v1/admin/uploads` 响应结构；若实现阶段新增字段，必须同步 OpenAPI、Orval、API 文档和测试。
- 数据库：默认不变。
- 对象存储：不改变 bucket、key 前缀、ACL 或适配层访问边界。
- Web 管理端：头像上传等待时间应收敛；默认不新增页面 UI。
- 小程序 / 店主 Web：不涉及。
- Docker Compose：需要通过 Docker Web 或等价入口验证 `localhost:3000` 上传链路。
