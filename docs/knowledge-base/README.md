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
updated_at: 2026-08-30 14:50:52
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
| sprint-005 | [`retrospectives/sprint-005-retrospective.md`](retrospectives/sprint-005-retrospective.md) | draft |
| sprint-006 | [`retrospectives/sprint-006-retrospective.md`](retrospectives/sprint-006-retrospective.md) | draft |
| sprint-007 | [`retrospectives/sprint-007-retrospective.md`](retrospectives/sprint-007-retrospective.md) | draft |
| sprint-008 | [`retrospectives/sprint-008-retrospective.md`](retrospectives/sprint-008-retrospective.md) | draft |
| sprint-009 | [`retrospectives/sprint-009-retrospective.md`](retrospectives/sprint-009-retrospective.md) | draft |
| sprint-010 | [`retrospectives/sprint-010-retrospective.md`](retrospectives/sprint-010-retrospective.md) | draft |
| sprint-011 | [`retrospectives/sprint-011-retrospective.md`](retrospectives/sprint-011-retrospective.md) | draft |
| sprint-012 | [`retrospectives/sprint-012-retrospective.md`](retrospectives/sprint-012-retrospective.md) | draft |
| sprint-013 | [`retrospectives/sprint-013-retrospective.md`](retrospectives/sprint-013-retrospective.md) | draft |
| sprint-014 | [`retrospectives/sprint-014-retrospective.md`](retrospectives/sprint-014-retrospective.md) | draft |
| sprint-015 | [`retrospectives/sprint-015-retrospective.md`](retrospectives/sprint-015-retrospective.md) | draft |
| sprint-016 | [`retrospectives/sprint-016-retrospective.md`](retrospectives/sprint-016-retrospective.md) | draft |
| sprint-017 | [`retrospectives/sprint-017-retrospective.md`](retrospectives/sprint-017-retrospective.md) | draft |
| sprint-018 | [`retrospectives/sprint-018-retrospective.md`](retrospectives/sprint-018-retrospective.md) | draft |
| sprint-019 | [`retrospectives/sprint-019-retrospective.md`](retrospectives/sprint-019-retrospective.md) | draft |
| sprint-020 | [`retrospectives/sprint-020-retrospective.md`](retrospectives/sprint-020-retrospective.md) | draft |
| sprint-021 | [`retrospectives/sprint-021-retrospective.md`](retrospectives/sprint-021-retrospective.md) | draft |
| sprint-022 | [`retrospectives/sprint-022-retrospective.md`](retrospectives/sprint-022-retrospective.md) | draft |
| sprint-023 | [`retrospectives/sprint-023-retrospective.md`](retrospectives/sprint-023-retrospective.md) | draft |
| sprint-024 | [`retrospectives/sprint-024-retrospective.md`](retrospectives/sprint-024-retrospective.md) | draft |
| sprint-025 | [`retrospectives/sprint-025-retrospective.md`](retrospectives/sprint-025-retrospective.md) | draft |
| sprint-026 | [`retrospectives/sprint-026-retrospective.md`](retrospectives/sprint-026-retrospective.md) | draft |
| sprint-027 | [`retrospectives/sprint-027-retrospective.md`](retrospectives/sprint-027-retrospective.md) | draft |
| sprint-028 | [`retrospectives/sprint-028-retrospective.md`](retrospectives/sprint-028-retrospective.md) | draft |

## 最佳实践索引

| 主题 | 文档 | 来源 |
|------|------|------|
| 管理端列表页一致性 | [`best-practices/admin-list-page-consistency.md`](best-practices/admin-list-page-consistency.md) | sprint-002/003 复盘 |
| 管理端表单页一致性 | [`best-practices/admin-form-page-consistency.md`](best-practices/admin-form-page-consistency.md) | sprint-003 复盘 |
| 管理端弹窗宽度 CSS 层叠 | [`best-practices/admin-modal-width-css-cascade.md`](best-practices/admin-modal-width-css-cascade.md) | sprint-003 复盘 |
| 管理端媒体上传全链路 | [`best-practices/admin-media-upload-chain.md`](best-practices/admin-media-upload-chain.md) | sprint-002 复盘 |
| Clipboard helper fallback | [`best-practices/clipboard-fallback.md`](best-practices/clipboard-fallback.md) | sprint-006 复盘 / REQ-0036 |
| 小程序自定义导航 | [`best-practices/miniapp-custom-navigation.md`](best-practices/miniapp-custom-navigation.md) | sprint-008 复盘 / REQ-0053 |
| 小程序商品列表排序 | [`best-practices/miniapp-product-list-sorting.md`](best-practices/miniapp-product-list-sorting.md) | BUG-0091 |
| 小程序媒体四联验收 | [`best-practices/miniapp-media-four-part-acceptance-practice.md`](best-practices/miniapp-media-four-part-acceptance-practice.md) | BUG-0125 / BUG-0126 / REQ-0111 |
| 防御性模式模板 | [`best-practices/defensive-pattern-template.md`](best-practices/defensive-pattern-template.md) | `/spec-study apply deepseek-harness` |

## 与 issues 的边界

- **issues/**：个案 REQ/BUG、验收与 trace（事实源）
- **knowledge-base/**：可复用的模式、流程改进、预防策略（不复制整份 BUG 文档）
