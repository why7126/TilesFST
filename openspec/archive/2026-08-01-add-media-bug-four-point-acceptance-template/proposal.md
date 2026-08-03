## Why

媒体类 BUG 近几个 Sprint 连续暴露出“对象存在但端侧不可用”“缩略图名义存在但收益缺失”“小程序 evidence 滞后”等验收缺口。REQ-0091 已评审通过，需要将媒体类 BUG 修复后的 `key`、`object`、`URL`、`render` 四联验收固化为 OpenSpec 变更，避免后续缺陷只修 UI 表象或只验证单一链路节点。

## What Changes

- 新增媒体类 BUG 四联验收模板要求，覆盖原 BUG 场景、`key`、`object`、`URL`、`render`、证据状态和失败/阻塞处理。
- 明确四联验收适用于媒体类 BUG 修复、返修、回归测试、Sprint 验收和发布前检查。
- 将知识库中媒体上传链路 gate 转化为可测试要求：上传状态机、同会话即时回显、Docker Web `:3000` 边界文件、`object_key` 与受控媒体 URL 一致性。
- 明确模板不得泄露真实客户数据、密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或 MinIO 凭证。
- 明确后续实现只沉淀模板和治理文档，不新增上传接口、对象存储能力、缩略图/转码能力或源码行为。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `object-storage`: 补充媒体类 BUG 四联验收模板要求，要求媒体缺陷修复必须同时记录对象 key、对象存在性、受控 URL 可访问性和端侧渲染 evidence。

## Impact

- Backend / API: 本 Change 本身不新增或修改接口；若后续实现选择自动化检查或脚本化审计，必须另行同步 API、Pydantic Schema、OpenAPI、Orval 和测试。
- Web / Admin / Miniapp: 本 Change 本身不新增 UI；若模板落入 Web 管理端或发布工具 UI，必须遵守 Design System semantic token 和媒体上传 best practice。
- Object Storage / MinIO: 影响媒体类 BUG 的验收治理口径；要求继续遵守单桶策略、标准前缀、后端受控读取和安全输出。
- Database: 默认无数据库结构变化。
- Docs / Rules: 后续 `/opsx-apply` 应将模板沉淀到 `rules/media.md`、`rules/object-storage.md`、`docs/standards`、`docs/knowledge-base` 或 BUG acceptance 模板中的一个或多个位置。
- Tests: 默认至少需要文档/模板结构校验或人工验收记录；若新增脚本、自动化检查或 UI，必须补充对应 pytest/Vitest/CI 验证。
