## 背景

媒体维护命令的最终 JSON stdout 是现有生产审计和脚本解析的稳定契约，不能因为增加进度展示而被污染。进度能力应作为显式 opt-in 的运维体验增强，默认行为保持不变。

## 目标

- 长耗时媒体维护任务在 dry-run 和 apply 中都能展示可读进度。
- 最终 JSON stdout 保持兼容，现有 `jq`、日志归档和自动化脚本不需要调整。
- 进度行不泄露真实 object key、文件名、对象存储私有 endpoint、密钥、连接串、`.env` 内容或本机绝对路径。
- 聚合任务能展示当前阶段，避免执行者无法判断卡在扫描、回填还是审计。

## 非目标

- 不新增管理端任务看板、WebSocket、SSE、后台任务队列或进度持久化表。
- 不改变缩略图、display 图、证书缩略图或对象 key 审计的既有业务规则。
- 不改变 `--apply --confirm-backup` 的生产写入门禁。
- 不引入必须依赖交互式终端控制符的动态进度条作为唯一输出。

## 关键设计

### CLI 开关

维护入口增加可选 `--progress` 参数。未传入时只输出最终 JSON，传入后在执行过程中输出普通文本进度行。命令帮助文案需要明确 `--progress` 不改变最终 JSON stdout。

### 输出通道

最终 JSON 继续写入 stdout。进度信息写入 stderr，便于生产执行时将 stdout 保存为审计 JSON，同时将 stderr 作为运行日志采集。

推荐进度字段：

- `task`
- `stage`
- `total`
- `completed`
- `success`
- `failed`
- `skipped`
- `progress_percent`

### 进度计数

`completed` 表示已经完成判定的 item 数，包含成功、失败和跳过。`progress_percent` 按 `completed / total` 计算，建议保留两位小数。若任务总量只能按阶段计算，则使用阶段级 `total` 并在阶段名中表达当前阶段。

`backfill-image-variants` 中单个源图可能对应 thumbnail 与 display 两类派生写入；进度需要说明 item 级扫描进度与写入估算之间的口径差异，避免把 `estimated_writes` 误读为扫描总数。

### 聚合任务阶段

`media-drift-reconcile` 至少展示以下阶段：

- SKU pending 主图正式化
- 证书图片 key 迁移
- 缩略图回填
- 对象 key 审计

如子任务已有 item 级进度，聚合任务可以透传；如无法透传，则至少输出阶段开始、阶段完成和阶段汇总。

### 子任务 item 级心跳

聚合任务开启 `--progress` 时，子任务内部进度也需要继续输出到 stderr。阶段执行时间较长时，进度行应使用当前聚合任务名和子任务阶段名，按当前子任务 item 总数更新 `completed`、`total` 和 `progress_percent`。

对于对象存储或数据库 I/O，进度行可以在慢操作前输出枚举化状态，例如 `checking_source`、`checking_target`、`copying_object`、`updating_db`。这些状态只表达当前动作类别，不输出对象 key、文件名、数据库值或异常详情。

### 脱敏策略

进度输出只允许出现任务名、阶段名、计数、百分比和枚举化状态。失败定位仍以最终 JSON 中既有的脱敏 hash、标准前缀和失败原因枚举为准，进度行不新增真实对象定位信息。

## 测试策略

- 单元测试覆盖进度报告器的计数、百分比、输出通道和脱敏约束。
- CLI 级测试覆盖默认 stdout JSON 兼容，以及启用 `--progress` 后 stdout 仍可解析 JSON、stderr 出现进度行。
- 媒体任务测试覆盖 `backfill-image-variants` 的跳过、成功、失败计数，`media-drift-reconcile` 的阶段级输出，以及 `business_id_media_key_migration` 的 item 级 I/O 状态心跳。

## 产品数据采集与链路观测

本设计不触发产品数据采集与链路观测门禁，原因是未新增 API、DB、请求日志、行为事件、Task Trace 或端侧请求封装。后续若方案引入持久化进度或任务追踪写入，需要在实现前重新补齐观测规范评估。

## 风险与缓解

- 风险：进度输出混入 stdout 导致生产脚本无法解析最终 JSON。缓解：测试显式断言 stdout 可直接 JSON parse，进度写 stderr。
- 风险：进度行泄露对象 key 或环境信息。缓解：进度字段白名单化，脱敏测试覆盖敏感片段。
- 风险：聚合任务阶段总量和子任务 item 总量口径混淆。缓解：阶段名与 Runbook 明确口径，最终 JSON 仍作为审计事实源。
