# 瓷砖 SKU 管理规范

## Purpose
定义瓷砖 SKU 数据模型、列表筛选、创建更新、上下架删除、图片视频上传、弹窗交互与视觉验收要求，确保商品资料可维护且展示素材完整。
## Requirements
### Requirement: SKU 管理视觉验收 Gate

SKU 管理页视觉对齐 MUST 通过 **HTML 原型**并排验收 gate。`prototype/images/*.png` 为可选 Golden Reference；有则纳入 sprint acceptance-report，无则不阻塞 archive。弹窗验收 MUST 包含矮视口下主体可滚动与头尾固定可见。列表页验收 MUST 包含分页 DOM 与用户管理页一致及表格卡片内无重复标题行。

#### Scenario: 列表页并排验收

- **WHEN** 团队在 1440×1024 视口并排对比 `/admin/tile-skus` 与 `tile-sku-management-list.html`
- **THEN** diff checklist（Shell、Sidebar active、4 指标卡、五维筛选、表格列、素材 badge、分页）MUST 全部 pass
- **AND** 分页左侧 MUST 为「共 N 条」、右侧为页码与每页条数，DOM MUST 对齐用户管理页（`page-summary` + `page-right`）
- **AND** `table-card` 内 MUST NOT 出现原型未定义的卡片内标题行
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗并排验收

- **WHEN** 打开新增/编辑弹窗并排 `tile-sku-create-modal.html`
- **THEN** checklist（880px、字段顺序、无状态字段、多图主图、多视频、三按钮底栏、参考价格（元））MUST pass

#### Scenario: 弹窗矮视口滚动验收

- **WHEN** 在视口高度 ≤900px 打开新增/编辑 SKU 弹窗
- **THEN** 用户 MUST 可通过弹窗主体滚动访问全部字段与 footer 按钮
- **AND** 验收结果 MUST 记录在 fix change `trace.md`

### Requirement: 瓷砖 SKU 数据模型

系统 MUST 在 SQLite/MySQL 中维护 SKU 商品主数据。`tiles` 表 MUST 保留或等价实现以下字段：`id`、`name`（商品名称 NOT NULL，运营填写并作为公开展示主标题）、`sku_code`（系统生成的唯一内部编码，UNIQUE NOT NULL）、`brand_id`（FK `brands.id` NOT NULL）、`category_id`（FK `tile_categories.id` NOT NULL）、`spec_id`（FK `tile_specs.id`，创建 SKU 时 SHOULD 非空；迁移失败历史记录 MAY 为 NULL 直至运营补选）、`size`（规格尺寸 NOT NULL，MUST 与所选规格 `display_name` 冗余同步）、`surface_finish`（表面工艺 NOT NULL，业务层允许空语义存 `"-"`）、`color_family`（可选）、`reference_price`（必填语义，REAL，≥0，两位小数；新建默认 0）、`remark`（可选）、`status`（`PUBLISHED` | `DRAFT` | `NEEDS_COMPLETION` | `DISABLED`）、`created_at`、`updated_at`。`tile_images` MUST 保留 `is_main` 与 `sort_order`。系统 MUST 维护 `tile_videos` 表存储 SKU 关联视频元数据（`tile_id`、`object_key`、`file_name`、`file_size_bytes`、`duration_seconds`、`sort_order`）。

#### Scenario: 新 SKU 默认草稿

- **WHEN** 通过 API 创建 SKU 且未指定 status
- **THEN** 数据库记录 `status` MUST 为 `DRAFT`

#### Scenario: SKU 编码唯一约束

- **WHEN** 插入或更新导致 `sku_code` 与已有记录冲突
- **THEN** 系统 MUST 拒绝并返回 `TILE_SKU_CODE_DUPLICATED`

#### Scenario: SKU 编码系统生成

- **WHEN** 创建草稿或正式创建 SKU
- **THEN** 系统 MUST 生成唯一 `sku_code`
- **AND** 管理端前端 MUST NOT 要求运营手工填写 SKU 编码
- **AND** `sku_code` MUST NOT 由商品名称派生为会随商品名称修改而变化的值

#### Scenario: SKU 编码稳定

- **WHEN** 运营更新商品名称、品牌、类目、规格、价格、图片或视频
- **THEN** 系统 MUST 保持既有 `sku_code` 不变

#### Scenario: 主图标记

