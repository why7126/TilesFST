# REQ-0005 品牌管理列表页 - 产品原型图上下文工程

## 原型目标
用于指导前端开发还原 TILESFST 管理后台“瓷砖品牌”列表页。优先参考 `prototype/web/brand-management.html`；Golden Reference PNG 待导出至同目录 `brand-management.png`。

## 视觉来源
继承 admin-home V5：固定 Sidebar、右侧独立滚动、暗色旗舰风、品牌金激活态、0.5px 分割线、3px 卡片圆角。

## 页面画布
- 推荐尺寸：1440 × 1024
- Sidebar：264px，100vh sticky
- 主内容最大宽度：1080px
- 当前导航：瓷砖品牌高亮

## 结构
```text
page-header → metric-grid → filter-card → table-card → pagination
```

## 关键约束
- 不出现导出按钮。
- 不出现批量操作。
- 不出现“品牌检索”标题。
- 不出现“品牌列表”标题。
- 操作列为：编辑、启用/停用、删除。
- 删除仅 SKU数量=0 且状态=停用时可点击。
- 分页右侧展示“每页显示 20/50/100”。

## 删除按钮视觉
- 可删除：风险色 `#E07050`。
- 不可删除：弱文字色，cursor not-allowed。
- hover tooltip：仅允许删除未关联SKU且已停用的品牌。

## 一致性检查
Logo、导航、用户菜单、卡片、表格、按钮、输入框、分页均与 admin-home V5 风格一致。
