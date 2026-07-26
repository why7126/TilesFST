---
change_id: fix-admin-video-upload-stuck-at-99
status: proposed
created_at: 2026-07-24 20:45:00
updated_at: 2026-07-24 20:45:00
source_bug: BUG-0085-admin-video-upload-stuck-at-99
---

# Acceptance - fix-admin-video-upload-stuck-at-99

## 验收范围

- 管理端 SKU 视频上传前端状态。
- 后端授权上传与对象存储写入响应闭环。
- Web Nginx、外层 HTTPS Nginx 或等价网关上传路径超时配置。
- 上传相关回归测试和生产 smoke。

## 关键验收

1. 合法 MP4 上传返回 200，响应包含 `object_key` 与 `/media/{object_key}`。
2. 99% 后如接口尚未返回，前端展示服务端保存/等待确认状态，不再只显示“上传中 99%”。
3. 对象存储中存在响应 object key 对应对象，`/media/{object_key}` 可受控读取。
4. 外层与容器内 Nginx 不再因默认 60 秒超时导致 499/504。
5. SKU 图片、品牌 Logo、Banner 图片、品牌证书上传不回归。
6. 不引入前端直连未授权对象存储写入能力。
