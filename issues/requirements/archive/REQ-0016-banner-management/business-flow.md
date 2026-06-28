---
title: 业务流程
purpose: Banner 管理列表、弹窗、上线下线与媒体上传主流程
content: 基于 requirement.md v1 与 prototype/web/banner-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 11:07:50
updated_at: 2026-06-28 11:07:50
note: REQ-0016-banner-management
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
┌──────────────────────────────────────────────────────────────┐
│ 路径 A：Banner 列表                                           │
│   /admin/banners → 筛选 / 指标卡 / 表格 / 分页                 │
│   ├─ 新增/编辑 → 弹窗（按 jump_type 分化）→ POST/PUT → 刷新   │
│   ├─ 上线 → 确认 → POST online → 刷新                         │
│   ├─ 下线 → 确认 → POST offline → 刷新                        │
│   └─ 删除（非 ONLINE）→ 确认 → DELETE                         │
└──────────────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────────────┐
│ 路径 B：Dashboard 快捷入口（REQ-0004 MODIFIED）                 │
│   /admin/dashboard → 快捷「新增 Banner」→ /admin/banners?…    │
└──────────────────────────────────────────────────────────────┘
```

## 2. 与关联 REQ 差异

| 对比项 | REQ-0005 品牌 | REQ-0016 Banner |
|---|---|---|
| 状态字段位置 | 列表启停 | 列表上线/下线（弹窗无状态） |
| 唯一键 | name | (display_client, position, title) |
| 条件字段 | 无 | 按 jump_type 分化 |
| 图片 | logo 上传 | SKU 图库引用 / 自定义 MinIO |
| 删除条件 | sku_count=0 且 DISABLED | status ≠ ONLINE |

## 3. 访问与权限

```text
JWT → require_admin_access
  ├─ role ∈ {admin, employee} → 允许
  └─ role = store_owner → 403 AuthForbidden
```

| 产品角色 | 后端 role | Banner 菜单 | Banner API |
|---|---|---|---|
| 后台运营 | employee | ✓ | ✓ |
| 后台管理员 | admin | ✓ | ✓ |
| 店主 | store_owner | ✗ | ✗ |

## 4. Banner 列表查询

```text
GET /api/v1/admin/banners?page=1&page_size=10&keyword=&display_client=&status=&time_status=
  ↓
响应：items[] + pagination + summary
  summary: total_count, filtered_count, online_count, pending_count
  每项含 time_status（ACTIVE|PENDING|EXPIRED，计算字段）
  ↓
渲染 metric-grid + filter + table + pagination
```

### 4.1 筛选

```text
用户输入 keyword / 选择展示端 / 状态 / 时间状态
  ↓
点击「查询」→ page=1 重新请求
  ↓
点击「重置」→ 清空条件 → 重新请求
```

## 5. 新增 / 编辑 Banner（弹窗）

```text
点击「＋ 新增 Banner」或行内「编辑」
  ↓
弹窗公共字段：title*, display_client*, position*, image*, jump_type*, sort_order*, valid_from/to, remark
  ↓
按 jump_type 展示条件块：
  ├─ SKU_DETAIL    → sku_id*；图默认 SKU 主图；可切换图库或 custom_upload
  ├─ EXTERNAL_LINK → external_url*（https）；custom_upload 图
  ├─ TOPIC_PAGE    → topic_id*（GET /topics 搜索）；custom_upload 图
  └─ NO_JUMP       → 跳转目标禁用「无需配置」；custom_upload 图
  ↓
切换 jump_type → 清空不兼容目标字段
切换 display_client → position 重置为合法默认项
  ↓
POST（新增 status=DRAFT）/ PUT（编辑，不自动改 status）
  ↓
成功 → Toast → 关弹窗 → 刷新列表 + summary
失败 → BANNER_TITLE_DUPLICATED / BANNER_JUMP_TARGET_INVALID 等
```

**弹窗约束**：MUST NOT 展示状态策略说明块或状态编辑控件。

## 6. 上线 / 下线流程

```text
列表行点击「上线」或「下线」
  ↓
二次确认（对齐 BrandManagementPage / REQ-0008）
  ↓
POST .../online 或 .../offline
  ↓
上线前服务端校验：image、jump 目标、sort、有效期逻辑
  ↓
成功 → Toast → 刷新行/列表
```

**时间状态**（列表展示，非弹窗编辑）：

- `ACTIVE`：ONLINE 且在 valid_from~valid_to 内
- `PENDING`：ONLINE 且 valid_from 在未来
- `EXPIRED`：valid_to 已过（status 可为 ONLINE 或展示 EXPIRED badge）

## 7. 删除流程

```text
判断 deletable = (status ∈ {DRAFT, OFFLINE, EXPIRED})
  ├─ status = ONLINE → 删除置灰，提示「已上线 Banner 需先下线后删除」
  └─ deletable → 确认弹窗
        ↓
     DELETE /api/v1/admin/banners/{id}
        ↓
     服务端二次校验
```

## 8. SKU 详情跳转 — 图片与跳转

```text
用户选择 jump_type = SKU_DETAIL
  ↓
选择 sku_id（搜索名称/编码）
  ↓
默认 image_source = sku_main_image，预览 SKU 主图
  ↓
可选：切换 sku_gallery_image（记录 sku_gallery_asset_id）
  或 custom_upload → POST upload-image → object_key
  ↓
保存 banner.sku_id + image_object_key + image_source
```

## 9. 专题跳转 — 最小 topics 主数据

```text
migration 种子 topics（≥2 条 ENABLED）
  ↓
GET /api/v1/admin/topics?keyword=&status=ENABLED
  ↓
弹窗 topic 下拉/搜索
  ↓
保存 banner.topic_id
（专题 CRUD 与前台专题页不在本期）
```

## 10. 媒体上传

```text
custom_upload：
  用户选择文件
    ↓
  POST /api/v1/admin/banners/upload-image（或通用 media API）
    ↓
  后端校验 MIME/大小 → MinIO MINIO_PREFIX_BANNERS/*
    ↓
  返回 object_key → 写入 banner.image_object_key

sku 图库引用：
  不重复上传 → 直接引用 tiles 媒体 object_key
```

## 11. 本期不包含

- 店主 Web / 小程序 Banner 轮播消费端
- 类目页跳转类型创建
- 专题管理 CRUD、外链白名单引擎、过期自动下线 job
