---
review_id: REV-REQ-0131-001
requirement_id: REQ-0131-media-object-key-business-id-layout
date: 2026-08-29
participants:
  - product
  - ai
result: approved
created_at: 2026-08-29 19:30:52
updated_at: 2026-08-29 19:30:52
---

# 需求评审

## 评审结论

REQ-0131 评审通过，允许进入 Sprint 规划。

本需求的目标、范围、旧媒体兼容要求、迁移模式、对象存储规范落地和横切观测门禁均已明确。当前 readiness 为 Partially Ready，原因是关联的 media-upload best-practice 仍为 draft，且本需求不新增 UI 原型 PNG；该状态不阻塞进入 Sprint，但后续 OpenSpec Change 必须补齐实现设计、迁移验证和文档同步证据。

## 检查结果

| 检查项 | 结论 | 说明 |
|---|---|---|
| 目标与范围 | 通过 | 统一所有媒体对象 Key 按业务对象 id 分目录，覆盖新上传、暂存、正式化、旧 key 兼容、迁移和规范文档。 |
| 验收标准 | 通过 | acceptance.md 已覆盖 Key 矩阵、旧媒体显示、迁移 dry-run、执行、二次审计、回滚、派生图和端侧禁止拼接 URL。 |
| 影响边界 | 通过 | 明确涉及后端上传/媒体服务、数据库引用、管理端/店主端/小程序消费策略、对象存储与维护任务。 |
| 产品数据采集与链路观测 | 通过 | 已声明 request_logs、task_traces、task_trace_spans、backend_api、端侧请求链路和 maintenance_jobs 适用。 |
| 安全与合规 | 通过 | 要求后端鉴权、受控媒体 URL、禁止 raw URL、禁止对象 Key 泄露原始文件名或本机路径。 |
| 知识库引用 | 通过 | 已引用 media-upload best-practice 与 sprint-025/sprint-026 媒体复盘。 |

## 评审约束

- 后续 Change 必须保留旧数据库引用的读取兼容，不得要求前端或小程序根据新目录自行推导路径。
- 存量迁移必须支持 dry-run、apply、audit、失败分类、备份引用与回滚，避免一次性全量迁移带来不可控风险。
- 若引入媒体别名表、迁移状态表或修改既有字段，必须同步 SQLite/MySQL schema、数据库文档和测试。
- 若上传或媒体读取接口响应字段变化，必须同步 OpenAPI、Orval、API 文档和端侧调用测试。
- 对象存储与媒体规范文档必须作为本需求的验收产物之一，不能只停留在代码实现。

## 后续动作

建议纳入当前规划中的 `sprint-027`，再执行 `/req-opsx REQ-0131-media-object-key-business-id-layout` 创建 OpenSpec Change。
