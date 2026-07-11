---
requirement_id: REQ-0020-theme-comfort-refine
title: Web / 管理端主题舒适度优化与主题切换
terminal: multi
version: v1
status: archived
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0000-build-design-system
created_at: 2026-07-11 17:13:53
updated_at: 2026-07-11 20:13:04
---

# REQ-0020 Web / 管理端主题舒适度优化与主题切换

## 1. 需求背景

当前 Web 与管理端 Design System 以“工业石材 · 暗色旗舰风”为默认视觉方向，深色背景和品牌金强调能够承载高端、克制、精密的品牌气质。但用户反馈当前主题色过深，管理端长时间使用后容易产生眼睛疲劳，说明现有默认暗色主题对高频、长时、表格和表单密集的后台操作场景不够友好。

现有 `rules/ui-design.md` 已声明默认暗色，并预留 `.light` 或 `[data-theme="light"]` 作为浅色主题通道；`src/web/src/styles/globals.css` 也已存在 light theme 变量。但父需求 `REQ-0000-build-design-system` 明确不包含浅色主题完整验收，因此当前浅色或舒适主题不能被视为已交付能力。

本需求在保留品牌展示页暗色旗舰风的前提下，为 Web 管理端新增主题切换能力，并补齐主题舒适度策略、Design System token 预览、关键页面验收与用户偏好持久化要求。经 `/req-complete` 确认，本期主题模式包含「系统默认」「暗色旗舰」「舒适暗色」「浅色」四类，偏好采用本地持久化与账号级持久化二者结合。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部管理员 | 长时间处理 SKU、品牌、类目、用户、日志等管理任务时减少视觉压迫和眼睛疲劳。 |
| 企业内部运营人员 | 可根据环境光、个人习惯和工作时长切换不同主题色，而不是被迫使用单一深色主题。 |
| 产品负责人 | 在保留 TILESFST / STONEX 品牌质感的同时提升后台可用性和舒适度。 |
| 前端开发人员 | 有明确主题 token、切换入口、持久化和页面适配规则，避免各页面局部改色。 |
| QA / 测试人员 | 可用固定页面矩阵验证登录页、列表页、表单页、弹窗和 `/design-system` 的主题表现。 |

## 3. 需求目标

- Web 管理端必须提供用户可感知的主题切换能力，允许用户在不同主题色之间切换。
- 管理端主题切换必须优先解决长时间操作的视觉舒适度问题。
- 品牌展示页允许继续保持“工业石材 · 暗色旗舰风”，不得因管理端舒适主题而削弱品牌首屏展示效果。
- 主题能力必须基于 Design System semantic token 和 CSS variables，不得在业务页面零散硬编码颜色。
- `/design-system` 必须补充主题 token、组件状态和关键页面样例的对比验收入口。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 管理端主题切换 | 为 Web 管理端提供主题切换入口，允许用户切换不同主题色。 |
| 主题模式策略 | 本期包含系统默认、暗色旗舰、舒适暗色、浅色四类主题模式。 |
| 用户偏好持久化 | 主题选择采用本地持久化与账号级服务端持久化二者结合。 |
| 登录页覆盖 | 登录页必须验证主题策略，至少保证入口、背景、表单、按钮和文字对比不造成视觉疲劳。 |
| 列表页覆盖 | 首批以瓷砖 SKU 列表页验证标题、指标卡、筛选区、表格、sticky 操作列和分页。 |
| 表单页覆盖 | 首批以瓷砖 SKU 表单/编辑场景验证输入框、选择器、帮助文案、错误提示和保存 CTA。 |
| 弹窗覆盖 | 首批以瓷砖 SKU 新建/编辑弹窗验证遮罩、弹窗卡片、标题、表单、危险操作、确认按钮和反馈文案。 |
| `/design-system` 覆盖 | 设计验收页必须展示主题 token、基础组件、管理端代表组件和主题切换状态。 |
| Design System 文档与 token 约束 | 更新主题使用规则、token 边界和禁止裸 Hex 的验收口径。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 店主品牌展示页强制改浅色 | 店主端品牌展示页、首页 Hero 和品牌氛围区域允许继续保持暗色旗舰风；除品牌展示页外的店主 Web 页面需要支持舒适主题。 |
| 小程序主题切换实现 | 微信小程序主题策略待确认，本期仅记录影响范围，不作为实现必选项。 |
| 重做所有业务页面视觉 | 本需求定义横切主题能力和代表页面验收，不要求一次性重绘所有页面。 |
| 新增后端业务模块 | 主题切换本身不新增瓷砖、品牌、用户等后端业务能力。 |
| 数据库表结构变更 | 默认不修改 SQLite / MySQL 表结构；如后续决定服务端保存用户偏好，必须在 Change 中单独论证。 |
| Orval 接口生成 | 默认不涉及 OpenAPI / Orval；如新增用户偏好 API，后续 Change 必须同步 Orval。 |
| Docker / 部署策略调整 | 不改变 Docker Compose、Nginx、环境变量或部署拓扑。 |

