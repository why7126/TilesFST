---
requirement_id: REQ-0062-admin-banner-placement-scope
title: 管理后台 Banner 投放范围配置优化 - 验收标准
status: done
created_at: 2026-07-20 18:40:54
updated_at: 2026-07-20 23:08:34
---

# REQ-0062 验收标准

## 功能 AC

- [ ] AC-001 Banner 管理列表筛选中的展示端只出现“小程序”或等价只读表达，不出现 Web 首页、专题页等旧展示端。
- [ ] AC-002 新增 Banner 弹窗打开时展示端默认为“小程序”，且用户不能保存为非小程序展示端。
- [ ] AC-003 编辑 Banner 弹窗仅能编辑新范围内 Banner，不存在编辑旧 Web 首页、专题页或旧运营位 Banner 的入口。
- [ ] AC-004 展示位置选项仅包含“首页轮播”和“品牌列表页轮播”。
- [ ] AC-005 新建 Banner 默认展示位置为“首页轮播”。
- [ ] AC-006 Banner 列表保留“展示位置”独立列，并以中文展示“首页轮播”或“品牌列表页轮播”。
- [ ] AC-007 服务端创建 Banner 时拒绝旧展示端，例如 `WEB_HOME`、`TOPIC` 或其他非小程序值。
- [ ] AC-008 服务端创建 Banner 时拒绝旧展示位置，例如 `HOME_TOP_CAROUSEL`、`HOME_MID_SLOT`、`TOPIC_TOP_BANNER` 或未知位置。
- [ ] AC-009 服务端更新 Banner 时同样执行展示端与展示位置合法组合校验。
- [ ] AC-010 旧数据删除后，Banner 列表、summary、分页总数均不包含已删除的旧 Web 首页、专题页和旧运营位 Banner。
- [ ] AC-011 旧数据删除逻辑输出或记录删除条件与删除数量，验收可复核。
- [ ] AC-012 旧数据删除只删除 Banner 业务记录，不因本需求自动物理删除 MinIO 媒体对象。
- [ ] AC-013 小程序首页接口只返回“首页轮播”位置中已上线且有效期内的 Banner。
- [ ] AC-014 小程序首页接口不得返回“品牌列表页轮播”位置 Banner。
- [ ] AC-015 品牌列表页接口或数据聚合只返回“品牌列表页轮播”位置中已上线且有效期内的 Banner。
- [ ] AC-016 品牌列表页无轮播数据时隐藏轮播或展示品牌化兜底，不使用首页轮播数据兜底。
- [ ] AC-017 首页轮播和品牌列表页轮播均按稳定排序展示，优先沿用 `sort_order ASC, updated_at DESC`。
- [ ] AC-018 小程序公开响应不暴露管理端备注、内部对象 key 或未授权字段。
- [ ] AC-019 `admin` 与 `employee` 可继续访问 Banner 管理；`store_owner` 仍不可访问页面和 API。
- [ ] AC-020 Banner 图片上传仍通过后端鉴权与 MinIO 适配层，不允许前端直连未授权对象存储。
- [ ] AC-021 Banner 跳转类型包含“品牌详情”，选择后展示“关联品牌”可搜索选择控件。
- [ ] AC-022 品牌详情 Banner 可使用品牌 Logo 作为 Banner 图；品牌无 Logo 时提示自定义上传。
- [ ] AC-023 小程序首页和品牌列表页轮播点击品牌详情 Banner 时进入 `pages/brand-detail/index?brandId=...`。

## API / DB / Orval AC

