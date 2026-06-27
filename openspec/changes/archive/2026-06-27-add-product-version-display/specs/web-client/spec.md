## ADDED Requirements

### Requirement: 产品版本常量与 Web 端展示

Web 客户端 MUST 在 `src/shared/` 维护单一产品版本常量（如 `PRODUCT_VERSION = 'v0.0.1'`），管理端与店主端 MUST 引用同一导出。产品版本 MUST 由发版时人工更新该常量；MUST NOT 从 `package.json`、`pyproject.toml`、FastAPI `version` 或 CI/Git 构建信息读取。Web 客户端 MUST NOT 在登录页、页脚或关于页展示产品版本（本期 Out）。Web 客户端 MUST NOT 展示 API / OpenAPI / 后端版本号作为产品版本。

#### Scenario: 单一事实源

- **WHEN** 开发者查看产品版本定义
- **THEN** MUST 存在且仅存在一处 `src/shared/` 产品版本常量导出
- **AND** 管理端 `AdminSidebar` 与店主端 `Sidebar` MUST import 同一常量

#### Scenario: 禁止自动版本源

- **WHEN** 实现读取展示用版本号
- **THEN** MUST NOT 使用 npm package version、FastAPI app version 或 git sha 作为 `PRODUCT_VERSION` 展示值

### Requirement: 店主端侧边栏产品版本展示

店主端使用筛选侧栏的页面（如经 `LandingPage`、`ListPage` 与 `CatalogBody` 渲染的模板）MUST 在 `Sidebar` **最上方**（第一个筛选 section 之上）展示品牌名与产品版本 pill。布局语义 MUST 与管理端一致：品牌名左、版本 pill 紧邻右侧；版本值 MUST 等于 `PRODUCT_VERSION`。版本 MUST 在侧栏内展示；MUST NOT 仅在顶栏 `SiteNav` 展示而侧栏缺失。

#### Scenario: 店主端侧栏顶部版本

- **WHEN** 用户访问店主端带侧栏页面（如首页或目录列表）
- **THEN** 侧栏最上方 MUST 可见品牌名（默认 STONEX 或 DS 等价）与版本 pill
- **AND** pill 文案 MUST 等于 `PRODUCT_VERSION`

#### Scenario: 筛选区无回归

- **WHEN** 用户查看店主端侧栏筛选 checkbox 区
- **THEN** 筛选 section 标题与选项 MUST 正常展示
- **AND** brand-head MUST NOT 挤压或遮挡筛选交互

#### Scenario: 店主端版本 pill 样式

- **WHEN** 开发者查看店主端版本 pill 实现
- **THEN** MUST 复用与管理端相同的 badge 组件或等价 semantic token 类
- **AND** TSX MUST NOT 包含裸 Hex
