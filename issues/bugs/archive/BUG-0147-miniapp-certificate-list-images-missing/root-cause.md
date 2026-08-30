---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
root_cause_status: confirmed
category: data-contract
created_at: 2026-08-30 10:28:24
updated_at: 2026-08-30 10:28:24
---

# 根因结论

小程序证书列表页只允许图片类证书使用 `thumbnail_url` 渲染卡片封面；后端公开证书列表虽然能识别生产证书为 `file_kind: "image"`，但当前列表聚合链路只从 `record.file_url` 推导 `thumbnail_url`，没有在 `file_url` 为空或历史数据不完整时，从可信 `file_key` / 主图记录 / 标准图片前缀兜底生成受控媒体 URL。生产接口返回 `file_kind: "image"` 且 `thumbnail_url: null`，因此前端按设计进入“证书”占位态。

直接原因：`GET /api/v1/miniapp/certificates` 对图片类证书返回空 `thumbnail_url`。  
根本原因：后端公开证书聚合契约没有保证图片类证书具备列表可用缩略图 URL，且对历史证书媒体字段的 key、object、URL 一致性缺少闭环兜底。  
触发条件：生产证书记录具备图片 MIME 或文件名，能够被识别为图片证书，但聚合得到的 `file_url` 为空，或无法按 `/media/{object_key}` 推导同目录 `.thumb.webp`。  
缺陷分类：后端公开 API 数据契约 + 生产历史媒体数据一致性。

# 证据链

| 证据 | 类型 | 摘要 |
|---|---|---|
| 用户截图 Image #1 | 截图 | 小程序证书列表页首屏多张证书卡片媒体区域均显示“证书”文字占位。 |
| 生产接口只读请求 | 复现 / 接口证据 | `GET /api/v1/miniapp/certificates?page=1&pageSize=12` 返回 6 条证书，均为 `file_kind: "image"`，且 `file_url: null`、`thumbnail_url: null`。 |
| `src/miniapp/pages/certificates/index.wxml` | 代码定位 | 证书卡片 `<image>` 仅在 `file_kind == 'image' && thumbnail_url && !image_failed` 时渲染；否则显示“证书”占位。 |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | `_to_certificate_item()` 使用 `record.file_url` 调用 `_certificate_thumbnail_url()`；当 `record.file_url` 为空时缩略图必然为空。 |
| `src/backend/app/repositories/miniapp_home_repository.py` | 代码定位 | 公开证书查询仅对 `images/default/brand-certificates/%` 前缀的 `file_key` 拼接 `/media/`，否则回退到 `file_url`。历史路径、空 `file_url` 或不匹配前缀会导致公开 `file_url` 为空。 |

# 确认范围

已确认：

- 小程序列表页显示占位不是布局问题，而是缺少 `thumbnail_url` 后触发的预期降级。
- 生产接口当前未满足图片类证书列表卡片的媒体字段契约。
- 修复面至少涉及后端公开证书列表 API 和证书媒体 key / URL / 缩略图一致性。

仍需在修复阶段补证：

- 生产数据库中 `brand_certificates.file_key`、`brand_certificates.file_url`、`brand_certificate_images.file_key`、`brand_certificate_images.file_url` 的实际分布。
- 对象存储中对应原图与 `.thumb.webp` 是否存在。
- 证书详情页是否同样受空 URL 或缺缩略图影响。

# 验证方式

修复前验证：

1. 请求 `GET /api/v1/miniapp/certificates?page=1&pageSize=12`。
2. 确认图片类证书存在 `file_kind: "image"` 且 `thumbnail_url: null`。
3. 打开小程序证书列表页，确认卡片媒体区域显示“证书”占位。

修复后验证：

1. 同一接口中图片类证书返回非空 `thumbnail_url`，且 URL 使用 `/media/images/default/brand-certificates/...thumb.webp` 或等价受控媒体路径。
2. 请求缩略图 URL 返回成功，MIME 与扩展名符合预期，不暴露对象存储原始 key 以外的敏感信息。
3. 小程序证书列表页卡片显示实际证书图片；图片失败时仍能降级为“证书”占位。
4. 媒体维护 dry-run / apply / 再次 dry-run 能分别报告候选、写入结果和幂等结果。
