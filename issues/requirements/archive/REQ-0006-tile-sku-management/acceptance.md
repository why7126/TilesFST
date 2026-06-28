---
title: 需求验收标准
purpose: 瓷砖SKU管理功能、接口、数据、UI 与异常场景验收
content: 基于 requirement.md 与 prototype/web/tile-sku-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0006-tile-sku-management
---

# 验收标准

## 1. 功能验收

### 1.1 访问与布局

- [ ] **AC-001** 已登录且具备 SKU 管理权限的用户可访问 SKU 管理页，页面标题为「瓷砖SKU」。
- [ ] **AC-002** Sidebar OPERATIONS 下「瓷砖SKU」为激活态；继承 `AdminLayout`：264px Sidebar、右侧独立滚动、内容区最大宽度 1120px。
- [ ] **AC-003** 页面头部含 eyebrow「OPERATIONS / SKU」、说明文案、主按钮「＋ 新增SKU」（品牌金实底）。
- [ ] **AC-004** 只读账号不展示「新增SKU」及行内写操作入口。

### 1.2 数据概览

- [ ] **AC-005** 展示 4 个指标卡：SKU 总数、已上架、待完善、草稿。
- [ ] **AC-006** 指标卡数字使用品牌金；视觉与 admin-home metric-card 一致。

### 1.3 搜索与筛选

- [ ] **AC-007** 筛选区含：关键词、品牌、类目、状态、素材完整度、查询、重置。
- [ ] **AC-008** 关键词 placeholder 为「SKU名称 / SKU编码」；支持名称与编码模糊搜索。
- [ ] **AC-009** 品牌/类目下拉含「全部品牌」「全部类目」及有效选项（来自品牌/类目 API）。
- [ ] **AC-010** 状态下拉：全部状态 / 已上架 / 草稿 / 待完善 / 已停用。
- [ ] **AC-011** 素材完整度：全部 / 已完整 / 缺主图 / 缺图片 / 缺视频。
- [ ] **AC-012** 点击「查询」或回车触发搜索，页码重置为 1；「重置」清空条件并重新加载。

### 1.4 SKU 列表

- [ ] **AC-013** 表格列：SKU信息、品牌/类目、规格/工艺、参考价格、素材、状态、更新时间、操作。
- [ ] **AC-014** SKU信息列含主图缩略图（44×44）、SKU 名称、SKU 编码。
- [ ] **AC-015** 参考价格格式化为 `¥ 268.00`（两位小数）；价格为 `0` 时展示 `¥ 0.00`；历史无价格（null）时 MAY 展示「—」。
- [ ] **AC-016** 素材列展示主图状态（主图已设 / 缺主图）及「N图 / M视频」计数。
- [ ] **AC-017** 状态徽章：已上架、草稿、待完善、已停用；颜色语义与原型一致。
- [ ] **AC-018** 操作列：编辑、上下架/恢复、更多；默认按更新时间倒序。

### 1.5 分页

- [ ] **AC-019** 分页左侧：`共 {total} 条`，total 与当前筛选结果一致。
- [ ] **AC-020** 分页右侧：上一页、页码、下一页 + 每页条数（10 / 20 / 50 / 100，默认 20）。
- [ ] **AC-021** 当前页码使用品牌金实底；切换每页条数后 page=1，保留筛选条件。

### 1.6 新增 / 编辑弹窗

- [ ] **AC-022** 弹窗宽 880px，`max-height` 不超过视口，主体可滚动；遮罩半透明。
- [ ] **AC-023** 标题「新增SKU」含「创建后默认草稿」提示；副标题说明无状态选择。
- [ ] **AC-024** 字段顺序：SKU名称*、SKU编码*、所属品牌*、所属类目*、规格尺寸*、表面工艺、主色系、参考价格（元）*、SKU图片、SKU视频、备注说明。
- [ ] **AC-025** 弹窗内**不出现**状态字段或状态选择控件。
- [ ] **AC-026** 价格字段 Label 必须为「参考价格（元）」；placeholder「请输入参考价格」；支持两位小数。
- [ ] **AC-027** 必填项校验失败：字段边框风险色 + 字段下方错误文案；不关闭弹窗。
- [ ] **AC-028** 底部按钮：取消（幽灵）、保存草稿（描边）、创建SKU（品牌金主按钮）。
- [ ] **AC-029** 创建成功：Toast「SKU创建成功，已保存为草稿」；关闭弹窗；列表刷新至第一页；新记录 status=草稿。
- [ ] **AC-030** 编辑弹窗字段与新增一致，回填现有数据；仍不展示状态字段。

