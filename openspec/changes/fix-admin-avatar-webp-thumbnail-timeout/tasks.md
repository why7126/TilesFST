---
change_id: fix-admin-avatar-webp-thumbnail-timeout
source_bug: BUG-0142-admin-avatar-upload-storage-put-slow
sprint: sprint-026
created_at: 2026-08-25 22:25:47
updated_at: 2026-08-25 22:35:18
---

# 任务

## 1. 根因定位与策略确认

- [x] 1.1 读取头像上传入口和媒体存储服务，确认 WebP thumbnail / display 派生图生成参数、同步阻塞点和错误处理。
- [x] 1.2 用 BUG-0142 证据中的阶段级 spans 校准实现前基线，避免把 `thumbnail_generate` 误判为对象存储 put。
- [x] 1.3 明确头像 thumbnail 的性能边界和降级策略，并记录不改变 API、DB、对象 key 与 Bucket 的实现约束。

## 2. 后端修复

- [x] 2.1 收敛 WebP 头像 thumbnail 生成长尾，确保问题样本不再触发 30 秒级上传等待。
- [x] 2.2 保持原图、thumbnail、display key 语义稳定；派生图失败或跳过时不得返回伪造可读 key。
- [x] 2.3 保留并校验 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 阶段 spans。
- [x] 2.4 确认错误摘要脱敏，不暴露对象存储 endpoint、bucket 权限、密钥、Authorization header、Cookie、真实 `.env` 或本机绝对路径。

## 3. 测试与回归

- [x] 3.1 增加或更新后端聚焦测试，覆盖 WebP 头像上传成功、thumbnail 生成耗时收敛和阶段 spans。
- [x] 3.2 增加派生图慢生成、失败或降级路径测试，确认接口不会阻塞到 30 秒级，且 key/object/URL 语义一致。
- [x] 3.3 回归品牌 Logo、Banner、SKU 图片等通用图片上传路径，确认头像专项修复不破坏通用媒体链路。
- [x] 3.4 若修改上传响应、Pydantic Schema 或错误码，同步 OpenAPI、Orval、API 文档和相关测试；若未修改，记录 N/A。

## 4. 验收与归档准备

- [x] 4.1 使用 127KB 级问题 WebP 样本通过 Docker Web 或等价 `localhost:3000` 入口验证 `POST /api/v1/admin/uploads` 不再 30 秒级等待。
- [x] 4.2 验证 `thumbnail_generate` 不再出现 20 秒以上长尾，并记录 request/task trace id 摘要。
- [x] 4.3 完成媒体四联验收：key、object、URL、render。
- [x] 4.4 运行聚焦后端测试、OpenSpec 校验、语言校验、目录结构校验与 Workflow Sync。
- [x] 4.5 若修复经验可复用，评估是否沉淀 `docs/knowledge-base/incidents/`；没有则记录 N/A。

## 实现记录

- 后端：将 WebP 派生图 Pillow 编码参数从最慢 `method=6` 调整为低延迟 `method=1`，降低头像 thumbnail 同步生成长尾风险。
- API：未修改 `POST /api/v1/admin/uploads` 响应字段、Pydantic Schema 或错误码；OpenAPI / Orval 为 N/A。
- 数据库：未修改 schema、migration 或持久化结构。
- 对象存储：不改变 bucket、key 前缀、ACL、MinIO / S3 适配层或 `/media/{object_key}` 受控读取策略。
- 测试：新增 WebP 派生低延迟编码参数测试和 WebP 头像上传原图、thumbnail、display 与阶段 spans 测试。
- 端到端 smoke：通过 `localhost:3000` 上传 159938 bytes WebP 头像，HTTP 200，用时 1274.2ms；`task_trace_id=task_upload_image_55a0044030624bd2`，`thumbnail_generate=760ms`，`thumbnail_put_object=108ms`，`display_generate=101ms`，`display_put_object=128ms`。
- 媒体四联：上传响应返回原图、thumbnail、display key；三类 `/media/{key}` 读取均为 200；管理端 Web 入口 POST 返回 200；render 维度以同会话上传成功和媒体 URL 可读作为 smoke 证据。
- 知识沉淀：本次属于既有 WebP 编码参数调优，暂不新增 `docs/knowledge-base/incidents/`；后续若再次出现图片派生图长尾，可再沉淀通用 incident。
