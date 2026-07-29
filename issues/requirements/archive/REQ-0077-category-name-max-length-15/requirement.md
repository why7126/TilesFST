---
requirement_id: REQ-0077-category-name-max-length-15
title: 类目名称输入最多 15 个字符
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0005-tile-category-management
created_at: 2026-07-28 00:04:27
updated_at: 2026-07-28 08:18:00
---

# REQ-0077 类目名称输入最多 15 个字符

## 1. 需求背景

`REQ-0005-tile-category-management` 定义了管理端瓷砖类目管理能力，`REQ-0067-admin-category-edit-modal-validation` 进一步收敛了类目新增 / 编辑弹窗的字段与校验规则，其中类目名称当前最多 10 个字符。

产品方反馈，10 个字符上限在维护部分瓷砖类目时偏短，容易导致运营使用不自然缩写，影响后台主数据可读性，也可能让小程序分类页、商品列表筛选入口中的类目含义不够完整。本需求将类目名称输入上限从 10 个字符放宽到 15 个字符，并要求前端校验、后端兜底、错误提示、接口契约和相关展示回归保持一致。

本需求是 `REQ-0005-tile-category-management` 的子需求 / refinement，覆盖 `REQ-0067-admin-category-edit-modal-validation` 中“类目名称最多 10 个字符”的长度规则；除长度上限外，不改变类目编码自动生成、字符集、同层级唯一、排序权重、层级上限等既有规则。

## 2. 目标用户

- **后台管理员 / 内部员工**：在管理端新增或编辑瓷砖类目时，可以输入更完整的类目名称。
- **运营与商品维护人员**：在后续维护 SKU、筛选类目和核对分类树时，能读取更清晰的类目主数据。
- **前台消费方用户**：通过小程序或 Web 展示端查看分类、筛选入口和商品列表时，类目名称应保持可读且布局稳定。

## 3. 范围

### 3.1 本期包含

- 管理端新增类目、编辑类目弹窗的类目名称长度上限调整为 15 个字符。
- 管理端前端表单即时校验、错误提示和保存前拦截同步调整。
- 后端创建 / 更新类目 API 的 Pydantic Schema 或业务校验同步调整，确保服务端兜底上限为 15 个字符。
- OpenAPI / Orval / API 文档 / 测试在接口契约变化时同步更新。
- 检查并回归管理端类目列表、类目树、小程序分类页、Web 展示端分类入口中对类目名称 15 字符的展示兼容性。
- 测试夹具与最小合法 payload 中如存在 10 字符假设，需同步调整。

### 3.2 本期不包含

- 不调整类目名称允许字符集，仍沿用中文、英文、数字规则。
- 不调整同层级类目名称唯一规则。
- 不调整类目编码自动生成策略和编码展示规则。
- 不调整类目层级上限、上级类目选择规则、排序权重规则或启停规则。
- 不做历史类目数据迁移、清洗或批量重命名。
- 不新增类目别名、多语言名称、简称、SEO 名称或展示名称字段。

## 4. 功能要求

### FR-001 类目名称长度上限调整

- 管理端新增类目弹窗中，类目名称字段 MUST 允许输入 1 到 15 个字符。
- 管理端编辑类目弹窗中，类目名称字段 MUST 允许输入 1 到 15 个字符。
- 类目名称 trim 后 MUST 非空。
- 类目名称超过 15 个字符时，前端 MUST 阻止保存并展示字段级错误。
- 字符数按用户可见字符计数，中文、英文、数字均按 1 个字符计算。
- 现有“最多 10 个字符”规则 MUST 被替换，不得在前端校验、后端校验、错误提示、测试夹具或文档中继续作为有效约束。

### FR-002 后端 API 兜底校验

- 创建类目 API MUST 在服务端接受长度为 1 到 15 个字符的合法类目名称。
- 更新类目 API MUST 在服务端接受长度为 1 到 15 个字符的合法类目名称。
- 创建或更新时，如果类目名称超过 15 个字符，后端 MUST 返回稳定业务错误，且响应结构继续遵守统一 response envelope。
- 后端不得仅依赖前端校验；Pydantic Schema、Service 层或等价业务层 MUST 有兜底。
- 如当前错误码仅表达“名称非法”而不区分具体原因，可沿用现有错误码；如新增错误码，MUST 同步错误码文档、OpenAPI 和测试。

