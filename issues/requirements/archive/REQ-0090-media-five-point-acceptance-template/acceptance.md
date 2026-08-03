---
requirement_id: REQ-0090-media-five-point-acceptance-template
acceptance_status: passed
created_at: 2026-08-01 09:50:59
updated_at: 2026-08-02 19:32:35
---

# Acceptance

## 功能 AC

- [ ] AC-001 模板必须包含 key、object、URL、thumbnail benefit、miniapp render 五个维度，且五个维度均有检查目标、通过标准、证据字段和失败记录要求。
- [ ] AC-002 每个媒体样例必须支持 `pass`、`fail`、`n/a`、`blocked` 四种状态；`n/a` 和 `blocked` 必须填写原因。
- [ ] AC-003 key 维度必须检查 `object_key` 或等价脱敏标识与业务资源的关系，确认不使用用户原始文件名，且符合 MinIO 单桶 + 前缀策略。
- [ ] AC-004 object 维度必须检查对象存储中 object 的存在性、MIME、大小、权限和安全边界，不得暴露 MinIO 凭证或内部绝对路径。
- [ ] AC-005 URL 维度必须检查后端响应、Web 渲染或小程序使用的媒体 URL 是否可访问，并记录 HTTP 状态、错误码、URL 类型和用户可见表现。
- [ ] AC-006 thumbnail benefit 维度必须说明缩略图或封面图的实际收益；没有缩略图时必须记录 `n/a` 原因，不能空置。
- [ ] AC-007 miniapp render 维度必须检查微信小程序端的真实或等价预览渲染结果，覆盖加载、播放、占位、失败态和域名/组件限制。
- [ ] AC-008 模板必须能嵌入后续媒体相关 `acceptance.md`、Sprint 验收报告或发布检查清单，并支持多个媒体样例独立记录。
- [ ] AC-009 模板失败记录必须足以支撑后续 `/bug-capture`，至少包含失败现象、影响范围、复现入口、期望结果和实际结果。
- [ ] AC-010 模板必须明确不新增上传接口、缩略图生成流水线、视频转码能力、对象存储架构或自动化测试框架；如需实现这些能力，必须另走 OpenSpec Change。
- [ ] AC-011 后续 `/req-opsx` design 必须确认模板最终落点，并说明是否沉淀到 `rules/media.md`、`rules/object-storage.md`、长期文档、issue 模板或发布检查流程。
- [ ] AC-012 模板不得记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。

## 媒体五联模板样例

| 样例 | 媒体类型 | 业务资源 | key | object | URL | thumbnail benefit | miniapp render | 结论 |
|---|---|---|---|---|---|---|---|---|
| sample-001 | image/video/logo/certificate | 待填写 | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/blocked |

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷；结合 `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` 的媒体链路复盘行动项。

- [ ] AC-XCUT-001 媒体上传类后续需求引用本模板时，必须检查上传控件或流程是否具备 `idle → uploading → done/failed` 状态机；若该需求不包含上传控件，记录 `N/A — 仅模板治理，不新增上传 UI`。
- [ ] AC-XCUT-002 媒体上传类后续需求引用本模板时，必须检查同一会话上传成功后能即时回显缩略图、文件卡片或媒体 URL；若该需求不包含即时回显场景，记录 `N/A — 无端上上传回显入口`。
- [ ] AC-XCUT-003 媒体上传类后续需求引用本模板时，必须通过 Docker Web `http://localhost:3000` 边界文件验收，而不是只调用后端 `:8000`；若该需求不涉及真实上传，记录 `N/A — 未执行上传实现，仅定义验收模板`。
- [ ] AC-XCUT-004 媒体上传类后续需求引用本模板时，必须检查失败信息出现在上传控件或媒体样例记录中，不能只依赖全局 toast；若该需求无上传控件，记录 `N/A — 失败记录写入模板样例而非 UI 控件`。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: add-media-five-point-acceptance-template
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

