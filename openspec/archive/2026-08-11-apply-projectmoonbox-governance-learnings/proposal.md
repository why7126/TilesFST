## 背景

本项目已通过 `/spec-study ProjectMoonBox` 完成跨项目治理学习，候选内容包括日志优先学习、推送前 Git 安全检测、原型驱动 UI 验收、Issue 当前态看板和引导式反馈契约。用户已确认应用全部候选项。

这些内容均属于治理资产增强，不涉及业务功能实现，但会改变命令技能、校验脚本和长期规则的执行约束，因此必须通过 OpenSpec Change 与 Sprint scope 承载。

## 变更内容

- 增强 `/spec-study`：学习对象存在 `docs/spec-logs/CHANGELOG.md` 时先读日志索引，再按主题补读单次日志，最后横向校验真实治理资产。
- 新增 `/git-check`：提供推送前安全检测技能与脚本，扫描 staged/tracked 文件中的真实环境文件、运行时数据、大文件、密钥、连接串、本机绝对路径等风险。
- 补充原型驱动 UI 验收标准：带 `prototype/` 的 UI Change 必须形成 UI Contract、Skeleton、1440px 视觉证据、computed style 和 Mock/API 边界说明。
- 增强 Issue 生命周期：新增 `issues/requirements/CHANGELOG.md` 与 `issues/bugs/CHANGELOG.md` 当前态看板索引边界，继续以 registry、trace、Sprint 和 OpenSpec 为机器事实源。
- 增强命令引导式反馈：命令需要用户选择时优先使用原生交互卡片，无法支持时降级为文本结构化选项。
- 写入同一次 `/spec-study apply` 学习报告，汇总采纳、未采纳、验证和只读保护结果。

## 能力范围

### 新增能力

- `agent-workflow-tooling`：新增 `/git-check` 推送前安全检测命令。

### 修改能力

- `agent-workflow-tooling`：增强 `/spec-study` 学习顺序、命令反馈契约和治理学习报告要求。
- `agent-context-governance`：增强上下文预算校验、日志优先学习和引导式反馈约束。
- `design-system`：补充原型驱动 UI 验收合同和证据门禁。
- `sprint-planning-governance`：补充 Issue 当前态看板索引与 Sprint scope 同步边界。

## 影响

- API：不影响。
- 数据库：不影响。
- Web：不修改业务 UI；后续带 prototype 的 Web/管理端 UI Change 需遵守新增门禁。
- 小程序：不修改小程序业务代码；后续小程序 UI Change 如带 prototype 需遵守证据门禁。
- 管理端：不修改管理端业务代码；后续管理端 UI Change 需补齐 UI Contract 与视觉证据。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增或更新治理脚本校验；业务测试不适用。
