# 瓷砖SKU管理页面 - 列表页原型上下文 v4

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 TilesFST 管理后台「瓷砖SKU」列表页。开发时应优先参考 `prototype/web/tile-sku-management-list.html`；`prototype/images/tile-sku-management-list.png` 为**可选** Golden Reference（有则辅助验收，无则以 HTML 为准）。

## 2. 设计来源

- 全局设计规范：`ui-design.md`
- 管理后台首页上下文：`admin-home-context.md`
- 管理后台首页 HTML：`admin-home.html`
- 管理后台首页图片：`admin-home.png`
- 页面版本：REQ-0006-tile-sku-management-v4

## 3. 页面画布

| 项目 | 值 |
|---|---|
| 推荐设计稿尺寸 | 1440 × 1024 |
| 页面布局 | 左侧固定 Sidebar + 右侧工作台内容 |
| Sidebar 宽度 | 264px |
| Sidebar 高度 | 100vh |
| 右侧内容 | 独立滚动 |
| 主内容最大宽度 | 1120px |

## 4. 信息架构

```text
.admin-shell
├── aside.sidebar
│   ├── .logo TILESFST
│   ├── OPERATIONS 导航，瓷砖SKU active
│   ├── SYSTEM 导航
│   └── .sidebar-user 用户菜单
└── main.main-content
    └── .content-inner
        ├── .page-head 标题 + 新增SKU按钮
        ├── .metric-grid 4个指标卡
        ├── .filter-card 筛选区
        └── .table-card SKU列表 + 分页
```

## 5. 核心区域说明

### 5.1 标题区

- 标题：瓷砖SKU
- 说明：维护瓷砖商品资料、规格、价格与素材完整度
- 主按钮：新增SKU，品牌金实底，右侧对齐

### 5.2 数据概览

四个指标卡：SKU总数、已上架、待完善、草稿。数字使用品牌金。

### 5.3 筛选区

筛选项包括关键词、品牌、类目、状态、素材完整度。筛选控件使用暗色输入框和 0.5px 细边框。

### 5.4 表格

列结构：

| 列 | 说明 |
|---|---|
| SKU信息 | 主图缩略图、SKU名称、SKU编码 |
| 品牌 / 类目 | 品牌与类目上下两行 |
| 规格 / 工艺 | 规格尺寸与表面工艺 |
| 参考价格 | `¥ 268.00` 格式 |
| 素材 | 图片数、视频数、主图状态 |
| 状态 | 已上架 / 草稿 / 待完善 / 已停用 |
| 更新时间 | 时间 |
| 操作 | 编辑 / 上下架 / 更多 |

### 5.5 分页

列表底部左侧显示 `共 12,860 条`，右侧显示页码选择与每页条数。当前页码使用品牌金实底。

## 6. 一致性检查清单

- [ ] Sidebar 固定 100vh。
- [ ] 当前导航高亮「瓷砖SKU」。
- [ ] 页面有品牌金「新增SKU」按钮。
- [ ] 表格素材列同时展示图片数、视频数、主图状态。
- [ ] 分页左侧显示总数，右侧显示页码和每页条数。
- [ ] 视觉继承管理后台首页暗色旗舰风。