### FR-003 错误提示与表单体验

- 超长错误提示 SHOULD 统一为：`类目名称最多 15 个字符`。
- 空名称、非法字符、同层级重复名称的提示继续沿用既有规则，不因本需求改变。
- 前端 SHOULD 在输入或失焦时展示即时校验结果，并在保存时再次校验。
- 保存失败时弹窗 MUST 保持打开，并将后端字段级错误映射到类目名称字段。

### FR-004 展示兼容性回归

- 管理端类目列表名称列 MUST 能稳定展示 15 字符类目名称，不得与编码、副行、操作列或状态列重叠。
- 管理端左侧类目树 MUST 能稳定展示 15 字符类目名称；空间不足时可使用既有截断 / tooltip 策略，但不得破坏树节点层级识别。
- 小程序分类页、商品列表筛选入口或 Web 展示端分类入口如直接展示类目名称，MUST 验证 15 字符名称下布局不重叠、不溢出关键容器。
- 本需求不要求所有前台端完整展示 15 个字符；若前台视觉空间有限，可沿用合理截断，但数据层不得把合法 15 字符名称拒绝保存。

### FR-005 契约与测试同步

- 若 API Schema 中存在 `max_length=10`、`maxLength: 10` 或等价规则，MUST 更新为 15。
- 若 Orval 生成客户端受 OpenAPI 影响，MUST 重新生成并提交对应生成物。
- 后端测试 MUST 覆盖 15 字符名称可创建 / 可更新，以及 16 字符名称被拒绝。
- 前端表单测试 SHOULD 覆盖 15 字符可保存、16 字符显示错误。
- 小程序或 Web 展示端如存在固定展示测试，应补充 15 字符样例的布局或快照验证。

## 5. UI / UE 约束

- 管理端弹窗继续复用现有 `CategoryFormModal` 或等价 Design System 组件，不新增独立弹窗样式。
- 字段标签、必填标识、帮助文案和错误提示沿用当前管理端表单规范。
- 错误提示必须短、明确、可定位，不使用大段说明文案替代表单校验。
- 类目树、列表和前台展示入口应优先使用既有文本溢出策略；如需要新增 tooltip 或截断样式，必须遵守 semantic token 和现有组件风格。
- UI 不得因为 15 字符名称导致按钮、表格列、树节点、筛选控件出现文字重叠或横向撑破页面。

## 6. 数据与接口约束

- `tile_categories.name` 或等价字段的数据长度约束 MUST 支持至少 15 个用户可见字符。
- 如果数据库字段长度当前大于等于 15 且无需迁移，应在实现说明中记录无需 DB migration 的原因。
- 如果数据库字段、索引或约束当前限制为 10，必须通过 OpenSpec Change 明确数据库迁移方案，并同步 SQLite / MySQL 结构文档与测试。
- 创建 / 更新类目请求体中的名称字段约束必须与 OpenAPI 一致。
- 前端不得手写与后端重复的接口类型；接口契约变化必须通过 Orval 同步。

## 7. 关联需求与变更

| 需求 / Change | 关系 |
|---|---|
| REQ-0005-tile-category-management | 父需求；定义类目管理基础能力 |
| REQ-0067-admin-category-edit-modal-validation | 被本需求覆盖部分长度规则；其他校验规则继续有效 |
| update-category-name-max-length-15 | 预期后续 OpenSpec Change |
| api-governance | API envelope、错误码、OpenAPI / Orval 同步约束 |

## 8. 状态

```yaml
requirement_id: REQ-0077-category-name-max-length-15
priority: P1
status: done
iteration: null
owner: product
parent_requirement: REQ-0005-tile-category-management
expected_openspec_change: update-category-name-max-length-15
readiness: Ready
next_command: /req-opsx REQ-0077-category-name-max-length-15
```
