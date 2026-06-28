# 瓷砖类目管理 - 列表页原型上下文

## 文件

- HTML：`prototype/web/tile-category-management.html`
- 原型图：`prototype/images/tile-category-management.png`

## 目标

指导 AI Coding 精准还原瓷砖类目管理列表页。HTML 是最高优先级视觉参考，PNG 是 Golden Reference。

## 布局

- 画布：1440 × 1024。
- 左侧 Sidebar：264px，固定 100vh。
- 右侧内容：`height: 100vh; overflow: auto;`，最大内容宽度 1080px。
- 当前激活导航：OPERATIONS / 瓷砖类目。

## 页面区域

1. 页面头部：眉标 `CATEGORY MANAGEMENT`、标题「瓷砖类目管理」、说明文案、主按钮「＋ 新增类目」。
2. 数据概览：类目总数、启用类目、绑定 SKU、最大层级。
3. 类目检索：名称/编码输入框、状态下拉、层级下拉、查询、重置。
4. 类目管理区：左侧类目树，右侧类目列表。
5. 列表工具栏：只允许「调整排序」，不得出现「导出」。
6. 分页：页码 + 每页显示数。

## 关键业务规则

- 删除入口仅展示在 SKU 数量为 0 且状态为停用的类目行。
- 有 SKU 绑定或启用状态的类目不得展示删除入口。
- 类目最多支持三级。
- 查询条件重置后恢复全部状态和全部层级。

## 视觉一致性

沿用后台首页 Sidebar、用户菜单、卡片、表格、Badge、分页、按钮样式。品牌金仅用于 Logo、主按钮、激活态、关键数字和可点击主操作。
