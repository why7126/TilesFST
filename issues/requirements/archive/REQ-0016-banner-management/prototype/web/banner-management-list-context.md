# REQ-0016 Banner 管理 - 列表页原型上下文工程

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 TILESFST 管理后台 Banner 管理列表页。开发时应优先参考：

1. `prototype/web/banner-management-list.html`
2. `prototype/web/banner-management-list.png`
3. `requirement.md`
4. `rules/ui-design.md`
5. `user-management-list.html` / `user-management-list.png`

## 2. 页面画布

| 项目 | 值 |
|---|---|
| 设计稿尺寸 | 1440 × 1024 |
| 布局 | 左侧固定 Sidebar + 右侧内容区 |
| Sidebar 宽度 | 264px |
| 右侧内容最大宽度 | 1080px |
| 页面滚动 | 右侧 main-content 独立滚动 |
| 默认弹窗 | 不展示 |

## 3. 页面结构

```text
<body>
  <div class="admin-shell">
    <aside class="sidebar">...</aside>
    <main class="main-content">
      <div class="content-inner">
        <section class="page-hero">...</section>
        <section class="filter-card">...</section>
        <section class="summary-grid">...</section>
        <section class="table-section">...</section>
      </div>
    </main>
  </div>
</body>
```

## 4. Sidebar

- Logo：`TILESFST`。
- 当前激活菜单：`OPERATIONS > Banner管理`。
- SYSTEM 菜单保留用户管理、系统设置。
- 用户菜单固定在左侧底部，与用户管理页保持一致。

## 5. 页面标题区

- 眉标：`OPERATIONS / BANNER MANAGEMENT`
- 标题：`Banner管理`
- 说明：`维护前台首页、小程序首页与专题运营位的 Banner 内容、排序、跳转与生效时间。`
- 右侧主按钮：`＋ 新增 Banner`

## 6. 搜索筛选区

筛选区使用 `.filter-card`，内部使用 6 列 grid：关键词、展示端、状态、时间状态、搜索按钮、重置按钮。所有输入、选择器、按钮高度 40px。

## 7. 统计区

4 个 `.metric-card`：Banner 总数 32、当前筛选 14、已上线 9、待生效 3。指标卡继承用户管理页面视觉，右上角保留金色弱光圆形装饰。

## 8. 列表区

表格字段：Banner、展示端、跳转类型、状态、有效期、排序、更新时间、操作。

- Banner 缩略图尺寸为 `86 × 38px`，使用石材纹理渐变模拟真实运营图。
- `跳转类型` 使用轻量 Badge 展示。本期可创建：SKU详情、外部链接、专题页、无跳转；样例数据可出现「类目页」badge 但 **不可创建**（见 requirement.md §3.2）。
- 表格整体仍保持用户管理列表页的行高、细分割线、弱文字与金色操作按钮样式。

## 9. 分页

分页位于表格底部，左侧显示每页条数选择与 `1-10 / 32`，右侧显示页码、上一页、下一页。

## 10. 一致性检查清单

- [ ] Sidebar 宽度 264px。
- [ ] 当前菜单为 Banner管理。
- [ ] 页面右侧无首页顶部欢迎区。
- [ ] 搜索筛选卡片在标题下方。
- [ ] 指标卡、表格、分页与用户管理页一致。
- [ ] 表格包含跳转类型字段。
- [ ] 主按钮为品牌金实底。
- [ ] 列表页默认不展示 modal-backdrop。
- [ ] HTML 与 PNG 视觉一致。
