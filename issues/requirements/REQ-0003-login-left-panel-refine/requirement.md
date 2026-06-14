# REQ-0003 登录页左栏文案与布局微调

## 1. 背景

Sprint 001 登录页在 REQ-0002（TilesFST 品牌、移除企微、视口无滚动）落地后，产品方对 **登录页左侧品牌区** 提出四项微调：

1. 左栏 **白色主标题** 文案由「TilesFST」改回 **「瓷砖信息管理后台」**（金色 Logo「TilesFST」保留）。
2. **忘记密码** 本期暂不开放，须 **隐藏入口**（非占位跳转）。
3. Logo「TilesFST」与下方眉标/主标题 **垂直间距过大**，须收紧。
4. 统计卡第三格「126 / 门店同步」被右下角 **材质拼贴（CALACATTA / 900×1800 区域）遮挡**，须将统计卡或相关区块 **整体上移**，保证三格数据可读。

本需求为 **追溯补登**：产品决策已确认，实现文件路径已明确；本文档补齐需求真相，**本期不创建 OpenSpec Change**（待后续统一纳入 fix-* change）。

## 2. 目标用户

- 企业内部员工：登录管理端前的首屏认知。
- 产品/设计：登录页左栏信息层级与视觉完整性。

## 3. 范围

| 项目 | 内容 |
|---|---|
| 左栏主标题 | `.brand-title` 白色文案 →「瓷砖信息管理后台」 |
| 左栏 Logo | `.logo` 金色 **TilesFST** 不变 |
| 忘记密码 | 登录表单区隐藏「忘记密码？」入口 |
| 左栏间距 | 收紧 `.brand-top`（Logo）与 `.brand-content` 间距 |
| 统计卡布局 | 避免 `.stats-card` 与 `.material-board` 重叠遮挡 |
| 不包含 | 忘记密码完整流程（见后续独立 REQ）、企微、全站 rebranding |

## 4. 业务目标

- 左栏主标题语义更清晰（管理后台定位）。
- 减少未实现能力对用户的干扰（隐藏忘记密码）。
- 修复左栏视觉缺陷（间距、遮挡），提升首屏专业度。

## 5. 功能要求

### FR-001 左栏白色主标题

- 登录页左栏 `.brand-title`（白色/ `--login-text`）MUST 显示 **「瓷砖信息管理后台」**。
- 金色 `.logo` MUST 仍为 **TilesFST**。

### FR-002 隐藏忘记密码入口

- 登录页右栏 MUST NOT 展示「忘记密码？」可点击入口。
- 「记住登录状态」保留；表单布局在隐藏链接后 MUST NOT 产生明显空洞（可调整 `.form-options` 对齐）。

### FR-003 Logo 与内容间距

- Logo 与下方 `TILE DATA OPERATING SYSTEM` 眉标之间垂直间距 MUST 明显小于当前实现（目标：视觉紧凑，与登录页整体密度一致）。
- 调整 SHOULD 通过 CSS（如 `.brand-top` margin-bottom、`.brand-content` padding-top）完成，避免破坏 50/50 分屏。

### FR-004 统计卡不被材质拼贴遮挡

- 桌面端（>= 1024px）三列统计卡（含 **126 / 门店同步**）MUST 完整可见，不被 `.material-board` 覆盖。
- 实现方式 MAY：上移 `.stats-card`、调整 `.material-board` 的 `bottom`/`right`、或提高统计区 `z-index` 并保证可读性；MUST NOT 删除材质拼贴或统计卡。

## 6. UI / UE 约束

- 继续沿用登录页 **CSS Port**（`login-page.css`），禁止裸 Hex。
- 右栏隐藏忘记密码 MUST NOT 引入 notice 横幅或破坏 REQ-0002 无整页滚动约束。
- 移动端（< 1024px）无左栏，FR-001/003/004 主要验收桌面端；FR-002 全端生效。

## 7. 关联需求

| 需求 | 关系 |
|---|---|
| REQ-0001 | 登录页基础能力、CSS Port |
| REQ-0002 | 品牌 Logo TilesFST、无企微、视口锁定；**本需求 MODIFIED 左栏主标题文案** |

## 8. 状态

```yaml
requirement_id: REQ-0003-login-left-panel-refine
priority: P1
status: resolved
implementation_mode: retroactive  # 追溯补登
owner: 产品负责人
iteration: sprint-001
openspec_change: fix-login-left-panel-refine
```
