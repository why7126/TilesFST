# Design: fix-user-modal-avatar-upload-display

## 1. 背景

`BUG-0019` 表明用户头像展示链路断裂：

```text
头像上传 → MinIO object → users.avatar_object_key → 用户接口 avatar_url → 浏览器加载 → 弹窗/列表展示
```

运行时验证：上传与 DB 写入正常，断点在 URL 生成与前端绑定。

## 2. 根因摘要

| ID | 根因 |
|---|---|
| RC-001 | `UserFormModal` 硬编码 initials，不读取 `avatarKey` / URL |
| RC-002 | 上传成功后丢弃响应 `url`，无 `avatarUrl` state |
| RC-003 | 缺少 idle/uploading/uploaded/failed 状态机与进度 UI |
| RC-004 | `UserManagementPage` 列表不渲染头像图片 |
| RC-005 | `UserAdminService.to_item()` 未生成 `avatar_url` |

## 3. 修复策略

### D1 后端 avatar_url

参照 `brand_admin_service._logo_url`：

```python
def _avatar_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{object_key}"
```

- `UserAdminItem` schema 增加 `avatar_url: str | None`。
- 列表/详情/创建/更新响应均通过 `to_item()` 填充。
- 同步 OpenAPI → Orval → `docs/03-api-index.md`（若索引含用户字段）。

### D2 UserFormModal（对齐 BrandFormModal）

- State：`avatarKey`、`avatarUrl`、`avatarUploadState`、`avatarUploadProgress`、`avatarUploadError`。
- 打开编辑弹窗：从 `user.avatar_url` 初始化预览。
- `handleAvatarChange`：uploading → 调用 `uploadAvatar(file, onProgress)` → 成功 set key+url → uploaded；失败 → failed。
- UI：有 `avatarUrl` 时 `<img>` + 文案「已上传头像」；无则 initials +「默认头像」。
- 上传中禁用保存；进度条/百分比与品牌 Logo 控件一致。
- 失败展示错误，保留重试；重置 file input value。

### D3 UserManagementPage 列表

- 用户列：有 `avatar_url` 时 `<img className="avatar">`（或等价），`onError` 回退 initials。
- 无 `avatar_url` 保持 `getUserInitials()`。

### D4 uploadAvatar 封装

- 扩展 `users-api.uploadAvatar(file, onProgress?)`，使用 axios `onUploadProgress`（参照 `uploadBrandLogo`）。
- 不改变上传端点或 `UploadResult` schema。

## 4. 测试策略

| 类型 | 覆盖 |
|---|---|
| pytest | 用户列表/详情返回 `avatar_url`；GET `/media/{key}` 200 |
| Vitest | 弹窗上传状态机、预览更新、失败重试、列表头像渲染 |
| 回归 | 用户 CRUD、重置密码、冻结/解冻、删除；品牌 Logo 上传不回退 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| Orval 类型漂移 | 变更后立即 regenerate 并修复编译 |
| 共享 upload 封装影响其他入口 | 可选参数 onProgress，默认行为不变 |
| 列表 img 破坏布局 | 复用 `.avatar` 尺寸与 fallback |

## 6. 参考实现

- `src/web/src/features/admin/components/BrandFormModal.tsx`
- `src/backend/app/services/brand_admin_service.py` `_logo_url`
- `openspec/changes/archive/2026-06-26-fix-brand-logo-upload-progress/`
- `openspec/changes/archive/2026-06-26-fix-brand-logo-display-after-storage-fix/`
