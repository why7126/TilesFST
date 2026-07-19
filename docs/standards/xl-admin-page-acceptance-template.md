---
purpose: XL 管理端页面分层验收模板
content: DB、API、上传、Orval、Web、Docker、横切 UI 七层 gate 与证据记录规范
source: REQ-0039-xl-admin-page-layered-acceptance-template / add-xl-admin-page-acceptance-template
update_method: 复杂管理端页面验收口径、横切 UI best-practices 或证据规则变化时同步更新
created_at: 2026-07-16 09:24:12
updated_at: 2026-07-16 09:24:12
---

# XL 管理端页面分层验收模板

## 1. 适用范围

本文档用于字段多、链路长、可能跨 DB、API、上传、Orval、Web、Docker 与横切 UI 多层的复杂管理端页面。后续 REQ `acceptance.md`、OpenSpec Change `design.md` / `tasks.md`、Sprint 验收报告或 Change trace 可引用本模板，并按页面实际范围逐层记录 required 或 N/A。

本模板不要求轻量页面执行无关 gate。任一 gate 标记 `not_applicable` 时，必须写明具体事实，例如“不新增 API contract”“页面不含上传控件”“不修改 Docker/Nginx 配置”。

## 2. 状态与字段

Gate 状态统一使用：

| 状态 | 含义 |
|---|---|
| `required` | 已识别为本 Change 必须覆盖，尚未完成验收 |
| `not_applicable` | 不适用于当前页面，必须填写 N/A reason |
| `passed` | 已完成验收并有摘要证据 |
| `failed` | 已验收失败，必须记录后续处理 |
| `blocked` | 因外部依赖或范围冲突暂无法验收 |

每层 gate 必须至少记录：

| 字段 | 要求 |
|---|---|
| `status` | 使用上方状态之一 |
| `owner` | 负责补齐或验收该层的人或角色 |
| `evidence` | 命令摘要、测试结果摘要、截图路径、接口响应摘要或 Docker 验证摘要 |
| `na_reason` | 仅 `not_applicable` 时填写，不得留空 |
| `remaining_risk` | 已知剩余风险；无风险写“无” |

## 3. 七层 Gate 矩阵

| Gate | Required 判定 | 标准检查范围 | N/A 示例 |
|---|---|---|---|
| DB | 新增或修改持久化字段、表、查询、状态流转或服务层模型 | 表结构、迁移、SQLite/MySQL 差异、Pydantic Schema、Repository/Service、数据库文档、数据库相关测试 | `not_applicable` — 仅新增文档或纯前端展示，不涉及持久化模型 |
| API | 新增或修改接口路径、请求、响应、权限、错误码或分页/筛选契约 | 路径、方法、权限、请求、响应、统一 envelope、错误码、OpenAPI、接口文档、集成测试 | `not_applicable` — 不新增或修改 API contract |
| 上传 | 页面含图片、视频、Logo、头像、文件等上传或媒体读取链路 | 后端授权上传、MIME/大小限制、对象 key、MinIO 单桶前缀、失败态、即时回显、Nginx/Docker 边界 | `not_applicable` — 页面不含上传控件或上传链路 |
| Orval | API contract 变化会影响 Web 客户端类型或调用函数 | 导出 OpenAPI、运行 Orval、复核生成客户端引用、避免手写重复类型 | `not_applicable` — 无 API contract 变化，无需重新生成客户端 |
| Web | 新增或修改管理端页面、路由、交互、状态或可视验收 | 路由、权限、列表、筛选、表格、分页、表单、弹窗、抽屉、loading/empty/error、前端测试、桌面与窄屏视口 | `not_applicable` — 仅后端治理或文档变更，不改 Web 源码 |
| Docker | 变更影响本地/Docker 运行、Nginx、环境变量、代理或对象存储边界 | compose、Dockerfile、Nginx、环境变量、MinIO、Web 代理、`http://localhost:3000` 入口验证 | `not_applicable` — 不改运行环境、代理、上传大小或部署配置 |
| 横切 UI | 命中管理端列表、表单、弹窗、媒体上传或复杂工作台页面模式 | semantic token、DS modal、fixed toast、无裸 Hex、无 layout shift、桌面与窄屏关键视口、命中标签的知识库检查项 | `not_applicable` — 非 UI Change 或不涉及对应横切标签 |

## 4. 横切 UI Gate

后续复杂管理端页面的 `design.md` 或验收材料必须声明 `knowledge_base_refs`，并对命中的标签说明落实或 N/A。不得只列文件名而缺少页面级判定。

推荐引用：

