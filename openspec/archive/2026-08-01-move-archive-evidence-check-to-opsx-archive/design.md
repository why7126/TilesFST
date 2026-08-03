## Context

`agent-workflow-tooling` 已经在 Sprint archive/readiness 中定义 archived Change 缺失 `trace.md` 时必须具备 `## 归档验证摘要` 兜底证据。当前问题是检查发生得偏晚：单个 Change 执行 `/opsx-archive` 后，证据缺口可能要等到 Sprint close 才被发现，导致修复链路回到历史归档目录中补证据，反馈成本较高。

`/opsx-archive` 是单个 Change 从 active 进入 archived 的边界，因此它应在归档路径确定后立即执行同一套证据完整性检查，并在输出中说明证据状态。Sprint readiness 继续保留该检查，作为跨 Sprint 范围的二次复核和历史兼容兜底。

## Goals / Non-Goals

**Goals:**

- 在 `/opsx-archive <change-id>` 成功归档单个 Change 时，立即校验 archived Change 的 `trace.md` 或 `归档验证摘要` 证据完整性。
- 复用或抽取现有 fallback summary 解析规则，保证 `/opsx-archive` 与 `/sprint-archive` 对必填摘要项的判断一致。
- 在缺失证据时输出可执行诊断信息：Change id、归档路径、候选文件、缺失项和建议修复位置。
- 补充测试覆盖 trace 存在、trace 缺失但 fallback 完整、trace 缺失且 fallback 不完整三类路径。

**Non-Goals:**

- 不改变 canonical archive root，仍使用 `openspec/archive/YYYY-MM-DD-<change-id>/`。
- 不放宽 `trace.md` 的优先级；`trace.md` 存在时仍视为归档证据充分。
- 不为历史 archive 全量回填 `trace.md` 或 `归档验证摘要`。
- 不修改业务 API、数据库、前端、小程序、Docker 或 Orval 生成链路。

## Decisions

1. `/opsx-archive` 在归档目标路径确定后执行 archived evidence check。
   - 原因：检查需要读取归档后的实际目录，避免 active/archived 路径语义混淆。
   - 备选：归档前在 active Change 目录预检。该方式无法覆盖 wrapper/CLI 移动后的路径和输出证据，仍可能遗漏归档结果。

2. 归档证据完整性规则由共享 helper 或脚本函数承载。
   - 原因：`validate-sprint-archive-readiness.py` 已有 fallback summary 章节和必填项判断，`/opsx-archive` 应复用相同口径。
   - 备选：在 `/opsx-archive` 重新实现独立解析。该方式会产生两套规则，后续必填项变化时容易漂移。

3. `/sprint-archive` readiness 保留检查，但定位为二次防线。
   - 原因：历史归档 Change、手工迁移或早期归档仍可能缺证据，Sprint close 仍需保护整体闭环。
   - 备选：完全移除 Sprint readiness 检查。该方式会降低历史兼容和批量 Sprint 收尾可靠性。

4. `/opsx-archive` 输出保持摘要化。
   - 原因：符合上下文预算规则，成功路径只需要报告 evidence status、archive path 和是否有 warning/blocker。
   - 备选：输出候选文件完整章节。该方式会扩大命令输出并增加敏感信息暴露面。

## Risks / Trade-offs

- 归档后才发现 fallback 缺失时，Change 已经移动到 archive 目录。缓解：报告明确修复路径，并保证 `/opsx-archive` 不输出闭环成功结论，后续可补齐摘要后重跑校验或继续收尾。
- 共享 helper 抽取可能影响 Sprint readiness 既有测试。缓解：先以现有测试为回归基线，新增 opsx archive evidence tests 后再调整实现。
- 部分历史 archive 缺少 `trace.md` 且无 fallback summary。缓解：本变更只前移新增归档检查，Sprint readiness 继续按既有规则报告历史缺口，不做自动回填。
