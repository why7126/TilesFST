## 1. 模板文档

- [x] 1.1 新增 XL 管理端页面分层验收模板长期文档，优先放入 `docs/standards/`。
- [x] 1.2 在模板中定义 DB、API、上传、Orval、Web、Docker、横切 UI 七层 gate。
- [x] 1.3 为每层 gate 提供 status、owner、evidence、N/A reason、remaining risk 字段。
- [x] 1.4 在模板中加入摘要化证据规则，禁止复制完整 OpenAPI、Orval 生成物、大段测试日志、密钥、真实环境变量或本机绝对路径。

## 2. 横切 UI 与知识库引用

- [x] 2.1 将 admin-list、admin-form、admin-modal、media-upload best-practices 转化为模板中的横切 UI gate。
- [x] 2.2 在模板中要求后续 Change design 引用 `knowledge_base_refs` 并说明落实或 N/A。
- [x] 2.3 确认模板保留 N/A 机制，避免无上传、无 API 或无 Docker 变更的页面被迫执行无关 gate。

## 3. OpenSpec 与追溯

- [x] 3.1 确认 `xl-admin-page-acceptance-template` delta spec 覆盖模板结构、gate 标准、横切 UI 引用和沉淀位置。
- [x] 3.2 更新 Change trace，记录 REQ-0039、知识库引用、prototype 状态和 N/A 决策。
- [x] 3.3 更新 REQ-0039 trace 中的 OpenSpec Change 追溯状态。

## 4. 验证

- [x] 4.1 运行 OpenSpec 校验并修复格式或场景层级问题。
- [x] 4.2 复核本 Change 未修改 `src/`、DB/API、上传、Orval、Docker Compose 或小程序代码。
- [x] 4.3 记录无需 Orval、无需 Docker Compose 验证的原因；若实现阶段触及运行时代码，必须回到 Change 范围确认。
