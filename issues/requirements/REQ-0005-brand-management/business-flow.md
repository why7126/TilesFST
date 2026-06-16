---
title: 业务流程
purpose: 瓷砖品牌管理列表、筛选、弹窗与删除主流程
content: 基于 requirement.md 与 prototype/web/brand-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005-brand-management
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
进入 /admin/brands
  ↓
浏览 / 搜索 / 筛选品牌列表
  ↓
可选操作：
  ├─ 新增品牌 → 弹窗 → POST → Toast + 刷新列表
  ├─ 编辑品牌 → 弹窗 → PUT → Toast + 刷新
  ├─ 启用 / 停用 → 确认（可选）→ POST enable/disable → Toast
  └─ 删除（仅 SKU=0 且停用）→ 确认弹窗 → DELETE → Toast
```

## 2. 访问与权限流程

```text
用户携带 JWT 访问 /admin/brands
  ↓
ProtectedRoute：已登录？
  ├─ 否 → /admin/login
  └─ 是 → 具备 brand:list（或运营角色默认允许）？
        ├─ 否 → 403 或重定向 /admin/dashboard
        └─ 是 → 渲染 BrandManagementPage
```

### 2.1 角色与菜单

| 产品角色 | 后端 role（建议） | 品牌管理菜单 | 说明 |
|---|---|---|---|
| 后台运营 | `employee` | OPERATIONS > 瓷砖品牌 | 日常主数据维护 |
| 后台管理员 | `admin` | 同上 | 全量品牌操作 |
| 前台用户 | `store_owner` | 不可见 | 不允许进入管理端 |

## 3. 列表查询流程

```text
页面加载
  ↓
GET /api/v1/admin/brands?page=1&page_size=20&keyword=&status=
  ↓
响应含 items + total + summary（品牌总数/启用/停用/未关联SKU）
  ↓
渲染 page-header + metric-grid + filter-card + table + pagination
```

### 3.1 搜索与重置

```text
用户输入关键词 / 选择状态
  ↓
点击「查询」或回车
  ↓
page 重置为 1，带 query 重新请求
  ↓
点击「重置」→ 清空条件 → 重新请求默认列表
```

### 3.2 每页显示数

```text
用户切换每页显示数（20 / 50 / 100）
  ↓
page 重置为 1
  ↓
保留 keyword、status 筛选条件重新请求
```

## 4. 新增品牌流程

```text
点击「新增品牌」
  ↓
打开弹窗（720px，字段两行网格 + Logo/介绍通栏）
  ↓
填写：品牌名称*、品牌排序*、简称、英文名、Logo、介绍
  ↓
客户端校验：名称非空、排序正整数、长度上限
  ↓
POST /api/v1/admin/brands
  ↓
成功：
  ├─ Toast「品牌已创建」
  ├─ 关闭弹窗，刷新列表
  └─ 新记录 status=ENABLED（不在弹窗展示）
失败：BRAND_NAME_DUPLICATED、校验错误等
```

## 5. 编辑品牌流程

```text
列表点击「编辑」
  ↓
GET /api/v1/admin/brands/{id}（或列表项回填）
  ↓
打开弹窗，字段同新增
  ↓
PUT /api/v1/admin/brands/{id}
  ↓
成功 → Toast「品牌已更新」→ 刷新列表
```

## 6. 启用 / 停用流程

```text
点击「停用」或「启用」
  ↓
（可选）确认
  ↓
POST .../disable 或 .../enable
  ↓
成功 → Toast → 刷新列表与指标卡
  ↓
停用后前台（未来）不展示该品牌
```

## 7. 删除流程

```text
渲染操作列时计算：
  canDelete = (sku_count === 0 AND status === DISABLED)
  ↓
canDelete = false → 删除按钮置灰，hover 提示固定文案
  ↓
canDelete = true → 点击「删除」
  ↓
确认弹窗：标题「删除品牌」，按钮「取消」「删除品牌」
  ↓
DELETE /api/v1/admin/brands/{id}
  ↓
服务端二次校验 sku_count 与 status
  ├─ 通过 → 物理删除或软删除（实现时定稿）→ Toast → 刷新
  └─ 拒绝 → BRAND_DELETE_FORBIDDEN
```

## 8. Logo 上传流程

```text
弹窗内选择 JPG/PNG/WebP
  ↓
POST 后端授权上传（MinIO，前缀如 brands/logos/）
  ↓
返回 logo_url 或 object_key 写入品牌 payload
  ↓
列表展示缩略图；无 Logo 时首字母占位
```

## 9. 与现有能力的衔接

| 依赖 | 说明 |
|---|---|
| REQ-0004-admin-home | `AdminLayout`、Sidebar 264px、metric-card、表格与分页视觉 |
| REQ-0005-user-management | 分页跳页、每页显示数交互可参考 |
| MinIO | Logo 走后端授权上传 |
| SKU（未实现） | `sku_count` 可先为 0 或子查询预留 |

## 10. 异常流程

| 场景 | 期望行为 |
|---|---|
| 非授权角色访问 API | HTTP 403 |
| 品牌名称重复 | HTTP 409，`BRAND_NAME_DUPLICATED` |
| 非法删除 | HTTP 409/422，`BRAND_DELETE_FORBIDDEN` |
| 排序非正整数 | 前端拦截 + 后端校验 |
| Logo 上传失败 | 保留原 Logo，提示错误 |
| 网络错误 | Toast，不丢筛选条件 |
