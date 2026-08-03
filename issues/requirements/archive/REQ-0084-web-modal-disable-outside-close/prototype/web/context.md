---
requirement_id: REQ-0084-web-modal-disable-outside-close
title: Web 端弹窗禁用外部点击关闭 - Prototype Context
status: approved
owner: product
source: requirement.md
created_at: 2026-07-30 23:09:16
updated_at: 2026-07-30 23:18:07
---

# Prototype Context

## 目的

本 prototype 仅表达交互策略：点击遮罩或弹窗外空白区域时，标准弹窗保持打开；用户通过关闭图标、取消按钮或保存成功等明确路径关闭。它不是视觉重设计稿，不作为弹窗尺寸、颜色或组件结构的最终来源。

## 覆盖场景

- 管理端表单弹窗：SKU、品牌、类目、证书、Banner 等资料维护。
- 管理端确认弹窗：删除、上下架、批量操作等确认流程。
- Web 展示端标准弹窗：商品详情、品牌详情、图片预览、联系或咨询弹窗。
- 含上传控件弹窗：上传过程中误点外部不关闭，不打断上传状态机。

## 交互规则

| 操作 | 期望结果 |
|---|---|
| 点击遮罩 / 外部空白区域 | 弹窗保持打开，展示轻微状态提示或不做可见反馈。 |
| 点击关闭图标 | 弹窗关闭；若后续定义未保存保护，则按保护策略处理。 |
| 点击取消按钮 | 弹窗关闭；若后续定义未保存保护，则按保护策略处理。 |
| 点击保存按钮 | 成功后关闭；失败后保持打开并展示错误。 |
| 上传中误点外部 | 弹窗保持打开，上传状态继续。 |

## 待导出

- PNG Golden Reference：待后续设计或 OpenSpec 阶段按实际组件截图导出。
- Playwright 验证：后续实现阶段覆盖真实组件，而非仅验证本静态 prototype。

## 知识库引用

- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-013-retrospective.md`
