---
purpose: 命令执行顺序与治理脚本门禁矩阵
content: workflow 命令阶段、最小相关验证、Workflow Sync 与 AI Usage Hook 顺序
source: /spec-study apply MoonBox 治理质量学习项
update_method: 命令族、治理脚本或验证矩阵变化时更新
created_at: 2026-08-21 08:18:18
updated_at: 2026-09-10 10:31:22
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
| 证据来源诊断 | 手动排查证据来源描述时运行 `python scripts/validate-environment-tiered-evidence.py --change <change-id>`、`--sprint <sprint-id>` 或 `--release-dir releases/<version>`；不作为默认 workflow 阻断门禁自动应用 |
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

## 5. Apply 持续执行契约

适用于 `.agents/skills/opsx-apply/SKILL.md` 与 `.agents/skills/openspec-apply-change/SKILL.md`。两入口 MUST 使用同一契约；CLI 的笼统 pause 提示应按下述阻塞分类处理。

### 5.1 持续执行

通过目标解析、Sprint 纳入及适用前置门禁后，当前命令 MUST 持续推进当前 Change 内所有依赖满足且已获授权的任务，包含实现、必需测试、文档和状态同步。完成一组任务、进度汇报、任务数量较多、上下文压缩均不得作为主动结束理由；进度使用中间消息，不请求用户重复发送“继续”或再次调用 apply。

普通实现细节由 Agent 依据已有设计、验收和项目惯例决定。当前范围内可恢复错误（类型错误、测试夹具漂移、构建失败、缺少可推导的声明字段）MUST 先定位、修复、聚焦复测，再继续；不得仅因首次报错等待指导。不得放宽断言、跳过必需验证或修改范围外契约来换取通过。

### 5.2 真正阻塞与独立任务

只有以下情形允许暂停相关任务：关键需求或范围存在无法从证据消解的歧义；实现需要改变已批准的 API、DB、权限等边界；必要授权或明确要求的人工确认缺失；必需外部资源不可用且无合法替代；有证据表明当前条件下无法自行解决的失败。Sprint 未纳入等全局前置门禁失败时不得开始实现。

暂停前 MUST 记录受阻任务、原因、证据、已尝试处理、依赖影响及恢复条件，并继续不依赖该阻塞的独立任务。必要问题可在工作过程中提出；已回答的决策和已有授权必须承接，不重复确认。UI Skeleton 首轮确认等人工门禁仍有效，等待期间不得推进其依赖实现。

没有可执行的独立任务后才可整体暂停并汇报部分完成。用户明确停止或取消时立即停止全部相关工作；用户补充信息或询问进度不等于取消。禁止无限重试同一失败；只有出现新证据、输入或可验证修复时重试。

### 5.3 检查点与恢复

任务相关验证通过后才勾选完成。证据不足、受阻任务和未通过的必需验证保持未完成；不得删除、降低或伪造验收项。必要同步收尾本身应有可追踪任务，避免仅业务代码完成就把 Change 推导为 applied。

上下文压缩后或外部中断恢复时，从 tasks、当前 diff、验证证据和已确认决策承接。只补读变化或缺失内容；未受后续修改影响的通过验证不机械重跑。恢复同一 Change 的剩余任务属于原命令范围。

### 5.4 部分完成状态

部分完成 MUST 报告实际完成数、剩余任务、阻塞及恢复条件，archive_ready 为 false；有完成项时 Change 保持 in_progress，零完成项沿用 proposed，不新增工作流状态枚举。

部分完成同步 MUST 使用无完成事件的事实刷新，先 dry-run 检查派生状态，再移除 dry-run 写入：

```bash
python scripts/sync-workflow-status.py --change <change-id> --sprint <resolved-sprint-id> --dry-run
```

不得在部分完成时发送 `--event opsx.apply`，该事件会将关联 Issue 子文档推进 applied。不得要求 linked trace 已为 applied，也不得建议归档。若预览会错误推进完成态或覆盖人工结论，保留任务与阻塞证据，报告同步阻塞；不得手改 marker 块或伪造状态。使用真实解析的 Sprint，不以无事件刷新绕过 Sprint 准入。

### 5.5 完成与授权边界

仅在全部适用任务及必需验证完成后发送 `opsx.apply` 完成事件，并验证 linked trace 的 applied 与待验收记录。同步失败先修复并重跑；尚未成功时不得报告整个命令完成。archive_ready 还必须考虑人工验收和其他归档门禁，不等同于任务全勾选。

当前 apply 的持续执行不授权自动 archive、发布、部署、进入其他 Change 或创建 follow-up；必要人工确认和不可逆动作授权仍保留。AI Usage 缺失属于 best-effort 诊断，不得单独判定开发失败。


### 5.6 收尾前检查与问题汇总

每次准备最终回复前 MUST 逐项核对未完成任务的原编号、已有授权、前置依赖、资源条件、必需验证和恢复条件，形成当前可执行清单。清单非空即继续实际工作，进度用中间消息报告；不得仅以“已完成一组”“用户询问进度”或“还有人工待验”结束。所有剩余任务真实受阻或用户明确停止才整体暂停；不得仅从总勾选数判断。

必要人工问题 MUST 集中列出当前已知事项并映射受阻任务；承接已有确认，只因新增事实补问。等待期间继续独立工作，未答复不是批准。不要为追求一次提问延迟当前阻塞性问题，也不得把某一页面的确认扩大到无关任务。上下文恢复承接既有确认和失败计数。

每次进度及最终结果分别报告实现完成、自动验证通过、人工待验、外部阻塞。四者是任务维度，不是新增互斥状态；实现完成不代表验证通过，根因确认不代表行为验收通过。所有AC和证据缺口保留。

### 5.7 有限重试

同一工具或验证、目标任务和规范化错误类别构成失败签名；时间戳、随机ID及临时路径不作为新错误。首次失败先诊断，只有新证据、输入、资源变化或可验证修复才允许再次尝试。同一路径连续两次同类失败且无进展后 MUST 记录次数、错误摘要、已尝试措施和恢复条件，切换独立任务。只有新条件被实际验证后才恢复；保留累计失败历史，改命令措辞或重新计数不是新条件。上下文压缩不得清空记录，也不得靠不断声明新方案无限重试。

### 5.8 行为验收与证据

持续执行治理变更 MUST 在两个apply入口分别实际验证首次失败修复、局部阻塞继续、进度问询继续，以及合法暂停、有限重试和已有确认恢复。场景驱动器可以模拟用户或外部条件，但必须标注来源，Agent响应及工具动作必须真实发生。原始会话和prompt仅在内存中处理，不持久化；证据仅存脱敏事件、任务依赖、授权引用、工具结果、规则版本及收尾时机。

`scripts/validate-apply-behavior.py` 校验脱敏事件证据；`scripts/run-apply-behavior.py` 提供隔离场景运行入口。检查器单测和预制事件夹具仅证明检查器能力，不作为实际行为通过。缺实际接口或证据时对应场景待验并说明恢复条件，继续其余工作，不放宽必需验收。测试通过后仍按§5.4–5.5同步实际状态，不自动归档或发布。
