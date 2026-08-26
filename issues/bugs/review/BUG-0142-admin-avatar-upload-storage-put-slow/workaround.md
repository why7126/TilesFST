---
bug_id: BUG-0142-admin-avatar-upload-storage-put-slow
document_status: ready
created_at: 2026-08-25 17:52:49
updated_at: 2026-08-25 17:52:49
---

# 临时规避方案

## 可用规避

在正式修复前，可采用以下临时规避方式降低管理端头像上传长等待风险：

1. 优先使用 JPEG 或 PNG 头像进行管理端上传。当前对照复现中约 146KB JPEG 头像上传未出现 30 秒级等待。
2. 若必须使用 WebP，先压缩或重新导出 WebP，再上传；保留原始慢样本用于后续补证。
3. 测试或运维人员可直接调用后端 `POST /api/v1/admin/uploads` 做受控复现，记录 `task_trace_id`、请求总耗时、content type 和 size，避免只凭浏览器等待时间判断。
4. 若出现 30 秒级等待但最终返回 200，可先使用返回的 `object_key` 保存头像，并立即访问 `/media/{object_key}`、thumbnail URL 和 display URL 确认对象可读。

## 风险与限制

- 改用 JPEG / PNG 只能降低触发概率，不能修复 WebP 上传链路的慢点。
- 直接调用后端接口仍必须使用合法管理端鉴权，不得绕过上传校验。
- 当前观测口径不能拆分原图写入、派生图生成和派生图写入；临时规避无法证明根因已消失。
- 如果对象存储本身存在连接抖动或重试，所有图片上传类型仍可能受影响。

## 推荐正式修复方向

1. 为头像上传链路补充阶段级 task trace 或结构化日志，拆分 file read、原图 put、thumbnail generation、thumbnail put、display generation、display put。
2. 基于补证结果决定修复策略：降低 WebP 派生编码成本、优化对象存储客户端连接/超时、减少同步派生写入，或将非关键派生处理异步化。
3. 保持上传响应中的 `object_key`、thumbnail / display key 和 `/media/...` URL 一致，避免性能修复引入媒体对象不可读或回显缺失。
