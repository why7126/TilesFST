## Context

`BUG-0003-brand-image-display-layout-shift` 关联 `REQ-0005-brand-management` 与 `add-brand-management`。当前品牌管理已具备品牌列表、品牌弹窗、Logo 上传和 `logo_object_key` 保存能力，但缺少“上传后 URL 可被浏览器展示”的闭环。

已确认代码线索：

| 线索 | 路径 | 结论 |
|---|---|---|
| Logo URL 生成 | `src/backend/app/services/brand_admin_service.py` | `_logo_url()` 返回 `/media/{object_key}` |
| 上传返回 | `src/backend/app/api/v1/uploads.py` | `upload_brand_logo()` 返回 `/media/brands/logos/{filename}` |
| 后端入口 | `src/backend/app/main.py` | 当前仅挂载 `/api/v1` 与 `/health`，未挂载 `/media` |
| 列表展示 | `src/web/src/pages/admin/BrandManagementPage.tsx` | `brand.logo_url` 直接进入 `<img src>` |
| 弹窗回显 | `src/web/src/features/admin/components/BrandFormModal.tsx` | `brand.logo_url` / 上传返回 `url` 直接进入预览图 |
| Tips 布局 | `BrandManagementPage.tsx` + `admin-home.css` | `admin-notice` 条件插入普通文档流，自动消失导致高度变化 |

## Decisions

### D1：媒体访问策略

修复 MUST 在后端提供受控媒体访问能力，保证品牌 Logo 上传返回的 `url` 和品牌列表返回的 `logo_url` 能被浏览器加载。

允许方案：

1. **受控 `/media/{object_key}` 代理**：后端校验 object_key 后从 MinIO 或本地开发存储读取对象并返回响应。
2. **签名 URL / 预览 URL**：上传和品牌列表返回可短期访问的签名 URL；字段仍可命名为 `url` / `logo_url`，若新增 `preview_url` 必须更新 OpenAPI 与 Orval。
3. **开发环境静态服务 + 生产 MinIO 代理**：仅当文档明确区分环境并保持接口语义一致时可用。

不允许方案：

- 前端直接拼接未授权 MinIO 地址。
- 暴露真实对象存储密钥、内部绝对路径或运行时目录。
- 仅改前端占位图掩盖真实媒体不可访问问题。

### D2：对象 Key 与文件安全

修复 MUST 继续遵守：

- 图片上传经后端鉴权。
- MIME Type / 扩展名校验。
- 不信任前端传入文件路径。
- 不使用用户原始文件名作为最终可信对象 Key。
- 遵守 MinIO 单桶与业务前缀策略。

若本 change 需要调整当前 `brands/logos/{safe_name}` 生成方式，应同步测试覆盖 object_key 安全性。

### D3：品牌列表与编辑弹窗展示

前端 MUST 使用后端返回的可访问 URL 渲染品牌 Logo。

- 列表页：有 Logo 时显示图片；无 Logo 时保留品牌首字/缩写占位。
- 编辑弹窗：打开时回显当前 Logo；更换 Logo 后即时更新预览；保存后再次打开仍显示最新 Logo。
- 图片加载失败时应保持稳定尺寸和空态，不得造成表格或弹窗布局跳动。

### D4：Tips 布局策略

品牌页自动消失状态提示 MUST 不参与主体内容高度计算。

推荐方案：

1. 固定定位 toast 容器，挂在管理端内容区右上或顶部安全区域。
2. 页面级稳定提示槽，始终预留高度，内容出现/消失不改变后续内容位置。
3. 复用或抽取管理端通知组件，但不得新增与 Design System 冲突的样式。

表单内错误文案可以继续 inline 展示，但列表页状态反馈不得推挤 `page-hero`、统计卡、筛选区、表格或分页。

### D5：API / Orval 策略

- 如果只补齐 `/media/{object_key}` 可访问服务，且 `UploadResult.url` / `BrandAdminItem.logo_url` schema 不变，则 MAY 不运行 Orval。
- 如果新增或改名字段（如 `preview_url`）、改变 UploadResult 或品牌响应结构，则 MUST 更新 OpenAPI、运行 Orval，并同步 `docs/03-api-index.md`。

## Test Strategy

| 层级 | 验证 |
|---|---|
| 后端 pytest | 上传合法/非法 Logo；返回 URL 可访问；非法 object_key 不泄露路径；权限保持 admin/employee |
| 前端 Vitest | 品牌列表 Logo 渲染；编辑弹窗 Logo 回显与更换；notice/toast 不作为推挤主体的文档流节点 |
| 集成/手工 | 上传 Logo → 保存 → 列表展示 → 编辑回显；启停/删除/保存提示出现消失不造成页面位移 |
| 构建 | Web build；必要时后端测试与 Docker Compose 验证 |

## Risks

| 风险 | 影响 | 缓解 |
|---|---|---|
| 媒体代理绕过权限或暴露路径 | 安全风险 | object_key 校验、禁止绝对路径、后端受控读取 |
| URL 策略影响 SKU 图片/视频 | 媒体链路回归 | 测试 SKU 上传展示或限定本 change 仅品牌 Logo |
| Orval 未同步 | 前端类型错配 | schema 变更时强制运行 Orval |
| toast 固定定位遮挡内容 | UI 可用性下降 | 遵守管理端 DS，移动/桌面都检查 |

## Open Questions

| 问题 | 当前决策 |
|---|---|
| 是否使用签名 URL 还是 `/media` 代理 | 实现前在 tasks 中确认；默认优先受控 `/media` 代理以兼容现有 URL |
| 是否更新长期媒体文档 | 若修复形成通用媒体访问策略，需同步 docs/06-video-asset-management.md 或 docs/03-api-index.md |
