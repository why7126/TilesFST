---
req_id: REQ-0016-banner-management
status: captured
created_at: 2026-06-28 10:55:38
updated_at: 2026-06-28 10:55:38
recorded_by: product
source: 产品
priority_hint: P1
parent_requirement: REQ-0004-admin-home
---

# 一句话

管理后台实现 Banner 管理：列表页 + 按跳转类型（SKU 详情 / 外部链接 / 专题页 / 无跳转）分化的新增/编辑弹窗；状态在列表操作，弹窗不展示状态策略块。

# 原始描述

实现 Banner 管理功能，设计已完成。交付范围包括：

## 列表页

- 原型：`prototype/web/banner-management-list.html`
- Golden：`prototype/images/banner-management-list.png`
- 上下文：`prototype/web/banner-management-list-context.md`
- 列表字段：Banner、展示端、跳转类型、状态、有效期、排序、更新时间、操作。

## 弹窗（按跳转类型 4 套）

| 跳转类型 | HTML | Golden | 上下文 |
|---|---|---|---|
| SKU 详情 | `banner-management-modal-sku-detail.html` | `banner-management-modal-sku-detail.png` | `banner-management-modal-sku-detail-context.md` |
| 外部链接 | `banner-management-modal-external-link.html` | `banner-management-modal-external-link.png` | `banner-management-modal-external-link-context.md` |
| 专题页 | `banner-management-modal-topic-page.html` | `banner-management-modal-topic-page.png` | `banner-management-modal-topic-page-context.md` |
| 无跳转 | `banner-management-modal-no-jump.html` | `banner-management-modal-no-jump.png` | `banner-management-modal-no-jump-context.md` |

## 关键业务规则

1. **弹窗不展示状态策略信息**：新增默认草稿或后台默认策略；上线/下线/删除在列表完成。
2. **SKU 详情**：必填关联 SKU；Banner 图默认 SKU 主图，可切换图库或自定义上传；保存记录图片来源。
3. **外部链接**：必填外链；校验协议/格式/安全；小程序外链走白名单或中转页。
4. **专题页**：必填关联专题；支持名称/编码检索；前台进专题详情。
5. **无跳转**：不展示跳转目标字段；前台仅展示不响应点击。

## UI/UE

- TILESFST 暗色旗舰风；与用户管理等参考页一致（Sidebar、标题区、列表卡、弹窗、按钮、输入框）。
- 主 CTA 品牌金；圆角 2px；输入高度 40px；弹窗宽 640px、最大高 92vh、内容可滚动。
- 禁止占位版本；字段、规则、状态须可开发执行。

## 设计包来源

产品提供完整设计包（外部目录名 `REQ-0010-banner-management`；项目内分配 **REQ-0016** 因 REQ-0010 已用于产品版本展示）。HTML、PNG Golden、context 已落盘至 `prototype/web/`。

# 背景与关联

- 父需求：`REQ-0004-admin-home`（侧栏已有「Banner 管理」占位入口与首页快捷操作「新增 Banner」）。
- 关联：`REQ-0006-tile-sku-management`（SKU 详情跳转、图库主图）、瓷砖类目/品牌等 OPERATIONS 导航同级页。
- 展示端：管理端配置；店主 Web / 小程序为 Banner 消费端（本期以管理端为主，消费端展示规则在 PRD 展开）。

# 待澄清

- [ ] 展示端枚举：店主 Web、小程序是否多选；与跳转类型的组合矩阵。
- [ ] 专题页主数据：是否已有专题模块或本期 mock / 后续 REQ。
- [ ] 外链白名单与小程序中转页：是否本期实现或仅管理端校验 + 文档约束。
- [ ] 列表操作全集：上线、下线、删除之外是否含编辑、排序拖拽、复制。
- [ ] 有效期：是否支持永久 + 区间；过期自动下线策略。
- [x] 设计包 HTML/PNG/context 落盘 — 已完成（`prototype/web/`）。

# 探索结论

（/req-explore 后人工确认写入）
