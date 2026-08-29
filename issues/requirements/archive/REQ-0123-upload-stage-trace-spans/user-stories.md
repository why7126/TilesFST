---
requirement_id: REQ-0123-upload-stage-trace-spans
title: 上传链路阶段级耗时写入 trace spans - 用户故事
owner: product
source: requirement.md
created_at: 2026-08-25 18:43:20
updated_at: 2026-08-25 18:43:20
---

# 用户故事

## US-001 头像上传阶段耗时可追踪

作为后端 / 媒体能力开发，我希望当前登录用户头像上传时记录阶段级 trace spans，以便在小文件上传变慢时判断瓶颈是否位于文件读取、对象存储写入或派生图生成。

验收要点：

- 头像上传成功后，可以定位同一次上传的 trace spans。
- 至少能看到 `file_read` 与 `original_put_object`。
- 若头像链路生成 thumbnail / display，必须记录对应生成和写入阶段；不生成时必须说明跳过原因。
- 任一阶段失败时，失败前已完成阶段不丢失。

## US-002 通用图片上传六阶段完整记录

作为测试负责人，我希望通用图片上传成功路径稳定产出六个基础阶段，以便用自动化测试确认上传性能可观测性没有退化。

验收要点：

- 成功路径包含 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- 每个 span 包含阶段名、耗时、状态和必要的脱敏 metadata。
- span 顺序与上传处理顺序一致，且归属于同一次上传。
- 记录 spans 不绕过文件大小、MIME Type、扩展名、鉴权和对象 key 安全校验。

## US-003 对象存储或派生生成异常可定位

作为运维 / 发布负责人，我希望上传链路在对象存储写入慢、写入失败或派生图生成失败时仍保留结构化阶段证据，以便判断是基础设施问题、格式处理问题还是业务降级问题。

验收要点：

- 原图写入失败时，trace 能看到失败停在 `original_put_object`。
- thumbnail 或 display 生成失败时，trace 能看到对应 `*_generate` 失败，并能判断后续 `*_put_object` 是跳过还是未执行。
- 错误摘要脱敏，不包含密钥、Authorization header、Cookie、本机绝对路径或完整内部对象路径。
- 日志只能作为辅助证据，不能替代 task trace spans。

## US-004 后续展示或查询边界明确

作为产品 / 项目负责人，我希望在实现前明确 spans 是否对管理端或 API 暴露，以便控制开发范围和避免不必要的 Orval / DB 变更。

验收要点：

- 如果仅内部可观测，OpenSpec 需说明 trace 的事实源、测试入口和排障方式。
- 如果上传响应或任务查询响应新增 trace 字段，必须同步 OpenAPI、Orval、API 文档和测试。
- 如果管理端展示耗时，必须使用紧凑阶段列表，不展示内部对象 key、堆栈或敏感配置。
- DB 影响必须明确为复用现有 task trace 或新增结构，不能在实现阶段含混处理。
