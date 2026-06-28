---
bug_id: BUG-0036-banner-modal-datetime-picker
status: pending_review
created_at: 2026-06-28 16:20:00
updated_at: 2026-06-28 16:20:00
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> **裁定说明（prototype HTML > capture）**：弹窗「有效期」采用 **单字段区间** 展示，格式 `YYYY-MM-DD HH:mm 至 YYYY-MM-DD HH:mm`（分钟精度，对齐 `banner-management-modal-*.html` 示例 `2026-06-01 00:00 至 2026-07-01 23:59`）。**不要求** UI 选择秒；提交时 `valid_from` 秒为 `00`、`valid_to` 秒为 `59`（策略填充）。MODIFIED 消化 capture 中 `yyyy/mm/dd hh:mm:ss` 秒级交互要求。
>
> 修复 MUST 满足 REQ-0016 **AC-027**、**AC-013**、**AC-051**，且不得回归 AC-025～AC-039 弹窗功能。

## AC-001 弹窗 MUST 提供可操作的 DateTime 选择（时分）

**Given** admin 已登录 Web 管理端（Chrome 或 Safari 桌面，local 或 Docker）  
**When** 打开 Banner 新增/编辑弹窗，操作「有效期」字段  
**Then** MUST 能通过 UI **明确选择**日期、小时、分钟（非仅日期、非依赖浏览器原生 `datetime-local` 不稳定控件）  
**And** MUST NOT 使用裸 `<input type="datetime-local">` 作为最终方案

## AC-002 弹窗有效期 MUST 为单字段区间（对齐 HTML 原型）

**Given** 弹窗已打开  
**When** 观察「有效期」表单项  
**Then** MUST 为 **一个** 占满整行的「有效期」字段（`banner-form-row full`）  
**And** 展示/编辑形态 MUST 为区间文案：`{开始} 至 {结束}`  
**And** 单段格式 MUST 为 `YYYY-MM-DD HH:mm`（24 小时，分钟精度）  
**And** MUST NOT 拆为两个独立标签「有效期开始」「有效期结束」输入框（与当前实现不同）

## AC-003 空值与长期有效 MUST 支持

**Given** 弹窗已打开  
**When** 用户清空有效期或仅配置开始/结束一侧（按 fix change design 约定）  
**Then** MUST 允许保存（与 REQ-0016：空 `valid_to` = 长期有效）  
**And** 空值语义 MUST 与 `requirement.md` / 后端校验一致

## AC-004 提交 payload MUST 为合法 ISO datetime

**Given** 用户配置有效期 `2026-06-01 00:00 至 2026-07-01 23:59`  
**When** 点击「保存 Banner」  
**Then** 请求 body 的 `valid_from` MUST 为可解析 ISO datetime（如 `2026-06-01T00:00:00+00:00` 或等价带时区形式）  
**And** `valid_to` MUST 为 `2026-07-01T23:59:59+00:00`（或等价，结束秒为 `59`）  
**And** 后端 MUST 返回 200，无「有效期格式无效」类错误

## AC-005 编辑回填 MUST 保留配置时刻

**Given** 已保存 Banner 且 `valid_from` / `valid_to` 均有值  
**When** 再次打开编辑弹窗  
**Then** 有效期区间 MUST 正确回填为对应 `YYYY-MM-DD HH:mm 至 YYYY-MM-DD HH:mm`  
**And** 再次保存 MUST NOT 无意改变已存时刻（除秒策略填充外）

## AC-006 列表「有效期」列 MUST 与配置一致

**Given** 已配置有效期的 Banner  
**When** 查看列表「有效期」列  
**Then** MUST 展示开始与结束时刻（现有两行或区间展示均可）  
**And** 展示精度 MUST 至少到分钟，格式可读（如 `YYYY-MM-DD HH:mm` 或 `replace('T',' ')` 等价）  
**And** MUST 与弹窗配置一致

## AC-007 time_status MUST 按配置计算

**Given** 已上线 Banner，`valid_from` 在未来  
**When** 查看列表状态  
**Then** MUST 展示「待生效」或等价 `time_status=PENDING`  
**Given** `valid_to` 已过  
**Then** MUST 展示「已过期」或等价 `time_status=EXPIRED`  
**And** 上线按钮 disabled 规则 MUST 与修复前一致（已过期不可上线）

## AC-008 四套 jump_type 弹窗 MUST 均通过 AC-001～AC-002

**Given** 修复完成  
**When** 分别打开 `NO_JUMP`、`SKU_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE` 新增弹窗  
**Then** 有效期 DateTime 交互 MUST 一致且符合 AC-001～AC-002

## AC-009 修复范围 MUST 为前端（+ 可选共享 UI 组件）

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、OpenAPI 字段名、SQLite schema  
**And** MUST NOT 要求 Orval 重生成（除非仅文档同步）

## AC-010 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI  
**Then** DateTime 控件 MUST 使用 semantic token / `cn()`  
**And** MUST NOT 新增裸 Hex  
**And** 新增组件 SHOULD 置于 `shared/ui`（或 fix change design 指定路径）

## AC-011 弹窗 HTML 并排验收（REQ-0016 AC-051）

**Given** 修复完成  
**When** 1440×1024 并排对比弹窗与 `prototype/web/banner-management-modal-{type}.html`  
**Then** 单字段「有效期」区间形态 MUST 视觉/交互对齐 HTML 原型  
**And** MUST 在 Change `trace.md` 记录并排结论

## AC-012 测试与记录 MUST 补齐

**Given** 进入 `fix-banner-modal-datetime-picker`（或 `fix-banner-modal-ui`）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 Vitest（区间解析、ISO 提交、回填）  
**And** MUST 更新 Change trace，关闭 AC-027 有效期相关项

## AC-013 REQ-0016 AC-027 对齐确认

**Given** BUG-0036 修复完成  
**When** 对照 `acceptance.md` AC-027（公共字段含「有效期」）  
**Then** 有效期字段 MUST 可操作且对齐 prototype HTML 单字段区间形态
