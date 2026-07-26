# Proposal: 优化 Agent 上下文预算与 Harness 噪音

## 背景

BUG-0061 全流程会话分析显示，token 消耗主要来自重复读取治理规则、OpenSpec/Sprint 工件、生成物 diff，以及每轮注入的 Harness/pm-harness 相关常驻上下文。主流程累计约 21.67M tokens，其中 input/cached input 占绝大多数，说明优化重点应放在读取边界、搜索排除、输出截断和常驻上下文瘦身。

## 目标

- 建立项目级 Agent 上下文预算规则，成为所有 命令技能的共同约束。
- 默认排除 Harness/模板工程/agent 资产/生成物/历史归档等高噪音目录。
- 限制大 diff、OpenAPI/Orval 生成物、测试/同步输出的展开方式。
- 新增轻量校验脚本，防止技能文件回退到宽泛读取或缺少预算守则。
- 不改变业务功能、API、数据库、Web/小程序运行逻辑。

## 非目标

- 不改 Codex Desktop 或系统级权限注入机制。
- 不删除 Harness 工程或模板资产。
- 不修改现有 BUG-0061 业务修复代码。
- 不改变 OpenSpec、Issue、Sprint 生命周期门禁。

## 风险与缓解

- 风险：规则过严导致必要历史上下文读取不足。
  - 缓解：允许在明确说明原因后按需放开 archive/Harness/生成物读取。
- 风险：校验脚本误伤非命令技能文件。
  - 缓解：校验只覆盖 `.agents/skills/{req,bug,opsx,sprint,build}-*`、`.agents/skills/capture`、`.agents/skills/initialize-project`，并要求最低限度的预算引用与禁用模式。
