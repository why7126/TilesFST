---
bug_id: BUG-0085-admin-video-upload-stuck-at-99
title: 管理后台视频上传长时间卡在 99% 验收标准
status: done
created_at: 2026-07-24 20:36:23
updated_at: 2026-07-26 15:25:45
severity: high
related_requirement:
related_bug: BUG-0081-prod-cos-video-upload-fails
related_change:
---

# Acceptance - BUG-0085 管理后台视频上传长时间卡在 99%

## AC-0085-01 合法视频上传闭环成功

**Given** 管理员已登录生产或等价验收环境的管理后台  
**And** 选择一个符合 `ALLOWED_VIDEO_TYPES` 且未超过 `MAX_VIDEO_SIZE_MB` 的 MP4 视频  
**When** 在 SKU 新增或编辑弹窗上传该视频  
**Then** `POST /api/v1/admin/uploads/tile-videos` MUST 返回 `200`  
**And** 响应体 MUST 包含 `object_key` 与 `/media/{object_key}`  
**And** 前端 MUST 将视频加入 SKU 表单视频列表并显示成功状态。

## AC-0085-02 99% 后不得无解释长时间等待

**Given** 浏览器请求体上传已经接近完成  
**When** 后端仍在保存对象或等待对象存储响应  
**Then** 前端 MUST 不再只显示“上传中 99%”作为唯一状态  
**And** MUST 显示可理解的服务端等待状态，例如“正在保存视频，请稍候”或等价文案  
**And** 该状态不得阻止失败后的重试路径。

## AC-0085-03 反代和对象存储响应链路不再超时截断

**Given** 上传请求经外层 HTTPS Nginx、容器内 Web Nginx 和 backend 到达对象存储  
**When** 上传一个合法视频且对象存储写入耗时长于普通小文件上传  
**Then** 外层与容器内 Nginx MUST 对 `/api/v1/admin/uploads/` 使用上传专用超时配置  
**And** 不得出现约 60 秒默认超时导致的 `504` 或 `499`  
**And** 对象写入成功后接口 MUST 在配置的超时窗口内把结果返回给浏览器。

## AC-0085-04 对象存储写入与受控读取可验证

**Given** 视频上传接口返回成功  
**Then** 对象存储 Bucket 中 MUST 存在响应 `object_key` 对应对象  
**And** object key MUST 使用 `videos/...` 规范前缀  
**And** `/media/{object_key}` MUST 可经后端受控读取，不要求前端直连对象存储原始地址。

## AC-0085-05 错误场景可诊断

**Given** 对象存储不可用、权限不足、bucket/region/endpoint 配置错误、MIME 不允许或文件大小超限  
**When** 管理员上传视频  
**Then** 上传接口 MUST 返回明确错误码与错误信息  
**And** 前端 MUST 显示失败状态并允许重新选择文件上传  
**And** 日志 MUST 能支持定位是代理超时、对象存储配置、权限、网络还是文件校验问题。

## AC-0085-06 回归范围

**Given** BUG-0085 修复完成  
**Then** SKU 图片上传、品牌 Logo 上传、Banner 图片上传和品牌证书上传 MUST 不受影响  
**And** 视频上传大小限制、Nginx `client_max_body_size` 与系统媒体设置 MUST 保持一致  
**And** 不得引入前端直连未授权对象存储写入能力。

## 建议验证命令

```bash
uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py
```

若修复涉及前端状态文案或上传组件，还应补充并运行对应 Vitest 用例。
