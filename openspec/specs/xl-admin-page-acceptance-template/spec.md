# xl-admin-page-acceptance-template Specification

## Purpose
TBD - created by archiving change add-xl-admin-page-acceptance-template. Update Purpose after archive.
## Requirements
### Requirement: XL 管理端页面分层验收模板

系统 MUST 提供一套可复用的 XL 管理端页面分层验收模板，用于后续复杂管理端页面在需求、OpenSpec、实现和验收阶段统一记录 DB、API、上传、Orval、Web、Docker 与横切 UI gate 的状态、证据、N/A 理由和剩余风险。

#### Scenario: 模板包含七层 gate

- **WHEN** 团队为复杂 Web 管理端页面创建或引用验收模板
- **THEN** 模板 MUST 包含 DB、API、上传、Orval、Web、Docker 和横切 UI 七层 gate
- **AND** 每层 gate MUST 支持 `required`、`not_applicable`、`passed`、`failed`、`blocked` 或等价状态
- **AND** 每层 gate MUST 支持 owner、evidence、N/A reason、remaining risk 或等价字段

#### Scenario: N/A 必须有理由

- **WHEN** 某个复杂管理端页面将任一 gate 标记为不适用
- **THEN** 模板 MUST 要求记录具体 N/A 理由
- **AND** 理由 MUST 说明不涉及该层的事实，例如不新增 API contract、不含上传控件或不修改 Docker/Nginx 配置

#### Scenario: 验收证据保持摘要化

- **WHEN** 后续 Change 使用模板记录 gate 证据
- **THEN** 证据 MUST 使用命令摘要、测试结果摘要、截图路径、接口响应摘要或 Docker 验证摘要
- **AND** 证据 MUST NOT 复制完整 OpenAPI、Orval 生成物、大段测试日志、密钥、真实环境变量或本机绝对路径

### Requirement: DB API 上传 Orval Web Docker gate 标准

系统 MUST 在 XL 管理端页面分层验收模板中定义 DB、API、上传、Orval、Web 和 Docker gate 的标准检查范围，使后续页面能够按层确认 required 或 N/A。

#### Scenario: DB gate 覆盖数据模型边界

- **WHEN** 模板使用者检查 DB gate
- **THEN** DB gate MUST 覆盖表结构、迁移、SQLite/MySQL 差异、Pydantic Schema、Repository/Service、数据库文档和测试

#### Scenario: API gate 覆盖接口契约

- **WHEN** 模板使用者检查 API gate
- **THEN** API gate MUST 覆盖接口路径、方法、权限、请求、响应、统一 envelope、错误码、OpenAPI、接口文档和集成测试

#### Scenario: 上传 gate 覆盖媒体链路

- **WHEN** 模板使用者检查上传 gate
- **THEN** 上传 gate MUST 覆盖后端授权上传、MIME/大小限制、对象 key、MinIO 单桶前缀、失败态、即时回显和 Nginx/Docker 边界

#### Scenario: Orval gate 覆盖生成客户端判定

- **WHEN** 模板使用者检查 Orval gate
- **THEN** Orval gate MUST 要求 API contract 变化时导出 OpenAPI 并运行 Orval
- **AND** 无 API contract 变化时 MUST 记录 Orval N/A 理由

#### Scenario: Web 和 Docker gate 覆盖运行环境

- **WHEN** 模板使用者检查 Web 和 Docker gate
- **THEN** Web gate MUST 覆盖管理端路由、权限、列表、筛选、表格、分页、表单、弹窗、抽屉、loading/empty/error 和前端测试
- **AND** Docker gate MUST 覆盖 compose、Dockerfile、Nginx、环境变量、MinIO、Web 代理和 `localhost:3000` 入口验证判定

### Requirement: 横切 UI gate 知识库引用

系统 MUST 在 XL 管理端页面分层验收模板中保留横切 UI gate，并要求引用管理端列表、表单、弹窗和媒体上传最佳实践，防止已知复发类缺陷回归。

#### Scenario: 横切 UI gate 引用知识库

- **WHEN** 模板或后续 Change 记录横切 UI gate
- **THEN** trace、design 或验收材料 MUST 引用适用的 `knowledge_base_refs`
- **AND** 引用范围 MUST 覆盖命中的 admin-list、admin-form、admin-modal、media-upload 标签

#### Scenario: 横切 UI gate 转为可测试 AC

- **WHEN** 后续复杂管理端页面引用模板
- **THEN** 横切 UI gate MUST 至少检查 semantic token、DS modal、fixed toast、无裸 Hex、无 layout shift、移动或窄屏关键视口
- **AND** 与页面无关的横切项 MUST 标记 N/A 并说明原因，而不是删除整节

#### Scenario: 后续 design 说明落实或 N/A

- **WHEN** 后续 `/req-opsx` 为复杂管理端页面生成 Change design
- **THEN** design MUST 说明每个适用横切标签如何落实或 N/A
- **AND** 不得仅引用 best-practices 文件而缺少页面级判定

### Requirement: 模板沉淀位置与引用方式

系统 MUST 将 XL 管理端页面分层验收模板沉淀到长期治理文档或等价模板位置，并保证后续需求、OpenSpec Change 和验收报告可以稳定引用。

#### Scenario: 标准文档存在

- **WHEN** 本 Change 实现完成
- **THEN** 仓库 MUST 存在长期模板文档或等价模板
- **AND** 文档 SHOULD 位于 `docs/standards/`，若不在该目录 MUST 在 Change trace 或 design 中说明替代位置

#### Scenario: 后续需求引用模板

- **WHEN** 后续复杂管理端页面需求生成 acceptance、OpenSpec tasks 或验收报告
- **THEN** 这些材料 SHOULD 引用 XL 管理端页面分层验收模板
- **AND** 使用者 MUST 按 gate 逐层记录 required、N/A、证据和剩余风险

