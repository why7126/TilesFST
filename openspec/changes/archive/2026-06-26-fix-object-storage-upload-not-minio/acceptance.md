---
change_id: fix-object-storage-upload-not-minio
bug_id: BUG-0006-object-storage-upload-not-minio
status: proposed
created_at: 2026-06-26 13:47:54
---

# 验收标准

## AC-001 MinIO 单桶写入

- [ ] 管理端上传品牌 Logo 后，对象写入 `MINIO_BUCKET=tile-info-platform`
- [ ] 管理端上传头像、SKU 图片、SKU 视频后，对象写入同一 Bucket
- [ ] MinIO Console 或 `mc ls` 可看到对应对象
- [ ] 未新增 `tile-images`、`tile-videos` 等业务 Bucket

## AC-002 标准对象前缀

- [ ] 图片类对象使用 `original/` 前缀
- [ ] 视频类对象使用 `videos/` 前缀
- [ ] 如涉及视频封面，使用 `videos/covers/` 前缀
- [ ] 对象 Key 不使用用户原始文件名

## AC-003 后端授权与校验

- [ ] 上传仍需 admin / employee 或对应既有权限
- [ ] MIME 白名单仍生效
- [ ] 文件大小限制仍生效
- [ ] 前端不直连未授权 MinIO

## AC-004 URL 与读取

- [ ] 上传响应返回的 URL 可读取 MinIO 对象
- [ ] `/media/{object_key}` 或等价 URL 不暴露 MinIO 密钥和内部 endpoint
- [ ] 非法 object_key 被拒绝
- [ ] 不存在对象返回稳定错误

## AC-005 API 与文档

- [ ] 若响应 schema 未变，记录无需 Orval 的理由
- [ ] 若响应 schema 有变，完成 OpenAPI、Orval、前端调用方同步
- [ ] 更新 API、对象存储、视频资产、data 目录相关文档
- [ ] `.env.example` 覆盖必要 MinIO 与上传限制变量

## AC-006 回归测试

- [ ] 后端 pytest 覆盖 MinIO 写入
- [ ] 后端 pytest 覆盖媒体读取与非法 object_key
- [ ] 回归品牌 Logo、用户头像、SKU 图片/视频上传入口
- [ ] Docker Compose 上传闭环验证通过或记录阻塞原因
