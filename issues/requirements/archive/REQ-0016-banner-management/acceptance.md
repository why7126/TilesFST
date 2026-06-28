---
title: 需求验收标准
purpose: Banner 管理页、弹窗变体、接口与媒体验收
content: 基于 requirement.md v1 与 prototype/web/banner-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 11:07:50
updated_at: 2026-06-28 11:07:50
note: REQ-0016-banner-management
---

# 验收标准

## 1. 功能验收 — Banner 列表页

### 1.1 访问与布局

- [ ] **AC-001** 已登录 `admin`/`employee` 可访问 `/admin/banners`；页面标题「Banner 管理」。
- [ ] **AC-002** Sidebar OPERATIONS「Banner 管理」激活；`admin-nav.ts` 配置 `path: '/admin/banners'`；继承 `AdminLayout`。
- [ ] **AC-003** 页头眉标 `OPERATIONS / BANNER MANAGEMENT`、说明文案、主按钮「＋ 新增 Banner」。
- [ ] **AC-004** 列表页默认不展示弹窗遮罩；无导出、无批量操作。

### 1.2 数据概览

- [ ] **AC-005** 四指标卡：Banner 总数、当前筛选、已上线、待生效；与 API `summary` 一致。
- [ ] **AC-006** 指标卡视觉与用户管理页 metric-card 一致（semantic token，无裸 Hex）。

### 1.3 搜索与筛选

- [ ] **AC-007** 筛选区：关键词、展示端、状态、时间状态、查询、重置；控件高度 40px。
- [ ] **AC-008** 关键词匹配 title、关联 SKU 名称/编码、专题名称/编码。
- [ ] **AC-009** 展示端：全部 / Web 首页 / 小程序首页 / 专题页。
- [ ] **AC-010** 状态：全部 / 草稿 / 已上线 / 已下线 / 已过期。
- [ ] **AC-011** 时间状态：全部 / 当前生效 / 待生效 / 已过期。
- [ ] **AC-012** 查询重置 page=1；重置清空全部筛选。

### 1.4 列表表格

- [ ] **AC-013** 列：Banner（缩略图 86×38）、展示端、跳转类型、状态、有效期、排序、更新时间、操作。
- [ ] **AC-014** 跳转类型 Badge：SKU 详情、外部链接、专题页、无跳转（样例可出现「类目页」但本期不可创建该类）。
- [ ] **AC-015** 操作：编辑；上线/下线（依状态）；删除（条件展示）。

### 1.5 上线 / 下线

- [ ] **AC-016** 上线/下线二次确认（对齐 `BrandManagementPage` / REQ-0008）。
- [ ] **AC-017** 新建保存为 `DRAFT`；弹窗不含状态字段。
- [ ] **AC-018** 上线前校验图片、跳转目标、排序、有效期逻辑完整。

### 1.6 删除

- [ ] **AC-019** `status=ONLINE` 时删除不可点；提示「已上线 Banner 需先下线后删除」。
- [ ] **AC-020** `DRAFT`/`OFFLINE`/`EXPIRED` 可删除；确认弹窗 + 服务端二次校验。

### 1.7 分页

- [ ] **AC-021** 左侧每页 10/20/50 + `1-10 / 32` 式范围；右侧页码、上一页、下一页。
- [ ] **AC-022** 无跳页输入框。

### 1.8 Dashboard 快捷入口

- [ ] **AC-023** Dashboard「新增 Banner」导航至 Banner 管理并可达新增弹窗（非 toast 占位）。

## 2. 功能验收 — 弹窗（公共）

- [ ] **AC-024** 弹窗宽 640px、最大高 92vh、内容可滚动。
- [ ] **AC-025** 标题 `新增 Banner · {跳转类型}` / `编辑 Banner · {跳转类型}`。
- [ ] **AC-026** MUST NOT 展示状态策略说明块或状态编辑控件。
- [ ] **AC-027** 公共字段：标题*、展示端*、展示位置*、Banner 图*、跳转类型*、排序*、有效期、运营备注。
- [ ] **AC-028** 标题 hint：同展示端+展示位置下不可重复，2–30 字；冲突返回 `BANNER_TITLE_DUPLICATED`。
- [ ] **AC-029** 切换 `display_client` 时 `position` 重置为合法默认项。
- [ ] **AC-030** 切换 `jump_type` 清空不兼容跳转目标字段。

## 3. 功能验收 — 弹窗变体

### 3.1 SKU 详情

