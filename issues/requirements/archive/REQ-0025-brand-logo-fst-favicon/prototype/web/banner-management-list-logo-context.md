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

- Logo：使用上传的「菲尚特」产品 Logo，采用 `50px × 50px` 方形图片容器。
- 品牌文字：右侧展示 `菲尚特`，同一行展示版本号 `v0.0.6`，下一行展示 `家居建材管理后台`。
- 顶部品牌区参考上传的 SoulKing 侧边栏布局，但视觉风格必须保持 TILESFST 暗色旗舰风。
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


## 11. 本次 Logo 增补实现说明

- `product-logo-card` 替代原 `.logo` 文字区域。
- Logo 图片使用白底方形卡片承载，避免深色背景影响品牌识别。
- 品牌区与导航区之间保留 28px 底部间距，保证与原导航节奏一致。
- 不新增页面主体交互，不改变 Banner 管理业务功能。


## 11. v4 视觉变更

- `.product-logo-card` 取消背景、边框、圆角容器感与投影，Logo 区域不再形成独立卡片。
- `.product-logo-mark` 取消额外边框和背景底纹，仅负责控制 Logo 图片尺寸。
- `.sidebar-collapse` 使用绝对定位，`right: 0` 贴紧 Sidebar 内右边框，避免与版本号挤压。
- 主内容区、筛选区、指标卡、列表与分页沿用 v1，无结构性变更。

## 12. v4 一致性检查清单

- [ ] 产品 Logo 区域无底纹、无边框、无投影。
- [ ] 收起/展开按钮贴紧侧边栏内右边框。
- [ ] Logo、产品名称、版本号、副标题无遮挡。
- [ ] Banner 管理列表页信息结构与 v1 一致。


## v4 视觉还原补充

- 侧边栏品牌区 Logo 图标为 64×64px，必须明显高于右侧「菲尚特 FST / 家居建材管理后台 · v0.0.6」文字组合高度。
- 品牌名称展示为「菲尚特 FST」，版本号合并至副标题行，展示为 `家居建材管理后台 · v0.0.6`。
- Logo 区域保持透明，无底纹、无边框、无卡片背景、无阴影。
- 展开/收起按钮相对侧边栏右边框向内收 6px；hover 时显示弱边框，但边框右侧仍需与侧边栏内边框保留间隙。
- 其余 Banner 管理列表页布局、筛选、指标卡、表格、分页不变。


## v4 视觉还原补充

### 侧边栏品牌区

- Logo 图片：54 × 54px，不加底纹、不加边框。
- 品牌文字：主标题为「菲尚特 FST」，字号 14px，行高 18px。
- 副标题：`家居建材管理后台`，字号 11px，行高 16px，与主标题间距 3px。
- 版本号：`v0.0.6` 位于主标题右上角，使用 18px 高度、小圆角、0.5px 边框。
- 收起按钮：34 × 34px 正方形 hover 热区，距离 Sidebar 内右边框 10px，hover 后边框不得贴边。

### 验收检查

- [ ] Logo 高度不再明显超过两行品牌文字高度。
- [ ] 版本号在「菲尚特 FST」右上角，且有边框。
- [ ] 展开 / 收起按钮 hover 边框为正方形。
- [ ] 展开 / 收起按钮 hover 边框与侧边栏右边框存在少量间隙。


## 13. v7 视觉优化说明

### 13.1 侧边栏品牌区结构

```text
product-logo-card
├── product-logo-mark        50 × 50px
├── product-logo-copy
│   ├── 菲尚特FST + v0.0.6
│   └── 家居建材管理后台
└── sidebar-collapse         34 × 34px
```

### 13.2 CSS 实现约束

- `.product-logo`：左右内边距为 8px，避免按钮贴边。
- `.product-logo-card`：三列 Grid，`grid-template-columns: 50px minmax(0,1fr) 34px`。
- `.product-logo-mark`：`50px × 50px`，不设置背景、边框或阴影。
- `.product-logo-version`：位于主标题右上角，保留 `0.5px` 边框、18px 高度。
- `.sidebar-collapse`：不再绝对定位，作为品牌区第三列与 Logo 同行；按钮为 `34px × 34px` 正方形，右侧与侧边栏内边框保留间隙。

### 13.3 v7 一致性检查清单

- [ ] 产品 Logo、品牌文字组、展开/收起按钮在同一行。
- [ ] 产品 Logo 区域无底纹、无边框、无投影。
- [ ] 品牌文案为「菲尚特FST」与「家居建材管理后台」。
- [ ] 版本号位于「菲尚特FST」右上角并有边框。
- [ ] 展开/收起按钮为正方形边框按钮。
- [ ] 展开/收起按钮 hover 边框与 Sidebar 右边框保留少量间隙。
- [ ] 主体 Banner 管理页面不发生结构性变化。


## v7 继续优化说明

- 展开/收起按钮与产品 Logo 保持同一行，但整体向右侧边栏边界微调，避免与版本号视觉重叠。
- 按钮维持正方形边框，悬浮边框与侧边栏右边界保留少量安全间隙。
- Logo 区域继续保持无底纹、无边框，延续 v5 的企业级视觉一致性。


## v7 侧边栏 Logo 区精调

- Sidebar 内边距：左右各 10px。
- Logo 图标：40 × 40。
- 产品名称：`菲尚特FST`，字号 15px。
- 版本号：位于产品名称右上角，保留边框。
- 收起/展开按钮：28 × 28，正方形边框，与产品 Logo 区同一行，避免与版本号重叠。
