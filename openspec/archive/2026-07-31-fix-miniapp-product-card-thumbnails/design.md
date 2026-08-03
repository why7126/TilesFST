## Context

`BUG-0092` 为提升小程序商品卡片图片加载速度，引入列表缩略图优先策略。`BUG-0094` 证明该策略在生产 pending 主图数据上不完整：公开 SKU 主图 object key 为 `images/default/tiles/pending/<uuid>.jpg`，原图存在，但后端列表 URL 被转换成 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`，而该 thumbnail 对象不存在，最终小程序商品卡片进入“暂无图片”兜底。

## Root Cause

- 缩略图 key 生成规则与上传 key 生命周期未形成统一契约。
- 公开列表接口把原图 key 机械映射到 `thumbnails/` 前缀，而没有确认对象存在或回退。
- 未传 `tile_id` 上传的 SKU 图片可长期保留在 `images/default/tiles/pending/`，但历史数据没有同路径缩略图。
- 商品卡片失败兜底只负责稳定 UI，不应承担纠正后端不可访问 URL 的责任。

## Design

### Thumbnail Key Contract

缩略图对象 key 必须由原图 object key 稳定派生，且位于原图同目录，仅通过文件名后缀区分。例如原图 `images/default/tiles/pending/<uuid>.jpg` 对应缩略图可以采用 `images/default/tiles/pending/<uuid>.thumb.jpg` 或等价明确后缀。最终实现需要统一封装 helper，避免调用方拼接路径。

`thumbnails/` 前缀可作为历史兼容读取或迁移来源，但不得继续作为 pending 主图列表缩略图的最终写入约定。

### Generation And Backfill

新上传或关联 SKU 主图时，系统应在原图对象成功写入后生成列表缩略图。生成失败不得破坏原图上传，但需要返回或记录可观测错误，后续审计/回填可补偿。

历史回填脚本应扫描公开 SKU 主图，输出 dry-run 清单和执行摘要，至少包含公开 SKU 总数、无主图数量、pending 主图数量、原图对象缺失数量、缩略图对象缺失数量、生成成功数、失败数和失败原因摘要。日志不得输出密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。

### Cover Image Resolution

小程序首页和商品列表接口生成 `cover_image` 时，应优先返回同路径缩略图 URL；当缩略图不存在或生成失败时，应安全回退到原主图 URL或占位语义，不能返回已知不可访问的缩略图 URL。

所有复用商品卡片的入口应共享同一 URL 解析逻辑，避免首页、列表、搜索和品牌详情商品 Tab 行为分叉。

### Testing

测试需要覆盖 key 派生、对象存在性检查、pending 主图、历史回填、列表接口 `cover_image` 生成和小程序商品卡片懒加载/失败兜底。`BUG-0092` 的图片性能核心验收必须保留，不能为了恢复图片展示而回到首屏外图片全量请求。

## Risks

- 历史对象数量较多时，回填耗时和对象存储限流可能影响执行窗口；脚本需支持分批和可重入。
- 如果同一原图曾被多个 SKU 共享，缩略图生成应幂等，避免重复写入导致不必要的对象存储成本。
- 若生产对象存储 provider 对 `HEAD` 或 metadata 行为不同，存在性检查需要通过适配层封装并补充 provider 兼容测试。
