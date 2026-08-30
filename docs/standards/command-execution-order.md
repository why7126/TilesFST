---
purpose: 命令执行顺序与治理脚本门禁矩阵
content: workflow 命令阶段、最小相关验证、Workflow Sync 与 AI Usage Hook 顺序
source: /spec-study apply MoonBox 治理质量学习项
update_method: 命令族、治理脚本或验证矩阵变化时更新
created_at: 2026-08-21 08:18:18
updated_at: 2026-08-30 12:55:22
---

# 命令执行顺序与治理脚本门禁矩阵

## 1. 总原则

命令执行遵循“事实源先行、最小相关验证、状态同步收尾”的顺序。治理脚本矩阵用于帮助 Agent 选择验证范围，不替代各 `.agents/skills/*/SKILL.md` 的 MUST 门禁。

选择验证前 SHOULD 先看本次 diff scope 和触达面。已通过且未被后续改动影响的检查不需要因为提交、归档或最终汇报而机械重复；CI 负责全量矩阵，本地命令负责提供与本次变更相匹配的最小相关证据。OpenSpec、Sprint、Workflow Sync、AI Usage 等项目强制门禁仍必须按命令技能执行。

## 2. 通用顺序

1. 读取 AGENTS、OpenSpec、规则和目标对象的必要片段。
2. 确认 Issue、Change、Sprint 阶段允许当前命令。
3. 执行本命令的治理或实现工作。
4. 运行最小相关校验。
5. 状态变化时运行 Workflow Sync。
6. Workflow Sync 成功后运行 AI Usage Hook。
7. 输出执行链路复盘、下一步和待用户决策/处理。

## 3. 治理脚本门禁矩阵

| 触达范围 | 最小相关校验 |
|---|---|
| `.agents/skills/`、`rules/agent-context-budget.md` | `python scripts/validate-agent-context-budget.py` |
| OpenSpec Change 文档或 delta spec | `python scripts/validate-openspec-language.py`、`openspec validate <change-id>` |
| 目录边界、docs、issues、iterations、releases、mintlify、deploy | `python scripts/validate-directory-structure.py` |
| 长期文档、规则、技能说明、知识库 | `python scripts/validate-doc-prose-hygiene.py <focused-paths>` |
| Sprint scope | `python scripts/validate-sprint-scope.py <sprint-id> --item <change-id|REQ|BUG>` |
| 环境分层 evidence / 生产证据后置 | `python scripts/validate-environment-tiered-evidence.py --change <change-id>`、`--sprint <sprint-id>` 或 `--release-dir releases/<version> --target production` |
| BUG 根因、返修根因或问题排查证据 | `python scripts/validate-root-cause-evidence.py --bug <BUG-id>` 或 `--change <change-id>` |
| API / OpenAPI / Orval | API 治理校验、OpenAPI 生成和相关 pytest / Vitest |
| DB schema | DB 文档、schema/migration 校验和相关 pytest |
| UI / prototype / 管理端页面 | 相关 Vitest、Playwright 或截图证据；prototype 场景遵守 `docs/standards/prototype-ui-acceptance.md` |
| 小程序 | 静态校验、设备/DevTools evidence 和相关脚本 |
| 发布 / usage docs / Mintlify | release、usage-docs、Mintlify 和部署 config 校验 |
| 安全 / env / 本地数据 | `python scripts/git-check.py` 或聚焦安全脚本 |

## 4. 输出要求

验证通过时输出命令和结果摘要；失败时只展开失败项、关键路径和修复建议。无法运行某项校验时，必须说明原因、影响范围和替代证据。

业务测试不适用时应明确说明不涉及 API、DB、Web、小程序、管理端、Orval 或 Docker Compose。
