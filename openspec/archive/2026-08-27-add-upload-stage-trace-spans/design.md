---
change_id: add-upload-stage-trace-spans
source_requirement: REQ-0123-upload-stage-trace-spans
sprint: sprint-026
created_at: 2026-08-25 18:58:00
updated_at: 2026-08-25 18:58:00
---

# 设计

## 设计目标

本 Change 将头像上传与通用图片上传的阶段级耗时写入既有 Task Trace spans。日志可以继续输出同类摘要，但不作为验收事实源；测试和排障应能从结构化 trace 中看到阶段名称、耗时、状态和脱敏错误摘要。

## 阶段模型

上传链路使用固定基础阶段名：

| 阶段 | 计时边界 | 适用范围 |
|---|---|---|
| `file_read` | 从读取上传文件流开始，到后端获得可校验和处理的字节内容结束 | 头像上传、通用图片上传 |
| `original_put_object` | 从调用对象存储适配层写入原图开始，到对象存储确认或失败结束 | 头像上传、通用图片上传 |
| `thumbnail_generate` | 从开始生成 thumbnail 派生图开始，到生成结果或失败结束 | 通用图片上传；头像如生成派生图则适用 |
| `thumbnail_put_object` | 从调用对象存储适配层写入 thumbnail 开始，到确认或失败结束 | 通用图片上传；头像如生成派生图则适用 |
| `display_generate` | 从开始生成 display 派生图开始，到生成结果或失败结束 | 通用图片上传；头像如生成派生图则适用 |
| `display_put_object` | 从调用对象存储适配层写入 display 开始，到确认或失败结束 | 通用图片上传；头像如生成派生图则适用 |

每个 span 至少包含 `span_name`、`status`、`duration_ms`、`started_at`、`ended_at`、`error_code`、`error_message` 和脱敏 `metadata`。实现阶段应优先复用现有 Task Trace 存储和查询结构；若现有结构没有 span 持久化能力，必须先补充 DB/API 设计并更新对应文档。

## 失败与跳过语义

- 已完成阶段的 spans 必须在后续阶段失败时保留。
- 当前阶段失败时必须写入 `failed` span，并记录脱敏错误摘要。
- 后续阶段因前置失败未执行时，可以记录 `skipped` span；如现有 Task Trace 不适合写跳过 span，必须保证 trace 能明确解释后续阶段未出现的原因。
- 头像上传如业务策略不生成 thumbnail 或 display，相关阶段可记录 `skipped` 与跳过原因，或在实现记录中明确该头像链路不适用的稳定依据。
- 错误摘要不得包含 AccessKey、SecretKey、Authorization header、Cookie、真实 `.env`、本机绝对路径、完整堆栈或未脱敏对象路径。

## 接入方案

1. 在上传入口建立或取得当前请求对应的 `task_trace_id`、`request_id` 或等价关联标识。
2. 用单调时钟包裹文件读取、对象存储写入和派生图生成阶段。
3. 每个阶段完成后立即写入 span；失败时在抛出或降级前写入失败 span。
4. 通用图片上传成功路径必须产出六个基础阶段；头像上传至少产出 `file_read` 和 `original_put_object`，并按实际派生策略补齐派生阶段或跳过原因。
5. 维持上传安全校验、对象 key 策略、单 Bucket + 前缀策略和后端鉴权边界。

## 原型与验收冲突报告

`REQ-0123` 仅包含 `prototype/web/context.md`，用于说明本需求默认不新增用户可见 UI。当前 Change 不生成 UI Contract、UI Skeleton 或视觉验收材料；若实现阶段决定在管理端展示 spans，需要先补充 UI 范围说明并遵守 `rules/ui-design.md`。

## 兼容性与边界

- API：默认无响应契约变化；若新增 trace 字段或查询接口，必须同步 OpenAPI、Orval、API 文档和测试。
- 数据库：默认复用既有 Task Trace；如需新增表、JSON 字段或索引，必须同步 SQLite/MySQL schema、数据库文档、迁移与测试。
- Web 管理端：默认无可见 UI 变更。
- 小程序 / 店主 Web：不涉及。
- 对象存储：不新增 Bucket，不改变 key 规则或前端访问边界。

## 验收方式

- 后端单元或集成测试验证头像上传成功路径产生基础 spans。
- 后端单元或集成测试验证通用图片上传成功路径产生六个基础 spans。
- 对象存储写入失败测试验证失败阶段和已完成阶段均保留。
- 派生图生成失败或跳过测试验证 `failed` / `skipped` 状态和错误摘要脱敏。
- 若实现不改 API、DB 或 UI，开发记录必须说明不需要 Orval、迁移和视觉验收的依据。