- **WHEN** SKU 有多张图片且其中一张 `is_main=1`
- **THEN** 列表与详情 MUST 将该图作为主图缩略图
- **AND** 同一 SKU MUST NOT 有多张 `is_main=1`（业务层保证唯一）

#### Scenario: 参考价格默认零

- **WHEN** 通过 create API 创建 SKU 且未显式修改参考价格
- **THEN** `reference_price` MUST 持久化为 `0`（非 null）

#### Scenario: spec_id 与 size 同步

- **WHEN** SKU 创建或更新提交有效 `spec_id`
- **THEN** `tiles.size` MUST 等于对应 `tile_specs.display_name`
- **AND** 对应规格 `sku_count` MUST 正确维护

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

### Requirement: 管理端 SKU 创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。请求 MUST 接受 SKU 基础字段（含商品名称 `name`、`spec_id`）、图片列表（含 `is_main`）、视频列表，以及 `save_mode`（`draft` | `create`）。请求 MUST NOT 要求前端传入 `sku_code`；系统 MUST 在创建时生成唯一、稳定的 SKU 编码。`save_mode=draft` 时 MUST 仅校验商品名称必填；`save_mode=create` 时 MUST 校验商品名称、品牌、类目、**spec_id**（所选规格 MUST 存在且 `ENABLED`）、**参考价格（含 0）** 必填；**表面工艺 MUST 为可选**（留空时业务层 MAY 存 `"-"`）。新 SKU `status` MUST 默认为 `DRAFT`；缺主图时 MAY 设为 `NEEDS_COMPLETION`。

#### Scenario: 保存草稿成功

- **WHEN** 提交 `save_mode=draft` 且商品名称非空
- **THEN** 系统返回 HTTP 200 与 SKU 对象
- **AND** `status` MUST 为 `DRAFT`
- **AND** 响应 MUST 包含系统生成的唯一 `sku_code`

#### Scenario: 创建 SKU 成功

- **WHEN** 提交 `save_mode=create` 且全部必填项合法（含商品名称、`spec_id` 指向 ENABLED 规格、`reference_price=0`、表面工艺可空）
- **THEN** 系统返回 HTTP 200
- **AND** 系统 MUST 自动生成唯一 `sku_code`
- **AND** `status` MUST 为 `DRAFT` 或 `NEEDS_COMPLETION`（缺主图时）
- **AND** `size` MUST 等于所选规格 display_name

#### Scenario: 创建 SKU 选择停用规格被拒绝

- **WHEN** 提交 `save_mode=create` 且 `spec_id` 指向 `DISABLED` 规格
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `TILE_SPEC_DISABLED`

#### Scenario: 创建 SKU 缺少参考价格被拒绝

- **WHEN** 提交 `save_mode=create` 且 `reference_price` 为 null 或未提供
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: SKU 编码生成冲突

- **WHEN** 系统生成的 `sku_code` 已存在
- **THEN** 系统 MUST 重试生成或拒绝并返回 `TILE_SKU_CODE_DUPLICATED`
- **AND** 系统 MUST NOT 要求运营手工处理编码冲突

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；MUST NOT 通过 PUT 直接修改 `status`（使用 publish/unpublish）。PUT MUST 要求 `reference_price` 非 null（含 `0.0`）；**MUST NOT** 因 surface_finish 留空而拒绝更新。若 PUT 变更 `spec_id` 至新规格，新规格 MUST 为 `ENABLED`；若保留原 `spec_id` 且该规格已 DISABLED，MAY 允许更新非规格字段。PUT 接收图片列表时 MUST 将提交的 images 视为该 SKU 的完整图片关联事实源；被移除图片不应继续关联到该 SKU。系统 MUST 保证同一 SKU 至多一张图片为主图，并按提交后的 `sort_order` 回填图片顺序。管理端 SKU 表单在创建、保存草稿或编辑成功后 MUST 直接关闭并刷新列表，MUST NOT 在弹窗内额外展示任务追踪反馈。

#### Scenario: 更新 SKU 资料

- **WHEN** PUT 合法字段且 `sku_code` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后 SKU 对象
- **AND** `updated_at` MUST 已更新
- **AND** 若含 `spec_id`，`size` MUST 同步

#### Scenario: 编辑弹窗保存成功直接关闭

- **WHEN** 管理端 SKU 编辑弹窗提交合法修改且更新接口返回成功
- **THEN** 弹窗 MUST 直接关闭
- **AND** 管理端 MUST 刷新 SKU 列表
- **AND** 弹窗内 MUST NOT 显示“SKU 已更新”任务追踪 feedback 或复制追踪 ID 入口

