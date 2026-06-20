---
title: 业务流程
purpose: 瓷砖SKU管理列表、筛选、弹窗、素材上传与上下架主流程
content: 基于 requirement.md 与 prototype/web/tile-sku-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0006-tile-sku-management
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee / 只读）
  ↓
进入 /admin/tile-skus（或等价路由）
  ↓
浏览 / 搜索 / 筛选 SKU 列表
  ↓
可选操作：
  ├─ 新增 SKU → 弹窗 → POST → Toast + 刷新列表（page=1）
  ├─ 编辑 SKU → 弹窗 → PUT → Toast + 刷新
  ├─ 上下架 / 恢复 → POST publish/unpublish → Toast
  └─ 删除（仅草稿/已停用且无引用）→ 确认 → DELETE → Toast
```

## 2. 访问与权限流程

```text
用户携带 JWT 访问 SKU 管理页
  ↓
ProtectedRoute：已登录？
  ├─ 否 → /admin/login
  └─ 是 → 具备 tile_sku:list（或运营角色默认允许）？
        ├─ 否 → 403 或重定向 /admin/dashboard
        └─ 是 → 渲染 TileSkuManagementPage
              ↓
              只读角色？→ 隐藏新增/编辑/删除/上下架入口
```

### 2.1 角色与菜单

| 产品角色 | 后端 role（建议） | SKU 管理菜单 | 写操作 |
|---|---|---|---|
| 后台运营 | `employee` | OPERATIONS > 瓷砖SKU | 增删改查、上下架（删除受规则约束） |
| 后台管理员 | `admin` | 同上 | 全量 SKU 操作 |
| 只读账号 | `employee` + 只读权限点 | 可见菜单 | 仅查看 |
| 店主 | `store_owner` | 不可见 | 不允许进入管理端 |

## 3. 列表查询流程

```text
页面加载
  ↓
GET /api/v1/admin/tile-skus?page=1&page_size=20&keyword=&brand_id=&category_id=&status=&material_completeness=
  ↓
响应含 items + total + summary（SKU总数/已上架/待完善/草稿）
  ↓
默认按 updated_at 倒序
  ↓
渲染 page-head + metric-grid + filter-card + table + pagination
```

### 3.1 搜索与重置

```text
用户输入关键词 / 选择品牌、类目、状态、素材完整度
  ↓
点击「查询」或回车
  ↓
page 重置为 1，带 query 重新请求
  ↓
点击「重置」→ 清空全部条件 → 重新请求默认列表
```

### 3.2 分页

```text
左侧展示 total → 「共 {total} 条」
  ↓
右侧：‹ 页码 › + 每页条数（10 / 20 / 50 / 100，默认 20）
  ↓
切换每页条数 → page=1，保留筛选条件
切换页码 → 带当前筛选条件请求
```

## 4. 新增 SKU 流程

```text
点击「新增SKU」
  ↓
打开弹窗（880px，内部滚动；标题含「创建后默认草稿」提示）
  ↓
填写字段（顺序见 requirement.md §4.2）：
  名称*、编码*、品牌*、类目*、规格*、工艺*、主色系、参考价格（元）、图片、视频、备注
  ↓
图片：多张上传 → 缩略图网格 → 指定一张主图（is_main）
视频：多个上传 → 文件卡片列表
  ↓
客户端校验必填项；失败 → 字段风险色边框 + 下方错误文案
  ↓
「保存草稿」或「创建SKU」→ POST /api/v1/admin/tile-skus
  ↓
成功：
  ├─ Toast「SKU创建成功，已保存为草稿」
  ├─ 关闭弹窗，列表刷新至第一页
  └─ 新记录 status=DRAFT（弹窗无状态控件）
失败：保留弹窗输入，展示服务端错误（如编码重复）
```

### 4.1 缺主图草稿

```text
用户未设主图
  ↓
点击「保存草稿」或「创建SKU」
  ↓
