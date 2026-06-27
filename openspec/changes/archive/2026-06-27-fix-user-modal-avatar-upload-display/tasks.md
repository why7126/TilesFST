## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0019-user-modal-avatar-upload-display` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 确认 BUG 状态为 `approved`
- [x] 1.3 对照 `BrandFormModal` 与 `brand_admin_service._logo_url` 实现模式

## 2. 后端 avatar_url

- [x] 2.1 `UserAdminItem` schema 增加 `avatar_url: str | None`
- [x] 2.2 `UserAdminService.to_item()` 生成 `/media/{object_key}`（参照 `_logo_url`）
- [x] 2.3 同步 OpenAPI、运行 Orval、更新 `docs/03-api-index.md`（若需）
- [x] 2.4 pytest：用户列表/详情返回可访问 `avatar_url`（参照品牌 Logo URL 测试）

## 3. UserFormModal 上传与预览

- [x] 3.1 增加 `avatarUrl`、上传状态机（idle/uploading/uploaded/failed）、进度 state
- [x] 3.2 编辑模式从 `user.avatar_url` 初始化预览
- [x] 3.3 选择文件后立即上传；成功更新 key+url+预览；失败展示错误
- [x] 3.4 上传中展示进度条/百分比；上传中禁止保存
- [x] 3.5 重置 file input；对齐 BrandFormModal UI 文案与 DS token

## 4. uploadAvatar 封装

- [x] 4.1 `uploadAvatar(file, onProgress?)` 支持 `onUploadProgress`
- [x] 4.2 确认品牌/SKU 等其他上传入口不回退

## 5. UserManagementPage 列表头像

- [x] 5.1 有 `avatar_url` 时渲染 `<img>`，无则 initials
- [x] 5.2 图片 onError 回退 initials，无布局跳动

## 6. 测试与验收

- [x] 6.1 Vitest：弹窗上传状态机、预览更新、失败重试
- [x] 6.2 Vitest：列表头像渲染与 fallback
- [x] 6.3 回归用户管理 CRUD、重置密码、状态变更测试
- [x] 6.4 手工：弹窗更换头像 → 进度 → 预览 → 保存 → 列表/再编辑回显（Vitest + pytest 覆盖等价路径）
- [x] 6.5 更新 change `trace.md` 与 `BUG-0019/trace.md`
- [x] 6.6 评估是否更新 `docs/knowledge-base/incidents/`（跳过：交付缺口，无 incidents 沉淀）
