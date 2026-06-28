---
bug_id: BUG-0003-brand-image-display-layout-shift
status: approved
updated_at: 2026-06-25 22:19:51
root_cause_type: code/frontend-ui/media-routing
---

# 根因分析

## 1. 直接原因

### 1.1 品牌图片 URL 指向未挂载的 `/media` 路径

品牌 Logo 上传接口和品牌列表接口都会返回 `/media/{object_key}` 格式的图片地址：

```text
src/backend/app/api/v1/uploads.py
src/backend/app/services/brand_admin_service.py
```

关键行为：

- `upload_brand_logo()` 返回 `url: /media/brands/logos/{filename}`。
- `BrandAdminService._logo_url()` 根据 `brands.logo_object_key` 生成 `logo_url: /media/{object_key}`。
- `BrandManagementPage.tsx` 和 `BrandFormModal.tsx` 直接把 `logo_url` / 上传返回 `url` 放入 `<img src="...">`。

但 FastAPI 入口 `src/backend/app/main.py` 当前只挂载：

```text
/api/v1
/health
```

未看到 `/media` 静态文件服务、MinIO 签名 URL 代理、对象读取 API 或 Nginx 反向代理规则。因此浏览器请求 `/media/brands/logos/...` 时没有可用服务承接，导致列表页和编辑弹窗中的 `<img>` 无法加载。

### 1.2 上传接口只返回对象 Key 形式的占位 URL，未确保文件可访问

`src/backend/app/api/v1/uploads.py` 当前上传逻辑只基于文件名生成 object_key 和 `/media/...` URL，未在该代码路径中体现以下能力：

- 写入 MinIO 或本地可服务目录。
- 生成签名 URL 或受控公开 URL。
- 保证 `/media/{object_key}` 可被后端或 Web 服务访问。

这使“上传成功返回 URL”和“前端能够通过 URL 展示图片”之间缺少闭环。

### 1.3 状态 Tips 作为普通文档流节点条件插入

`src/web/src/pages/admin/BrandManagementPage.tsx` 在页面主体最前面条件渲染：

```text
notice ? <p className="admin-notice">...</p> : null
```

该节点位于 `page-hero` 前，属于正常文档流。`src/web/src/features/admin/styles/admin-home.css` 中 `.admin-notice` 仅定义了 `margin-bottom`、`padding`、`border`、`background` 等样式，没有固定定位、浮层容器或预留空间策略。

因此状态变更时：

1. `setNotice('品牌已启用' / '品牌已停用')` 插入一行 `admin-notice`。
2. 3.2 秒后定时器清空 notice。
3. 插入和移除都会改变页面主体的纵向布局高度。

这就是 Tips 出现/消失时页面上下波动的直接原因。

## 2. 根本原因

### 2.1 媒体上传与展示链路没有统一验收闭环

品牌 Logo 能保存 `logo_object_key`，但系统没有在品牌管理流程中强制验证：

- 上传响应 URL 是否真实可访问。
- 品牌列表返回的 `logo_url` 是否可被浏览器加载。
- 编辑弹窗根据既有 `logo_url` 是否能回显。

这导致“上传接口可调用”和“图片可展示”被当成同一件事，但实际缺少媒体访问层。

### 2.2 媒体访问策略与对象存储规范未在实现层对齐

项目规范要求图片上传走后端授权与 MinIO / 对象存储，并对外使用签名 URL 或受控公开策略。当前品牌 Logo 实现返回相对 `/media` 地址，但缺少与 MinIO 单桶策略、对象前缀、签名 URL 或受控媒体路由的完整对接。

### 2.3 管理端提示组件缺少统一浮层/非占位模式

品牌页、用户页、类目页等管理端页面都存在局部 `notice` 状态和 `.admin-notice` 样式使用。当前模式适合表单内错误说明或静态提示，但不适合“操作成功后几秒自动消失”的状态反馈，因为自动消失提示会造成布局高度变化。

## 3. 触发条件

### 3.1 图片不显示

满足以下条件时触发：

1. 管理员或员工进入「瓷砖品牌」。
2. 在新增或编辑弹窗中上传品牌 Logo。
3. 上传接口返回 `object_key` 与 `/media/...` URL。
4. 保存品牌后，列表页或编辑弹窗根据 `logo_url` 渲染 `<img>`。
5. 浏览器请求 `/media/...`，但后端或 Web 服务未提供对应媒体访问能力。

### 3.2 Tips 布局波动

满足以下条件时触发：

1. 在品牌列表页执行启用、停用、删除、保存等会调用 `setNotice()` 的操作。
2. 页面顶部插入 `admin-notice`。
3. 定时器几秒后移除 `admin-notice`。
4. 页面主体随提示节点出现和消失发生纵向位移。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui / media-routing |
| 是否接口缺陷 | 是，上传和品牌接口返回的媒体 URL 缺少可访问保障 |
| 是否数据库缺陷 | 否，当前线索显示 `logo_object_key` 字段可承载对象 Key |
| 是否权限缺陷 | 待修复阶段验证；媒体访问必须保持后端授权或受控公开策略 |
| 是否对象存储缺陷 | 是，媒体对象访问链路未闭环到 MinIO/受控 `/media` 服务 |
| 是否 Design System 缺陷 | 是，自动消失 Tips 使用占位文档流导致页面抖动 |
| 主要修复面 | 后端媒体访问 URL 策略、品牌 Logo 展示回显、管理端 notice/toast 布局策略 |

## 5. 后续修复建议

1. 明确品牌 Logo 的媒体访问策略：签名 URL、受控 `/media/{object_key}` 后端代理，或开发环境静态文件服务，但必须符合 `rules/security.md` 与 `rules/object-storage.md`。
2. 上传接口返回的 `url` / `preview_url` 必须能被前端实际加载；品牌列表和编辑弹窗回显应使用同一可访问 URL。
3. 修复时补充品牌 Logo 上传、保存、列表展示、编辑回显的前端测试或集成测试。
4. 将品牌页自动消失状态提示改为不参与主体文档流的固定 toast，或为提示区域保留稳定高度，避免内容位移。
5. 回归检查用户管理、类目管理、SKU 管理等页面是否复用同类 `.admin-notice` 自动消失模式，避免同类问题扩散。
