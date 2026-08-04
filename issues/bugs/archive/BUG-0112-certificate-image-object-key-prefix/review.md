---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀评审记录
review_status: approved
reviewed_at: 2026-08-04 08:24:14
reviewer: AI
decision: approved
created_at: 2026-08-04 08:24:14
updated_at: 2026-08-04 08:24:14
---

# BUG-0112 评审记录

## 评审结论

确认修复，状态批准为 `approved`。该缺陷触及对象存储 key 规范、品牌证书图片/文档类型分流、缩略图生成、历史对象迁移和工作流技能口径，需通过后续 OpenSpec Change 承接修复。

## 评审清单

| 项目 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 当前规范已要求图片类资源使用 `images/`，证书图片落入非 `images/` 前缀属于明确偏差；根因已指向规范、实现、脚本和技能口径漂移。 |
| 严重等级合理 | 通过 | `high` 合理；问题影响对象存储治理、历史迁移、缩略图派生和跨端媒体验收，但未直接导致所有证书功能不可用。 |
| 回归验收明确 | 通过 | acceptance 已覆盖图片证书、PDF 证书、缩略图、历史对象迁移、规范收敛、Skill 收敛和自动化测试。 |
| 是否需 hotfix 路径 | 不需要 | 暂未发现阻断生产上传或公开展示的直接故障，建议纳入常规 BUG 修复 Change 与 Sprint。 |

## 处理决定

- 允许执行 `/bug-opsx BUG-0112-certificate-image-object-key-prefix` 创建修复 Change。
- 允许后续纳入 Sprint 正式范围。
- 修复必须覆盖规范、脚本、技能、后端媒体前缀分流、历史数据迁移策略和测试。
