---
note: workflow-sync — 6/6 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-015
title: Sprint 015 Acceptance Report
status: completed
created_at: 2026-07-31 15:17:00
updated_at: 2026-07-31 23:09:20
---

# Sprint 015 Acceptance Report

## 验收状态

最终结论：通过，Sprint 已关闭。2026-07-31 23:07:14 执行 `/sprint-archive sprint-015`，Readiness 校验显示 6/6 Change 已归档、109/109 任务完成且归档 trace 齐备；1 个 REQ 与 5 个 BUG 均已处于 archive/done。小程序 DevTools / 真机验收与对象存储历史回填仍按原记录保留为 follow_up/运营执行项，不阻断本次 Sprint 归档。

## 正式范围

| 类型 | 编号 | Change | 状态 | 验收 |
|---|---|---|---|---|
| REQ | REQ-0086-miniapp-brand-list-ui-interaction-optimization | update-miniapp-brand-list-ui-interaction-optimization | done，已归档（`update-miniapp-brand-list-ui-interaction-optimization` archived 2026-07-31 21:19:20） | 已移除品牌矩阵与类目区说明文案；类目胶囊字号比品牌名称小 2rpx；小程序静态测试通过；DevTools / 真机验收 follow_up |
| BUG | BUG-0096-admin-sku-category-filter-only-top-level | fix-admin-sku-category-cascade-filter | done，已归档（`fix-admin-sku-category-cascade-filter` archived 2026-07-31 21:25:00） | 已归档，Readiness PASS |
| BUG | BUG-0097-admin-sku-material-main-image-tag-redundant | fix-admin-sku-material-main-image-tag | done，已归档（`fix-admin-sku-material-main-image-tag` archived 2026-07-31 15:36:22） | 前端回归通过，已归档 |
| BUG | BUG-0095-admin-category-tree-count-shows-product-count | fix-admin-category-tree-count | done，已归档（`fix-admin-category-tree-count` archived 2026-07-31 17:29:59） | 后端、前端回归通过；“全部类目”计数列、文字左对齐与选中态边框返修通过，已归档 |
| BUG | BUG-0094-miniapp-list-images-not-loading-after-speed-fix | fix-miniapp-product-card-thumbnails | done，已归档（`fix-miniapp-product-card-thumbnails` archived 2026-07-31 21:33:42） | 后端媒体与小程序静态回归通过，已归档；历史回填执行和真机验收保留 follow_up |
| BUG | BUG-0098-admin-filter-dropdown-ui-consistency | fix-admin-filter-dropdown-ui-consistency | done，已归档（`fix-admin-filter-dropdown-ui-consistency` archived 2026-07-31 23:00:57） | 已完成品牌页、类目页、规格页、品牌证书页、Banner 管理页、用户管理页、系统设置页、日志审计页、接口文档页和界面主题统一下拉返修；前端回归通过，已归档 |

## 归档校验摘要

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-31 23:07:14 | `python scripts/validate-sprint-archive-readiness.py --sprint sprint-015` | PASS：6/6 Change archived，109/109 tasks done |
| 2026-07-31 23:07:14 | `python scripts/promote-issues-for-archive.py --sprint sprint-015` | PASS：无待移动 Issue，所有范围 Issue 已在 archive |

## 验收清单

