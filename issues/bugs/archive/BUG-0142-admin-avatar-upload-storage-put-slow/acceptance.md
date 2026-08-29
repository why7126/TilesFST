---
bug_id: BUG-0142-admin-avatar-upload-storage-put-slow
acceptance_status: passed
created_at: 2026-08-25 17:52:49
updated_at: 2026-08-28 16:21:48
---

# 验收计划

## 回归验收项

| 编号 | 验收项 | 预期结果 | 状态 |
|---|---|---|---|
| AC-001 | WebP 头像上传性能 | 使用触发问题的 127KB 级 WebP 样本调用 `POST /api/v1/admin/uploads`，不再出现 30 秒级等待。 | pass |
| AC-002 | 阶段级慢点可定位 | 修复前已能通过日志详情确认 `thumbnail_generate=28464ms`，修复后该阶段不再出现 20 秒以上长尾耗时。 | pass |
| AC-003 | 上传响应完整 | 上传返回 200，并包含原图、thumbnail、display 的 key / URL 和 `task_trace_id`。 | pass |
| AC-004 | 媒体读取可用 | `/media/{object_key}`、`/media/{thumbnail_key}`、`/media/{display_key}` 均可通过后端受控 URL 读取。 | pass |
| AC-005 | 管理端回显不回归 | 管理端头像上传完成后可即时回显；失败时显示可理解失败态，不长时间卡住。 | pass |
| AC-006 | 其他图片上传不回归 | 品牌 Logo、Banner、瓷砖图片等图片上传路径不因头像性能修复出现 key、object、URL 或 render 回归。 | pass |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0142-admin-avatar-upload-storage-put-slow |
| 标题 | 管理端头像上传小文件对象存储写入耗时 30 秒以上 |
| 严重等级 | high |
| 影响范围 | Web 管理端 / 后端上传接口 / 对象存储 / 头像派生图 |
| 复现入口 | 管理端头像上传，或受控调用 `POST /api/v1/admin/uploads` |
| 受影响端 | admin / backend / storage |
| 环境 | docker |
| 媒体类型 | image / avatar / thumbnail / display |
| 业务资源 | 管理端当前用户头像，脱敏 object key 前缀为 `images/default/user/avatars/` |
| 修复前实际结果 | 127KB 级 WebP 头像上传返回 200，但接口等待约 31.7 秒；阶段级日志确认 `thumbnail_generate=28464ms`，外层 `storage_put_object` 显示 30 秒级累计耗时。 |
| 修复后期望结果 | WebP 头像上传不再出现 30 秒级等待，`thumbnail_generate` 不再出现 20 秒以上长尾耗时，且原图、thumbnail、display 对象与 URL 均可读取并回显。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | 上传响应返回 `images/default/user/avatars/<uuid>.<ext>`、`.thumb.webp`、`.display.webp` 等脱敏 key，符合单 Bucket 与标准前缀策略。 | 若 key 缺失或前缀错误，记录响应摘要和后端生成 key 逻辑。 |
| object | pass | 对象存储中原图、thumbnail、display 均存在，MIME、size、扩展名和权限边界符合预期。 | 若对象缺失、0 字节或读取异常，记录受影响 key、HTTP 状态和存储 provider 摘要。 |
| URL | pass | `/media/{object_key}`、`/media/{thumbnail_key}`、`/media/{display_key}` 通过后端受控 URL 返回 200，不直连未授权对象存储。 | 若 403 / 404 / 502，记录 URL 类型、业务错误码和 request/task trace id。 |
| render | pass | 修复前证据 `screenshots/network-upload-31s.png` 显示管理端头像最终回显，上传 POST 返回 200 但等待 `31.74 秒`；修复后同一入口不再长时间等待。 | 若回显缺失或卡住，记录页面入口、Network 摘要和用户可见表现。 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | pass | 管理端头像上传从 uploading 到 done/failed 的状态变化正常，不长期停留在等待态。 |
| 同会话即时回显 | pass | 修复前截图显示头像最终回显；修复后上传成功后同一页面或弹窗立即展示头像预览，且不出现 30 秒级等待。 |
| Docker Web 边界 | pass | 修复前截图来自 `localhost:3000` Web 入口；修复后通过 Docker Web 入口或等价 Web 入口上传问题 WebP 样本，接口总耗时和 Network 状态通过。 |
| 媒体代理一致性 | pass | 上传响应 key 与 `/media/{key}` 读取一致，thumbnail / display URL 同步验证通过。 |
| 历史对象与审计 | n/a | 本 BUG 不涉及历史对象迁移、缩略图回填或审计脚本。 |
| 小程序 evidence | n/a | 本 BUG 只影响 Web 管理端头像上传，不影响小程序页面或组件。 |

## 测试建议

- 增加后端聚焦测试，覆盖头像上传返回原图、thumbnail、display key，并验证 task trace 包含阶段级耗时字段或 span。
- 增加对象存储客户端 mock 测试，模拟单个 `put_object` 慢调用，确认 slow span 能定位到具体阶段。
- 增加 WebP 样本性能 smoke，记录 127KB 级 WebP 上传在本地 Docker 环境下不出现 30 秒级等待。
- 保留管理端 UI 测试或 smoke，确认上传成功后头像预览即时更新。

## 验收结论

当前状态：`passed`

根因已由阶段级日志详情确认为 `confirmed`：主要慢点为头像 WebP 缩略图生成阶段 `thumbnail_generate`，不是对象存储原图或缩略图写入。修复已收敛 WebP thumbnail 生成长尾耗时，并保留媒体四联验收。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 23:14:36
accepted_by: workflow-sync
source_change: fix-admin-avatar-webp-thumbnail-timeout
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

