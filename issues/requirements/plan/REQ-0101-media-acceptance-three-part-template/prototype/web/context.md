---
requirement_id: REQ-0101-media-acceptance-three-part-template
status: pending_review
created_at: 2026-08-06 11:24:19
updated_at: 2026-08-06 11:24:19
owner: product
source: requirement.md
---

# Prototype Context

REQ-0101 是验收模板治理需求，本期不新增 Web 管理端页面、弹窗、表单或小程序页面，因此不产出独立 HTML 原型。

若后续 OpenSpec Change 决定将模板工具化到管理端或文档站，界面策略如下：

- 首屏应是可编辑或可复制的三段验收表，不做营销式说明页。
- 三段结构固定为“列表展示字段”“生成策略”“历史对象维护或重生成”。
- 每段内使用紧凑表格承载状态、证据入口、影响项和备注。
- 影响矩阵使用五列或五行结构覆盖 API、Orval、DB、对象存储、admin web 列表。
- 状态使用 `pass`、`fail`、`n/a`、`blocked`，不得用颜色作为唯一信息载体。
- 若落入 Web 管理端，必须复用 Design System semantic token 和 shared UI 组件。
