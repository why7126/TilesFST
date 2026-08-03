## Context

BUG-0100 证明当前 SKU 图片缩略图链路只完成了对象 key 和对象存在性：上传入口传入 `same_directory_thumbnail_object_key(object_key)`，`save_upload_file()` 将原图 `content` 原样写入 `.thumb` key；历史商品卡片图片审计回填脚本也通过复制原图 bytes 补齐缩略图对象。现有规格已要求列表场景优先使用同目录 `.thumb` URL，但没有明确“缩略图必须是真实轻量派生图”。

## Goals / Non-Goals

**Goals:**

- 新上传 SKU 图片生成真实缩略图，保持比例并限制最大宽高。
- 大图缩略图的 bytes 不得与原图完全一致，文件体积通常应小于原图。
- 小图、透明图、JPG/PNG/WebP、异常图片和缩略图生成失败都有明确策略。
- 历史 `.thumb` 对象可审计、可重生成、可重入。
- 公开商品卡片继续优先使用后端受控 `.thumb` URL，详情高清场景不被降级。
- 对象操作继续通过后端对象存储适配层，避免前端直连对象存储。

**Non-Goals:**

- 不新增前端直传对象存储。
- 不引入多 Bucket 或独立 thumbnail bucket。
- 不实现视频转码、多清晰度图片、CDN 图片处理或复杂媒体管线。
- 不改变 SKU 图片数量、主图排序、移除关联语义。
- 不要求本 Change 新增公开 API；若实现阶段确需新增字段或错误码，再同步 API/Orval/docs。

## Decisions

### D1. 缩略图生成在后端媒体模块内封装

实现阶段应在后端媒体模块提供统一图片缩略图生成 helper，由上传链路和历史重生成脚本复用。该 helper 负责：

- 校验并解码支持的图片格式。
- 按最大宽高等比缩小，禁止放大小图。
- 根据源格式和透明度选择输出格式与质量。
- 返回缩略图 bytes、content type、尺寸、size 和处理结果。

### D2. 同目录 `.thumb` key 规则保持不变

本 Change 不改变 `same_directory_thumbnail_object_key()` 语义。原图：

```text
images/default/tiles/pending/<uuid>.jpg
```

对应缩略图仍为：

```text
images/default/tiles/pending/<uuid>.thumb.jpg
```

已绑定 SKU 的正式目录同理使用文件名差异化 `.thumb`。历史 `thumbnails/` 前缀只作为兼容读取或迁移来源，不作为新生成 SKU 列表缩略图最终位置。

### D3. 失败策略以不破坏原图上传为优先

推荐策略：原图上传成功后，缩略图生成失败不应造成数据库引用半成功或原图不可访问。实现可选择：

- 返回上传失败并不写入业务引用。
- 或原图上传成功、缩略图失败时记录 Task Trace / 日志告警，并允许 `/media` 读取层回退原图。

无论选择哪种策略，都必须在 Change 实现中明确，并通过测试覆盖。

### D4. 历史重生成必须 dry-run 优先

历史脚本应先输出 dry-run 摘要：公开 SKU 总数、原图存在数、缩略图存在数、疑似同 size、疑似同 bytes、需要重生成、跳过、失败原因。apply 模式只处理需要重生成的对象，并保持幂等；已合格缩略图不得被重复破坏。

### D5. 测试从存在性提升到有效性

现有测试只证明缩略图 key 存在或缺失时可回退。修复必须新增测试证明：

- 大图缩略图像素尺寸低于原图或不超过目标最大宽高。
- 缩略图 bytes 不等于原图 bytes。
- 缩略图 size 通常小于原图 size。
- 小图不被放大，透明图不出现不符合约定的背景丢失。

## Risks / Trade-offs

- [Risk] 新增图片处理依赖导致 Docker 镜像构建失败。  
  Mitigation: 同步依赖文件，运行后端测试和 Docker 构建相关验证。
- [Risk] 透明 PNG/WebP 转换后视觉失真。  
  Mitigation: 保持透明格式或明确背景策略，补充透明图测试。
- [Risk] 小图重编码后体积变大。  
  Mitigation: 小图不放大；如输出异常增大，可保留原图或跳过重写并记录。
- [Risk] 历史重生成脚本处理大量对象耗时较长。  
  Mitigation: 支持 limit、dry-run、分批 apply、失败原因统计和可重入执行。

## Migration Plan

1. 在后端媒体模块增加真实缩略图生成 helper。
2. 更新 SKU 图片上传链路，写入真实 `.thumb` 对象而不是复制原图 bytes。
3. 更新历史商品卡片图片审计/回填脚本，使 backfill 从复制原图改为重生成缩略图，并扩展 dry-run 指标。
4. 补充后端媒体处理、上传接口、历史脚本和公开商品卡片 URL 回归测试。
5. 如引入依赖、API、DB、错误码或环境变量变化，同步相关文档、OpenAPI/Orval 和 Docker 验证。

## Open Questions

- 缩略图最大宽高和质量参数的最终默认值由实现阶段结合现有商品卡片尺寸确定。
- PNG/WebP 透明图是否保持源格式，或允许 WebP 统一输出，需要实现阶段用测试和兼容性确认。
- 原图上传成功但缩略图失败时选择“上传失败”还是“上传成功并告警回退”，需要在 apply 阶段落定并写入测试。
