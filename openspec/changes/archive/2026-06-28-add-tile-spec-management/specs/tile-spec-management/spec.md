## ADDED Requirements

### Requirement: 瓷砖规格数据模型

系统 MUST 在 SQLite 中维护 `tile_specs` 表。表 MUST 包含：`id`、`width_mm`（1–9999 NOT NULL）、`length_mm`（1–9999 NOT NULL）、`thickness_mm`（可选 REAL，1 位小数）、`unit`（NOT NULL DEFAULT `'mm'`）、`display_name`（NOT NULL，服务端生成）、`sort_order`（正整数 NOT NULL）、`status`（`ENABLED` | `DISABLED`）、`sku_count`（非负整数 DEFAULT 0）、`remark`（可选，最大 200 字）、`created_at`、`updated_at`。业务唯一键 MUST 为 `(width_mm, length_mm, unit)`。`display_name` MUST 按 `{width_mm}×{length_mm}{unit}` 生成。

#### Scenario: 新规格默认启用

- **WHEN** 通过 API 创建规格且未指定 status
- **THEN** 数据库记录 `status` MUST 为 `ENABLED`
- **AND** `unit` MUST 为 `mm`

#### Scenario: 宽长单位唯一约束

- **WHEN** 插入或更新导致 `(width_mm, length_mm, unit)` 与已有记录冲突
- **THEN** 系统 MUST 拒绝并返回 `TILE_SPEC_DUPLICATED`

### Requirement: 管理端规格列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-specs`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 20/50/100）、关键词模糊搜索（`display_name`、宽/长数值、备注）与状态筛选。响应 MUST 包含 `items`、`pagination` 与 `summary`（规格总数、启用数、停用数、未关联 SKU 数）。

#### Scenario: 运营人员查询规格列表

- **WHEN** `employee` 携带有效 token 请求 `GET /api/v1/admin/tile-specs`
- **THEN** 系统返回 HTTP 200，`data` 包含分页列表与 summary

#### Scenario: 非管理端用户被拒绝

- **WHEN** `store_owner` 或未认证用户请求 `GET /api/v1/admin/tile-specs`
- **THEN** 系统 MUST 返回 HTTP 401 或 403

### Requirement: 管理端规格创建与更新 API

系统 MUST 提供 `POST /api/v1/admin/tile-specs` 与 `GET/PUT /api/v1/admin/tile-specs/{id}`，`admin` 与 `employee` 可调用。POST/PUT MUST 接受 `width_mm`、`length_mm`、可选 `thickness_mm`、`sort_order`、可选 `remark`；MUST NOT 接受客户端提交的 `display_name` 或 `status`（启停走专用端点）。服务端 MUST 生成 `display_name` 并校验唯一键。

#### Scenario: 创建规格成功

- **WHEN** 提交合法宽、长与正整数 `sort_order`
- **THEN** 系统返回 HTTP 200 与规格对象
- **AND** `display_name` MUST 为 `{width}×{length}mm`
- **AND** `status` MUST 为 `ENABLED`

#### Scenario: 更新规格宽长

- **WHEN** PUT 修改 `width_mm` 或 `length_mm`
- **THEN** 系统 MUST 重新生成 `display_name`
- **AND** MUST 执行唯一性校验

### Requirement: 管理端规格启停 API

系统 MUST 提供 `POST /api/v1/admin/tile-specs/{id}/enable` 与 `POST /api/v1/admin/tile-specs/{id}/disable`，`admin` 与 `employee` 可调用。已关联 SKU（`sku_count > 0`）的规格 MUST 允许停用。

#### Scenario: 停用规格

- **WHEN** 对 `ENABLED` 规格调用 disable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `DISABLED`

#### Scenario: 启用规格

- **WHEN** 对 `DISABLED` 规格调用 enable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `ENABLED`

### Requirement: 管理端规格条件删除 API

系统 MUST 提供 `DELETE /api/v1/admin/tile-specs/{id}`，`admin` 与 `employee` 可调用。仅当 `sku_count = 0` 且 `status = DISABLED` 时 MUST 允许删除；否则 MUST 返回 `TILE_SPEC_DELETE_FORBIDDEN`。

#### Scenario: 允许删除

- **WHEN** 规格 `sku_count` 为 0 且 `status` 为 `DISABLED`
- **THEN** 系统 MUST 删除记录并返回 HTTP 200

#### Scenario: 禁止删除已关联 SKU

- **WHEN** 规格 `sku_count` > 0
- **THEN** 系统 MUST 返回 HTTP 409，`TILE_SPEC_DELETE_FORBIDDEN`

#### Scenario: 禁止删除启用状态规格

- **WHEN** 规格 `status` 为 `ENABLED` 且 `sku_count` 为 0
- **THEN** 系统 MUST 返回 HTTP 409，`TILE_SPEC_DELETE_FORBIDDEN`

### Requirement: 规格 sku_count 维护

系统 MUST 在 SKU 创建、删除或变更 `spec_id` 时维护对应 `tile_specs.sku_count`。计数 MUST NOT 为负。

#### Scenario: SKU 绑定规格

- **WHEN** SKU 创建或更新设置 `spec_id=S`
- **THEN** `tile_specs` 中 id=S 的 `sku_count` MUST 增加相应数量
- **AND** 若变更 spec，旧规格 MUST 减 1、新规格 MUST 加 1

### Requirement: 历史 SKU 规格迁移

系统 MUST 提供 migration 或一次性脚本，尝试将现有 `tiles.size` 匹配至 `tile_specs.display_name` 或解析 `(\d+)×(\d+)mm` 回填 `tiles.spec_id`。匹配失败 MUST 保留原 `size` 且 `spec_id` 可为 NULL。

#### Scenario: 自动匹配成功

- **WHEN** `tiles.size` 等于某规格 `display_name`
- **THEN** migration MUST 写入对应 `spec_id`
- **AND** MUST NOT 删除原 `size` 文本

#### Scenario: 自动匹配失败

- **WHEN** 无法匹配任何规格
- **THEN** `spec_id` MUST 保持 NULL
- **AND** 运营 MUST 可在 SKU 编辑页手动选择规格后保存

### Requirement: 瓷砖规格管理 PNG 视觉验收 Gate

规格管理页视觉对齐 MUST 通过 HTML 原型并排验收 gate；PNG Golden Reference 补齐后 MUST 纳入 sprint acceptance-report。

#### Scenario: 列表页并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/tile-specs` 与 `tile-size-management.html`
- **THEN** checklist（Shell、Sidebar active、4 指标卡、状态筛选、状态列、启停操作、删除规则、分页）MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗并排验收

- **WHEN** 打开新增/编辑弹窗并排 `tile-size-management-modal.html`
- **THEN** checklist（720px、宽长、只读 display_name、无状态字段、实时重复校验）MUST pass
