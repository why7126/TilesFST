## Context

REQ-0090 已完成 capture、generate、complete 和 review，状态为 `approved`。需求目标是建立一套媒体五联验收模板，覆盖 `key`、`object`、`URL`、`thumbnail benefit` 与 `miniapp render`。它来源于 Sprint 016 媒体链路复盘：媒体类验收不能只确认对象存在，还要覆盖对象路径、URL 可访问、缩略图真实收益和小程序渲染。

当前相关能力边界：

- `object-storage` 已定义 MinIO 单桶、对象 Key、受控读取和缩略图生成规则。
- `xl-admin-page-acceptance-template` 已定义复杂管理端页面的分层验收模板，其中上传 gate 覆盖媒体链路，但它面向复杂管理端页面，不适合直接作为所有媒体类 REQ/BUG/Release 的通用模板。
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 提供上传链路横切 gate。
- `issues/requirements/archive/REQ-0090-media-five-point-acceptance-template/acceptance.md` 已给出五联模板样例与 AC-XCUT。

## Goals / Non-Goals

**Goals:**

- 新增 `media-acceptance-template` OpenSpec capability。
- 将五联维度定义为后续媒体类验收的稳定契约。
- 明确每个媒体样例的状态、证据、N/A 理由、blocked 原因和失败转 BUG 信息。
- 明确媒体上传横切 gate 的复用方式。
- 明确实现阶段需要沉淀长期模板文档或等价模板位置。

**Non-Goals:**

- 不新增上传接口、媒体上传组件或管理端页面。
- 不新增缩略图生成、裁剪、压缩、多规格图片或视频转码能力。
- 不修改对象存储架构、MinIO bucket 策略、API 契约、数据库 schema 或 Orval。
- 不强制实现自动化脚本；若后续需要自动化五联检查，应另行明确脚本、CI 或 API 范围。

## Decisions

### D1 新增独立 capability，而不是修改 object-storage

选择新增 `media-acceptance-template`。`object-storage` 是存储与受控读取能力，五联模板覆盖验收治理、发布检查、BUG 复现和小程序端证据，不应混入对象存储运行时规格。

备选方案是修改 `object-storage`，但会把验收模板与存储行为绑定过紧，也无法自然覆盖 Sprint/Release/BUG 的模板引用方式。

### D2 模板长期落点：`docs/standards/media-five-point-acceptance-template.md`

本 Change 的长期模板文档落点为 `docs/standards/media-five-point-acceptance-template.md`。选择 `docs/standards/` 是因为该目录已经承载上传规范、小程序 evidence 模板和页面验收模板，适合被后续 REQ、BUG、OpenSpec Change、Sprint 和 Release 稳定引用。

不将模板并入 `rules/media.md` 或 `object-storage` 正式运行时规格，是为了避免把验收治理口径误读为上传、缩略图、视频转码或对象存储实现变更。

### D3 原型冲突处理

`prototype/web/context.md` 明确本需求不新增 Web 管理端、店主端或小程序页面，只保留未来可视化工具的策略。因此本 Change 不触发 UI Explore Gate，也不要求 HTML/PNG 原型。若后续实现可视化工具，必须另行补 UI 原型并遵守 `rules/ui-design.md`。

优先级判断：`prototype/web/context.md` 与 `acceptance.md` 一致，均说明“不新增运行时 UI”；不存在 HTML/PNG 与 acceptance 冲突。

### D4 横切 gate 只转为可测试检查项，不复制知识库正文

`docs/knowledge-base/best-practices/admin-media-upload-chain.md` 中的上传状态机、即时回显、Docker `:3000` 验收和失败信息位置，将在 spec 中表达为模板使用要求。Change design 和 trace 引用知识库路径，不复制整份最佳实践正文。

## Risks / Trade-offs

- [Risk] 模板过重导致每次媒体变更都难以填写。  
  Mitigation: 模板按媒体样例记录，允许 `n/a`，但必须填写理由。

- [Risk] 模板仅被文档化，后续媒体变更忘记引用。  
  Mitigation: tasks 要求沉淀长期模板位置，并在实现/归档说明中记录引用方式。

- [Risk] 后续误将模板需求扩展为上传实现或自动化脚本。  
  Mitigation: Non-Goals 和 spec 明确实现边界；自动化必须单独确认范围。

- [Risk] 小程序渲染证据依赖环境，可能被 blocked。  
  Mitigation: 模板支持 `blocked` 状态并要求记录阻塞原因、责任环境和重试条件。

## Migration Plan

本 Change 不涉及运行时数据迁移。实现阶段需要：

1. 新增或更新长期模板文档。
2. 在文档中提供五联样例表和状态说明。
3. 在 Change trace/implementation 中记录最终落点。
4. 验证 OpenSpec spec、REQ trace 与文档引用一致。

## Implementation Record

- 长期模板文档：`docs/standards/media-five-point-acceptance-template.md`
- 文档索引：`docs/README.md`
- 实现记录：`openspec/archive/2026-08-01-add-media-five-point-acceptance-template/implementation.md`
- 运行时边界：无 API、DB、Orval、Web、小程序、管理端运行时或 Docker Compose 变更。

## Open Questions

- 长期模板最终落点是 `docs/standards/`、`rules/media.md`，还是与对象存储文档合并引用？
- 是否在后续 Sprint/Release 工具中增加自动提示“媒体变更需引用五联模板”？
