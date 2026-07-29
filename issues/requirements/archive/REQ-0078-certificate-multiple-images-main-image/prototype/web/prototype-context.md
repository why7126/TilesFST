---
purpose: REQ-0078 Web 管理端原型上下文
content: 品牌证书多图上传、主图设置、删除兜底和列表缩略图验收说明
source: issues/requirements/archive/REQ-0078-certificate-multiple-images-main-image/requirement.md
created_at: 2026-07-28 22:32:00
updated_at: 2026-07-28 22:38:51
status: approved
---

# Prototype Context

## 目标

本原型用于锁定 `REQ-0078` 的管理端验收重点：

- 品牌证书编辑弹窗支持多张图片上传、主图设置和删除兜底。
- 品牌证书列表优先展示主图缩略图。
- 上传控件覆盖 idle、uploading、done、failed 状态。
- 弹窗宽度、滚动、fixed toast、DS confirm 和上传链路遵守 knowledge-base 横切 AC。

## 视觉与组件约束

- 视觉方向沿用“工业石材 · 暗色旗舰风”。
- 实现阶段优先复用品牌证书管理页现有列表、弹窗和上传组件；如需要抽象上传图片卡片，应先在 OpenSpec 设计中说明。
- TSX/CSS 实现不得新增裸 Hex；使用 semantic token 或现有 CSS 变量。
- 原型 HTML 仅用于验收语义参考，不替代最终 React / Tailwind / shadcn 实现。

## 原型文件

| 文件 | 说明 |
|---|---|
| `certificate-multiple-images-main-image.html` | 列表主图缩略图、证书编辑弹窗多图状态的静态验收原型 |
| `prototype-context.md` | 本上下文说明 |
| `certificate-multiple-images-main-image.png` | 待导出，后续可由浏览器截图或设计工具生成 |

## 样例数据

| 场景 | 样例 | 预期 |
|---|---|---|
| 三张图片 | 封面、检测页、附页 | 封面为主图，位于第一位 |
| 设置主图 | 点击附页“设为主图” | 附页移动到第一位且唯一主图 |
| 删除主图 | 删除当前封面 | 下一张图片自动成为主图 |
| 上传失败 | 超限图片 | 控件内显示失败原因，不写入 done 列表 |
| PDF 兼容 | PDF 证书无图片 | 列表继续显示 PDF 占位 |

## 验收重点

- 1440px 桌面视口下，弹窗 computed width 与设计批准宽度一致。
- 720px 高度以下，弹窗 body 可滚动，底部操作区不遮挡图片区。
- 列表分页 DOM 不因主图缩略图改造回归。
- 上传成功后同会话即时回显，失败原因在上传控件内展示。
- 状态操作 confirm 和 fixed toast 不因本需求回归。
