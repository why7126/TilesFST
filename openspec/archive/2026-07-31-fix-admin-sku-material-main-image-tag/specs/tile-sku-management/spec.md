## MODIFIED Requirements

### Requirement: 管理端 SKU 列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 10/20/50/100）、关键词模糊搜索（商品名称 `name`、系统内部编码 `sku_code`）、`brand_id`、`category_id`、`status`、`material_completeness`（`complete` | `missing_main_image` | `missing_images` | `missing_videos`）筛选。响应 MUST 包含 `items`、`pagination` 与 `summary`（SKU 总数、已上架、待完善、草稿）。列表 MUST 默认按发布状态与业务时间排序：已发布 SKU MUST 优先于未发布 SKU；已发布 SKU MUST 按 `published_at` 降序；未发布 SKU MUST 按 `created_at` 降序；主排序时间为空或重复时 MUST 使用稳定兜底排序，避免分页、刷新或重复请求后顺序跳动。管理端列表 MUST 以商品名称作为主标题，SKU 编码仅作为内部辅助信息或检索依据，视觉层级 MUST 弱于商品名称。管理端 SKU 列表 MUST 展示“发布时间”列，位置 MUST 位于“更新时间”列之前；“发布时间” MUST 使用与“更新时间”完全一致的日期时间格式、空值占位和视觉层级。管理端 SKU 列表筛选区 MUST NOT 展示素材完整度条件筛选，常规列表请求 MUST NOT 提交 `material_completeness`。管理端 SKU 列表素材列 MUST 只展示图片数量与视频数量；素材列 MUST NOT 显示「主图已设」「缺主图」或其他素材状态标签。系统 MUST 使用 `published_at` 表示最近一次发布成功时间，不得直接以 `updated_at` 或 `created_at` 冒充发布时间；后端 MUST 补充管理端列表响应契约并同步 OpenAPI、Orval、接口文档和测试。排序修复 MUST NOT 改变现有分页、筛选、鉴权、错误响应、加载态、空态和失败态。

#### Scenario: 运营人员查询 SKU 列表

- **WHEN** `employee` 携带有效 token 请求 `GET /api/v1/admin/tile-skus`
- **THEN** 系统返回 HTTP 200，`data` 包含分页列表与 summary

#### Scenario: 商品名称与编码搜索

- **WHEN** 管理员输入商品名称关键词或已知 SKU 编码请求列表
- **THEN** 系统 MUST 返回匹配的 SKU
- **AND** 管理端页面 MUST 以商品名称作为匹配结果主展示

#### Scenario: 管理端列表编码弱展示

- **WHEN** 管理端 SKU 列表展示商品信息列
- **THEN** 商品名称 MUST 是主标题
- **AND** SKU 编码如展示 MUST 使用弱化内部辅助样式
- **AND** 上架、下架、删除确认文案 MUST 使用商品名称作为确认对象主标题

#### Scenario: 管理端列表展示发布时间列

- **WHEN** 管理端 SKU 列表渲染表格列
- **THEN** 页面 MUST 展示“发布时间”列
- **AND** “发布时间”列 MUST 位于“更新时间”列之前
- **AND** “发布时间”列的标题、单元格文字样式、对齐方式和行高 MUST 与“更新时间”列保持一致

#### Scenario: 发布时间格式与更新时间一致

- **WHEN** SKU 列表项包含合法发布时间
- **THEN** 管理端 MUST 使用与“更新时间”列相同的格式化函数和时区策略展示“发布时间”
- **AND** 若“更新时间”展示秒级时间，“发布时间”也 MUST 展示秒级时间

#### Scenario: 发布时间空值占位

- **WHEN** SKU 未发布、发布时间为空、字段缺失或时间不可解析
- **THEN** 管理端 MUST 在“发布时间”列展示统一占位，例如 `-`
- **AND** 页面 MUST NOT 展示 `null`、`undefined`、`Invalid Date` 或空白塌陷
- **AND** 该行其他字段和操作 MUST 正常渲染

#### Scenario: 发布时间字段来源明确

- **WHEN** 实现管理端 SKU 列表发布时间展示
- **THEN** 系统 MUST 使用 `published_at` 作为发布时间字段
- **AND** `published_at` MUST 表示最近一次发布成功时间
- **AND** 系统 MUST NOT 直接以 `updated_at` 或 `created_at` 冒充发布时间

