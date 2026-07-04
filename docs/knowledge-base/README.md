---
title: 知识库说明
purpose: 说明 incidents、retrospectives、troubleshooting、best-practices、faq 目录职责
content: 项目模板文档
source: AI自动生成，人工确认
update_method: 相关流程或内容变化时更新
owner: 项目文档负责人
status: draft
note: 企业初始化模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-04 12:34:17
---

# 知识库

知识库用于沉淀长期可复用经验，不承担需求或 BUG 工单职责。

## 目录

| 目录 | 职责 | 典型来源 |
|------|------|----------|
| `retrospectives/` | Sprint 整迭代经验复盘 | `/sprint-exps sprint-xxx` |
| `incidents/` | 故障/事故复盘 | `/bug-opsx` tasks、生产问题 |
| `troubleshooting/` | 排障手册 | 重复出现的运维问题 |
| `best-practices/` | 跨 Sprint 最佳实践 | 复盘行动项、模式总结 |
| `faq/` | 常见问题 | 团队问答沉淀 |

## Sprint 复盘索引

| Sprint | 文档 | 状态 |
|--------|------|------|
| sprint-002 | [`retrospectives/sprint-002-retrospective.md`](retrospectives/sprint-002-retrospective.md) | draft |
| sprint-003 | [`retrospectives/sprint-003-retrospective.md`](retrospectives/sprint-003-retrospective.md) | draft |
| sprint-004 | [`retrospectives/sprint-004-retrospective.md`](retrospectives/sprint-004-retrospective.md) | draft |

## 最佳实践索引

| 主题 | 文档 | 来源 |
|------|------|------|
| 管理端列表页一致性 | [`best-practices/admin-list-page-consistency.md`](best-practices/admin-list-page-consistency.md) | sprint-002/003 复盘 |
| 管理端表单页一致性 | [`best-practices/admin-form-page-consistency.md`](best-practices/admin-form-page-consistency.md) | sprint-003 复盘 |
| 管理端弹窗宽度 CSS 层叠 | [`best-practices/admin-modal-width-css-cascade.md`](best-practices/admin-modal-width-css-cascade.md) | sprint-003 复盘 |
| 管理端媒体上传全链路 | [`best-practices/admin-media-upload-chain.md`](best-practices/admin-media-upload-chain.md) | sprint-002 复盘 |

## 与 issues 的边界

- **issues/**：个案 REQ/BUG、验收与 trace（事实源）
- **knowledge-base/**：可复用的模式、流程改进、预防策略（不复制整份 BUG 文档）
