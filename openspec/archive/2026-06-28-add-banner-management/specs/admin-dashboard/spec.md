## MODIFIED Requirements

### Requirement: 管理端 Sidebar 品牌与导航

管理端 Sidebar MUST 展示品牌名 **TILESFST**（全大写），MUST NOT 出现 STONEX。品牌名右侧 MUST 紧邻展示产品版本 pill（如 `v0.0.1`），版本值 MUST 来自跨端单一常量 `PRODUCT_VERSION`（`src/shared/`），MUST NOT 来自 `package.json`、FastAPI OpenAPI version 或构建/Git 信息。版本 pill MUST 为小号圆角 badge，使用 semantic token，MUST NOT 使用裸 Hex。导航 MUST 包含 OPERATIONS 分组（首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理）与 SYSTEM 分组（用户管理、系统设置）。当前路由为首页时，「首页」项 MUST 为 active 态；当前路由为 `/admin/tile-skus` 时，「瓷砖SKU」项 MUST 为 active 态；当前路由为 `/admin/brands` 时，「瓷砖品牌」项 MUST 为 active 态；当前路由为 `/admin/banners` 时，「Banner 管理」项 MUST 为 active 态。「瓷砖SKU」MUST 导航至 `/admin/tile-skus`；「瓷砖品牌」MUST 导航至 `/admin/brands`；「Banner 管理」MUST 导航至 `/admin/banners`，MUST NOT 仅展示占位 toast。

#### Scenario: 品牌与分组展示

- **WHEN** 用户查看管理端 Sidebar
- **THEN** 顶部 MUST 展示 **TILESFST** Logo 文案
- **AND** TILESFST 右侧同一行 MUST 展示产品版本 pill，文案 MUST 等于 `PRODUCT_VERSION`
- **AND** MUST 展示 OPERATIONS 与 SYSTEM 两个分组及各自导航项
- **AND** MUST NOT 展示 STONEX 或旧品牌名

#### Scenario: Banner 管理导航 active 态

- **WHEN** 用户位于 `/admin/banners`
- **THEN** 「Banner 管理」导航项 MUST 为 active 样式
- **AND** 「首页」与其他项 MUST 为非 active 样式

#### Scenario: Banner 管理可导航

- **WHEN** 用户点击 Sidebar「Banner 管理」
- **THEN** 系统 MUST 导航至 `/admin/banners`
- **AND** MUST NOT 仅展示「功能建设中」占位 toast

#### Scenario: 其他未实现导航占位

- **WHEN** 用户点击除「首页」「瓷砖SKU」「瓷砖品牌」「Banner 管理」「用户管理」（若 admin）外尚无实现的 Sidebar 项
- **THEN** 系统 MUST 展示占位反馈（如 toast「功能建设中」或占位页）
- **AND** MUST NOT 导致白屏或未捕获异常

### Requirement: 管理端 Dashboard 快捷操作

`/admin/dashboard` MUST 展示「快捷操作」区块，采用四列宫格，且 MUST 仅包含：新增 SKU、新增品牌、新增类目、新增 Banner。MUST NOT 包含：导入 SKU、导入图片、价格管理、操作日志。「新增 SKU」MUST 导航至 `/admin/tile-skus`（MAY 通过 query 打开新增弹窗），MUST NOT 仅展示占位 toast。「新增品牌」MUST 导航至 `/admin/brands`（MAY 通过 query 打开新增弹窗），MUST NOT 仅展示占位 toast。「新增 Banner」MUST 导航至 `/admin/banners`（MAY 通过 `?action=create` 打开新增弹窗），MUST NOT 仅展示占位 toast。

#### Scenario: 快捷操作四项

- **WHEN** 用户查看快捷操作区块
- **THEN** MUST 展示且仅展示 4 个快捷操作卡片
- **AND** 标题 MUST 分别为「新增 SKU」「新增品牌」「新增类目」「新增 Banner」

#### Scenario: 新增 Banner 快捷操作

- **WHEN** 用户点击「新增 Banner」快捷操作
- **THEN** 系统 MUST 导航至 `/admin/banners`
- **AND** MAY 通过 query 自动打开新增 Banner 弹窗
- **AND** MUST NOT 仅展示占位 toast

#### Scenario: 新增类目快捷操作占位

- **WHEN** 用户点击「新增类目」
- **THEN** 系统 MUST 展示占位反馈或导航至类目页（若已实现）
- **AND** MUST NOT 抛出未捕获错误

#### Scenario: 已删除快捷操作不得出现

- **WHEN** 用户查看 `/admin/dashboard` 全文
- **THEN** MUST NOT 出现「导入 SKU」「导入图片」「价格管理」「操作日志」入口