#### Scenario: 恢复上架刷新发布时间

- **WHEN** 已下架 SKU 通过 `POST /api/v1/admin/tile-skus/{id}/publish` 恢复上架成功
- **THEN** 系统 MUST 将 `published_at` 刷新为本次发布成功时间
- **AND** 管理端列表与发布响应 MUST 返回刷新后的 `published_at`

#### Scenario: 下架后发布时间响应为空

- **WHEN** 已发布 SKU 通过 `POST /api/v1/admin/tile-skus/{id}/unpublish` 下架成功
- **THEN** 系统 MAY 保留数据库中的历史 `published_at`
- **AND** 管理端列表与下架响应 MUST 返回 `published_at: null`

#### Scenario: 列表响应补充发布时间契约

- **WHEN** 当前管理端 SKU 列表响应不包含发布时间字段
- **THEN** 后端 MUST 补充响应字段并保持分页、summary、鉴权和错误响应结构不变
- **AND** Pydantic Schema、OpenAPI、Orval、接口文档和后端/前端测试 MUST 同步更新

#### Scenario: 已发布 SKU 默认按发布时间降序

- **GIVEN** 管理端存在多条 `PUBLISHED` SKU
- **AND** 这些 SKU 的 `published_at` 不同
- **WHEN** 管理员请求默认 SKU 列表
- **THEN** 已发布 SKU MUST 按 `published_at` 从新到旧返回
- **AND** 系统 MUST NOT 因 `updated_at` 更晚而把发布时间更旧的 SKU 排到前面

#### Scenario: 未发布 SKU 默认按创建时间降序

- **GIVEN** 管理端存在多条非 `PUBLISHED` SKU
- **AND** 这些 SKU 的 `created_at` 不同
- **WHEN** 管理员请求默认 SKU 列表
- **THEN** 未发布 SKU MUST 按 `created_at` 从新到旧返回
- **AND** 系统 MUST NOT 因最近编辑导致 `updated_at` 覆盖草稿创建顺序

#### Scenario: 混排结果分组稳定

- **GIVEN** 管理端 SKU 列表同时包含已发布和未发布 SKU
- **WHEN** 管理员请求默认 SKU 列表
- **THEN** 已发布 SKU MUST 排在未发布 SKU 之前
- **AND** 已发布分组内 MUST 按 `published_at` 降序
- **AND** 未发布分组内 MUST 按 `created_at` 降序
- **AND** 主排序时间为空或重复时 MUST 使用稳定兜底排序

#### Scenario: 搜索筛选分页保持排序契约

- **WHEN** 用户执行分页、关键词搜索、品牌筛选、类目筛选或状态筛选
- **THEN** 列表 MUST 继续遵循发布状态与业务时间排序契约
- **AND** 翻页、刷新或重复请求 MUST NOT 出现重复、漏项或顺序跳动
- **AND** 排序修复 MUST NOT 改变加载态、空态、失败态和行操作行为

#### Scenario: 管理端页面不展示素材完整度筛选

- **WHEN** 管理端 SKU 列表筛选区渲染
- **THEN** 页面 MUST NOT 展示素材完整度条件筛选控件
- **AND** 页面触发常规列表请求时 MUST NOT 提交 `material_completeness`

#### Scenario: 素材列只显示图片视频数量

- **GIVEN** 管理端 SKU 列表项存在任意图片/视频数量组合
- **WHEN** 管理端渲染该行「素材」列
- **THEN** 素材列 MUST 显示图片数量与视频数量
- **AND** 素材列 MUST NOT 显示「主图已设」「缺主图」或其他素材状态标签

#### Scenario: 素材不完整状态仍可通过数量识别

- **GIVEN** 管理端 SKU 列表存在缺图、缺视频或素材不完整的 SKU
- **WHEN** 管理员查看素材列
- **THEN** 管理端 MUST 仍能通过图片数量与视频数量识别素材缺失
- **AND** 移除素材状态标签与素材完整度筛选控件 MUST NOT 影响分页、关键词筛选、品牌筛选、类目筛选、状态筛选、状态列、操作列或 SKU 维护操作
