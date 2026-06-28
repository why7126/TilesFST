# REQ-0016 Banner 管理 - 弹窗原型上下文（专题页）

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 Banner 管理「新增/编辑 Banner」弹窗在 **专题页** 跳转类型下的视觉与交互。

优先级：
1. `prototype/web/banner-management-modal-topic-page.html`
2. `prototype/web/banner-management-modal-topic-page.png`
3. `requirement.md`
4. `rules/ui-design.md`

## 2. 页面结构

- 左侧 Sidebar 与 Banner 管理列表页保持一致，当前激活菜单为 `OPERATIONS / Banner管理`。
- 页面主体保留 Banner 管理列表作为弹窗背景。
- 中央弹窗宽度 640px，最大高度 92vh，内容区可滚动。
- 弹窗标题：`新增 Banner · 专题页`。

## 3. 表单字段

公共字段：Banner 标题、展示端、展示位置、Banner 图片、跳转类型、排序、有效期、运营备注。

当前跳转类型：`专题页`。

## 4. 条件交互

- 选择 `专题页` 后展示关联专题选择器。
- 专题下拉需支持按专题名称 / 专题编码搜索。
- 前台点击 Banner 后进入专题详情页。
- Banner 图片由用户上传或从专题封面复用，当前原型以已上传运营图展示。

## 5. UI 一致性

- 主按钮使用品牌金实底，深色文字。
- 输入框、选择器高度统一 40px。
- 弹窗不展示「状态策略信息」。
- 圆角、分割线、弱文字、徽章色值遵循 `ui-design.md`。
