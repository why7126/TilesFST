---
title: 业务流程
purpose: REQ-0003 变更不涉及新业务流程，记录登录页展示态调整
source: REQ-0003 requirement.md
update_method: 范围变更时同步
owner: 产品负责人
status: ready
---

# 业务流程

## 1. 说明

本需求 **不新增** 认证或找回密码业务流程，仅调整 `/admin/login` **静态展示与布局**。

## 2. 登录页展示态（变更后）

```text
/admin/login
├── 左栏 .brand-panel（桌面端）
│   ├── .logo → TilesFST（金色，不变）
│   ├── .brand-content
│   │   ├── 眉标 TILE DATA OPERATING SYSTEM
│   │   ├── .brand-title → 瓷砖信息管理后台（白色）
│   │   ├── 描述文案
│   │   └── .stats-card（三格完整可见，含 126）
│   ├── .material-board（右下角，不遮挡 stats）
│   └── .brand-bottom
└── 右栏 .form-panel
    ├── 语言切换
    ├── 登录表单（无「忘记密码？」）
    ├── 登录按钮
    └── 安全说明
```

## 3. 与 REQ-0002 差异

| 元素 | REQ-0002 | REQ-0003 |
|---|---|---|
| `.logo` | TilesFST | TilesFST（不变） |
| `.brand-title` | TilesFST | **瓷砖信息管理后台** |
| 忘记密码 | 占位按钮可见 | **隐藏** |
| Logo 下间距 | 未专项收紧 | **收紧** |
| stats vs material-board | 未专项 | **126 格不被遮挡** |

## 4. 验收路径

```text
打开 /admin/login（桌面 >= 1024px）
  → 目视检查左栏标题、间距、统计卡
  → 目视检查右栏无忘记密码
  → 1280×720 / 1440×1024 视口复验无整页滚动（REQ-0002 仍满足）
```
