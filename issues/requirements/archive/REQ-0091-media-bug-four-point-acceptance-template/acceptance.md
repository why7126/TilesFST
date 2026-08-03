---
requirement_id: REQ-0091-media-bug-four-point-acceptance-template
title: 媒体类 BUG 四联验收模板 - 验收标准
acceptance_status: passed
created_at: 2026-08-01 09:55:10
updated_at: 2026-08-02 19:32:35
---

# 验收标准

## 功能 AC

- [ ] AC-001 模板必须提供“原 BUG 场景”记录区，包含 BUG 编号、标题、严重等级、影响范围、复现入口、受影响端、环境、修复前实际结果和修复后期望结果。
- [ ] AC-002 模板必须覆盖 `key`、`object`、`URL`、`render` 四个验收维度，且每个维度均支持 `pass`、`fail`、`n/a`、`blocked` 状态。
- [ ] AC-003 `key` 验收必须要求记录媒体类型、业务资源、对象 key 或脱敏对象标识，并确认 key 稳定、可追溯、符合 MinIO 单桶前缀策略。
- [ ] AC-004 `key` 验收必须明确禁止使用用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径作为对象存储 key。
- [ ] AC-005 `object` 验收必须确认对象存储中真实 object 存在，并记录 MIME Type、文件大小、扩展名、权限边界和对象可读性检查结果。
- [ ] AC-006 `object` 验收失败时必须能记录对象不存在、大小为 0、类型不匹配、权限错误或存储环境不可用等失败原因。
- [ ] AC-007 `URL` 验收必须区分相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL，并记录页面/接口入口、HTTP 状态、业务错误码和用户可见表现。
- [ ] AC-008 `URL` 验收必须确认前端不得直连未授权对象存储，媒体访问遵循后端鉴权、代理或签名 URL 策略。
- [ ] AC-009 `render` 验收必须覆盖受影响端的媒体展示、占位、失败态和用户可见行为；涉及微信小程序时必须记录合法域名、组件限制和不依赖 Web 浏览器专属 API。
- [ ] AC-010 若某端或某维度不适用，模板必须要求记录 `n/a` 原因和影响判断，不允许留空。
- [ ] AC-011 若验收被阻塞，模板必须要求记录 `blocked` 原因、缺失资源、环境限制、负责人或下一步补证方式。
- [ ] AC-012 任一 `fail` 记录必须包含实际结果、期望结果、复现步骤、影响范围和排查线索，可直接支撑原 BUG 返修或后续 `/bug-capture`。
- [ ] AC-013 模板不得记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。
- [ ] AC-014 后续 `/req-opsx` 必须明确模板最终落点，并说明是否沉淀到 `rules/media.md`、`rules/object-storage.md`、`docs/standards`、`docs/knowledge-base` 或 BUG acceptance 模板。
- [ ] AC-015 若模板接入 Sprint 或 Release 检查流程，必须明确哪些媒体类 BUG 触发四联验收，以及哪些 evidence 可作为发布前补证项。

## 模板草案

```markdown
## 媒体类 BUG 四联验收

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-xxxx |
| 严重等级 | P0 / P1 / P2 |
| 影响范围 | Web 管理端 / 店主 Web / 小程序 / 后端接口 |
| 复现入口 | 页面、接口或操作路径 |
| 环境 | local / test / miniapp trial / prod |
| 修复前实际结果 |  |
| 修复后期望结果 |  |

### 四联检查

| 维度 | 状态 | 证据 | 失败/阻塞处理 |
|---|---|---|---|
| key | pass / fail / n/a / blocked | 媒体类型、业务资源、object_key、前缀策略 |  |
| object | pass / fail / n/a / blocked | object 存在性、MIME、大小、权限 |  |
| URL | pass / fail / n/a / blocked | URL 类型、HTTP 状态、业务错误码、入口 |  |
| render | pass / fail / n/a / blocked | 端、页面/组件、截图/日志、失败态 |  |
```

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002 媒体上传链路复发类缺陷；结合 `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` 与 `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` 的媒体链路复盘。

- [ ] AC-XCUT-001 模板必须要求涉及上传的媒体类 BUG 记录上传状态机 evidence，覆盖 `idle → uploading → done/failed`，失败必须在上传控件或验收记录中可定位。
- [ ] AC-XCUT-002 模板必须要求同会话即时回显 evidence；涉及 Web 管理端上传/编辑/列表刷新时，不能只记录重新打开页面后的结果。
- [ ] AC-XCUT-003 模板必须要求涉及上传边界的 BUG 通过 Docker Web `http://localhost:3000` 验证边界文件；若不涉及上传边界，记录 `N/A — 本 BUG 不涉及文件大小、Nginx 或上传入口`。
- [ ] AC-XCUT-004 模板必须要求媒体读取链路验证 `object_key` 与 `/media/` 代理或等价受控 URL 一致，禁止只验证对象存储存在而不验证端侧 URL。
- [ ] AC-XCUT-005 模板必须要求涉及历史对象、缩略图、回填或审计脚本的 BUG 记录 dry-run/apply/统计摘要，且输出不得泄露本机路径、密钥或真实客户数据。
- [ ] AC-XCUT-006 模板必须要求小程序媒体 BUG 记录 DevTools、真机或体验版 evidence；若无法补证，必须进入 Release 前检查清单，不得写作真机通过。

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 acceptance 的 AC 条数 |
|---|---|---:|
| media-upload | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 6 |
| media-retrospective | `docs/knowledge-base/retrospectives/sprint-015-retrospective.md`、`docs/knowledge-base/retrospectives/sprint-016-retrospective.md` | 2 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: add-media-bug-four-point-acceptance-template
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

