---
requirement_id: REQ-0005-tile-category-management
title: 管理后台 - 瓷砖类目管理
terminal: web-admin
module: 管理后台 / 主数据 / 瓷砖类目
version: v2
status: draft
priority: P0
owner: product
source: 基于 admin-home V5、tile-category-management.html V2、tile-category-management-add.html V2 优化生成
---

# REQ-0005 管理后台 - 瓷砖类目管理

## 1. 需求背景

瓷砖类目是前台商品目录、SKU 归属、筛选导航的核心主数据。本页面基于 admin-home 后台框架延展，维护最多三级类目树、排序权重、启停状态与 SKU 绑定关系，并保持 TILESFST 管理后台暗色旗舰风、固定 Sidebar、右侧独立滚动、品牌金激活态等视觉与交互一致性。

## 2. 本版本优化点

| 序号 | 优化项 | 说明 |
|---|---|---|
| 1 | 删除导出功能 | 页面不出现导出按钮、导出入口、导出状态 |
| 2 | 工具栏收敛 | 列表工具栏仅保留「调整排序」 |
| 3 | 主操作置顶 | 页面头部提供主按钮「＋ 新增类目」 |
| 4 | 原型拆分 | 列表页与新增类目弹窗分别提供独立 HTML、PNG、上下文文件 |
| 5 | 删除条件收敛 | 仅当 SKU 数量 = 0 且状态 = 停用时展示/允许删除 |
| 6 | 类目树联动 | 左侧类目树与右侧列表联动筛选 |

## 3. 页面范围

**包含**：数据概览、类目检索、类目树、类目列表、新增类目弹窗、编辑类目、启用/停用、条件删除、分页、每页显示数、调整排序入口。

**不包含**：导出、批量操作、类目合并、多语言、前台预览、四级及以上类目、拖拽排序（「调整排序」可为后续迭代，本期可先占位或只读提示）。

## 4. 页面结构

```text
admin-shell
├── sidebar：固定 264px，瓷砖类目高亮
└── main-content
    ├── page-header：眉标、标题、说明、新增类目
    ├── metric-grid：类目总数 / 启用类目 / 绑定 SKU / 最大层级
    ├── filter-card：名称编码、状态、层级、查询、重置
    └── work-grid
        ├── tree-card：类目树（含全部类目根节点）
        └── table-card：工具栏（调整排序）+ 列表 + 分页
```

## 5. 页面头部

- 眉标：`CATEGORY MANAGEMENT`
- 标题：「瓷砖类目管理」
- 说明：「维护前台展示类目、层级路径、排序权重与 SKU 绑定关系。」
- 主按钮：「＋ 新增类目」
- 禁止出现导出按钮与批量操作入口。

## 6. 数据概览

| 指标 | 说明 |
|---|---|
| 类目总数 | 含一级、二级、三级全部类目 |
| 启用类目 | 状态为启用的类目数量 |
| 绑定 SKU | 已挂载到类目的 SKU 总数（可去重或按业务约定统计） |
| 最大层级 | 当前系统支持的最大层级（固定展示 3） |

指标卡只读，不作为编辑入口。

## 7. 类目检索

| 字段 | 控件 | 说明 |
|---|---|---|
| 类目名称 / 编码 | 输入框 | 模糊匹配名称、英文名或编码 |
| 状态 | Select | 全部状态、启用、停用 |
| 层级 | Select | 全部层级、一级类目、二级类目、三级类目 |
| 查询 | Button | 执行筛选，页码重置为 1 |
| 重置 | Ghost Button | 恢复「全部状态、全部层级」，清空关键词 |

## 8. 类目树

- 左侧 `tree-card` 宽 280px，展示全部类目及层级缩进（level-2 / level-3）。
- 根节点「全部类目」默认激活，展示系统 SKU 汇总。
- 每个节点右侧展示 SKU 数量（含子级汇总或当前节点绑定数，实现时与后端约定）。
- 点击节点后，右侧列表展示**当前节点及其子级**类目。
- 最多支持三级类目；三级类目不可再作为上级新增子级。

## 9. 类目列表

| 字段 | 说明 |
|---|---|
| 类目名称 | 主名称；副行展示编码与层级路径 |
| 层级 | 一级 / 二级 / 三级徽章 |
| 排序 | 排序权重，数字越小越靠前 |
| SKU 数量 | 已绑定 SKU 数 |
| 状态 | 启用 / 停用 |
| 更新时间 | 最近一次维护时间 |
| 操作 | 编辑、启用/停用、删除（条件展示） |

列表工具栏：
- 标题区展示当前树节点名称与记录数。
- 右侧仅「调整排序」按钮；不得出现「导出」。

分页：左侧「当前显示 x-y / N 条」；右侧页码 + 每页显示数（10 / 20 / 50）。

## 10. 删除规则

```text
允许删除 = SKU数量 = 0 AND 状态 = 停用
```

