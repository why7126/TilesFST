## MODIFIED Requirements

### Requirement: Banner 新增编辑弹窗

Web 客户端 MUST 提供 `BannerFormModal`，宽 **880px**（与瓷砖 SKU 弹窗 `.sku-modal-card` 一致，`max-width: 100%` 响应式保留）、最大高度 92vh、内容区可滚动（头尾固定）。弹窗外层卡片 MUST 使用专属类名 `banner-modal-card`，MUST NOT 在同一元素上同时挂载通用 `modal-card` 类以免被 `.admin-shell .modal-card { width: 520px }` 层叠覆盖；运行时 Computed width（视口 ≥ 880px）MUST 为 880px。弹窗 MUST 按 `jump_type` 展示条件字段：`SKU_DETAIL`（关联 SKU + 图库选图）、`EXTERNAL_LINK`（HTTPS 外链）、`TOPIC_PAGE`（关联专题）、`NO_JUMP`（无跳转目标）。弹窗 MUST NOT 展示状态编辑或状态策略说明块。Banner 图片模块 MUST NOT 展示冗余来源首行标题（如「自定义上传 / SKU 主图」）；自定义上传按钮 MUST 使用「选择/更换/上传中」文案并对齐 `BrandFormModal` 的 `hidden` file input 模式。关联 SKU 与关联专题 MUST 为单一可搜索选择控件（Combobox），MUST NOT 分离为独立搜索框与下拉框。运营备注 `textarea` MUST 占满整行且 placeholder 字号与同弹窗 input 一致。有效期 MUST 为单字段区间「{开始} 至 {结束}」，格式 `YYYY-MM-DD HH:mm`（分钟精度），MUST NOT 使用原生 `<input type="datetime-local">` 作为最终方案。视觉 MUST 对齐管理端大表单弹窗基准（宽度与 SKU 弹窗一致）；历史 `banner-management-modal-*.html`（640px）作为布局参考，宽度验收以本 requirement 为准。

#### Scenario: 公共字段

- **WHEN** 用户打开新增或编辑 Banner 弹窗
- **THEN** MUST 展示 Banner 标题、展示端、展示位置、Banner 图片、跳转类型、排序、有效期、运营备注
- **AND** 主按钮 MUST 为「保存 Banner」品牌金样式
- **AND** 弹窗主体超出视口时 MUST 可纵向滚动且 footer 操作按钮始终可达

#### Scenario: jump_type 切换

- **WHEN** 用户切换跳转类型
- **THEN** MUST 清空不兼容的跳转目标字段
- **AND** MUST 展示对应该类型的条件块

#### Scenario: SKU 详情变体

- **WHEN** `jump_type=SKU_DETAIL` 且用户选择 SKU
- **THEN** MUST 默认预览 SKU 主图（通过 SKU 详情或等效 API 获取 `image_object_key`）
- **AND** 点击「使用 SKU 主图」MUST 回填预览与 `image_object_key`；无主图 MUST 明确提示
- **AND** MUST 允许切换 SKU 图库其他图或自定义上传
- **AND** 关联 SKU MUST 为单一可搜索 Combobox

#### Scenario: 专题页变体

- **WHEN** `jump_type=TOPIC_PAGE`
- **THEN** 关联专题 MUST 为单一可搜索 Combobox
- **AND** 用户 MUST 在同一控件内搜索并选择专题

#### Scenario: 无跳转变体

- **WHEN** `jump_type=NO_JUMP`
- **THEN** MUST NOT 展示可编辑跳转目标
- **AND** MUST 展示禁用态「跳转目标：无需配置」

#### Scenario: 有效期区间

- **WHEN** 用户配置 Banner 有效期
- **THEN** MUST 通过 UI 选择日期与时分（分钟精度）
- **AND** 展示形态 MUST 为单字段「YYYY-MM-DD HH:mm 至 YYYY-MM-DD HH:mm」
- **AND** 提交 payload MUST 为合法 ISO datetime（结束秒 MAY 为 59）

#### Scenario: Dashboard 快捷打开新增

- **WHEN** 用户从 Dashboard 点击「新增 Banner」或访问 `/admin/banners?action=create`
- **THEN** MUST 打开新增 Banner 弹窗（导航后自动打开）

#### Scenario: 弹窗宽度与 SKU 对齐

- **WHEN** 视口宽度 ≥ 880px 且用户打开 Banner 或瓷砖 SKU 新增/编辑弹窗
- **THEN** Banner `.banner-modal-card` 与 SKU `.sku-modal-card` 外卡片宽度 MUST 均为 880px
- **AND** 窄视口下 `max-width: 100%` MUST 防止横向溢出屏幕

#### Scenario: 运行时 Computed 宽度与 CSS 层叠

- **WHEN** 全站 admin CSS bundle 已加载（含 `user-management.css`、`system-settings.css`、`banner-management.css`）且视口 ≥ 880px
- **THEN** Banner 弹窗 `.banner-modal-card` 的 Computed `width` MUST 为 880px
- **AND** MUST NOT 为 520px 或其他被 `.admin-shell .modal-card` 覆盖的值
- **AND** `BannerFormModal` 外层 MUST NOT 同时挂载 `modal-card` 与 `banner-modal-card`（除非组合选择器已保证 880px 且本场景仍 pass）

### Requirement: Banner 管理 PNG 视觉验收 Gate

Banner 管理视觉对齐 MUST 通过 PNG golden reference 与跨页弹窗一致性验收 gate。

#### Scenario: 列表 PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/banners` 与 `banner-management-list.png`
- **THEN** diff checklist（Shell、筛选四列、四指标卡、跳转类型列、分页、无弹窗遮罩）MUST 全部 pass
- **AND** 第一列仅标题 + 独立「展示位置」列 MUST pass（允许与 PNG 第一列叠放结构不一致，以 BUG-0039 acceptance 为准）

#### Scenario: 弹窗宽度并排验收

- **WHEN** 团队在视口 ≥ 880px 并排对比 Banner 弹窗与瓷砖 SKU 弹窗
- **THEN** 两弹窗宽度 MUST 视觉一致（880px）
- **AND** 四套 `jump_type` 条件字段显隐、无状态块、modal-body 可滚动 MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`（不以 640px modal PNG 为宽度 pass 条件）

#### Scenario: DevTools Computed 宽度验收

- **WHEN** 团队在 local dev 或 Docker 构建产物打开 Banner 新增/编辑弹窗（视口 ≥ 880px）
- **THEN** DevTools Computed `width` on `.banner-modal-card` MUST 为 880px
- **AND** Styles 面板 MUST 显示宽度生效规则来自 `.banner-modal-card`（或更高特异性），MUST NOT 仅由 `.admin-shell .modal-card { width: 520px }` 决定
- **AND** 验收结果 MUST 记录在 change `trace.md`
