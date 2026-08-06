---
change_id: optimize-admin-media-list-thumbnails
capability: tile-sku-management
created_at: 2026-08-05 09:40:00
updated_at: 2026-08-05 09:40:00
---

## MODIFIED Requirements

### Requirement: 管理端 SKU 列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 10/20/50/100）、关键词模糊搜索（商品名称 `name`、系统内部编码 `sku_code`）、`brand_id`、`category_id`、`status`、`material_completeness`（`complete` | `missing_main_image` | `missing_images` | `missing_videos`）筛选。`category_id` 在管理端 SKU 列表中 MUST 表示类目子树筛选：当传入父类目 ID 时，结果 MUST 包含该父类目自身及所有子孙类目的 SKU；当传入叶子类目 ID 时，结果 MUST 返回该叶子类目范围内 SKU。管理端 SKU 页类目筛选 UI MUST 使用单个级联下拉控件展示完整类目树，不得在筛选区并排生成多个类目筛选框；点击有下级的当前类目时，控件 MUST 在同一下拉层右侧展开下级类目面板，并支持选择任意层级类目；当前选择 MUST 展示在下拉触发框内，筛选项下方 MUST NOT 额外展示“当前：xxx”类辅助文案；下拉层 MUST 位于筛选控件下方并浮于 SKU 列表之上，不得被列表遮挡；品牌、类目、状态三个筛选下拉 MUST 使用一致的触发框、下拉层位置、层级、选项样式和选中态。响应 MUST 包含 `items`、`pagination` 与 `summary`（SKU 总数、已上架、待完善、草稿）。

列表 MUST 默认按上架状态与业务时间排序：未上架 SKU MUST 优先于已上架 SKU；未上架 SKU（`status != PUBLISHED`）MUST 按 `created_at` 降序；已上架 SKU（`status = PUBLISHED`）MUST 按 `published_at` 降序；主排序时间为空或重复时 MUST 使用稳定兜底排序，避免分页、刷新或重复请求后顺序跳动。该排序 MUST 在分页前对完整结果集生效，不能只对当前页排序。搜索、品牌筛选、类目筛选、状态筛选、素材完整度筛选和分页后，列表 MUST 继续遵循该排序契约。

管理端列表 MUST 以商品名称作为主标题，SKU 编码仅作为内部辅助信息或检索依据，视觉层级 MUST 弱于商品名称。管理端 SKU 列表 MUST 展示“发布时间”列，位置 MUST 位于“更新时间”列之前；“发布时间” MUST 使用与“更新时间”完全一致的日期时间格式、空值占位和视觉层级。系统 MUST 使用 `published_at` 表示最近一次发布成功时间，不得直接以 `updated_at` 或 `created_at` 冒充发布时间；后端 MUST 补充管理端列表响应契约并同步 OpenAPI、Orval、接口文档和测试。SKU 列表筛选区 MUST 参照其他管理端列表页铺满 filter-card 可用宽度，不得因预留多余网格列导致右侧出现空白；筛选项与重置按钮 MUST 按实际控件数量分配列宽。管理端 SKU 列表表头字段 MUST 保持单行显示；列数较多或窗口宽度不足时，列表 MUST 通过横向滚动、合理最小列宽或等价布局策略完整查看全部列，且表头与正文列 MUST 保持对齐。排序优化和表头修复 MUST NOT 新增显式排序控件、创建时间筛选或发布时间筛选，MUST NOT 改变现有分页、筛选、鉴权、错误响应、加载态、空态、失败态和行操作行为。

管理端 SKU 列表项存在主图时，响应 MUST 新增 `main_image_thumbnail_url` 或等价主图缩略图字段，并保留 `main_image_url` 原图字段语义。`main_image_thumbnail_url` MUST 基于后端受控媒体路径派生，不得要求前端直连未授权对象存储。管理端 SKU 列表图片展示 MUST 优先使用 `main_image_thumbnail_url`，当缩略图字段为空、加载失败或不可读时 MUST 回退 `main_image_url` 或既有无图占位。详情、编辑、上传预览和放大预览场景 SHALL 继续使用原图或原文件。新增字段 MUST 同步 OpenAPI、Orval、接口文档和测试。

#### Scenario: SKU 列表表头单行显示

- **WHEN** 管理员在常用桌面宽度打开管理后台 SKU 列表
- **THEN** 表头字段 MUST 保持单行显示

#### Scenario: SKU 列表列数较多时完整查看

- **WHEN** SKU 列表列数较多或窗口宽度不足
- **THEN** 用户 MUST 能通过横向滚动或等价布局完整查看所有列
- **AND** 表头与正文列 MUST 保持对齐

#### Scenario: SKU 列表主图缩略图优先

- **GIVEN** SKU 列表项存在主图对象
- **WHEN** 管理端请求 `GET /api/v1/admin/tile-skus`
- **THEN** 响应项 MUST 包含 `main_image_thumbnail_url`
- **AND** 响应项 MUST 保留 `main_image_url`
- **AND** Web 管理端列表 MUST 优先加载 `main_image_thumbnail_url`

#### Scenario: SKU 列表缩略图回退

- **GIVEN** SKU 列表项存在 `main_image_url` 但 `main_image_thumbnail_url` 为空、404 或加载失败
- **WHEN** 管理端渲染 SKU 列表图片
- **THEN** 页面 MUST 回退原图或既有无图占位
- **AND** 页面 MUST NOT 显示浏览器默认破图
- **AND** 表格行高、分页、筛选和操作列布局 MUST 保持稳定
