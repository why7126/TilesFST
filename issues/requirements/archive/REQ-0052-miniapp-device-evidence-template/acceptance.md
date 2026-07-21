---
requirement_id: REQ-0052-miniapp-device-evidence-template
title: 小程序 DevTools/真机验收 evidence 模板验收标准
status: done
created_at: 2026-07-19 17:08:59
updated_at: 2026-07-19 19:05:20
---

# REQ-0052 小程序 DevTools/真机验收 evidence 模板验收标准

## 1. 模板结构 AC

- [ ] AC-STRUCT-001 后续模板文档必须定义 `miniapp_device_evidence` 或等价命名的可复制结构。
- [ ] AC-STRUCT-002 模板必须包含 `template_ref`、`target`、`pages`、`evidence_items` 和 `summary` 字段或等价表格列。
- [ ] AC-STRUCT-003 `target` 必须能记录 REQ、BUG 或 OpenSpec Change ID。
- [ ] AC-STRUCT-004 `pages` 必须能记录页面路径、页面标题、关键 query 参数和验收场景。
- [ ] AC-STRUCT-005 `summary` 必须能记录最终结论、阻塞项、剩余风险和后续承接方式。

## 2. evidence 状态 AC

- [ ] AC-STATE-001 模板必须支持 `required`、`passed`、`failed`、`blocked`、`not_applicable`、`follow_up` 六类状态。
- [ ] AC-STATE-002 `passed` 必须有可复核证据，例如截图、录屏、命令摘要、人工验收摘要或 artifact 引用。
- [ ] AC-STATE-003 `failed` 必须记录失败表现、影响页面和后续处理建议。
- [ ] AC-STATE-004 `blocked` 必须记录阻塞原因，例如设备、账号、网络、版本或外部依赖。
- [ ] AC-STATE-005 `not_applicable` 必须记录 N/A reason，不得留空。
- [ ] AC-STATE-006 `follow_up` 必须记录剩余风险、责任人或后续承接方式。

## 3. DevTools evidence AC

- [ ] AC-DEVTOOLS-001 DevTools evidence 必须记录微信开发者工具版本或可识别版本摘要。
- [ ] AC-DEVTOOLS-002 DevTools evidence 必须记录基础库版本。
- [ ] AC-DEVTOOLS-003 DevTools evidence 必须记录模拟器设备或 viewport 宽度，例如 320、375、430 pt。
- [ ] AC-DEVTOOLS-004 DevTools evidence 必须记录页面路径和关键 query 参数。
- [ ] AC-DEVTOOLS-005 DevTools evidence 必须记录验收场景，例如首页首屏、自定义导航栏、分类列表或 SKU 详情页。
- [ ] AC-DEVTOOLS-006 DevTools evidence 必须记录截图、录屏、报告相对路径，或无法保存文件时的人工摘要。
- [ ] AC-DEVTOOLS-007 DevTools evidence 结论必须明确其不等同于真机验收，除非另有真机 evidence。

## 4. 真机 evidence AC

- [ ] AC-DEVICE-001 真机 evidence 必须记录设备型号。
- [ ] AC-DEVICE-002 真机 evidence 必须记录系统类型与版本。
- [ ] AC-DEVICE-003 真机 evidence 必须记录微信版本。
- [ ] AC-DEVICE-004 真机 evidence 必须记录小程序基础库版本。
- [ ] AC-DEVICE-005 真机 evidence 必须记录页面路径、关键 query 参数和用户状态。
- [ ] AC-DEVICE-006 真机 evidence 必须记录视口宽度、安全区、状态栏和胶囊避让结论。
- [ ] AC-DEVICE-007 真机 evidence 必须记录执行人、执行时间、截图/录屏引用、验收结论和剩余风险。
- [ ] AC-DEVICE-008 涉及自定义导航栏、fixed header、触控区域、分享/返回/关闭、图片预览或页面滚动的 Change，若无法执行真机验收，必须标记 `blocked` 或 `follow_up`，不得写作“真机通过”。

## 5. 自动化与人工验收边界 AC

- [ ] AC-BOUNDARY-001 模板必须区分静态测试、脚本/单元测试、DevTools 预览和真机验收四类证据来源。
- [ ] AC-BOUNDARY-002 静态测试通过只能证明文件、模板、配置或规则约束，不得证明 DevTools 实际渲染通过。
- [ ] AC-BOUNDARY-003 脚本/单元测试通过只能证明逻辑或配置，不得证明真机安全区和微信原生能力。
- [ ] AC-BOUNDARY-004 DevTools 通过不得自动等同真实设备触控、系统安全区和微信版本差异均通过。
- [ ] AC-BOUNDARY-005 没有 DevTools 或真机记录时，Sprint 验收报告、release note 或 Change trace 不得表述为“设备验收已完成”。

## 6. 安全与证据记录 AC

- [ ] AC-SAFE-001 截图、录屏和报告路径必须使用仓库相对路径或稳定 artifact 引用，不记录本机绝对路径。
- [ ] AC-SAFE-002 evidence 不得记录 token、Cookie、Authorization header、`.env` 内容、真实密钥、数据库 DSN 或 MinIO 凭据。
- [ ] AC-SAFE-003 evidence 不得包含真实客户数据、未脱敏手机号、地址或个人隐私。
- [ ] AC-SAFE-004 evidence 不得复制大段日志、完整构建输出或无法复核的口头描述。
- [ ] AC-SAFE-005 截图包含敏感信息时，必须脱敏或记录不可公开原因。

## 7. 引用与范围 AC

- [ ] AC-REF-001 后续实现应优先将模板沉淀到 `docs/standards/miniapp-device-evidence-template.md`。
- [ ] AC-REF-002 小程序 REQ 的 `acceptance.md` 可引用模板作为测试与验证 evidence 事实源。
- [ ] AC-REF-003 OpenSpec Change `tasks.md` 可引用模板作为人工验收任务格式。
- [ ] AC-REF-004 Sprint `acceptance-report.md` 可引用模板摘要设备验收通过、阻塞或 follow-up 结论。
- [ ] AC-REF-005 Release note 只应记录用户可理解的设备验收结论和剩余风险，不复制完整 evidence。
- [ ] AC-SCOPE-001 本需求不新增或修改小程序业务页面。
- [ ] AC-SCOPE-002 本需求不新增自动化截图、真机云测或小程序自动化工具链。
- [ ] AC-SCOPE-003 本需求不回填全部历史 DevTools/真机 evidence。
- [ ] AC-SCOPE-004 本需求不修改 API、数据库、Orval、Docker Compose、MinIO 或运行环境。

## 横切 AC（knowledge-base）

本 REQ 为微信小程序设备验收治理模板，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 管理端横切标签，因此无 `AC-XCUT-*` 管理端横切验收项。

参考复盘：`docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 中关于“小程序设备验收建立独立 Gate”“设备/视口验收残留”和“自动化覆盖与设备验收拆成不同任务状态”的经验，已转化为本文件的 DevTools evidence、真机 evidence、自动化边界和 follow-up AC。
