---
requirement_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
title: 规则/Skill 已读摘要复用纳入命令上下文预算治理 - 验收标准
status: done
created_at: 2026-07-16 09:07:01
updated_at: 2026-07-18 09:18:43
---

# 验收标准

## 功能 AC

- [ ] **AC-001** `rules/agent-context-budget.md` MUST 定义“已读摘要复用”的目标、适用范围、最小摘要字段和失效条件。
- [ ] **AC-002** 摘要复用范围 MUST 明确覆盖 `rules/` 与 `.agents/skills/*/SKILL.md`，并说明 `AGENTS.md`、`openspec/project.md` 和 `workflow-sync` Skill 的处理方式。
- [ ] **AC-003** 摘要最小字段 SHOULD 包含 `path`、`version_hint`、`summary`、`applicability` 和 `refresh_reason` 或等价信息。
- [ ] **AC-004** 文件变更、用户要求重读、任务风险升级、摘要不足、Workflow Sync/测试/校验失败时 MUST 触发补读或重新读取必要片段。
- [ ] **AC-005** 命令 Skill 的 `Context Budget Guardrails` SHOULD 明确“同一会话已读且无变更的规则和 Skill 用摘要承接”。
- [ ] **AC-006** 高风险命令仍 MUST 补读当前 Change、Issue、Sprint、trace 或 Final Step 相关片段，不得仅凭摘要绕过 OpenSpec、Issue lifecycle、安全、API、DB、发布等强门禁。
- [ ] **AC-007** `scripts/validate-agent-context-budget.py` 或等价校验 SHOULD 检查命令 Skill 是否引用 `rules/agent-context-budget.md`、是否包含摘要复用约束、是否存在默认宽泛读取模式。
- [ ] **AC-008** 校验失败时 SHOULD 输出具体 Skill 文件路径和行号，便于维护者修正。
- [ ] **AC-009** 命令成功路径输出 SHOULD 只展示摘要复用状态、补读片段、计数、warning 或 recommended action，不得输出完整规则、完整 Skill、完整 generated diff 或完整测试日志。
- [ ] **AC-010** 摘要复用机制 MUST NOT 持久化原始 prompt、系统/developer 指令、完整 session JSONL、工具输出正文、密钥、Cookie、Authorization header、`.env` 内容或真实客户数据。

## 非功能 AC

- [ ] **AC-NF-001** 本需求实现后，`python scripts/validate-agent-context-budget.py` MUST 通过，或在输出中明确列出仍待修复的 Skill。
- [ ] **AC-NF-002** 规则和 Skill 更新 MUST 避免复制长脚本、长命令或长规则正文；应引用规则路径或脚本路径。
- [ ] **AC-NF-003** 不得新增 Web 管理端、店主 Web、小程序页面、API 路由、数据库表或上传存储能力。
- [ ] **AC-NF-004** 若后续实现需要落盘保存摘要，MUST 先补充脱敏、生命周期、提交边界和清理策略；本需求默认仅要求同一会话内摘要承接。

## 横切 AC（knowledge-base）

N/A — 本需求为 Agent 工作流治理，不涉及管理端列表、表单、弹窗或媒体上传 UI 场景；未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签。