#### Scenario: 新增弹窗创建成功直接关闭

- **WHEN** 管理端 SKU 新增弹窗提交合法创建或保存草稿且接口返回成功
- **THEN** 弹窗 MUST 直接关闭
- **AND** 管理端 MUST 刷新 SKU 列表
- **AND** 弹窗内 MUST NOT 显示任务追踪 feedback 或复制追踪 ID 入口

#### Scenario: 更新缺少参考价格被拒绝

- **WHEN** PUT 请求将 `reference_price` 置为 null 或未提供合法数值
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: 更新 SKU 图片移除关联

- **WHEN** PUT 请求提交的 images 列表不包含某张原已关联图片
- **THEN** 系统 MUST 在保存后解除该 SKU 与该图片的关联
- **AND** 再次 GET SKU 详情时 MUST NOT 返回该图片
- **AND** 系统 MUST NOT 因解除关联而物理删除 MinIO 对象文件

#### Scenario: 更新 SKU 图片主图唯一与顺序

- **WHEN** PUT 请求提交多张图片且其中一张 `is_main=true`
- **THEN** 保存后同一 SKU MUST 至多一张图片 `is_main=1`
- **AND** 再次 GET SKU 详情时主图 MUST 位于图片列表第一位
- **AND** 图片 `sort_order` MUST 可按提交后的顺序回填

#### Scenario: 更新 SKU 移除全部图片

- **WHEN** PUT 请求提交空 images 列表
- **THEN** 系统 MUST 保存该 SKU 为无图片关联状态
- **AND** 再次 GET SKU 详情时 images MUST 为空
- **AND** 素材完整度 MUST 沿用缺图片/缺主图规则

### Requirement: 管理端 SKU 上下架 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus/{id}/publish` 与 `POST /api/v1/admin/tile-skus/{id}/unpublish`，`admin` 与 `employee` 可调用。上架校验 MUST 使用商品名称、规格、主图等业务完整性字段；SKU 编码 MUST 由系统内部保证存在，不作为运营手工补填项。

#### Scenario: 上架 SKU

- **WHEN** 对满足上架条件的 SKU 调用 publish
- **THEN** 系统返回 HTTP 200 且 `status` 为 `PUBLISHED`

#### Scenario: 上架缺少必填或主图被拒绝

- **WHEN** SKU 缺少商品名称/规格等必填项或主图且调用 publish
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `TILE_SKU_PUBLISH_FORBIDDEN`
- **AND** **MUST NOT** 因 surface_finish 留空或 `"-"` alone 而拒绝
- **AND** **`spec_id` 为空或 `size` 为空时 MUST 拒绝**

#### Scenario: 上架前缺少内部编码被拒绝

- **WHEN** 历史 SKU 缺少 `sku_code` 且调用 publish
- **THEN** 系统 MUST 补齐唯一编码或拒绝上架并返回可理解错误
- **AND** 系统 MUST NOT 要求运营手工填写编码

#### Scenario: 下架 SKU

- **WHEN** 对 `PUBLISHED` SKU 调用 unpublish
- **THEN** 系统返回 HTTP 200 且 `status` 为 `DISABLED` 或 `DRAFT`（实现定稿一种）

### Requirement: 管理端 SKU 条件删除 API

