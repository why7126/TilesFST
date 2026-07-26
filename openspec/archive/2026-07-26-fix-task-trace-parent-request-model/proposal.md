## Why

Task Trace 已能表达一次多节点任务的时间线，但主请求、子请求和 span 之间的追溯关系仍不够强：上传任务的 span 尚未稳定写入 `request_id`，Task Trace 也缺少明确的触发请求字段。排障时会出现“能看到任务，却不能可靠回到发起请求或相关子请求”的断点。

本变更用于补齐 Task Trace 的请求关联模型，让每条任务链路都能从主请求进入任务，也能从任务 span 回到对应请求日志。

## What Changes

- 为 Task Trace 任务摘要补充 `parent_request_id` 语义，优先作为 `task_traces` 或等价任务摘要表的独立字段实现。
- 规范 task span 的 `request_id` 写入策略：有请求上下文的 span 必须写入当前请求 ID，无直接请求上下文的内部节点必须有安全兜底。
- 统一任务型接口用同一个 `task_trace_id` 串联 request logs、usage events、audit logs、Task Trace 和 task spans。
- 管理端日志详情支持从主请求查看关联 Task Trace，并从 Task Trace span 定位对应请求日志。
- 上传场景作为首批验收路径，覆盖图片、视频、文件上传的主请求与 span 关联。
- 不迁移历史数据，但 API 和页面必须兼容历史缺失字段。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `product-usage-logging`: 修改产品使用日志与 Task Trace 规范，补充主请求、子请求、span 的强关联模型。

## Impact

- **Backend / API:** Task Trace service、repository、上传接口、任务型接口、日志详情接口、请求日志与 span 写入上下文。
- **Database:** 可能新增 `task_traces.parent_request_id` 或等价结构化字段；需要 SQLite / MySQL schema 与索引兼容。
- **Web Admin:** 管理端日志详情 Task Trace 分组展示 `parent_request_id` 与 span `request_id`，并支持复制或跳转定位。
- **Storage / Media Upload:** 图片、视频、文件上传作为首批验证场景；仍走后端鉴权和对象存储适配层。
- **OpenAPI / Orval / Docs / Tests:** 任何新增 API 字段和数据模型必须同步 OpenAPI、Orval、数据库文档、API 文档和测试。