### 1.7 图片管理

- [ ] **AC-031** 支持上传多张图片；缩略图网格展示。
- [ ] **AC-032** 必须可指定一张为主图；主图左上角「主图」标签；非主图可「设为主图」。
- [ ] **AC-033** 支持删除非主图、继续添加图片。
- [ ] **AC-034** 未设主图时允许保存草稿；列表素材列与筛选「缺主图」正确反映。

### 1.8 视频管理

- [ ] **AC-035** 支持上传多个视频；以文件卡片展示名称、大小/时长、上传状态。
- [ ] **AC-036** 支持删除视频、继续添加；视频非必填。

### 1.9 上下架与删除

- [ ] **AC-037** 已上架 SKU 可下架；草稿/已停用等可恢复或上架（文案与原型一致）。
- [ ] **AC-038** 已上架 SKU 不可删除；仅草稿/已停用且无业务引用时可删除。
- [ ] **AC-039** 非法删除时服务端返回明确错误码（如 `TILE_SKU_DELETE_FORBIDDEN`）。

### 1.10 空态与加载

- [ ] **AC-040** 无数据时表格展示空状态、说明文案与「新增SKU」入口。
- [ ] **AC-041** 加载中表格行展示 skeleton，筛选区布局不变。

## 2. 接口验收

| 接口（建议路径） | 说明 |
|---|---|
| `GET /api/v1/admin/tile-skus` | 分页列表 + 筛选 + summary |
| `POST /api/v1/admin/tile-skus` | 创建，默认 DRAFT |
| `GET /api/v1/admin/tile-skus/{id}` | 详情（编辑回填，含图片/视频） |
| `PUT /api/v1/admin/tile-skus/{id}` | 更新 SKU |
| `POST /api/v1/admin/tile-skus/{id}/publish` | 上架 |
| `POST /api/v1/admin/tile-skus/{id}/unpublish` | 下架 |
| `DELETE /api/v1/admin/tile-skus/{id}` | 条件删除 |
| `POST /api/v1/admin/media/upload`（或等价） | 图片/视频授权上传 |

- [ ] **AC-042** API 路径与 `rules/api.md` 一致（`/api/v1/admin/...`）。
- [ ] **AC-043** 变更后执行 OpenAPI 导出与 Orval 生成前端客户端。
- [ ] **AC-044** 权限点覆盖：tile_sku:list/create/update/publish/unpublish/delete（或等价命名）。

## 3. 数据验收

- [ ] **AC-045** 扩展 `tiles`（或新建 `tile_skus`）表：sku_code UNIQUE、brand_id、category_id、surface_finish、color_family、reference_price、remark、status 枚举等。
- [ ] **AC-046** `tile_images` 保留 `is_main`、`sort_order`；支持多图主图标记。
- [ ] **AC-047** 新增 SKU 视频元数据表或 media 关联（object_key、duration、size 等）。
- [ ] **AC-048** 图片/视频存 MinIO，经后端授权；禁止前端直连未授权存储。
- [ ] **AC-049** 品牌、类目外键与 REQ-0005 品牌/类目数据一致。

## 4. 技术验收

- [ ] **AC-050** 实现策略建议 CSS Port（对齐 admin-home / 品牌管理），semantic token，TSX 无裸 Hex。
- [ ] **AC-051** 复用 `AdminLayout`、`AdminSidebar`、分页与表格模式。
- [ ] **AC-052** 单元/组件测试：主图切换、必填校验、删除按钮禁用逻辑、价格格式化。
- [ ] **AC-053** 集成测试：CRUD、筛选、publish/unpublish、非法删除、编码重复。

## 5. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/tile-sku-management-list.html
2. prototype/web/tile-sku-create-modal.html
3. prototype/web/*-context.md
4. acceptance.md
5. rules/ui-design.md
6. prototype/images/*.png（可选 Golden Reference）
7. openspec/specs/（已归档能力）
```

- [ ] **AC-054** 列表页与 HTML 原型并排：指标卡、筛选、表格、分页（PNG 可选，不作为 gate 前置条件）。
- [ ] **AC-055** 弹窗与 modal HTML 并排：字段顺序、多图主图、多视频卡片、三按钮底栏（PNG 可选）。
- [ ] **AC-056** 1440×1024 视口下布局与原型一致；Sidebar 固定 100vh。

## 6. 不在本期

- SKU 批量导入/导出、复制、审批流、库存与促销价、店主端详情页、视频转码多清晰度。