| SKU 数量 | 状态 | 删除入口 |
|---:|---|---|
| 0 | 停用 | 展示可点击删除 |
| 0 | 启用 | 不展示删除（或置灰，与原型一致：启用行仅展示停用） |
| >0 | 任意 | 不展示删除 |

服务端必须二次校验，否则返回：

```json
{"code":"CATEGORY_DELETE_FORBIDDEN","message":"仅允许删除未绑定SKU且已停用的类目"}
```

删除确认弹窗标题「删除类目」，按钮「取消」「删除类目」。

## 11. 新增 / 编辑类目弹窗

- 宽度 560px，居中 Modal，暗色遮罩 + blur。
- 头部：标题「新增类目」或「编辑类目」、关闭按钮。
- 表单：**一行一个字段**，顺序固定：
  1. 上级类目（Select，可为空 → 一级类目）
  2. 类目名称（必填）
  3. 类目编码（必填，唯一，建议 `CAT-XXXX`）
  4. 排序权重（必填正整数）
  5. 类目描述（选填，最多 200 字）
  6. 状态（Switch，默认启用；文案如「新增后立即启用」）
- 底部：「取消」「保存类目」
- 选择三级类目作为上级时，禁止继续新增子级（前端拦截 + 后端校验 `CATEGORY_MAX_DEPTH_EXCEEDED`）。

### 字段规则

| 字段 | 必填 | 规则 |
|---|---|---|
| 上级类目 | 否 | 空 = 一级；有值时自动计算层级 |
| 类目名称 | 是 | 1–30 字 |
| 类目编码 | 是 | 系统唯一，保存后不建议修改 |
| 排序权重 | 是 | 正整数，非 0、负、小数 |
| 类目描述 | 否 | 最多 200 字 |
| 状态 | 是 | 默认启用 |

保存成功后关闭弹窗，刷新类目树、列表与数据概览。

## 12. 校验规则

- 类目编码唯一：重复时文案「类目编码已存在，请更换」；服务端 `CATEGORY_CODE_DUPLICATED`。
- 排序权重：错误文案「请输入正整数」。
- 上级类目为三级时不可新增子级。

## 13. 接口建议

- `GET /api/v1/admin/tile-categories`：keyword、status、level、parent_id、page、page_size；含 tree 与 summary。
- `GET /api/v1/admin/tile-categories/tree`：完整类目树（含 sku_count）。
- `POST /api/v1/admin/tile-categories`：parent_id、name、code、sort_order、description、status。
- `PUT /api/v1/admin/tile-categories/{id}`：编辑（code 是否可改由 design 定稿）。
- `POST /api/v1/admin/tile-categories/{id}/enable`：启用。
- `POST /api/v1/admin/tile-categories/{id}/disable`：停用。
- `DELETE /api/v1/admin/tile-categories/{id}`：仅 sku_count=0 且 DISABLED。
- `POST /api/v1/admin/tile-categories/reorder`（可选）：批量调整排序。

## 14. 权限点

| 权限点 | 说明 |
|---|---|
| category:list | 查看类目列表与树 |
| category:create | 新增类目 |
| category:update | 编辑类目 |
| category:enable | 启用类目 |
| category:disable | 停用类目 |
| category:delete | 删除类目 |
| category:reorder | 调整排序（若本期实现） |

## 15. 原型文件

| 类型 | 文件 | 说明 |
|---|---|---|
| 需求文档 | requirement.md | 本文件 |
| 列表上下文 | prototype/web/prototype-context-list.md | 列表页上下文 |
| 弹窗上下文 | prototype/web/prototype-context-add.md | 新增弹窗上下文 |
| HTML | prototype/web/tile-category-management.html | 列表页 Golden Reference |
| HTML | prototype/web/tile-category-management-add.html | 新增弹窗 Golden Reference |
| PNG | prototype/web/tile-category-management.png | 列表页截图（待补齐） |
| PNG | prototype/web/tile-category-management-add.png | 弹窗截图（待补齐） |

## 16. UI/UE 约束

- 必须使用全局 Design Token，禁止硬编码与规范不一致的颜色、圆角、间距。
- Sidebar 264px、100vh；右侧内容独立滚动；最大内容宽度 1080px。
- 卡片/表格语义底、0.5px 分割线、3px 圆角；主按钮品牌金实底。
- 弹窗 560px，遮罩暗色半透明 + blur。

## 17. 验收标准（摘要）

- 无导出按钮或导出入口。
- 页面顶部存在「＋ 新增类目」主按钮。
- 列表工具栏仅有「调整排序」。
- 左侧类目树与右侧列表联动；最多三级。
- 新增弹窗字段完整，一行一个信息。
- 删除入口仅出现在 SKU 数量为 0 且停用的类目行。
- 列表页与弹窗分别有独立 HTML、PNG、上下文文件。
- 视觉效果与后台首页、用户管理、品牌管理风格一致。

详细 AC 见 `acceptance.md`。
