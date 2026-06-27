## ADDED Requirements

### Requirement: 产品版本 pill 视觉一致性修复（Web 客户端）

Web 客户端 MUST 修复跨端产品版本 pill 的视觉一致性缺陷（BUG-0013）：管理端与店主端 MUST 共用同一 badge 组件或 variant，pill 样式 MUST 对齐 REQ-0010 原型与 `rules/ui-design.md` §8。pill MUST 含 `padding: 2px 7px` 等价、`font-weight: 500`、`tracking-badge`（或 prototype 0.04em）；MUST 使用 semantic token，MUST NOT 含裸 Hex。Vitest MUST 断言渲染的版本元素含 pill 关键 class（如边框与 muted 文字），不仅断言版本字符串。修复 MUST NOT 变更 `PRODUCT_VERSION` 单一事实源、登录页/页脚版本展示策略或 API。

#### Scenario: 跨端 badge 组件复用

- **WHEN** 开发者查看管理端 `AdminSidebar` 与店主端 `Sidebar` brand-head 实现
- **THEN** 两端 MUST 使用同一 `ProductVersionBadge`（或 `Badge` version variant）实现
- **AND** MUST NOT 在两端分别维护 divergent ad-hoc pill 样式

#### Scenario: 店主端 pill 与管理端视觉一致

- **WHEN** 用户访问店主端带侧栏页面（如 `LandingPage` / `ListPage`）
- **THEN** 侧栏顶部版本 pill MUST 与管理端 pill 视觉一致
- **AND** 版本值 MUST 仍等于 `PRODUCT_VERSION`

#### Scenario: 店主端原型并排验收

- **WHEN** 开发者在 1280×1024 下将店主端与 `product-version-sidebar-catalog.html` 并排对比
- **THEN** brand-head 内版本 pill MUST 与原型语义一致
- **AND** 筛选 section MUST 无回归

#### Scenario: Vitest 样式断言

- **WHEN** 运行 `cd src/web && pnpm test` 中与版本 badge 相关用例
- **THEN** 测试 MUST 断言 pill 元素含边框与 muted 文字等关键 class
- **AND** MUST 继续 import `PRODUCT_VERSION` 断言文案，MUST NOT duplicate 硬编码版本字符串