| 标签 | 知识库引用 | 模板检查项 |
|---|---|---|
| `admin-list` | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 分页 DOM 对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数；摘要指标卡使用 `.metric-label` / `.metric-value` / `.metric-desc` 或等价共享结构；操作反馈使用 fixed toast；状态/危险操作使用 DS confirm modal 且无 `window.confirm` |
| `admin-form` | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 全页仅一个主要保存 CTA，位于表单 footer 或等价固定操作区；页头不重复渲染保存按钮；恢复默认、dirty Tab 切换、取消修改等风险操作使用 DS modal；保存反馈使用 fixed toast，不在 summary 与主表单之间插入造成 layout shift 的块级提示 |
| `admin-modal` | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 业务弹窗 TSX className 不得同时挂载通用 `modal-card` 与专属类；宽/窄弹窗验收 computed width 或等价运行时宽度；矮视口下 body 可滚动，关闭按钮与底部主操作可访问 |
| `media-upload` | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 上传控件覆盖 `idle -> uploading -> done / failed` 状态机；同会话上传成功后即时回显缩略图、文件卡片或可访问 URL；上传失败信息展示在控件附近或字段组内；含上传能力的 Change 通过 Docker Web `http://localhost:3000` 验证边界文件 |

横切 UI gate 还必须检查：

- 使用 Design System semantic token，禁止新增裸 Hex。
- 危险确认使用 DS modal 或等价共享组件，禁止 `window.confirm` / `window.alert`。
- 成功/失败反馈采用 fixed toast 或固定反馈区域，不造成 hero、筛选区、表格或主表单 layout shift。
- 至少记录桌面视口和一个窄屏/移动视口的 UI 验收策略；具体视口按页面风险扩展。

## 5. 证据摘要规则

证据只记录可复核摘要，避免把生成物或敏感信息写入验收材料。

允许记录：

- 命令与结果摘要，例如 `pnpm test -- AdminPage.test.tsx` 通过。
- 测试失败的关键用例、断言和相关文件片段。
- 截图或报告的仓库相对路径。
- 接口请求/响应字段摘要、错误码摘要和权限判定摘要。
- Docker 验证入口、边界文件类型/大小和结果摘要。

禁止记录：

- 完整 OpenAPI JSON、完整 Orval generated 文件或大段测试日志。
- 密钥、token、Authorization header、真实环境变量值、数据库 DSN、MinIO 凭据。
- 本机绝对路径、真实客户数据、运行时数据库文件。

## 6. 可复制记录模板

```yaml
xl_admin_page_acceptance:
  template_ref: docs/standards/xl-admin-page-acceptance-template.md
  page_or_change: "<page-or-change-id>"
  knowledge_base_refs:
    - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  gates:
    db:
      status: not_applicable
      owner: backend
      evidence: "无 DB 变更；未新增表、迁移、Repository 或 Pydantic Schema"
      na_reason: "仅新增管理端静态模板文档，不涉及持久化模型"
      remaining_risk: "无"
    api:
      status: not_applicable
      owner: backend
      evidence: "未新增或修改 API contract"
      na_reason: "无接口路径、请求、响应、权限或错误码变化"
      remaining_risk: "无"
    upload:
      status: not_applicable
      owner: fullstack
      evidence: "页面不含上传控件或媒体读取链路"
      na_reason: "无图片、视频、Logo、头像或文件上传能力"
      remaining_risk: "无"
    orval:
      status: not_applicable
      owner: frontend
      evidence: "无 API contract 变化，因此未导出 OpenAPI 或运行 Orval"
      na_reason: "不影响 Web API 客户端类型"
      remaining_risk: "无"
    web:
      status: required
      owner: frontend
      evidence: "Vitest/Playwright/截图摘要待补"
      na_reason: ""
      remaining_risk: "待完成 UI 验收"
    docker:
      status: not_applicable
      owner: devops
      evidence: "未修改 compose、Dockerfile、Nginx、环境变量或代理"
      na_reason: "不影响运行环境"
      remaining_risk: "无"
    cross_cutting_ui:
      status: required
      owner: frontend
      evidence: "admin-list/admin-form/admin-modal/media-upload 标签落实或 N/A 摘要待补"
      na_reason: ""
      remaining_risk: "待完成横切 UI 检查"
```

## 7. 范围变化处理

如果实现阶段发现某层 gate 从 `not_applicable` 变为 `required`，必须回到 REQ、OpenSpec Change 或 Sprint 范围确认，并补齐对应 docs、tests、OpenAPI/Orval、DB 或 Docker 验证。不得在 `/opsx-apply` 中悄悄扩大范围。
