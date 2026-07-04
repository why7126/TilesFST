## MODIFIED Requirements

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示菲尚特品牌区，展开态顶部 MUST 包含菲尚特 Logo、品牌主标题 **菲尚特FST**、产品版本 badge 与副标题 **家居建材资料库**。产品版本值 MUST 来自跨端单一常量 `PRODUCT_VERSION`（`src/shared/`），MUST NOT 来自 `package.json`、FastAPI OpenAPI version 或构建/Git 信息。版本 badge MUST 为小号 badge，使用 semantic token，MUST NOT 使用裸 Hex。Logo、品牌文字组与展开/收起按钮 MUST 处于同一品牌行且不得互相遮挡；Logo 区域 MUST NOT 增加独立卡片背景、边框、渐变底纹或阴影。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。**仅 `role=admin` 用户 MUST 看到「系统设置」项**；`employee` MUST NOT 看到该项。当前路由为首页时，「首页」项 MUST 为 active 态；当前路由为 `/admin/tile-skus` 时，「瓷砖SKU」项 MUST 为 active 态（品牌金弱强调与左侧指示条）；当前路由为 `/admin/brands` 时，「瓷砖品牌」项 MUST 为 active 态；当前路由匹配 `/admin/settings` 或其子路径时，「系统设置」项 MUST 为 active 态。「瓷砖SKU」MUST 导航至 `/admin/tile-skus`，MUST NOT 仅展示占位 toast。「瓷砖品牌」MUST 导航至 `/admin/brands`，MUST NOT 仅展示占位 toast。「系统设置」MUST 配置 `path: '/admin/settings'`（或等价），MUST NOT 无 path 或无效点击。

#### Scenario: 品牌与分组展示

- **WHEN** 用户查看管理端 Sidebar 展开态
- **THEN** 顶部品牌区 MUST 展示菲尚特 Logo、**菲尚特FST**、产品版本 badge 与 **家居建材资料库**
- **AND** 产品版本 badge 文案 MUST 等于 `PRODUCT_VERSION`
- **AND** MUST 展示 OPERATIONS 与 SYSTEM 两个分组及各自导航项
- **AND** MUST NOT 展示 STONEX、TILESFST 或旧品牌名
- **AND** MUST NOT 展示 API 或后端版本号

#### Scenario: 品牌区布局与 Logo 容器

- **WHEN** 用户查看管理端 Sidebar 顶部品牌区
- **THEN** Logo、品牌文字组与展开/收起按钮 MUST 位于同一品牌行
- **AND** Logo MUST 保持比例，不拉伸、不裁切关键内容
- **AND** Logo 区域 MUST NOT 出现独立卡片背景、边框、渐变底纹或投影
- **AND** 展开/收起按钮 hover 后边框 MUST 与 Sidebar 内右边界保留安全间距

#### Scenario: 产品版本可访问性

- **WHEN** 辅助技术访问 Sidebar 顶部品牌区
- **THEN** 版本信息 MUST 可通过可见 badge 文本或 `aria-label`（如「产品版本 v0.0.1」）感知
- **AND** Logo MUST 具备可理解的替代文本（如「菲尚特家居建材」）

#### Scenario: Sidebar 收起态品牌识别

- **WHEN** 用户将管理端 Sidebar 切换到 collapsed 态
- **THEN** Sidebar MUST 保留 Logo 作为主要品牌识别元素
- **AND** 品牌文案、导航图标与展开/收起按钮 MUST NOT 重叠
- **AND** 展开/收起按钮 MUST 仍可点击并保留可访问标签

#### Scenario: 首页导航 active 态

- **WHEN** 用户位于 `/admin/dashboard`
- **THEN** 「首页」导航项 MUST 为 active 样式
- **AND** 其他导航项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌导航 active 态

- **WHEN** 用户位于 `/admin/brands`
- **THEN** 「瓷砖品牌」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: 瓷砖 SKU 导航 active 态

- **WHEN** 用户位于 `/admin/tile-skus`
- **THEN** 「瓷砖SKU」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: 瓷砖品牌可导航

- **WHEN** 用户点击 Sidebar「瓷砖品牌」
- **THEN** 系统 MUST 导航至 `/admin/brands`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 瓷砖 SKU 可导航

- **WHEN** 用户点击 Sidebar「瓷砖 SKU」
- **THEN** 系统 MUST 导航至 `/admin/tile-skus`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 系统设置可导航

- **WHEN** `admin` 用户点击 Sidebar「系统设置」
- **THEN** 系统 MUST 导航至 `/admin/settings`（或 `/admin/settings/basic`）
- **AND** MUST NOT 展示「功能建设中」占位 toast

#### Scenario: 系统设置 active 态

- **WHEN** `admin` 位于 `/admin/settings/media`
- **THEN** 「系统设置」导航项 MUST 为 active 样式

#### Scenario: 运营不展示系统设置

- **WHEN** `employee` 查看 SYSTEM 分组
- **THEN** MUST 仅展示「用户管理」
- **AND** MUST NOT 展示「系统设置」

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖SKU」「瓷砖品牌」「用户管理」（若可见）、「系统设置」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常