允许保存（status=DRAFT 或 NEEDS_COMPLETION，实现时定稿）
  ↓
列表素材列显示「缺主图」；素材完整度筛选可命中「缺主图」
```

## 5. 编辑 SKU 流程

```text
列表点击「编辑」
  ↓
GET /api/v1/admin/tile-skus/{id}（含图片、视频、品牌、类目）
  ↓
打开弹窗，字段同新增；弹窗仍不展示状态字段
  ↓
可切换主图、增删图片/视频、修改价格等
  ↓
PUT /api/v1/admin/tile-skus/{id}
  ↓
成功 → Toast → 刷新列表
```

## 6. 上下架 / 恢复流程

```text
已上架 SKU → 点击「下架」
  ↓
POST .../unpublish（或 status 变更）
  ↓
成功 → Toast → 刷新列表与指标卡

草稿 / 已停用 / 待完善 → 点击「上架」或「恢复」
  ↓
校验：必填项与主图是否满足上架策略（实现时定稿）
  ↓
POST .../publish
  ↓
成功 → status=PUBLISHED → Toast → 刷新
```

## 7. 删除流程

```text
渲染操作列时计算：
  canDelete = (status IN (DRAFT, DISABLED) AND no_business_reference)
  ↓
canDelete = false → 「更多」内删除置灰或不可见
  ↓
canDelete = true → 确认弹窗 → DELETE /api/v1/admin/tile-skus/{id}
  ↓
已上架 → 服务端拒绝（如 TILE_SKU_DELETE_FORBIDDEN）
```

## 8. 图片 / 视频上传流程

```text
弹窗内选择图片（JPG/PNG/WebP）或视频（MP4 等，见 rules/media.md）
  ↓
POST 后端授权上传 → MinIO（前缀如 tile-skus/images/、tile-skus/videos/）
  ↓
返回 object_key / url 写入 SKU payload
  ↓
图片：标记 is_main=1 的一张为主图；列表 SKU 信息列展示主图缩略图
视频：以卡片展示文件名、大小、上传状态；支持删除与继续添加
```

## 9. 与父需求 / 现有能力的差异

| 对比项 | REQ-0004 / 品牌 / 类目 | REQ-0006 SKU |
|---|---|---|
| 核心实体 | 品牌、类目主数据 | SKU 商品主数据 |
| 弹窗宽度 | 720px（品牌） | 880px |
| 弹窗状态字段 | 无（默认启用） | 无（默认草稿） |
| 素材 | 单 Logo | 多图 + 主图 + 多视频 |
| 价格 | 无 | 参考价格（元），列表 `¥ 268.00` |
| 指标卡 | 品牌四卡 / 类目四卡 | SKU总数/已上架/待完善/草稿 |
| 删除规则 | SKU=0 且停用 | 非已上架且无业务引用 |

## 10. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0004-admin-home | `AdminLayout`、Sidebar 264px、metric-card、表格与分页视觉 |
| REQ-0005-brand-management | 品牌下拉数据源、`brand_id` 关联 |
| REQ-0005-tile-category-management | 类目下拉数据源、`category_id` 关联 |
| `tiles` / `tile_images` 表 | 现有 schema 需扩展：编码、品牌、工艺、价格、视频等 |
| MinIO + rules/media.md | 图片/视频授权上传 |
| rules/ui-design.md | 暗色旗舰风、semantic token |

## 11. 异常流程

| 场景 | 期望行为 |
|---|---|
| 非授权角色访问 API | HTTP 403 |
| SKU 编码重复 | HTTP 409，`TILE_SKU_CODE_DUPLICATED` |
| 非法删除已上架 SKU | HTTP 409，`TILE_SKU_DELETE_FORBIDDEN` |
| 必填项缺失 | 前端字段校验 + 后端 422 |
| 上传失败 | 保留已填表单，提示错误，不关闭弹窗 |
| 无数据 | 表格空状态 + 「新增SKU」入口 |
| 加载中 | 表格 skeleton，筛选区布局不变 |
