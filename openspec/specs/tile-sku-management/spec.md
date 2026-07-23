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

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 10/20/50/100）、关键词模糊搜索（商品名称 `name`、系统内部编码 `sku_code`）、`brand_id`、`category_id`、`status`、`material_completeness`（`complete` | `missing_main_image` | `missing_images` | `missing_videos`）筛选。响应 MUST 包含 `items`、`pagination` 与 `summary`（SKU 总数、已上架、待完善、草稿）。列表 MUST 默认按 `updated_at` 降序。管理端列表 MUST 以商品名称作为主标题，SKU 编码仅作为内部辅助信息或检索依据，视觉层级 MUST 弱于商品名称。

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

#### Scenario: 素材完整度筛选缺主图

- **WHEN** 请求 `material_completeness=missing_main_image`
- **THEN** 返回项 MUST 均为未设置主图的 SKU

#### Scenario: 非管理端用户被拒绝

- **WHEN** `store_owner` 或未认证用户请求 `GET /api/v1/admin/tile-skus`
- **THEN** 系统 MUST 返回 HTTP 401 或 403

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

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；MUST NOT 通过 PUT 直接修改 `status`（使用 publish/unpublish）。PUT MUST 要求 `reference_price` 非 null（含 `0.0`）；**MUST NOT** 因 surface_finish 留空而拒绝更新。若 PUT 变更 `spec_id` 至新规格，新规格 MUST 为 `ENABLED`；若保留原 `spec_id` 且该规格已 DISABLED，MAY 允许更新非规格字段。PUT 接收图片列表时 MUST 将提交的 images 视为该 SKU 的完整图片关联事实源；被移除图片不应继续关联到该 SKU。系统 MUST 保证同一 SKU 至多一张图片为主图，并按提交后的 `sort_order` 回填图片顺序。

#### Scenario: 更新 SKU 资料

- **WHEN** PUT 合法字段且 `sku_code` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后 SKU 对象
- **AND** `updated_at` MUST 已更新
- **AND** 若含 `spec_id`，`size` MUST 同步

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

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。

#### Scenario: 上传 SKU 图片成功

- **WHEN** `admin` 或 `employee` 上传合法图片
- **THEN** 系统返回 object_key
- **AND** 创建/更新 SKU 时可关联图片并设置 `is_main`

#### Scenario: 非法 MIME 被拒绝

- **WHEN** 上传不允许的文件类型
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: 移除非主图图片

- **WHEN** 用户在 SKU 编辑弹窗中移除非主图图片
- **THEN** 当前主图 MUST 保持不变
- **AND** 剩余图片 MUST 重新生成连续 `sort_order`
- **AND** 保存后再次打开弹窗，被移除图片 MUST 不再出现

#### Scenario: 设置主图自动前置

- **WHEN** 用户在 SKU 编辑弹窗中点击某张非主图图片的「设为主图」
- **THEN** 该图片 MUST 立即成为唯一主图
- **AND** 该图片 MUST 移动到图片列表第一位
- **AND** 保存 payload 中该图片 MUST 为 `is_main=true` 且 `sort_order=0`

#### Scenario: 移除当前主图自动兜底

- **WHEN** 用户在 SKU 编辑弹窗中移除当前主图且移除前后一张图片存在
- **THEN** 移除前后一张图片 MUST 自动成为新主图
- **AND** 新主图 MUST 在弹窗内即时显示在图片列表第一位

#### Scenario: 移除最后位置主图自动兜底

- **WHEN** 用户移除当前主图且该主图已是移除前最后一张图片，但移除后仍有其它图片
- **THEN** 移除后列表第一张图片 MUST 自动成为新主图
- **AND** 新主图 MUST 在弹窗内即时显示在图片列表第一位

#### Scenario: 移除全部商品图片

- **WHEN** 用户移除 SKU 编辑弹窗中的最后一张商品图片
- **THEN** 图片列表 MUST 为空
- **AND** 弹窗 MUST 不再显示「主图」标签
- **AND** 「继续添加图片」入口 MUST 仍可用

#### Scenario: 图片上传状态不因移除能力回归

- **WHEN** 用户在同一 SKU 编辑弹窗会话中上传图片
- **THEN** 上传过程 MUST 体现 `idle→uploading→done/failed` 或等价状态机
- **AND** 上传成功的图片 MUST 即时回显并可继续执行「设为主图」与「移除」
- **AND** 上传失败 MUST 在上传控件或图片区域内展示错误

### Requirement: SKU 弹窗视频上传 UX 对齐 AC-035

SKU 管理弹窗（新增/编辑）「商品视频」能力 MUST 对齐 REQ-0006 **AC-035**：支持上传多个视频；以 **视频预览/播放器卡片** 展示缩略图与播放能力，并展示名称、大小/时长、**上传状态**；同一弹窗会话内 MUST 即时回显已上传视频。本 requirement 聚焦 **即时回显与上传状态**；保存后重开回填与列表页视频计数 MAY 在其它 change 验收。

#### Scenario: AC-035 即时回显 gate

- **WHEN** 团队在 SKU 弹窗内成功上传至少一个 MP4（同一弹窗会话，未关闭弹窗）
- **THEN** 「商品视频」区块 MUST 立即展示对应视频预览/播放器卡片（文件名 + 大小或占位）
- **AND** 上传过程 MUST 展示可感知上传状态
- **AND** 验收结果 MUST 记录在 fix change `trace.md`

#### Scenario: 弹窗视频区并排验收

- **WHEN** 打开新增/编辑 SKU 弹窗并排 `tile-sku-create-modal.html`「商品视频」区块
- **THEN** checklist（上传按钮、视频预览/播放器列表、移除入口、上传状态反馈）MUST pass

#### Scenario: 多视频追加验收

- **WHEN** 用户在同一弹窗会话内连续上传两个 MP4 且均成功
- **THEN** 视频列表 MUST 展示两个文件卡片
- **AND** 移除其中一个后列表 MUST 正确更新

