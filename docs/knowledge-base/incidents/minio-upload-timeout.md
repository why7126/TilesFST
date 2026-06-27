---
title: MinIO上传超时复盘示例
purpose: 提供故障复盘示例
content: 项目模板文档
source: AI自动生成，人工确认
update_method: 相关流程或内容变化时更新
owner: 项目文档负责人
status: draft
note: 企业初始化模板
---

# MinIO上传超时复盘

## 现象

上传大视频时接口超时。

## 可能原因

- 后端请求超时
- Nginx上传限制
- 临时目录空间不足
- MinIO连接异常

## 经验沉淀

大文件上传能力必须同时更新：

- `.env.example`
- Docker Compose
- Nginx `client_max_body_size`（Web 镜像 `src/web/nginx.conf`）
- 后端 `MAX_IMAGE_SIZE_MB` / `MAX_VIDEO_SIZE_MB` 与 MIME 白名单
- Web 镜像重建（`docker compose build web`）

**Sprint 002 案例**：`BUG-0020` — Docker Web `localhost:3000` 上传 MP4 返回 **413**，根因为 Nginx 默认 ~1MB 限制，与后端 env 未对齐。详见 `best-practices/admin-media-upload-chain.md`。

## 关联

- OpenSpec：`openspec/specs/object-storage/spec.md`
- 上传标准：`docs/standards/file-upload.md`