系统 MUST 提供 `DELETE /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。`status=PUBLISHED` 时 MUST 拒绝删除；仅当非已上架且无业务引用时 MUST 允许删除；否则 MUST 返回 `TILE_SKU_DELETE_FORBIDDEN`。

#### Scenario: 禁止删除已上架 SKU

- **WHEN** SKU `status` 为 `PUBLISHED`
- **THEN** 系统 MUST 返回 HTTP 409，`TILE_SKU_DELETE_FORBIDDEN`

#### Scenario: 允许删除草稿

- **WHEN** SKU `status` 为 `DRAFT` 且无业务引用
- **THEN** 系统 MUST 删除记录及相关图片/视频元数据并返回 HTTP 200

### Requirement: SKU 图片与视频上传

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。当主图原图对象存在时，系统 SHOULD 为列表场景生成同目录文件名差异化缩略图，并 SHALL 支持历史公开 SKU 主图缩略图回填。SKU 图片上传链路 SHALL 生成真实同目录缩略图；对于尺寸大于缩略图目标尺寸的支持图片，`.thumb` 对象 SHALL 经过后端 resize / compress 处理，SHALL NOT 只是原图 bytes 的复制品。

#### Scenario: SKU 编码稳定

- **WHEN** 运营更新商品名称、品牌、类目、规格、价格、图片或视频
- **THEN** 系统 MUST 保持既有 `sku_code` 不变

#### Scenario: 主图标记

- **WHEN** SKU 有多张图片且其中一张 `is_main=1`
- **THEN** 列表与详情 MUST 将该图作为主图缩略图

#### Scenario: SKU 图片上传生成真实缩略图

- **GIVEN** 管理端上传一张尺寸大于缩略图目标尺寸的 SKU 图片
- **WHEN** 上传接口成功写入原图对象
- **THEN** 后端 SHALL 在同目录写入 `.thumb` 缩略图对象
- **AND** 缩略图 SHALL 保持比例并限制在约定最大宽高内
- **AND** 缩略图 bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 上传响应中的原图 `/media/{object_key}` SHALL 继续可读取。

#### Scenario: 缩略图生成失败边界

- **GIVEN** 原图上传成功但图片解码、resize 或重编码失败
- **WHEN** 后端处理 SKU 图片上传结果
- **THEN** 系统 SHALL 按 Change 实现中约定的失败策略返回错误或记录可观测告警
- **AND** 系统 SHALL NOT 产生原图不可访问、数据库引用半成功或前端直连对象存储的状态
- **AND** Task Trace 或日志 SHOULD 能定位缩略图处理阶段且不得泄露敏感信息。

#### Scenario: 历史 SKU 主图缩略图重生成

- **GIVEN** 存量 SKU 主图原图存在且 `.thumb` 对象缺失或疑似与原图相同
- **WHEN** 运维执行历史缩略图重生成 apply
- **THEN** 系统 SHALL 生成真实同目录 `.thumb` 对象
- **AND** 主图顺序、主图唯一、图片移除关联语义和 SKU 公开状态 SHALL 保持不变
- **AND** 重生成脚本 SHALL 支持 dry-run 和幂等执行。

### Requirement: SKU 弹窗视频上传 UX 对齐 AC-035

SKU 管理弹窗（新增/编辑）「商品视频」能力 MUST 对齐 REQ-0006 **AC-035**：支持上传多个视频；以 **视频预览/播放器卡片** 展示缩略图与播放能力，并展示名称、大小/时长、**上传状态**；同一弹窗会话内 MUST 即时回显已上传视频。本 requirement 聚焦 **即时回显与上传状态**；保存后重开回填与列表页视频计数 MAY 在其它 change 验收。视频上传状态 MUST 区分客户端请求体上传中与服务端保存/等待确认阶段，避免在请求体上传完成后长期只显示“上传中 99%”。

#### Scenario: AC-035 即时回显 gate

- **WHEN** 团队在 SKU 弹窗内成功上传至少一个 MP4（同一弹窗会话，未关闭弹窗）
- **THEN** 「商品视频」区块 MUST 立即展示对应视频预览/播放器卡片（文件名 + 大小或占位）
- **AND** 上传过程 MUST 展示可感知上传状态

#### Scenario: 视频上传 99% 后展示服务端保存状态

- **GIVEN** 管理员在 SKU 新增或编辑弹窗上传合法 MP4 视频
- **AND** 浏览器请求体上传进度已达到前端封顶值或等价完成状态
- **WHEN** 上传接口尚未返回成功或失败响应
- **THEN** 前端 MUST 展示“正在保存视频，请稍候”或等价服务端等待状态
- **AND** 前端 MUST NOT 将该阶段仅表达为“上传中 99%”
- **AND** 上传控件 MUST 保持防重复提交约束，但失败后 MUST 允许重新选择同一文件重试。

#### Scenario: 视频上传失败可恢复

- **WHEN** SKU 视频上传接口返回对象存储不可用、代理超时、MIME 不允许、文件超限或网络失败
- **THEN** SKU 弹窗 MUST 在视频上传区域或等价固定反馈中展示可理解错误
- **AND** 已有视频列表 MUST 保持稳定
- **AND** 用户 MUST 可以重新选择文件并再次上传。

#### Scenario: 多视频追加验收

- **WHEN** 用户在同一弹窗会话内连续上传两个 MP4 且均成功
- **THEN** 视频列表 MUST 展示两个文件卡片