- [ ] 素材列只显示图片数量与视频数量，不显示「主图已设」「缺主图」或其他素材状态标签。
- [ ] SKU 页类目筛选使用单个级联下拉控件展示完整类目树，不在筛选区并排出现多个类目筛选框。
- [ ] 点击有下级的当前类目时，下级类目在同一下拉层右侧展开。
- [ ] 类目筛选选中后，不在筛选项下方展示「当前：xxx」文案。
- [ ] 类目下拉层位于筛选控件下方，并浮于 SKU 列表之上，不被列表或操作列遮挡。
- [ ] 品牌、类目、状态三个筛选下拉的触发框、下拉位置、选项样式和选中态保持一致。
- [ ] SKU 页可选择一级、二级、三级或更深层级类目。
- [ ] 选择父类目时，SKU 列表包含该父类目自身及所有子孙类目的 SKU。
- [ ] 选择子类目时，SKU 列表不返回无关父级或兄弟类目 SKU。
- [ ] 类目级联筛选可清空，重置后回到「全部类目」。
- [ ] 类目筛选与关键词、品牌、状态、分页和默认排序组合不回归。
- [ ] 素材列仍正确显示图片数量与视频数量。
- [ ] SKU 列表不展示素材完整度条件筛选，列表请求不提交 `material_completeness`。
- [ ] 缺图、缺视频或素材不完整状态仍可通过图片/视频数量识别。
- [ ] 移除所有素材状态标签后，列表行高、列宽、状态列和操作列不出现遮挡或布局抖动。
- [ ] SKU 新增、编辑、图片主图兜底、上下架、删除等操作不受影响。
- [ ] 管理端一级类目右侧数字显示直接子类目数量，不显示商品数量。
- [ ] 管理端叶子类目右侧数字显示 `0`。
- [ ] “全部类目”入口右侧数字显示顶层类目数量，不显示商品总数。
- [ ] “全部类目”入口右侧数字与一级类目右侧数字保持同列视觉对齐。
- [ ] “全部类目”文字与类目树标题文字保持左对齐，且不改变右侧数字位置。
- [ ] “全部类目”被选中时，选中态边框完整包住入口文字和右侧数字。
- [ ] 类目树展开/折叠和点击节点刷新右侧列表行为不回归。
- [ ] 小程序品牌列表页展示新版品牌 Hero、品牌矩阵标题、单品牌卡片和底部 TabBar 品牌选中态。
- [ ] 品牌卡片上行点击进入品牌详情页，下行类目胶囊点击进入品牌 + 类目商品列表页，类目胶囊字号比品牌名称小 2rpx。
- [ ] 类目胶囊点击携带 `brandId` 与 `categoryId`，且不触发品牌详情跳转。
- [ ] 小程序品牌列表页在 320、375、390、430 pt 视口下不遮挡微信胶囊、底部 TabBar 或主要内容。
- [ ] 真机验收不可用时标记 `blocked` 或 `follow_up`，不得写作真机通过。
- [ ] 小程序首页“新品推荐”“热销推荐”“全部产品”中有真实主图的商品卡片恢复展示真实图片，不全部显示“暂无图片”。
- [ ] 分类商品列表、品牌商品列表、搜索结果页、品牌详情商品区复用商品卡片时，有真实主图的商品卡片图片正常展示。
- [ ] 公开列表 `cover_image` 不返回已知不可访问的 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>`。
- [ ] `images/default/tiles/pending/<uuid>.<ext>` 主图生成同目录文件名差异化缩略图，且不以独立 `thumbnails/default/tiles/pending/` 前缀作为最终策略。
- [ ] 历史缩略图回填输出总数、成功数、失败数和失败原因摘要，且不泄露密钥、Authorization header、Cookie、`.env` 内容或本机路径。
- [ ] 商品卡片图片审计可输出公开 SKU、无主图、pending 主图、原图对象缺失和缩略图对象缺失统计。
- [ ] BUG-0092 图片加载性能核心验收不回退，首屏外商品卡片仍使用懒加载或等价延迟加载策略。
- [ ] 管理端品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档和界面主题等页面筛选下拉位置、尺寸、触发方式和视觉样式与瓷砖类目页一致。
- [ ] 管理端筛选下拉弹层宽度、边界对齐、打开方向、层级和阴影表现一致，且不被表格、页面容器、滚动区域、弹窗或 sticky action column 裁切。
- [ ] 筛选下拉选项文本、间距、图标、悬停态、选中态、禁用态、空态和加载态一致。
- [ ] 筛选重置后下拉框恢复默认展示，占位文案和筛选结果刷新行为与瓷砖类目页一致。
- [ ] BUG-0098 修复不改变现有筛选字段、查询参数、接口请求和查询结果语义。
- [ ] 管理端筛选下拉使用 Design System semantic token，不新增页面级裸 Hex 或与统一控件冲突的局部样式。
- [ ] 鼠标、键盘和窄屏窗口操作筛选下拉时不出现文本溢出、按钮遮挡、焦点丢失、不可点击或布局抖动问题。
