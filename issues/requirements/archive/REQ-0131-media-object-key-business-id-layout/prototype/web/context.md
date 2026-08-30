---
requirement_id: REQ-0131-media-object-key-business-id-layout
status: approved
created_at: 2026-08-29 19:23:12
updated_at: 2026-08-29 19:30:52
---

# 原型策略

本需求默认不新增用户可见页面，不生成独立 HTML 原型或 PNG 原型。

后续 OpenSpec Change 若仅调整媒体对象 Key 生成、pending/formalize、迁移脚本和文档规范，应复用既有管理端上传入口完成验收：

- 用户头像上传。
- 品牌 Logo 上传。
- Banner 图片上传。
- SKU 图片和 SKU 视频上传。
- 品牌证书图片与 PDF/文档上传。

## UI 验收关注点

- 上传控件状态机覆盖 `idle -> uploading -> done/failed`。
- 上传成功后同会话即时回显，保存后重新打开仍能回显正式业务 id 目录 URL。
- 字段级错误展示在上传控件或对应媒体对象下方。
- 用户界面不得展示 object key、内部路径、对象存储 endpoint、bucket、raw URL 或维护脚本输出。
- 若后续新增媒体迁移或审计 UI，必须另行补充 UI Contract、Design System 复用、权限和脱敏展示规则。

## Mock / API 边界

- 需求阶段不提供 Mock 数据。
- 后续实现必须以真实后端上传接口和 `/media/{object_key}` 受控读取作为验收入口。
- Docker Web 上传边界验收使用 `http://localhost:3000`，不得只调用后端 `:8000`。
