---
bug_id: BUG-0050-user-create-validation-message-unclear
title: 创建用户校验失败未明确提示具体问题点 - 评审记录
severity: medium
status: approved
owner: product
review_result: approved
reviewed_at: 2026-06-30 18:17:05
created_at: 2026-06-30 18:17:05
updated_at: 2026-06-30 18:17:05
related_requirement: REQ-0005-user-management
---

# 评审记录

## 评审结论

`approved`，确认需要修复。

BUG-0050 已满足进入修复流程的条件：问题可稳定复现，根因分析充分，严重等级为 `medium` 合理，回归验收标准明确。该问题不需要 hotfix 路径，可进入常规 `fix-*` OpenSpec Change。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `username="abc"` 时请求被 Pydantic Schema 层提前拦截，返回默认 422 `detail` |
| 严重等级合理 | 通过 | 不阻断合法创建，但影响管理员表单错误恢复效率，定级 `medium` |
| 回归验收明确 | 通过 | `acceptance.md` 覆盖 API 统一错误结构、前端提示、其他用户名规则与成功创建回归 |
| 是否需 hotfix 路径 | 不需要 | 问题影响体验和一致性，不涉及安全、数据损坏或生产阻断 |

## 修复门禁

- 后续可执行 `/bug-opsx BUG-0050-user-create-validation-message-unclear`。
- 建议 Change 命名沿用 `fix-user-create-validation-message-unclear`。
- 修复时必须补充后端接口测试与前端表单错误展示测试。
- 若采用全局 422 处理策略，需同步检查 API 治理文档与相关回归范围。

## 评审备注

本次评审只确认缺陷是否进入修复流程，不修改 `src/`，不创建 OpenSpec Change。
