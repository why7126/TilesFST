---
change_id: fix-admin-avatar-webp-thumbnail-timeout
source_bug: BUG-0142-admin-avatar-upload-storage-put-slow
sprint: sprint-026
created_at: 2026-08-25 22:25:47
updated_at: 2026-08-25 22:25:47
---

# 设计

## 根因结论

BUG-0142 的 confirmed 根因是头像上传同步请求路径中的 WebP thumbnail 生成出现 28 秒级长尾。阶段级证据显示对象存储写入本身不足以解释 31 秒等待：`original_put_object=151ms`、`thumbnail_put_object=87ms`，而 `thumbnail_generate=28464ms`。

外层 `storage_put_object` 为累计耗时口径，容易把派生图生成时间误表现为对象存储 put 慢。修复应围绕 WebP 解码、缩放、编码或派生图策略收敛，而不是只调对象存储重试或代理超时。

## 修复方案

1. 梳理头像上传调用 `save_upload_file` 的派生图路径，确认 WebP thumbnail / display 生成的解码、缩放、编码参数。
2. 对头像 thumbnail 生成增加性能保护：优先复用已验证的轻量尺寸、目标体积与编码参数；必要时对无法及时生成的派生图执行可观测降级，避免阻塞接口到 30 秒级。
3. 保持原图写入成功语义：若派生图降级或跳过，必须有明确 trace span、日志摘要和客户端可理解行为，不得静默返回不可读 key。
4. 保持三规格 key 语义：成功生成的 thumbnail 使用 `.thumb.webp` 或等价标识，display 使用 `.display.webp` 或等价标识；失败或跳过不得伪造对象存在。
5. 复用 REQ-0123 的阶段级 Task Trace spans，重点验证 `thumbnail_generate` 耗时回落，并确认外层累计 span 不再被用作唯一根因判断。

## 测试策略

- 后端聚焦测试覆盖 WebP 头像上传成功路径：返回原图、thumbnail、display key，并写入阶段 spans。
- 增加 WebP thumbnail 生成性能或超时保护测试，模拟慢生成路径，确认接口不会被阻塞到 30 秒级。
- 增加派生图生成失败或降级测试，确认已完成阶段保留、失败阶段可定位、后续 key/URL 不伪造。
- 媒体四联验收覆盖 key、object、URL、render，并验证管理端同会话头像回显。
- 回归品牌 Logo、Banner、SKU 图片等通用图片上传，避免头像专项策略破坏通用媒体链路。

## 风险与取舍

- 如果直接跳过 thumbnail 生成，可能造成头像列表或菜单继续使用原图，影响后续性能收益；因此跳过必须可观测，并在验收中标注降级。
- 如果只放宽代理或上传超时，会掩盖真实 thumbnail 生成长尾，不能视为修复。
- 如果新增响应字段，需要同步 OpenAPI、Orval 和 API 文档；本 Change 默认避免 API 合同变更。
- 修复不得引入前端直连对象存储或泄露 bucket、endpoint、secret、内部 SDK 堆栈。