- [ ] **AC-031** 必选关联 SKU（可搜索）；选择后默认 SKU 主图（`image_source=sku_main_image`）。
- [ ] **AC-032** 可切换 SKU 图库其他图（`sku_gallery_image` + `sku_gallery_asset_id`）或自定义上传。
- [ ] **AC-033** 保存记录 `image_source`；SKU 图库引用不重复上传文件。

### 3.2 外部链接

- [ ] **AC-034** 必填 `https://` 外链；禁止 `javascript:` 等非法 scheme。
- [ ] **AC-035** 展示说明：小程序外链需白名单或中转页；Banner 图须用户上传。

### 3.3 专题页

- [ ] **AC-036** 必选关联专题；支持名称/编码搜索（`GET /api/v1/admin/topics`）。
- [ ] **AC-037** 种子数据 ≥2 条 `ENABLED` 专题；无专题管理 CRUD 页。

### 3.4 无跳转

- [ ] **AC-038** 无可编辑跳转目标；禁用态「跳转目标：无需配置」。
- [ ] **AC-039** 说明：前台仅展示不响应点击。

## 4. 接口验收

| 接口 | 说明 |
|---|---|
| `GET /api/v1/admin/banners` | 分页 + keyword + display_client + status + time_status + summary |
| `GET /api/v1/admin/banners/{id}` | 详情 |
| `POST /api/v1/admin/banners` | 创建，默认 DRAFT |
| `PUT /api/v1/admin/banners/{id}` | 更新（不自动改 status） |
| `POST /api/v1/admin/banners/{id}/online` | 上线 |
| `POST /api/v1/admin/banners/{id}/offline` | 下线 |
| `DELETE /api/v1/admin/banners/{id}` | 条件删除 |
| `POST /api/v1/admin/banners/upload-image` | Banner 图上传（或等价 media API） |
| `GET /api/v1/admin/topics` | 只读 ENABLED 专题列表 |

- [ ] **AC-040** 路径符合 `rules/api.md`；统一 `ApiResponse` 包装。
- [ ] **AC-041** OpenAPI 更新 + Orval 重新生成。
- [ ] **AC-042** `store_owner` 调用上述 API 返回 403。

### 4.1 建议错误码

| code | 名称 | 场景 |
|---|---|---|
| 待分配 | `BANNER_TITLE_DUPLICATED` | 同端+位置下标题重复 |
| 待分配 | `BANNER_JUMP_TARGET_INVALID` | 跳转目标不完整或非法 |
| 待分配 | `BANNER_DELETE_FORBIDDEN` | ONLINE 状态删除 |
| 待分配 | `BANNER_NOT_FOUND` | id 不存在 |
| 待分配 | `BANNER_EXTERNAL_URL_INVALID` | 外链格式/协议非法 |

（数值编号在 OpenSpec / `error-codes.md` 阶段定稿）

## 5. 数据与媒体验收

- [ ] **AC-043** `banners` 表字段符合 requirement §5.1；`(display_client, position, title)` 唯一。
- [ ] **AC-044** `topics` 种子表 + migration；Banner 下拉仅 `ENABLED`。
- [ ] **AC-045** 自定义上传走 MinIO 单桶 + `MINIO_PREFIX_BANNERS`（或项目约定前缀）。
- [ ] **AC-046** 上传 MIME/大小符合 `rules/media.md`。

## 6. 技术验收

- [ ] **AC-047** 前端 semantic token；复用 `AdminListPage`、品牌页确认弹窗模式。
- [ ] **AC-048** 后端 pytest：CRUD、上线/下线、删除条件、唯一键、外链校验、RBAC。
- [ ] **AC-049** 前端 vitest（可选）：删除 disabled、jump_type 切换清空逻辑。

## 7. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/banner-management-list.html
2. prototype/web/banner-management-list.png
3. prototype/web/banner-management-modal-{sku-detail|external-link|topic-page|no-jump}.html
4. 对应 modal *.png
5. prototype/web/*-context.md
6. acceptance.md（本文件）
7. rules/ui-design.md
```

- [ ] **AC-050** 列表页 HTML 与 PNG 并排：筛选四列、四指标卡、跳转类型列、分页样式。
- [ ] **AC-051** 四套弹窗 HTML 与 PNG 并排：640px 弹窗、无状态块、条件字段正确显隐。
- [ ] **AC-052** `trace.md` 记录 PNG 并排验收日期与结果。

## 8. 不在本期

- 类目页跳转创建、店主端/小程序 Banner 展示、专题 CRUD、外链白名单引擎、拖拽排序、复制、批量、导出、过期自动下线 job。