## 5. 信息架构

```text
Design System Theme
├── theme modes
│   ├── system（跟随系统或产品默认）
│   ├── dark flagship（默认品牌暗色）
│   ├── comfort dark（长时间操作舒适暗色）
│   └── light（浅色主题，可复用现有预留通道并补齐验收）
├── Web Admin
│   ├── login page
│   ├── admin shell
│   ├── list pages
│   ├── form pages
│   └── modals / toast / confirm dialog
├── Web Catalog
│   ├── brand / hero pages（可保持暗色旗舰风）
│   └── catalog / list / detail pages（除品牌展示页外支持舒适主题）
└── /design-system
    ├── theme switcher
    ├── token comparison
    ├── component states
    └── admin representative samples
```

## 6. 功能要求

### FR-001 管理端主题切换入口

- MUST 在 Web 管理端提供清晰的主题切换入口，位置应符合管理端信息架构，例如用户菜单、设置页、顶部工具区或等价稳定入口。
- MUST 允许用户在不同主题色之间切换，至少覆盖当前暗色旗舰主题和一种更适合长时间使用的舒适主题。
- MUST 保持主题切换即时生效，用户无需刷新页面即可看到主要界面变化。
- MUST 在主题切换时保持当前页面、表单输入、筛选条件、分页状态和弹窗状态不发生无意丢失。
- MUST 支持四类主题模式：系统默认、暗色旗舰、舒适暗色、浅色。
- MUST 让用户能够识别当前主题模式，并能在四类模式之间切换。

### FR-002 用户主题偏好

- MUST 记住用户已选择的主题，并在用户再次进入管理端时恢复。
- MUST 使用本地持久化与账号级服务端偏好二者结合：本地偏好用于首屏快速恢复，账号级偏好用于跨设备和重新登录后恢复。
- MUST 在未获取到用户偏好时使用产品默认主题，不得出现无主题样式闪烁或不可读状态。
- SHOULD 在隐私和安全边界内保存偏好，不得把主题偏好与认证 token、密码或敏感业务数据混写。
- MUST 在退出登录或切换账号时避免错误沿用另一个用户的账号级主题偏好。

### FR-003 Design System Token 与主题模式

- MUST 基于 semantic token、CSS variables 和现有 Tailwind 语义 class 实现主题能力。
- MUST 保持 `bg-page`、`bg-surface`、`text-primary`、`text-secondary`、`border-border-default`、`text-brand-gold` 等语义 class 在不同主题下可用。
- MUST 明确当前 `dark`、预留 `light` 与新增舒适主题之间的设计语义，避免把 placeholder light theme 当作已验收生产能力直接启用。
- MUST 更新 `rules/ui-design.md` 或后续 Design System 文档，说明默认主题、舒适主题、品牌展示场景和主题切换策略。
- MUST NOT 在业务 TSX/CSS 中新增裸 Hex 或 token 对应的硬编码 `rgba(...)` 作为主题差异实现。

