---
bug_id: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
status: approved
created_at: 2026-07-31 13:07:33
updated_at: 2026-07-31 15:28:52
evidence_type: miniapp_true_device_network
---

# 真机网络证据

用户在真机上发现商品卡片图片请求异常，异常请求集中在 `/media/thumbnails/default/tiles/pending/` 路径。

## 请求样本

```text
https://tilesfst.wjoyhappy.site/media/thumbnails/default/tiles/pending/11e48e35-364f-4559-b9b5-89b87fce0e66.jpg
https://tilesfst.wjoyhappy.site/media/thumbnails/default/tiles/pending/8a925cc1-06cb-4040-b4e4-403f011ec60b.jpg
https://tilesfst.wjoyhappy.site/media/thumbnails/default/tiles/pending/e1f95760-36ac-476d-8468-d8bb3ed495dd.jpg
https://tilesfst.wjoyhappy.site/media/thumbnails/default/tiles/pending/4f027e44-6652-4a56-92c4-dfa02bb3ef4f.jpg
```

## 证据解读

- 真机已实际发起图片请求，问题不再是“图片请求未触发”。
- 请求 URL 均为 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- `tiles/pending` 来自未传 `tile_id` 上传商品图片时的对象 key 资源类型。
- 后端列表卡片缩略图 URL 生成会把原始 key 转换为 `/media/thumbnails/...`；当原始 key 为 `images/default/tiles/pending/<uuid>.jpg` 时，请求会变成 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- 后续应重点验证公开 SKU 主图是否仍引用 `tiles/pending` key，以及这些 pending key 是否具备对应缩略图对象或可靠原图回退。
