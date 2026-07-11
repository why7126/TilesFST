---
title: 用户故事
purpose: REQ-0013 管理端 Shell padding 与 content fluid 相关用户故事
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: done
created_at: 2026-06-28 09:20:59
updated_at: 2026-07-11 17:18:39
note: REQ-0013-admin-shell-padding-refine
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 后台管理员 / 内部员工 | P1 | 是 |
| US-002 | 后台管理员 / 内部员工 | P1 | 是 |
| US-003 | 后台管理员 / 内部员工 | P2 | 是 |

---

## US-001 宽屏下列表占用更多横向空间

**作为** 后台管理员，  
**我希望** 在宽屏（1440 / 1920）浏览 SKU、用户等列表时，表格区域更宽、左右暗区更少，  
**以便** 一次看到更多列信息，减少横向滚动或视觉空洞感。

### 验收要点

- 主内容 `padding` 为当前落地值 `24px 24px 48px`。
- `.content-inner` 统一 `max-width: min(1440px, 100%)`；无 SKU 页 1120px 分叉。
- 1920×1080 expanded 下 content-inner 受 **1440px** 软 cap 约束。
- 1440×1024 expanded 下 content-inner 随可用宽度 fluid，无旧 1080px 居中死区。
- 侧栏右缘至 content-inner 左缘间距较旧 1080px 方案显著减少。

### 关联功能

- FR-001、FR-004、FR-006（见 `requirement.md`）

---

## US-002 侧栏导航区更紧凑但不改列宽

**作为** 后台管理员，  
**我希望** 侧栏菜单与列边缘之间的留白减少，  
**以便** 导航区更紧凑，同时仍保留 264px / 72px 折叠契约。

### 验收要点

- expanded：`.sidebar` 当前 padding **`30px 10px 18px`**；比原 18px 水平 padding 收紧，文案不异常换行。
- collapsed：padding **`16px 10px 18px`**；72px 列宽不变；无 `.nav-scroll` 横向滚动。
- chevron、version badge、REQ-0011 折叠行为不受影响。
- 不替换 nav 占位图标（BUG-0021 Out）。

### 关联功能

- FR-002、FR-003、FR-007（见 `requirement.md`）

---

## US-003 平板与手机仍可读且不沿用桌面 6px

**作为** 后台管理员，  
**我希望** 在 ≤1023px 或手机宽度访问管理端时，壳层 padding 与桌面协调、不过挤，  
**以便** 小屏仍符合 REQ-0011 响应式结构。

### 验收要点

- ≤1023px：侧栏 **勿** 使用 desktop 紧凑 padding；sidebar 为 `22px 20px`，main 为 `20px 16px 40px`。
- ≤639px：main 为 `16px 12px 32px`。
- 侧栏双列 nav、隐藏 user menu、chevron 隐藏等行为与 REQ-0011 一致。

### 关联功能

- FR-005（见 `requirement.md`）

---

## 非本期故事

| 编号 | 描述 |
|---|---|
| US-101 | 侧栏列宽 264→220 收窄 |
| US-102 | 导航项 Lucide 真图标（BUG-0021） |
| US-103 | 店主端 / 小程序壳层 padding |
| US-104 | 按页面类型拆分 content max-width（列表 full / dashboard 窄） |