### FR-004 管理端登录页主题覆盖

- MUST 覆盖 Web 管理端登录页主题表现，保证背景、材质拼贴、表单容器、输入框、主按钮、错误提示和语言切换在主题切换或默认主题下可读、稳定、舒适。
- MUST 保留登录页品牌识别和专业感，不得把登录页改成与品牌无关的通用浅色模板。
- MUST 避免登录页在移动端或桌面端出现背景过亮、对比不足、表单边界不清或文本疲劳问题。
- SHOULD 明确登录页是否允许用户登录前切换主题；若允许，主题偏好应在登录后延续。

### FR-005 管理端列表页主题覆盖

- MUST 覆盖管理端列表页主题表现，包括标题区、指标卡、筛选 / 搜索区、表格、sticky 操作列、分页、loading、empty 和 error 状态。
- MUST 确保舒适主题下表格行、分割线、hover 态、禁用态和操作列仍具备足够可读性。
- MUST 避免大面积纯黑、过高对比文字、刺眼品牌金或过低对比分割线导致长时间阅读疲劳。
- MUST 选择瓷砖 SKU 管理页作为首批列表页验收样例，覆盖指标卡、筛选区、表格、sticky 操作列和分页。

### FR-006 管理端表单页主题覆盖

- MUST 覆盖管理端表单页主题表现，包括输入框、选择器、复选框、只读字段、帮助文案、错误提示、保存 CTA 和取消 / 重置操作。
- MUST 保证舒适主题下表单边界、focus ring、错误色和必填标记清晰但不过度刺激。
- MUST 保持表单 dirty 提示、成功 toast 和错误反馈的既有交互语义。
- MUST 选择瓷砖 SKU 编辑/表单场景作为首批表单页验收样例。

### FR-007 管理端弹窗主题覆盖

- MUST 覆盖管理端弹窗主题表现，包括普通编辑弹窗、确认弹窗、危险操作弹窗、上传反馈和重置密码等代表场景。
- MUST 保证遮罩、弹窗卡片、边框、阴影、标题、正文、按钮和错误区域在舒适主题下层级清楚。
- MUST 保持 Design System modal pattern，不得回退到 `window.confirm`、`window.alert` 或孤立浏览器默认控件。
- MUST 选择瓷砖 SKU 新建/编辑弹窗作为首批弹窗验收样例，并覆盖媒体上传状态 UI 的主题表现。

### FR-008 `/design-system` 主题验收

- MUST 在 `/design-system` 或等效设计验收页提供主题切换或主题对比入口。
- MUST 展示不同主题下的核心 token 样本、Button、Input、Checkbox、Badge、Card、Modal、Table、Pagination 和 Toast 等状态。
- MUST 展示登录页、列表页、表单页、弹窗的代表性主题验收样例或链接。
- MUST 明确当前主题模式的名称、用途和推荐使用场景，帮助开发和 QA 判断页面是否应用正确主题。
- SHOULD 支持截图或视觉对比材料，便于后续评审确认舒适度改进。

### FR-009 店主展示端边界

- MUST 允许店主 Web 品牌展示页继续保持暗色旗舰风，尤其是 Hero、品牌叙事、材质展示和高端氛围区域。
- MUST 不因管理端舒适主题而强制改变店主端所有页面默认视觉。
- MUST 支持店主 Web 除品牌展示页外的页面使用舒适主题，包括商品列表、筛选、详情阅读和询价路径。
- SHOULD 明确店主 Web 是否暴露用户可见主题切换入口，或由管理端 / 全站偏好驱动。

## 7. UI 约束

