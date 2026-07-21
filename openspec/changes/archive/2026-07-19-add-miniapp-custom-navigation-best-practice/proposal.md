## Why

Sprint 008 已完成小程序全局自定义导航栏，但状态栏、微信原生胶囊、返回兜底、页面 offset 和截图验收矩阵仍主要沉淀在单次需求、验收和复盘记录中。后续小程序页面继续演进时，需要一份可复用 best-practice，避免新页面重复手写导航规则、把 DevTools 预览误写成真机通过，或让 fixed header 遮挡风险重新出现。

## What Changes

- 新增小程序自定义导航 best-practice，定义适用范围、首页/非首页导航结构、状态栏和胶囊数据来源、fallback、返回兜底、页面 offset 和页面接入 checklist。
- 新增截图验收矩阵，覆盖页面、入口、DevTools 视口、真机类型、页面状态和结论字段，并复用 `miniapp_device_evidence` 的 evidence 状态与安全边界。
- 要求后续涉及小程序自定义导航、fixed header、分享、返回或页面顶部布局的 REQ / Change 引用该 best-practice，若不适用必须记录豁免原因。
- 约定文档优先沉淀到 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，并在 Sprint 验收报告中只引用矩阵摘要、blocked 和 follow_up，不复制完整 evidence。
- 不新增小程序业务页面，不直接重构 `src/miniapp/components/custom-navigation/`，不新增自动化截图工具链，不修改 API、数据库、Orval、Docker Compose、MinIO 或对象存储。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-global-custom-navigation-bar`: 增加自定义导航 best-practice、页面接入 checklist、截图验收矩阵和后续流程引用规则。

## Impact

- 后端：无运行时代码、API、权限或上传链路变更。
- Web / 管理端：无运行时代码变更。
- 小程序：无页面、组件、样式、服务或配置变更；后续 Change 可引用该 best-practice 指导导航接入与验收。
- 数据库 / 存储 / Orval / Docker：无变更。
- 文档：实现阶段新增 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，并按需更新知识库索引。
- 测试：实现阶段至少补充文档存在性、关键章节和敏感信息边界的轻量校验。
