## 上下文

BUG-0116 是已评审通过的媒体类生产历史数据缺陷，关联 `REQ-0012-object-storage-key-layout` 和 `BUG-0099-public-sku-main-image-key-pending-path`。当前新上传链路已经趋向标准前缀和同目录缩略图，但历史数据仍可能漂移。

活跃 Change `add-prod-media-maintenance-jobs` 正在建立生产 Docker Compose 媒体维护入口。本修复 Change 不重复定义生产入口能力，而是定义 BUG-0116 的具体修复闭环：审计三类对象、执行受控迁移/回填、二次审计、回填媒体四联验收。

## 目标与非目标

目标：

- 覆盖 SKU 商品图片、品牌 Logo、品牌证书图片三类历史媒体对象。
- 统一 dry-run 输出，汇总 pending、files 图片证书、缺失原图、缺失缩略图、同 size / 同 bytes 缩略图和失败原因。
- 在受控 apply 中正式化 SKU pending 主图、迁移图片类证书 key、生成或重生成真实同目录 `.thumb` 缩略图。
- 验证 `/media/{object_key}` 或等价后端受控 URL，以及 Web 管理端、店主 Web、小程序受影响页面的 render 证据或 blocked 原因。
- 输出可直接支撑 BUG-0116 `acceptance.md` 四联验收的摘要。

非目标：

- 不新增对外 API 或用户可见 UI。
- 不新增视频转码、多清晰度、PDF 首页渲染或 OCR 能力。
- 不删除历史对象；删除或清理孤儿对象需要单独审批或后续 Change。
- 不在本 Change 中执行真实生产维护任务。
- 不绕过 `add-prod-media-maintenance-jobs` 的生产入口和备份门禁直接 apply 生产数据。

## 修复方案

### D1 统一维护任务编排

实现阶段应提供一个面向 BUG-0116 的维护任务或命令组合，至少包含：

- SKU pending 主图 dry-run / apply。
- SKU 缩略图 dry-run / apply。
- 品牌 Logo 缩略图 dry-run / apply。
- 证书图片 files → images key dry-run / apply。
- 证书图片缩略图 dry-run / apply。
- apply 后二次审计汇总。

如果 `add-prod-media-maintenance-jobs` 已完成，应通过其 maintenance CLI 或 Compose service 暴露以上任务；如果尚未完成，只允许完成本地等价测试和 dry-run 设计，不得声称生产 apply 可执行。

### D2 key 迁移必须按资源类型分流

SKU 图片：

- 公开 SKU 主图不得继续长期引用 `images/default/tiles/pending/`。
- 可迁移项应正式化到 `images/default/tiles/{tile_id}/` 或等价商品目录，并同步 `tile_images.object_key` 与 `tile_images.url`。

证书图片：

- JPG、JPEG、PNG、WebP 图片证书迁移到 `images/default/brand-certificates/`。
- PDF 和其他文档类证书继续留在 `files/default/brand-certificates/`。
- `brand_certificates.file_key` 和 `brand_certificate_images.file_key` 均需要覆盖。

品牌 Logo：

- 已在 `brands.logo_object_key` 引用的图片不强制迁移 key，除非仍是 legacy `original/` 前缀；本 BUG 的品牌主线重点是缩略图存在性和真实轻量化。

### D3 缩略图必须真实生成

同目录 `.thumb` 不是字符串占位，也不是原图 bytes 复制品。对支持的 JPG、PNG、WebP 原图，应复用后端图片处理逻辑生成缩略图。对于小图或透明图导致 size 收益不明显的边界，应记录处理结果和人工判断字段，而不是直接判定通过。

### D4 输出必须脱敏且可验收

所有命令输出只允许包含统计、脱敏 key、相对 URL、错误码、失败原因和建议动作。禁止输出生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

### D5 验收必须四联闭环

修复完成后必须按 BUG-0116 `acceptance.md` 和 `docs/standards/media-bug-four-point-acceptance-template.md` 回填：

- `key`：旧 key、新 key、资源类型、分流结果。
- `object`：原图、缩略图、MIME、size、同 bytes 检查、dry-run/apply/幂等摘要。
- `URL`：`/media/{object_key}` 或等价后端受控 URL 状态。
- `render`：Web 管理端、店主 Web、小程序页面证据；无法补齐时记录 blocked 和补证方式。

## 测试策略

- 后端单元测试覆盖 key 映射、PDF 不迁移、SKU pending 正式化、缩略图同 bytes 判定、dry-run 不写和 apply 幂等。
- 使用 fake storage / fake repository 或等价 fixture 验证缺失 object、目标已存在、不可处理 MIME、provider 不可用等失败摘要。
- 部署或维护入口测试覆盖 production provider 配置不泄密、SQLite 本地默认不误连生产、Compose 命令可 dry-run。
- 媒体四联验收记录测试或文档校验覆盖 `key`、`object`、`URL`、`render` 均有状态和证据字段。

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 误迁移 PDF 或文档证书 | 按 MIME 与扩展名双重分流；测试 PDF 不迁移。 |
| 对象存储缺失原图导致数据库先更新 | apply 前 stat 原图；原图缺失必须 fail / blocked，不写数据库。 |
| 缩略图生成失败后被视为成功 | 失败原因进入 retry_candidates，二次审计仍计入未通过。 |
| 生产环境输出敏感信息 | 增加脱敏扫描测试；输出只允许摘要和脱敏标识。 |
| 与生产维护入口 Change 重叠 | 本 Change 只定义 BUG-0116 修复闭环，执行入口复用或依赖 `add-prod-media-maintenance-jobs`。 |
