---
title: 需求验收标准
purpose: REQ-0003 登录页左栏与忘记密码隐藏验收
source: requirement.md
update_method: 实现完成后勾选
owner: 产品负责人
status: implemented
note: fix-login-left-panel-refine 已实现
---

# 验收标准

## 1. 左栏文案（FR-001）

- [x] AC-001 桌面端左栏 `.logo` 文案 MUST 为 **TilesFST**（金色）。
- [x] AC-002 桌面端左栏 `.brand-title` 文案 MUST 为 **「瓷砖信息管理后台」**（白色/主文字色）。
- [x] AC-003 `.brand-title` MUST NOT 仍为「TilesFST」。

## 2. 忘记密码隐藏（FR-002）

- [x] AC-010 登录页 DOM 中 MUST NOT 渲染可见的「忘记密码？」入口（`display: none`、条件不渲染或移除节点均可）。
- [x] AC-011 「记住登录状态」与登录按钮 MUST 正常展示且可交互。
- [x] AC-012 隐藏忘记密码后 `.form-options` 布局 MUST NOT 明显错位或留大块空白。

## 3. Logo 间距（FR-003）

- [x] AC-020 Logo「TilesFST」与下方「TILE DATA OPERATING SYSTEM」眉标垂直间距 MUST 较 REQ-0002 实现明显收紧（团队目视确认或通过截图对比）。
- [x] AC-021 收紧间距 MUST NOT 导致左栏内容溢出或触发页面级纵向滚动（REQ-0002 约束仍满足）。

## 4. 统计卡遮挡（FR-004）

- [x] AC-030 在 1440×1024 桌面视口，统计卡第三格 **「126」「门店同步」** MUST 完整可见。
- [x] AC-031 `.material-board` 中 **CALACATTA / 900×1800** 区域 MUST NOT 覆盖统计卡文字。
- [x] AC-032 三列统计（12,860 / 38,420 / 126）MUST 均可读。

## 5. 回归

- [x] AC-040 REQ-0002：无企微入口、视口无整页纵向滚动 — 仍 pass。
- [x] AC-041 `LoginForm.test.tsx` / `LoginPage.test.tsx` 更新后 MUST pass（断言无忘记密码、主标题文案）。
- [x] AC-042 `python scripts/validate-design-system.py` MUST pass。

## 6. 不在本期

- [x] 忘记密码完整流程 — 不验收（入口已隐藏）。
