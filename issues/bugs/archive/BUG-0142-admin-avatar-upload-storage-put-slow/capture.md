---
bug_id: BUG-0142-admin-avatar-upload-storage-put-slow
status: done
created_at: 2026-08-25 17:40:13
updated_at: 2026-08-27 23:14:42
severity_hint: high
environment: docker
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

管理端头像上传小文件时对象存储写入耗时异常。127KB WebP 头像上传 `POST /api/v1/admin/uploads` 最终返回 200，但接口等待约 31.74 秒；`task_trace` 显示 `storage_put_object` 约 31.7s/32.2s，媒体读取约 114ms。

# 复现步骤

1. 使用管理端账号登录。
2. 进入支持头像上传的管理端页面。
3. 选择约 127KB 的 WebP 头像文件并发起上传。
4. 观察浏览器 Network 中 `POST /api/v1/admin/uploads` 的等待时间和响应状态。
5. 查看后端 `task_trace` 中对象存储写入、派生图处理和媒体读取耗时。

# 期望 vs 实际

- 期望：127KB 级别头像上传应在可接受时间内完成，对象存储写入和头像派生图处理不应出现 30 秒级阻塞。
- 实际：接口返回 200，但整体等待约 31.74 秒；耗时主要集中在 `storage_put_object`，媒体读取仅约 114ms。

# 影响范围

- 管理端头像上传体验。
- 后端上传接口 `POST /api/v1/admin/uploads`。
- Backend 到对象存储的 `put_object` 链路。
- 头像上传后的派生图生成与多对象写入链路。

# 初步线索

- `task_trace` 指向 `storage_put_object` 耗时约 31.7s/32.2s，初步排除媒体读取本身是主要瓶颈。
- 疑似 Backend 到对象存储的 `put_object` 调用存在连接、重试、超时或同步阻塞问题。
- 也可能是头像上传触发派生图多次写入，每次写入串行等待，造成接口尾延迟放大。

# 建议验收或复现要点

- [ ] 使用同一 127KB WebP 头像复现上传，记录接口总耗时与 `task_trace`。
- [ ] 区分原图写入、头像派生图写入和媒体读取耗时，确认慢点是否集中在单次或多次 `put_object`。
- [ ] 对比本地文件存储与 MinIO / 对象存储环境下的上传耗时。
- [ ] 确认修复后同类小文件头像上传不再出现 30 秒级等待，且返回 200 后对象可正常读取。

# 附件

- 用户描述：`管理端头像上传小文件对象存储写入耗时 30 秒以上：127KB WebP 头像上传 POST /api/v1/admin/uploads 返回 200 但等待约 31.74 秒；task_trace 显示 storage_put_object 约 31.7s/32.2s，媒体读取约 114ms，疑似 Backend -> 对象存储 put 或头像派生图多次写入导致。`
