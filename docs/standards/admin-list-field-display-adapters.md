---
purpose: 管理端列表字段展示 adapter 检查表
content: image/name/fallback adapter 规则、首批列表盘点、横切验收与 N/A 记录
source: REQ-0095-admin-list-field-display-adapter-checklist / standardize-admin-list-field-display-adapters
update_method: 管理端列表展示字段、Design System 或横切 UI gate 变化时同步更新
created_at: 2026-08-04 09:00:00
updated_at: 2026-08-04 09:00:00
---

# 管理端列表字段展示 adapter 检查表

## 1. 适用范围

本文档用于管理端 CRUD 列表页在设计、实现、验收和回归时统一检查图片、名称和兜底展示。首批覆盖：

| 列表 | image adapter | name adapter | fallback adapter |
|---|---|---|---|
| 品牌列表 | 适用 | 适用 | 适用 |
| 证书列表 | 适用 | 适用 | 适用 |
| SKU 列表 | 适用 | 适用 | 适用 |
| Banner 列表 | 适用 | 适用 | 适用 |

后续分类、规格、用户、审计日志、上传资源等列表新增或重构时，必须按同一格式标记适用、推荐或 N/A。

## 2. 检查表字段

| 字段 | 要求 |
|---|---|
| 列表 | 写明管理端页面或业务对象。 |
| Adapter | 取值为 `image`、`name`、`fallback`。 |
| 检查项 | 写成可测试的单项规则，避免笼统描述。 |
| 期望表现 | 描述用户可观察结果，例如行高稳定、文案明确、无敏感信息泄露。 |
| 验证方式 | 自动测试、人工样例、源码检查或 N/A 理由。 |
| 状态 | `required`、`recommended`、`not_applicable`、`todo`、`passed`、`failed`。 |

## 3. image adapter

| 检查项 | 期望表现 | 验证方式 |
|---|---|---|
| 图片来源优先级 | 缩略图优先；缩略图缺失时回退原图或受控媒体 URL。 | 构造含缩略图、仅原图、无图三类样例。 |
| 主图选择 | 多图对象优先使用 `is_main`；无主图时按排序或第一张兜底。 | 使用多图 fixture 或接口样例验证。 |
| 无图态 | 无图片时显示统一占位、首字母或文件类型标识，不留空白。 | 人工样例或组件测试。 |
| 加载失败态 | 图片 404 或加载失败时回到稳定 fallback，不造成行高、列宽、操作列或分页抖动。 | 人工断网/错误 URL 样例；必要时截图记录。 |
| 容器尺寸 | 图片容器尺寸固定，裁切策略明确。 | 桌面和窄屏视口检查。 |
| 可访问性语义 | 识别性图片提供 `alt` 或 `aria-label`；纯装饰图片可空 alt。 | 源码检查或 Testing Library 查询。 |

## 4. name adapter

| 检查项 | 期望表现 | 验证方式 |
|---|---|---|
| 主名称来源 | 品牌名、证书名、SKU 名称、Banner 标题等主字段明确。 | 对照接口字段和页面渲染。 |
| 辅助名称来源 | 编号、品牌、分类、文件名、跳转目标等辅助字段层级弱于主名称。 | 人工样例或 DOM 断言。 |
| 空名称 | 空字符串、仅空格或字段缺失时显示统一可读兜底。 | 空字段 fixture。 |
| 长名称 | 长文本截断、换行或 tooltip 策略明确，不撑开表格。 | 长文本样例和窄屏检查。 |
| 去重 | 同一行避免重复展示语义相同的名称、编号或文件名。 | 人工审查或快照。 |
| 关联缺失 | 关联对象已删除或无权限时展示明确文案，不误导为未配置。 | 关联缺失样例。 |

## 5. fallback adapter

| 语义 | 建议展示 | 说明 |
|---|---|---|
| 未设置 | `未设置` | 用户可配置但尚未填写。 |
| 无数据 | `—` | 后端无值且无业务动作含义。 |
| 不适用 | `N/A` 或中文说明 | 当前列表或字段不适用。 |
| 加载失败 | `加载失败` 或稳定占位 | 媒体或关联数据读取失败。 |
| 未知枚举值 | 显示安全原值或 `未知状态` | 不得空白，不得崩溃。 |
| 无权限 | `无权限查看` 或隐藏敏感字段 | 不得泄露敏感信息。 |
| 接口字段缺失 | 稳定兜底 | 页面不得崩溃，验收记录需追踪契约问题。 |

## 6. 首批列表盘点

| 列表 | 已有可复用逻辑 | 待治理风险 |
|---|---|---|
| 品牌列表 | `getBrandLogoSrc`、`getBrandInitials` | Logo 加载失败、无 Logo、名称异常应与其他列表统一。 |
| 证书列表 | 证书类型、有效期、展示状态 helper | 图片/PDF/文件类型标识、证书编号和发证机构空值需统一。 |
| SKU 列表 | SKU 状态、时间展示 helper | 主图选择、缺主图、素材缺失、长名称和未知状态需统一。 |
| Banner 列表 | Banner 状态、跳转类型、图片来源 helper | 关联 SKU/品牌缺失、展示图缺失、有效期未设置需统一。 |

本检查表不要求一次性重构所有列表。后续 OpenSpec design 应按影响范围决定是仅补文档、抽公共 adapter 函数、抽单元格组件，还是逐页治理。

## 7. 横切验收

命中 `admin-list` 的后续 Change 必须引用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，并记录以下 gate：

- 分页 DOM 与用户管理基准一致：左侧 `page-summary`，右侧 `page-right` 页码和每页条数。
- 操作成功/失败反馈使用 fixed toast，不得推挤 hero、筛选区或表格。
- 状态变更、启停、上架/下架、删除等危险操作使用 Design System confirm modal。
- 禁止新增 `window.confirm`。
- 不修改列表 DOM、toast 或危险操作时，必须写明 N/A 理由。

若命中筛选下拉，还必须执行 `admin-filter-dropdown` gate：优先复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper，并验证 open/select/clear/reset、禁用/选中/空/加载态、overlay clipping 和 query 语义。

## 8. 分层验收 N/A 记录

仅落检查表或文档时，推荐记录：

```yaml
db:
  status: not_applicable
  reason: 不新增或修改持久化模型
api:
  status: not_applicable
  reason: 不新增或修改接口契约
upload:
  status: not_applicable
  reason: 不调整上传链路、缩略图生成或对象存储策略
orval:
  status: not_applicable
  reason: 无 OpenAPI contract 变化
docker:
  status: not_applicable
  reason: 不修改 Docker、Nginx、端口或环境变量
```
