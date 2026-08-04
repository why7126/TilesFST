---
requirement_id: REQ-0096-miniapp-network-panel-release-checklist
acceptance_status: passed
created_at: 2026-08-04 08:42:00
updated_at: 2026-08-04 23:12:32
---

# Acceptance

## 功能 AC

- [ ] AC-001 `/miniapp-prepare` 或等价小程序发布准备输出中，必须明确列出 DevTools Network 验证项。
- [ ] AC-002 `/miniapp-prepare` 或等价小程序发布准备输出中，必须明确列出体验版 Network 验证项。
- [ ] AC-003 DevTools Network checklist 必须要求记录 DevTools 版本、基础库版本、运行策略、`urlCheck`、页面路径、请求域名、HTTP 状态、业务响应状态和资源加载结论。
- [ ] AC-004 体验版 Network checklist 必须要求记录最新体验版入口、重新扫码、生产 API 域名、首页或列表页加载、详情页或媒体资源加载结论。
- [ ] AC-005 DevTools Network 结论必须说明“不等同于体验版或真机网络验收”。
- [ ] AC-006 体验版 Network 缺失时不得写作 `passed`；只能记录为 `blocked`、`follow_up` 或明确的 `not_applicable`。
- [ ] AC-007 Network evidence 状态必须覆盖 `required`、`passed`、`failed`、`blocked`、`not_applicable`、`follow_up`。
- [ ] AC-008 `failed` 记录必须包含失败表现、影响页面、影响范围和后续处理建议。
- [ ] AC-009 `blocked` 记录必须包含账号、设备、体验版、域名、网络、后端服务或外部依赖的阻塞原因与重试条件。
- [ ] AC-010 `follow_up` 记录必须包含剩余风险、责任人和承接方式，不得作为无风险通过。

## 页面与资源 AC

- [ ] AC-011 必验主路径至少覆盖首页、一个列表页和一个详情或媒体资源页面。
- [ ] AC-012 首页 Network 验证必须覆盖首页聚合接口、Banner、推荐商品、静态资源和错误态。
- [ ] AC-013 列表页 Network 验证必须覆盖列表接口、分页请求、空态和网络失败提示。
- [ ] AC-014 SKU 详情或证书详情 Network 验证必须覆盖图片、视频、证书图片或受控媒体 URL 的加载结论。
- [ ] AC-015 发布范围不涉及的页面必须记录 `not_applicable` 原因，不得静默删除检查项。

## 发布阻断 AC

- [ ] AC-016 生产 API smoke 失败时，小程序发布准备必须报告阻断，不得继续输出通过结论。
- [ ] AC-017 DevTools 或体验版实际请求仍指向本地或非预期环境时，必须标记 failed 并阻断发布准备通过。
- [ ] AC-018 关键 API 返回非 2xx HTTP 状态且页面无可接受降级时，必须标记 failed。
- [ ] AC-019 关键业务响应失败且影响首页、列表或详情主路径时，必须标记 failed。
- [ ] AC-020 图片、视频或证书资源域名不合法并导致核心内容不可用时，必须标记 failed 或 blocked。

## 文档与工作流 AC

- [ ] AC-021 后续 OpenSpec Change 必须明确是否扩展 `docs/standards/miniapp-device-evidence-template.md`，或仅更新 miniapp 命令 checklist。
- [ ] AC-022 若更新 `.agents/skills/miniapp-prepare/SKILL.md`，其 Gates / Output 必须区分自动门禁与人工 Network checklist。
- [ ] AC-023 若更新 `.agents/skills/miniapp-confirm/SKILL.md`，其 Output 必须能承接 DevTools Network、体验版 Network、阻塞项和剩余风险摘要。
- [ ] AC-024 若更新 `scripts/miniapp-env.py`，必须补充静态测试覆盖 checklist 文案，避免人工 checklist 被误判为自动通过。
- [ ] AC-025 若更新 `src/miniapp/README.md`，必须同步说明 release/miniapp 准备中的 Network evidence 边界。

## 安全 AC

- [ ] AC-026 Network evidence 记录不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。
- [ ] AC-027 截图、录屏、报告或人工摘要包含敏感信息时，必须先脱敏；无法公开保存时只记录安全摘要和不可公开原因。
- [ ] AC-028 小程序资源加载继续通过后端受控 URL、代理 URL、签名 URL 或已批准公开策略，不得要求前端直连未授权对象存储。

## 横切 AC（knowledge-base）

本 REQ 不命中 `req-complete` 指定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` UI 横切标签，因此无 AC-XCUT 条目。

复盘参考：`docs/knowledge-base/retrospectives/sprint-014-retrospective.md` 中的 T-014-003 / A-014-002 要求将小程序 DevTools、真机、体验版 Network evidence 前置到 release 准备清单，避免归档后遗漏发布证据。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: update-miniapp-network-panel-release-checklist
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

