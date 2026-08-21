## ADDED Requirements

### Requirement: Workflow 命令完成复盘
系统 MUST 在 workflow 命令完成输出中提供执行链路复盘，复盘内容 MUST 基于脚本、校验、文件、日志、截图、验收记录、用户补证、Workflow Sync 或 AI Usage 等证据，不得凭空猜测。

#### Scenario: 命令成功完成
- **WHEN** `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*`、`/release-*`、`/image-*`、`/usage-docs-*`、`/spec-opt` 或 `/spec-study apply` 完成
- **THEN** 最终输出 MUST 包含链路状态、问题证据、规范优化建议和 follow-up 自动创建状态
- **AND** 若没有明确可复用沉淀，规范优化建议 MUST 写为“无明显优化点”

#### Scenario: 发现可沉淀问题
- **WHEN** 命令执行发现可复用的流程、规则、脚本或文档优化点
- **THEN** 输出 MUST 给出建议命令或标准 capture 文案
- **AND** 系统 MUST NOT 自动创建 follow-up Issue 或 Change，除非用户在当前命令中明确授权

### Requirement: 证据化根因分析
系统 MUST 在问题排查、BUG 完善、BUG 来源实现、验收返修和效果不如预期场景中区分根因状态，并且 MUST 要求 confirmed 根因绑定证据链。

#### Scenario: 根因证据充足
- **WHEN** BUG 或返修文档声明根因状态为 `confirmed`
- **THEN** 文档 MUST 记录可定位证据入口、证据类型、结论和验证方式
- **AND** 证据 MUST 脱敏，不得包含密钥、真实客户数据、未脱敏日志或本机绝对路径

#### Scenario: 根因证据不足
- **WHEN** 现有信息不足以确认根因
- **THEN** 系统 MUST 将根因状态标记为 `unknown`、`hypothesis` 或 `probable`
- **AND** 输出 MUST 包含人工补证步骤、需要收集的证据类型和验收或复现要点

### Requirement: UI 返修截图逐项对照
系统 MUST 在 UI 型 `/opsx-modify` 中先处理验收反馈证据，再修改实现。若反馈包含附件截图、标注图、原型截图或实际截图，系统 MUST 建立逐项视觉对照表。

#### Scenario: 附件截图反馈
- **WHEN** `/opsx-modify` 的验收反馈包含附件截图、标注图、原型截图或实际截图
- **THEN** 系统 MUST 在返修前记录截图编号、页面或状态、期望表现、实际表现、偏差项、检查方式、处置结论和证据入口
- **AND** 若证据不足以定位偏差，系统 MUST 先请求补证或说明补证步骤，不得直接返修

#### Scenario: UI 返修完成
- **WHEN** UI 返修修改完成
- **THEN** 系统 MUST 将相关旧截图视为 stale
- **AND** 系统 MUST 重新取证或记录等价视觉验证，并更新 Change trace、验收记录或测试证据入口

### Requirement: Workflow Sync next 推导复核
Workflow Sync MUST 在 `req.opsx` / `bug.opsx` 创建或确认 Change 后刷新 Issue 当前态看板的下一步推导，避免派生态继续提示已完成的 `/req-opsx` 或 `/bug-opsx`。

#### Scenario: REQ 或 BUG 回填 Change
- **WHEN** Workflow Sync 处理 `req.opsx` 或 `bug.opsx`
- **AND** 同轮已经将 Change 回填到 Issue trace、registry 或 Sprint scope
- **THEN** `issues/requirements/CHANGELOG.md` 或 `issues/bugs/CHANGELOG.md` 的下一步 MUST 推导为后续 `/opsx-apply <REQ-id|BUG-id>` 或等价下一阶段命令
- **AND** 若仍提示 `/req-opsx` 或 `/bug-opsx`，系统 MUST 报告派生态漂移并修复后再完成父命令

### Requirement: 治理脚本门禁矩阵
系统 MUST 维护命令阶段到最小相关治理脚本的门禁矩阵，帮助 Agent 在不全量运行无关测试的前提下选择必要验证。

#### Scenario: 治理资产变更
- **WHEN** 命令修改 `.agents/skills/`、`rules/`、`docs/`、`scripts/` 或 OpenSpec Change 文档
- **THEN** 系统 MUST 按治理脚本门禁矩阵选择最小相关验证
- **AND** 输出 MUST 说明未运行业务测试的原因（如不涉及 API、DB、Web、小程序、管理端或 Docker）
