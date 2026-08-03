## Why

媒体链路已经跨越上传、对象存储、受控 URL、缩略图派生和小程序渲染，但后续 REQ、BUG、Sprint 和 Release 验收缺少统一模板，容易只验证“对象存在”而遗漏 URL 可访问、缩略图收益或端上渲染。REQ-0090 已从 Sprint 016 媒体链路复盘中沉淀出五联检查项，需要将其纳入 OpenSpec 能力，形成可复用的长期验收规范。

## What Changes

- 新增“媒体五联验收模板”能力，覆盖 `key`、`object`、`URL`、`thumbnail benefit`、`miniapp render` 五个维度。
- 定义模板适用范围：媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布前检查。
- 定义模板记录结构：媒体样例、业务资源、五联状态、证据、失败原因、N/A 理由和 blocked 处理。
- 定义失败项转 BUG 的最小信息要求，保证五联验收失败可追踪、可复现。
- 明确媒体上传横切 gate：上传状态机、同会话即时回显、Docker `http://localhost:3000` 边界文件验收和失败信息位置。
- 明确该 Change 不新增上传接口、缩略图生成流水线、视频转码能力、对象存储架构或运行时 UI。

## Capabilities

### New Capabilities

- `media-acceptance-template`: 定义媒体五联验收模板、适用场景、证据格式、横切 gate 和后续引用方式。

### Modified Capabilities

无。

## Impact

- 影响 OpenSpec 规范：新增 `media-acceptance-template` capability。
- 影响文档治理：实现阶段需将模板沉淀到长期文档或等价模板位置，并在 trace/design 中说明最终落点。
- 影响测试/验收：后续媒体类需求、BUG、Sprint 或 Release 应引用五联模板记录验收证据。
- 不直接影响后端 API、数据库 schema、Orval、Web 管理端运行时、小程序运行时或对象存储实现。
