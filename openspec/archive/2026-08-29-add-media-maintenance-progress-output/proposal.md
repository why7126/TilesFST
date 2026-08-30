## 背景

生产媒体维护 CLI 已经承担 `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`media-drift-reconcile` 等长耗时批处理任务。现有命令在结束时输出完整 JSON，适合审计归档和脚本解析，但生产 apply 期间缺少过程反馈，运维无法判断任务是否仍在推进、已处理多少对象、失败数量是否持续增加。

REQ-0130 要求在不破坏现有 stdout JSON 契约的前提下，为媒体维护任务提供可选进度输出，优先解决生产执行过程中的“黑盒等待”问题。

## 变更内容

- 为媒体维护 CLI 增加可选 `--progress` 进度输出开关，默认不启用。
- 保持最终任务结果 JSON 输出到 stdout；进度信息输出到 stderr 或等价隔离通道。
- 进度信息至少表达任务名、阶段、总量、已完成、成功、失败、跳过和进度百分比。
- 覆盖 `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`media-drift-reconcile`，其中聚合任务展示阶段级进度。
- 补充生产媒体维护 Runbook 与命令帮助文案，说明 stdout / stderr 边界、示例输出、日志采集和脱敏要求。
- 补充聚焦测试，验证 JSON 兼容、stderr 进度、计数准确性、阶段输出和敏感信息不泄露。

## 能力影响

### 修改能力

- `prod-media-maintenance-jobs`：新增媒体维护作业可选进度输出要求。
- `batch-image-processing-runbook`：新增 Runbook 对进度参数、输出通道和日志采集说明的要求。

## 影响范围

- 后端：涉及媒体维护 CLI 参数、进度报告逻辑和对应测试。
- 文档：涉及生产媒体维护 Runbook 或批量图片处理 Runbook。
- API：不涉及，不新增或修改 HTTP 接口。
- 数据库：不涉及，不新增表、字段、迁移或持久化任务进度。
- Web / 管理端 / 小程序：不涉及，不新增 UI、路由、状态管理或端侧请求封装。
- Orval：不涉及，无 OpenAPI 变更。
- Docker Compose：不涉及 compose 配置变更；生产验证仍可通过现有 docker-compose exec 命令执行。
- 对象存储：不改变对象 key、派生图生成策略、备份确认门禁或写入策略。

## 产品数据采集与链路观测

`product_data_collection_observability` 判定为不适用。本变更仅增加本地 CLI 进度输出，不新增 API、DB、请求日志、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。

若后续实现改为持久化任务进度、写入任务追踪表、接入请求日志或对外暴露任务状态接口，必须重新评估 affected layers、脱敏边界、保留周期和验证项。
