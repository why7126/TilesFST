---
requirement_id: REQ-0052-miniapp-device-evidence-template
title: 小程序 DevTools/真机验收 evidence 模板用户故事
status: done
created_at: 2026-07-19 17:08:59
updated_at: 2026-07-19 19:05:20
---

# REQ-0052 小程序 DevTools/真机验收 evidence 模板用户故事

## US-001 产品负责人区分设备验收结论

作为产品 / 需求负责人，我希望 Sprint 验收和 release note 能区分自动化通过、DevTools 通过、真机通过和人工 follow-up，以便发布说明不把静态检查误写为真实设备验收已完成。

验收要点：

- 模板明确 evidence 来源：静态测试、脚本测试、DevTools、真机、N/A 或 follow-up。
- 没有 DevTools 或真机证据时，结论不得写为设备验收通过。
- follow-up 必须记录剩余风险、责任人或后续承接方式。
- Sprint 强制关闭时可引用模板记录未完成设备验收边界。

## US-002 小程序开发记录运行环境

作为小程序开发，我希望 evidence 模板明确需要记录设备、微信版本、基础库版本、页面路径和视口，以便后续定位 DevTools/真机差异时有事实源。

验收要点：

- DevTools evidence 记录开发者工具版本或版本摘要、基础库版本、模拟器设备、视口宽度和页面路径。
- 真机 evidence 记录设备型号、系统版本、微信版本、基础库版本、页面路径和安全区结论。
- 页面路径支持记录关键 query 参数和用户状态。
- 截图、录屏或报告路径使用仓库相对路径或稳定 artifact 引用。

## US-003 测试人员按统一模板验收

作为测试 / 验收人员，我希望能按统一字段记录 DevTools 和真机验收结果，以便小程序导航、列表、详情、搜索等页面的设备证据不再散落在多个文档中。

验收要点：

- evidence 状态支持 `required`、`passed`、`failed`、`blocked`、`not_applicable` 和 `follow_up`。
- `failed` 必须记录失败表现和后续处理建议。
- `blocked`、`not_applicable`、`follow_up` 必须记录原因。
- 模板支持按页面、场景和视口拆分多条 evidence。

## US-004 AI Agent 在流程中复用 evidence 事实源

作为 AI / Codex Agent，我希望后续小程序 REQ、OpenSpec Change 和 Sprint 验收报告能引用同一模板，以便 `/opsx-apply`、`/sprint-archive` 或 `/sprint-exps` 不重复生成互相冲突的设备验收描述。

验收要点：

- 模板建议沉淀位置为 `docs/standards/miniapp-device-evidence-template.md`。
- 后续 `acceptance.md`、OpenSpec `tasks.md`、Change trace、Sprint `acceptance-report.md` 可引用模板。
- 自动化/静态测试 evidence 与 DevTools/真机 evidence 分层记录。
- usage hook、Workflow Sync 和其他成功路径输出仍保持 compact summary，不复制完整设备证据。

## US-005 复盘行动项能进入正式闭环

作为流程维护者，我希望 sprint-008 中暴露的 DevTools/真机验收残留能转化为可复用模板需求，以便后续 Sprint 不再把人工设备验收风险留在归档备注里。

验收要点：

- trace 中引用 sprint-008 复盘作为知识库来源。
- 模板允许将历史残留作为案例，但不强制回填全部历史证据。
- 强制关闭或人工 follow-up 必须有标准化证据字段。
- 后续若要自动生成 follow-up Issue，应拆为独立工具链能力。
