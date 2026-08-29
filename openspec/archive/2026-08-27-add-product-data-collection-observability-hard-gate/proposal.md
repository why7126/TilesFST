## 背景

`docs/standards/product-data-collection-observability.md` 已经建立产品数据采集与链路观测事实源，但如果入口、规则、技能和实现级脚本没有形成硬门禁，后续 API、DB、日志审计、行为埋点、Task Trace 与端请求封装变更仍可能无声明、无验收地绕过该规范。REQ-0127 要把“应当引用规范”升级为可读、可声明、可校验、可验收的流程约束。

## 变更内容

- 将产品数据采集与链路观测规范门禁接入 `AGENTS.md` 任务读取路由和完成检查清单。
- 在 API、数据库、测试、文档治理、需求管理、Sprint / OpenSpec 流程等相关规则中追加触发条件、声明字段、N/A 原因和验收要求。
- 在 req / opsx / sprint 技能检查清单中加入必读、必声明、必验收要求。
- 新增或增强实现级校验脚本，检查入口、规则、技能和 active Change 是否引用或声明该门禁。
- 不复制完整规范正文，详细采集模型继续以 `docs/standards/product-data-collection-observability.md` 为事实源。
- 不直接修改业务 API、DB、Web、小程序或 App 代码。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `product-data-collection-observability-standard`: 在已有通用采集规范能力上增加流程硬门禁，约束相关变更在 REQ、OpenSpec、Sprint、实现和归档阶段完成规范读取、适用性声明、N/A 原因、校验脚本和验收证据。

## 影响

- 文档入口：影响 `AGENTS.md` 与相关 `rules/` 的读取路由、触发条件和完成检查清单。
- 技能：影响 `.agents/skills/req-*`、`.agents/skills/opsx-*`、`.agents/skills/sprint-*` 中与需求、Change、实现、归档、迭代范围相关的检查清单。
- 校验脚本：新增或增强 `scripts/validate-product-data-observability-gates.py`，并补充对应测试。
- OpenSpec / Sprint / REQ：本 Change 来源于 `REQ-0127-product-data-collection-observability-hard-gate`，已纳入 `sprint-026`；后续 Workflow Sync 需要把 Change 回填到同一 Sprint scope。
- API / DB / Orval：本 Change 本身不改业务接口、Pydantic Schema、SQLite/MySQL schema、OpenAPI 或 Orval；它要求后续触发范围内的 Change 同步或声明 N/A。
- Web / 小程序 / App：本 Change 本身不改端侧代码；请求封装、行为埋点或链路 ID 透传变更会触发门禁。