- MUST 继续遵守 `rules/ui-design.md` 和 Design System semantic token 规则。
- MUST 保持管理端工作台风格：信息密度适中、层级清楚、适合高频扫描和反复操作。
- MUST 避免仅把背景整体调亮但不调整文字、边框、hover、focus、阴影和状态色的半成品主题。
- MUST 避免一套主题内出现过多相近色造成层级不清，也避免品牌金在大面积背景中产生视觉刺激。
- MUST 保证所有主题下文本、按钮、表单、表格和弹窗内容不重叠、不溢出、不被背景吞没。
- SHOULD 在 1366px、1440px、1920px 桌面宽度和移动登录页宽度下验证关键页面。
- SHOULD 考虑 `prefers-color-scheme`，但不得用系统偏好替代用户在管理端显式选择的主题。

## 8. 权限与安全

- MUST 不改变管理端与店主端的认证、授权和路由边界。
- MUST 不因主题偏好持久化暴露用户 token、Cookie、密码、MinIO 凭据、对象 key 或真实客户数据。
- MUST 不通过前端主题参数绕过服务端权限、功能开关或数据访问控制。
- SHOULD 将主题偏好视为低敏设置，但若采用服务端保存，仍必须经过认证用户上下文读写。

## 9. 关联需求与规范

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0000-build-design-system` | Design System 父需求；当前需求补齐主题舒适度和主题切换能力。 |
| 相关规范 | `rules/ui-design.md` | 当前默认暗色旗舰风、semantic token 和浅色预留规则来源。 |
| 相关规范 | `openspec/specs/design-system/spec.md` | Design System 正式能力事实源，后续 Change 需扩展主题要求。 |
| 相关页面 | `src/web/src/styles/globals.css` | Web 颜色变量权威定义，现有 dark / light 主题变量位置。 |
| 相关 token | `src/shared/design-system/tokens/colors.ts` | TS 颜色 token 与主题模式定义位置。 |
| 相关入口 | `src/web/src/pages/dev/DesignSystemPage.tsx` | `/design-system` 设计验收页入口。 |
| 相关页面 | Web 管理端登录页 | 舒适度验收必须覆盖。 |
| 相关页面 | Web 管理端列表页 | 舒适度验收必须覆盖。 |
| 相关页面 | Web 管理端表单页 | 舒适度验收必须覆盖。 |
| 相关组件 | Web 管理端弹窗 / Toast / Confirm Modal | 舒适度验收必须覆盖。 |

## 10. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 品牌感被削弱 | 若全站直接改浅色，店主展示端品牌氛围可能下降。 | 管理端优先新增主题切换，店主品牌展示页允许保留暗色旗舰风。 |
| 主题半成品 | 只替换背景色会导致文字、边框、状态色和弹窗层级不协调。 | 以 semantic token 为单位完整设计，并用页面矩阵验收。 |
| 既有页面样式分散 | 管理端 CSS Port 和业务页面样式较多，主题变量可能覆盖不完整。 | 先选登录页、列表页、表单页、弹窗和 `/design-system` 代表面验收，再逐步扩展。 |
| 浅色 token 未验收 | 仓库已有 light theme 变量但仍是 future / placeholder 语义。 | 后续 Change 必须将 light 或 comfort 主题正式纳入验收，不能直接默认启用。 |
| 偏好持久化边界不清 | 本地与账号级偏好体验不同，涉及退出登录和多账号切换。 | 在设计阶段明确持久化策略，必要时拆分 API / DB 影响。 |

## 11. 状态

```yaml
status: archived
lifecycle_stage: plan
next: /req-opsx REQ-0020-theme-comfort-refine
readiness: Ready
needs_prototype: true
needs_api_change: true
needs_database_change: true
needs_orval: true
needs_docker_validation: false
```

## 12. 待完善项

- `/req-review` 阶段确认是否批准进入 `/req-opsx`。
- `/req-opsx` 阶段需要将主题偏好 API、账号级持久化、DB 字段、OpenAPI / Orval 与测试纳入设计。
- 实现阶段需要导出或补充 PNG / 截图作为视觉验收材料。
