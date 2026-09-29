---
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
created_at: 2026-09-10 19:19:40
updated_at: 2026-09-10 19:19:40
---

## ADDED Requirements

### Requirement: Sprint 本体一致性关闭检查

系统 MUST 在Sprint关闭前校验所有Change的知识适用性，范围内失败、过期和已确认高风险冲突阻断；范围外须有理由，低风险缺失仅警告。

#### Scenario: 生命周期门禁
- **WHEN** 模型格式合法但跨Change关系类型错误
- **THEN** 系统 MUST 阻断关闭并定位来源，不能以格式通过替代语义通过
