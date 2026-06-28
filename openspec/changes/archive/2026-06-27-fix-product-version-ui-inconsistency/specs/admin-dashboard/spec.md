## ADDED Requirements

### Requirement: 产品版本 pill 视觉一致性修复（管理端）

Web 客户端 MUST 修复管理端 Sidebar brand-head 内产品版本 pill 的视觉一致性缺陷（BUG-0013）：版本 pill MUST 呈现可辨识的小号 badge 容器（可见边框、浅背景、弱化文字色），MUST NOT 退化为与主文字同色级的裸 sans-serif 文案。样式 MUST 对齐 `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html` 与 Golden Reference PNG 的布局语义；MUST 使用 semantic token（`text-muted`/`text-subtle`、`border-border-chip` 或 `border-border-default`、浅背景 token），TSX/CSS MUST NOT 含裸 Hex。实现 SHOULD 扩展 `src/web/src/shared/ui/badge.tsx` 而非平行 ad-hoc 组件。修复 MUST NOT 变更 `PRODUCT_VERSION` 常量来源、Sidebar 导航项或 API。

#### Scenario: 管理端版本 pill 可辨识

- **WHEN** 已登录 `admin` 或 `employee` 查看管理端 Sidebar 顶部 brand-head
- **THEN** `TILESFST` 右侧版本 pill MUST 展示可见边框与浅背景
- **AND** 版本文字 MUST 使用弱化色（`text-muted` 或等价 semantic token）
- **AND** pill MUST 与产品名垂直居中对齐、同一行 flex 排列（gap 约 8px）

#### Scenario: 管理端 pill 对齐 REQ-0010 原型

- **WHEN** 开发者在 1280×1024 下将实现与 `product-version-sidebar-admin.html`、Golden Reference PNG 并排对比
- **THEN** pill 高度（约 18px）、圆角（2px 工业圆角）、边框可见度与文字弱化层级 MUST 与原型语义一致
- **AND** change `trace.md` MUST 记录并排验收结论

#### Scenario: 管理端 brand-head 无布局回归

- **WHEN** 用户访问任意 `/admin/*` 经 `AdminLayout` 页面
- **THEN** `TILESFST` 品牌名 MUST 保持 serif 金色与既有 letter-spacing
- **AND** 导航项、用户菜单、主内容区 MUST 无回归

#### Scenario: 管理端 a11y 保持

- **WHEN** 辅助技术访问 brand-head 版本区
- **THEN** MUST 保留可见 pill 文案与 `aria-label`（如「产品版本 v0.0.1」）
