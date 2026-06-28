---
bug_id: BUG-0012-tile-sku-modal-form-field-rules
status: pending_review
created_at: 2026-06-27 11:35:29
updated_at: 2026-06-27 11:35:29
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 对齐 UAT 产品规则（表面工艺非必填、参考价格必填且默认 0），并同步 REQ-0006 `requirement.md` 字段定义与 `acceptance.md` AC-024、AC-015 delta。不得回归 AC-022～AC-030 弹窗布局与其它 SKU 管理功能。

## AC-001 表面工艺 MUST 为非必填

**Given** 管理员打开「新增 SKU」或「编辑 SKU」弹窗  
**When** 查看「表面工艺」字段 Label  
**Then** MUST NOT 显示必填星号 `*`  
**And** 留空表面工艺、填齐其它必填项后点击「创建 SKU」或编辑「保存」 MUST 成功保存

## AC-002 表面工艺留空存储语义 MUST 一致

**Given** 用户创建或编辑 SKU 且未填写表面工艺  
**When** 保存成功并重新打开编辑弹窗或查看列表「规格/工艺」列  
**Then** 后端 MUST 持久化可识别的空值语义（推荐 `"-"`，与现有草稿路径一致）  
**And** MUST NOT 返回「表面工艺不能为空」错误

## AC-003 参考价格 MUST 为必填且新建默认 0

**Given** 管理员打开「新增 SKU」弹窗  
**When** 弹窗初始化完成  
**Then** 「参考价格（元）」输入框 MUST 默认显示 `0`（或等价可提交值）  
**And** Label MUST 带必填星号 `*`  
**And** Label 文案 MUST 仍为「参考价格（元）」（REQ-0006 AC-026）

## AC-004 参考价格空值 MUST 被拦截

**Given** 新增或编辑 SKU 弹窗  
**When** 用户清空参考价格（空字符串 / 仅空格）并尝试「创建 SKU」或「保存」  
**Then** 前端 MUST 展示字段级或表单级错误（REQ-0006 AC-027 风格）  
**And** 后端 create/update API MUST 拒绝 `reference_price` 为 `null` 或未提供的请求

## AC-005 参考价格 0 MUST 合法且正确展示

**Given** SKU 参考价格为 `0`  
**When** 保存后在列表查看「参考价格」列  
**Then** MUST 显示 `¥ 0.00`（两位小数）  
**And** MUST NOT 显示「—」

## AC-006 参考价格格式 MUST 支持两位小数

**Given** 用户输入参考价格  
**When** 输入合法非负小数（如 `268`、`268.5`、`0`）  
**Then** MUST 正常保存  
**And** 列表 MUST 格式化为 `¥ xxx.xx`

## AC-007 上架 MUST NOT 因表面工艺留空而失败

**Given** SKU 已设主图且其它上架条件满足，表面工艺为空或 `"-"`  
**When** 执行上架操作  
**Then** MUST 成功上架  
**And** MUST NOT 返回「表面工艺不完整，无法上架」

## AC-008 草稿保存 MUST 保持可用

**Given** 新增 SKU 弹窗，仅填写 SKU 名称  
**When** 点击「保存草稿」  
**Then** MUST 仍可保存为草稿  
**And** 参考价格 MUST 按 AC-003 默认规则处理（默认 0 写入或草稿路径明确允许 0）

## AC-009 后端 schema 与 API MUST 对齐

**Given** 修复已合并  
**When** 检查 OpenAPI / Pydantic  
**Then** create/update 请求 MUST 要求 `reference_price` 为 number（含 `0.0`）  
**And** `surface_finish` MUST 保持可选  
**And** MUST 运行 Orval 同步前端类型

## AC-010 REQ-0006 文档 MUST 同步 delta

**Given** BUG-0012 修复进入 OpenSpec  
**When** 归档 fix change  
**Then** MUST 更新 `issues/requirements/archive/REQ-0006-tile-sku-management/requirement.md` 字段定义（表面工艺选填、参考价格必填）  
**And** MUST 更新 `acceptance.md`：AC-024 去掉表面工艺 `*`、AC-015 明确价格为 0 时展示 `¥ 0.00`

## AC-011 测试 MUST 补齐

**Given** 进入 `fix-tile-sku-modal-form-field-rules`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** MUST 更新 `TileSkuFormModal` 与 `test_admin_tile_skus` 相关用例  
**And** MUST 在 Change `trace.md` 记录字段规则验收结论

## AC-012 修复 MUST NOT 回归关联 BUG 修复

**Given** BUG-0011（弹窗滚动）、BUG-0009（列表 UI）已修复  
**When** 修改 SKU 弹窗表单  
**Then** 弹窗 880px、主体可滚动、头尾固定 MUST 保持  
**And** 列表分页与表格结构 MUST 不变