- [ ] AC-API-001 如请求体或响应体中的展示端、展示位置枚举变化，OpenAPI 必须同步。
- [ ] AC-API-002 Web 管理端 API 客户端类型必须通过 Orval 重新生成，或在实现记录中说明无需生成的证据。
- [ ] AC-API-003 API 文档必须说明当前仅支持小程序首页轮播和品牌列表页轮播。
- [ ] AC-DB-001 SQLite schema、MySQL schema 与 Pydantic 校验对展示端/展示位置的约束保持一致。
- [ ] AC-DB-002 数据库文档必须记录旧 Banner 数据删除策略和不物理删除媒体对象的边界。
- [ ] AC-DB-003 Banner 数据模型必须记录品牌详情跳转目标 `brand_id`，SQLite/MySQL schema 与 Pydantic Schema 保持一致。
- [ ] AC-TEST-001 后端测试覆盖非法旧展示端/旧展示位置被拒绝。
- [ ] AC-TEST-002 后端测试覆盖旧数据删除后列表统计不包含旧数据。
- [ ] AC-TEST-003 小程序测试覆盖首页轮播与品牌列表页轮播数据隔离。
- [ ] AC-TEST-004 前端测试覆盖展示端/展示位置选项收敛。
- [ ] AC-TEST-005 后端和前端测试覆盖 `BRAND_DETAIL`、`brand_id`、品牌 Logo 取图和小程序公开 `jump_type=brand` 映射。

## UI / UE AC

- [ ] AC-UI-001 Banner 管理页仍符合管理端暗色旗舰风和现有列表页密度，不因选项减少造成筛选区或表格错位。
- [ ] AC-UI-002 单一展示端的 UI 表达清晰，不让运营误以为仍可选择 Web 首页或专题页。
- [ ] AC-UI-003 展示位置文案固定为“首页轮播”和“品牌列表页轮播”，不得混用旧文案“首页顶部轮播”“小程序首页轮播”等造成歧义。
- [ ] AC-UI-004 错误提示使用用户可理解中文说明“当前仅支持小程序首页轮播和品牌列表页轮播”，不得只暴露内部枚举。
- [ ] AC-UI-005 颜色、边框、按钮、Badge 和激活态必须使用 Design System semantic token，不新增裸 Hex。
- [ ] AC-UI-006 “品牌详情”的表单布局和交互密度必须参照“SKU 详情”，不得拆成独立搜索框 + 下拉框。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防管理端列表、弹窗宽度和上传链路复发缺陷。

- [ ] AC-XCUT-001 Banner 管理列表分页 DOM 必须对齐用户管理基准，包含 `page-summary`、`page-right`、`page-buttons` 和 `page-size-wrap` 或等价共享分页组件。
- [ ] AC-XCUT-002 Banner 管理指标卡 DOM 必须使用 `.metric-label`、`.metric-value`、`.metric-desc` 结构或共享 `MetricCard`，不得只用裸 `strong/span` 承载。
- [ ] AC-XCUT-003 Banner 上线、下线、删除等状态/危险操作必须使用 DS confirm modal，不得使用 `window.confirm`。
- [ ] AC-XCUT-004 Banner 保存、删除、上线、下线成功或失败反馈必须使用 fixed toast 或等价固定反馈，不得在 hero 与表格之间插入造成 layout shift 的文档流 notice。
- [ ] AC-XCUT-005 Banner 弹窗 TSX 不得同时挂载通用 `modal-card` 与 `banner-modal-card` 等专属类。
- [ ] AC-XCUT-006 Banner 弹窗在 1440px 视口下 Computed width 必须符合当前 Banner/SKU 大弹窗基准；若本需求不调整弹窗宽度，也必须回归确认无 520px 层叠覆盖。
- [ ] AC-XCUT-007 矮视口下 Banner 弹窗 body 必须可滚动，footer 主操作按钮始终可达。
- [ ] AC-XCUT-008 Banner 图片上传必须呈现 `idle -> uploading -> done/failed` 状态机，失败信息显示在上传控件附近。
- [ ] AC-XCUT-009 Banner 图片上传成功后必须在同一会话即时回显缩略图或文件卡片，刷新列表/重开弹窗后 URL 仍可展示。
- [ ] AC-XCUT-010 Docker Web `:3000` 边界下必须验收 Banner 图片小文件上传成功、超限文件返回业务错误而非 Nginx 413。
