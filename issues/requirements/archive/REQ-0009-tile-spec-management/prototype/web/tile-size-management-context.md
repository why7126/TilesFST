# REQ-0009 瓷砖规格管理 - 产品原型图上下文工程

## 1. 原型目标

指导前端还原 TILESFST 管理后台「瓷砖规格」管理页面（v2 PRD：对齐品牌页启停/删除/指标卡，SKU 下拉联动见 acceptance AC-026~031）。

- `prototype/web/tile-size-management.html`：列表页静态展示。
- `prototype/web/tile-size-management-modal.html`：新增/编辑弹窗交互页。

PNG Golden Reference（**待导出**）：

- `prototype/web/tile-size-management.png`
- `prototype/web/tile-size-management-modal.png`

> 文件名保留 `tile-size-management` 历史命名；页面文案统一为「瓷砖规格」。

## 2. 视觉来源

继承管理后台暗色旗舰风：固定 Sidebar、右侧独立滚动、品牌金 CTA、0.5px 分割线、3px 卡片圆角。与 **瓷砖品牌管理页** 保持列表/启停/分页一致。

## 3. 页面画布

- 画布：1440 × 1024。
- Sidebar：264px，100vh sticky。
- 主内容 max-width：1080px。
- 导航高亮：瓷砖规格（类目之后、Banner 之前）。

## 4. 页面结构

```text
admin-shell
├── sidebar
└── main-content
    └── content-inner
        ├── page-header（MASTER DATA / 瓷砖规格 / ＋ 新增瓷砖规格）
        ├── metric-grid（总数 / 启用 / 停用 / 未关联SKU）
        ├── filter-card（关键词 + 状态 + 查询 + 重置）
        ├── table-card（无 section 标题）
        └── pagination（左共 x 条 / 右页码+每页条数）
```

## 5. 关键视觉约束

- 页面标题：**瓷砖规格**。
- 眉标：`MASTER DATA`。
- 主按钮：`＋ 新增瓷砖规格`。
- 指标卡四列：**规格总数、启用规格、停用规格、未关联 SKU**（非标准砖/大板）。
- 筛选：**关键词 + 状态（全部/启用/停用）**；无规格类型筛选。
- 无导出、无批量、无跳页输入框。

## 6. 表格字段

```text
尺寸名称 / 宽度(mm) / 长度(mm) / 厚度(mm) / 关联SKU / 排序 / 状态 / 更新时间 / 操作
```

- 尺寸名称主行 + 备注副行（可选）。
- 状态 badge：启用（gold）/ 停用（muted）。
- 操作：**编辑 | 启用或停用 | 删除**。
- 删除置灰两种场景：
  - `sku_count > 0` → hover「已关联 SKU，不允许删除」（或统一用品牌文案，以实现为准）
  - `sku_count = 0` 且启用 → hover「仅允许删除未关联SKU且已停用的规格」

## 7. 新增/编辑弹窗

- 标题：新增瓷砖规格 / 编辑瓷砖规格。
- 字段：宽度*、长度* → 尺寸名称(只读) → 厚度、排序* → 备注。
- **禁止**：单位、规格类型、常用尺寸、系统状态、可编辑尺寸名称。
- 宽长输入后实时 `宽度×长度mm`；重复时红色错误「该尺寸已存在，请勿重复创建」。
- modal HTML 内置 JS 演示实时生成（与 v1 一致）。

## 8. 启停确认（列表页实现参考）

列表 HTML 为静态；生产实现 MUST 对齐 `BrandManagementPage` 启停确认弹窗（REQ-0008）。

## 9. 分页

```text
左侧：共 86 条
右侧：‹ 1 2 3 … 5 ›  每页显示 [20]
```

## 10. SKU 表单（无独立 prototype HTML）

- 规格字段改为 `<select>`，数据源 `status=ENABLED`。
- 验收见 `acceptance.md` AC-026~031。

## 11. 一致性检查清单

- [ ] Logo、导航、用户菜单与既有 admin 页一致。
- [ ] 列表含状态列与启停操作（v2 新增）。
- [ ] 指标卡为启用/停用语义（v2 变更）。
- [ ] 文案全部为「瓷砖规格」而非「瓷砖尺寸」。
- [ ] HTML 与 PNG 一一对应（PNG 待导出）。
