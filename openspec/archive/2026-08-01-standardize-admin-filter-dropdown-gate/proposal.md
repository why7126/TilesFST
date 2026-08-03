## Why

管理端筛选下拉已经通过 BUG-0098 修复沉淀出共享组件、设计系统约束和最佳实践文档，但后续新增或修改列表页时仍容易只看单页实现，遗漏统一下拉 gate。需要把“进入最佳实践与 apply checklist”固化为 OpenSpec 契约，让 `/opsx-apply` 和页面验收在动手前就检查统一筛选下拉基准。

## What Changes

- 将管理端筛选下拉统一 gate 明确纳入 Design System：新增或修改管理端筛选区下拉时，必须先对照最佳实践、共享组件、设计系统样例和页面矩阵。
- 为 apply checklist 增加筛选下拉专门检查项：确认 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper 被复用，页面级一次性弹层样式不得绕过基准。
- 明确验收覆盖：普通下拉、可搜索下拉、空态、加载态、禁用态、已选中态、窄屏、弹层不裁切、筛选语义和查询参数不变。
- 不新增业务 API、数据库表、环境变量或用户可见业务功能。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `design-system`: 强化管理端筛选下拉统一 gate，要求最佳实践与设计系统样例成为新增/修改管理端筛选下拉的验收入口。
- `agent-workflow-tooling`: 强化 `/opsx-apply` checklist，对涉及管理端列表筛选下拉的 Change 增加最佳实践回读、共享组件复用和测试验收门禁。

## Impact

- 影响 OpenSpec：`openspec/specs/design-system/spec.md`、`openspec/specs/agent-workflow-tooling/spec.md` 的 delta spec。
- 影响文档：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` 可能补充更明确的 apply checklist。
- 影响技能/流程：`.agents/skills/opsx-apply/SKILL.md` 或等价 apply checklist 文档可能新增管理端筛选下拉 gate。
- 影响测试：管理端筛选下拉共享组件、页面矩阵或文档门禁测试按实现补充。
- 不影响 API、数据库、Orval、小程序、媒体上传、Docker Compose。
