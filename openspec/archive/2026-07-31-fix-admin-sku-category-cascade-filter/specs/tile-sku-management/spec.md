## MODIFIED Requirements

### Requirement: 管理端 SKU 列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 10/20/50/100）、关键词模糊搜索（商品名称 `name`、系统内部编码 `sku_code`）、`brand_id`、`category_id`、`status`、`material_completeness`（`complete` | `missing_main_image` | `missing_images` | `missing_videos`）筛选。`category_id` 在管理端 SKU 列表中 MUST 表示类目子树筛选：当传入父类目 ID 时，结果 MUST 包含该父类目自身及所有子孙类目的 SKU；当传入叶子类目 ID 时，结果 MUST 返回该叶子类目范围内 SKU。管理端 SKU 页类目筛选 UI MUST 使用单个级联下拉控件展示完整类目树，不得在筛选区并排生成多个类目筛选框；点击有下级的当前类目时，控件 MUST 在同一下拉层右侧展开下级类目面板，并支持选择任意层级类目；当前选择 MUST 展示在下拉触发框内，筛选项下方 MUST NOT 额外展示“当前：xxx”类辅助文案；下拉层 MUST 位于筛选控件下方并浮于 SKU 列表之上，不得被列表遮挡；品牌、类目、状态三个筛选下拉 MUST 使用一致的触发框、下拉层位置、层级、选项样式和选中态。响应 MUST 包含 `items`、`pagination` 与 `summary`（SKU 总数、已上架、待完善、草稿）。列表 MUST 默认按发布状态与业务时间排序：已发布 SKU MUST 优先于未发布 SKU；已发布 SKU MUST 按 `published_at` 降序；未发布 SKU MUST 按 `created_at` 降序；主排序时间为空或重复时 MUST 使用稳定兜底排序，避免分页、刷新或重复请求后顺序跳动。管理端列表 MUST 以商品名称作为主标题，SKU 编码仅作为内部辅助信息或检索依据，视觉层级 MUST 弱于商品名称。管理端 SKU 列表 MUST 展示“发布时间”列，位置 MUST 位于“更新时间”列之前；“发布时间” MUST 使用与“更新时间”完全一致的日期时间格式、空值占位和视觉层级。系统 MUST 使用 `published_at` 表示最近一次发布成功时间，不得直接以 `updated_at` 或 `created_at` 冒充发布时间；后端 MUST 补充管理端列表响应契约并同步 OpenAPI、Orval、接口文档和测试。排序修复 MUST NOT 改变现有分页、筛选、鉴权、错误响应、加载态、空态和失败态。

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

#### Scenario: 类目筛选使用级联选择控件

- **GIVEN** 管理后台存在多层级瓷砖类目
- **WHEN** 管理员打开 SKU 页类目筛选控件
- **THEN** 管理端 MUST 使用单个级联下拉控件展示完整类目树
- **AND** 管理员 MUST 能选择一级、二级、三级或更深层级类目
- **AND** 控件 MUST NOT 在筛选区并排展示多个类目筛选框
- **AND** 点击有下级的类目时，控件 MUST 在当前下拉层右侧展示下级类目面板
- **AND** 控件 MUST 在下拉触发框内展示当前选择路径
- **AND** 筛选项下方 MUST NOT 额外展示“当前：xxx”类辅助文案
- **AND** 下拉层 MUST 位于筛选控件下方并浮于 SKU 列表之上，不得被列表遮挡
- **AND** 品牌、类目、状态三个筛选下拉 MUST 保持触发框、下拉位置、菜单层级、选项样式和选中态一致

#### Scenario: 父类目筛选包含子孙 SKU

- **GIVEN** 某父类目下存在多个子孙类目
- **AND** 这些子孙类目下存在 SKU
- **WHEN** 管理员以该父类目筛选 SKU 列表
- **THEN** 系统 MUST 返回该父类目自身及所有子孙类目的 SKU
- **AND** 系统 MUST NOT 仅返回直接归属该父类目自身的 SKU

#### Scenario: 子类目筛选保持准确

- **GIVEN** 管理端存在二级或更深层级类目
- **WHEN** 管理员选择该子类目筛选 SKU 列表
- **THEN** 系统 MUST 返回该子类目子树范围内的 SKU
- **AND** 系统 MUST NOT 返回无关父级或兄弟类目的 SKU

#### Scenario: 类目筛选可清空

- **GIVEN** 管理员已选择任意层级类目
- **WHEN** 管理员点击重置或清空类目级联选择
- **THEN** 类目筛选条件 MUST 清空
- **AND** SKU 列表 MUST 恢复为不受类目限制的结果

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

- **WHEN** 用户执行分页、关键词搜索、品牌筛选、类目筛选、状态筛选或素材完整度筛选
- **THEN** 列表 MUST 继续遵循发布状态与业务时间排序契约
- **AND** 翻页、刷新或重复请求 MUST NOT 出现重复、漏项或顺序跳动
- **AND** 类目子树筛选 MUST NOT 改变加载态、空态、失败态和行操作行为

#### Scenario: 素材完整度筛选缺主图

- **WHEN** 管理员以 `material_completeness=missing_main_image` 请求列表
- **THEN** 系统 MUST 仅返回无主图 SKU
