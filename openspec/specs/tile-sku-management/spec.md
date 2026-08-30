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

系统 MUST 提供 `GET /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。接口 MUST 支持分页、关键词、品牌、类目、状态和素材完整度筛选，并保持既有排序、权限、错误响应、加载态、空态、失败态和行操作行为。管理端 SKU 列表项存在主图时，响应 MUST 提供 `main_image_thumbnail_url`、`main_image_display_url`、`main_image_original_url` 或等价多规格字段，并保留 `main_image_url` 兼容语义。管理端 SKU 列表图片展示 MUST 优先使用 `thumbnail` 规格，详情、编辑、上传预览和放大预览场景 SHOULD 使用 `display` 或 `original` 规格。

#### Scenario: SKU 列表返回主图多规格 URL

- **GIVEN** SKU 列表项存在主图对象
- **WHEN** 管理端请求 `GET /api/v1/admin/tile-skus`
- **THEN** 响应项 MUST 包含主图 `thumbnail` URL
- **AND** 响应项 SHOULD 包含主图 `display` URL 与 `original` URL 或等价语义字段
- **AND** 响应项 MUST 保留旧字段兼容或说明替代关系
- **AND** 响应 MUST NOT 暴露未授权对象存储地址、bucket 名称、access key、secret key 或原始 object key。

#### Scenario: SKU 列表主图规格 fallback

- **GIVEN** SKU 列表项存在原图但 `thumbnail` 不可用
- **WHEN** 管理端渲染 SKU 列表图片
- **THEN** 页面 MUST 按统一 fallback 顺序回退到 `display`、原图或无图占位
- **AND** 页面 MUST NOT 显示浏览器默认破图
- **AND** 表格行高、分页、筛选和操作列布局 MUST 保持稳定。

### Requirement: 管理端 SKU 创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。请求 MUST 接受 SKU 基础字段、图片列表、视频列表和 `save_mode`。当请求包含图片时，系统 MUST 通过媒体服务或对象存储适配层保留 `original`，并生成或调度生成 `thumbnail` 与 `display`。创建响应 SHOULD 返回图片多规格 URL 或可在后续 GET 中稳定获得多规格 URL。

#### Scenario: 创建 SKU 图片生成多规格资源

- **WHEN** 管理端创建 SKU 并提交合法图片
- **THEN** 系统 MUST 保留图片 `original`
- **AND** 系统 MUST 生成或调度生成 `thumbnail` 与 `display`
- **AND** 创建或后续详情响应 SHOULD 返回多规格 URL 语义
- **AND** 生成失败 MUST 有可诊断错误摘要或 warning，不得暴露内部路径或存储凭据。

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；提交图片列表时，系统 MUST 保持图片多规格资源与 SKU 关联一致。管理端 SKU 表单在上传、编辑或保存后 MUST 能同会话回显媒体入口，并 SHOULD 展示可理解的派生生成状态或 fallback。

#### Scenario: 更新 SKU 图片保持多规格关联

- **WHEN** PUT 请求提交图片列表
- **THEN** 保存后同一 SKU 的图片关联 MUST 能追溯到对应 `thumbnail`、`display`、`original`
- **AND** 被移除图片不应继续关联到该 SKU
- **AND** 系统 MUST NOT 因解除关联而物理删除 MinIO / 对象存储对象
- **AND** 再次 GET SKU 详情时 MUST 返回稳定的多规格 URL 或明确 fallback。

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

SKU 图片在 `tile_id` 已存在时 MUST 使用 `images/default/tiles/{tile_id}/{uuid}.{ext}`，SKU 视频在 `tile_id` 已存在时 MUST 使用 `videos/default/tiles/{tile_id}/{uuid}.{ext}`。新建 SKU 前上传的图片或视频 MUST 使用对应 pending 目录，并在 SKU 创建成功后 formalize 到正式 `tiles/{tile_id}` 目录。SKU 图片上传链路 SHALL 生成真实同目录缩略图；对于尺寸大于缩略图目标尺寸的支持图片，`.thumb` 对象 SHALL 经过后端 resize / compress 处理，SHALL NOT 只是原图 bytes 的复制品。历史 SKU pending 主图、旧目录视频 key 和过渡目录 MUST 保持读取兼容，迁移或正式化 MUST 保持主图顺序、主图唯一和视频元数据。

#### Scenario: SKU 图片上传生成真实缩略图

- **GIVEN** 管理端上传一张尺寸大于缩略图目标尺寸的 SKU 图片
- **WHEN** 上传接口成功写入原图对象
- **THEN** 后端 SHALL 在同一 SKU 业务对象目录或 pending 目录写入 `.thumb` 缩略图对象
- **AND** 缩略图 SHALL 保持比例并限制在约定最大宽高内
- **AND** 缩略图 bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 上传响应中的原图 `/media/{object_key}` SHALL 继续可读取。

#### Scenario: 新建 SKU 保存后正式化图片和视频

- **GIVEN** 新建 SKU 表单引用 pending 图片或 pending 视频
- **WHEN** SKU 创建成功并获得 `tile_id`
- **THEN** 系统 MUST 将 SKU 图片 formalize 到 `images/default/tiles/{tile_id}/`
- **AND** 系统 MUST 将 SKU 视频 formalize 到 `videos/default/tiles/{tile_id}/`
- **AND** `tile_images` 与 `tile_videos` 引用 MUST 指向 formalize 后的正式 key
- **AND** 主图唯一、图片排序、视频排序和公开状态校验 MUST 保持不变。

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

### Requirement: SKU 召回置顶运营配置

管理端 SKU 维护能力 MUST 支持运营配置召回置顶排序信息。系统 MUST 在 SKU 新建、编辑和详情回显中维护 `recall_pin_sort_order`、`recall_pin_starts_at`、`recall_pin_ends_at` 或等价字段。`recall_pin_sort_order` MUST 只允许正整数，默认值 MUST 为 `9999`；数值低于 `9999` 且处于有效期内时才表示该 SKU 可参与小程序普通商品列表和搜索 SKU 结果的召回置顶排序。管理端 SKU 列表 MUST 展示排序字段，但默认排序 MUST NOT 因该字段改变。

#### Scenario: 新建 SKU 默认召回排序值

- **WHEN** 管理端新建 SKU 且运营未填写召回排序值
- **THEN** 系统 MUST 将 `recall_pin_sort_order` 持久化为 `9999`
- **AND** 该 SKU MUST 按普通商品参与公开列表排序。

#### Scenario: 召回排序值正整数校验

- **WHEN** 管理端保存 SKU 时提交空值、非数字、零、负数或小数作为召回排序值
- **THEN** 系统 MUST 拒绝非法值或按空值规则归一化为 `9999`
- **AND** 非空非法值 MUST 在排序输入框下方给出红色字段级校验提示“排序值必须为正整数”
- **AND** MUST NOT 将该错误展示到弹窗顶部全局错误区
- **AND** 系统 MUST NOT 保存非正整数排序值。

#### Scenario: SKU 弹窗排序字段位置和帮助说明

- **WHEN** 管理端打开 SKU 新建或编辑弹窗
- **THEN** 召回排序字段 MUST 以“排序”作为标签
- **AND** MUST 放在“参考价格”字段之后
- **AND** MUST 标记为必填
- **AND** 标签旁 MUST 提供问号帮助图标，鼠标 hover 时说明默认值、正整数约束和数值越低越靠前。

#### Scenario: 召回置顶有效期校验

- **WHEN** 管理端保存 SKU 时提交生效开始时间晚于生效结束时间
- **THEN** 系统 MUST 拒绝保存
- **AND** 管理端 MUST 展示可理解的字段级校验提示。

#### Scenario: 召回配置保存回显

- **WHEN** 运营保存召回排序值和有效期后再次打开 SKU 详情或编辑弹窗
- **THEN** 系统 MUST 回显已保存的排序值、生效开始时间和生效结束时间
- **AND** 保存成功或失败反馈 MUST 使用既有 fixed toast，不得造成 SKU 列表或弹窗布局位移。

#### Scenario: 管理端列表排序不变

- **WHEN** 管理端请求 SKU 列表
- **THEN** 管理端 SKU 列表 MUST 在状态字段前展示“排序”字段
- **AND** 管理端 SKU 列表 MUST 继续遵循既有管理端排序规则
- **AND** MUST NOT 因 `recall_pin_sort_order` 较低而将 SKU 在管理端列表置顶
- **AND** 状态字段中的“已上架”“已下架”短标签 MUST 单行显示。

