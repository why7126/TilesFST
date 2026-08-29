---
requirement_id: REQ-0123-upload-stage-trace-spans
title: 上传链路阶段级耗时写入 trace spans - 验收标准
acceptance_status: passed
owner: product
source: requirement.md
created_at: 2026-08-25 18:43:20
updated_at: 2026-08-28 16:21:48
---

# 验收标准

## 功能 AC

- [ ] AC-001 头像上传成功路径可以定位同一次上传的 task trace spans，且至少包含 `file_read` 与 `original_put_object`。
- [ ] AC-002 通用图片上传成功路径必须包含 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六个基础阶段。
- [ ] AC-003 每个 span 至少包含阶段名、耗时毫秒值、成功/失败/跳过状态；如 task trace 支持时间戳，应记录开始和结束时间。
- [ ] AC-004 原图写入失败时，trace 能保留 `file_read` 成功记录和 `original_put_object` 失败记录。
- [ ] AC-005 thumbnail 或 display 生成失败时，trace 能记录对应 `*_generate` 失败，并能判断后续 `*_put_object` 是跳过、未执行还是失败。
- [ ] AC-006 对 SVG、PDF 或不适用派生图的格式，trace 中必须有可定位的跳过状态、错误状态或 OpenSpec 中明确的 N/A 说明。
- [ ] AC-007 日志可以输出阶段耗时摘要，但验收证据必须来自 task trace spans 或等价结构化任务追踪事实源。
- [ ] AC-008 记录 spans 不得绕过上传鉴权、文件大小、MIME Type、扩展名校验和对象 key 安全规则。
- [ ] AC-009 错误摘要和 metadata 必须脱敏，不包含真实 `.env`、AccessKey、SecretKey、Authorization header、Cookie、本机绝对路径或完整内部对象路径。
- [ ] AC-010 若上传响应、任务查询响应或管理端展示新增 trace 信息，必须同步 OpenAPI、Orval、API 文档和前后端测试；若不暴露 API，需在实现记录中说明不需要 Orval。
- [ ] AC-011 若新增 task trace 存储结构，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试；若复用现有结构，需在实现记录中说明不涉及 DB 变更。
- [ ] AC-012 自动化测试覆盖头像上传与通用图片上传两条分支，至少验证阶段名称集合、耗时字段存在和失败阶段保留。
- [ ] AC-013 后续实现验收需记录媒体证据五元组中的相关项：key、object、URL、render/Network、耗时或瓶颈收益；不适用项需说明原因。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 上传控件或调用方状态机必须可验证 `idle -> uploading -> done/failed`；如果本期无新增可见上传控件，需在实现记录中标注 `N/A — 本需求仅补后端 trace spans，沿用既有上传 UI`。
- [ ] AC-XCUT-002 同会话上传成功后的媒体回显不能因 trace spans 接入而退化；头像或通用图片上传后仍应在当前会话可见，若本期不触达 UI，需用现有回归测试或人工验收说明 `N/A — UI 未变更`。
- [ ] AC-XCUT-003 涉及上传边界、Nginx 或 Docker Web 路径时，必须从 `http://localhost:3000` 用户入口验证边界文件，不能只调用后端 `:8000`；若本期不改上传大小或 Nginx 配置，记录 `N/A — 未改边界配置`。
- [ ] AC-XCUT-004 `object_key` 与 `/media/{object_key}` 代理读取必须保持一致；trace span metadata 不得替代 key/object/URL 验收，也不得将 `data/uploads/` 作为新上传通过证据。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 23:07:39
accepted_by: workflow-sync
source_change: add-upload-stage-trace-spans
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

