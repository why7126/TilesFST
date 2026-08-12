## 1. 后端 Banner 列表响应

- [x] 1.1 扩展 `BannerRecord` / `BannerAdminItem`，新增只读 `jump_target_label` 字段。
- [x] 1.2 调整 Banner 列表查询，批量带出品牌名称、SKU 名称、专题名称或外部链接，避免前端按行请求。
- [x] 1.3 定义关联对象不存在、不可用或名称为空时的兜底值，列表不得空白或报错。
- [x] 1.4 保持创建/更新请求体、错误码、数据库 schema 和跳转校验规则不变。

## 2. OpenAPI / Orval / 文档

- [x] 2.1 更新 Pydantic Schema 并导出 OpenAPI。
- [x] 2.2 运行 Orval，更新 Web generated 类型。
- [x] 2.3 更新接口索引或相关 API 文档中 Banner 列表响应字段说明。
- [x] 2.4 确认不需要数据库 migration、MinIO、Docker 或 Nginx 变更。

## 3. Web 管理端列表 UI

- [x] 3.1 调整 `/admin/banners` 表头和行渲染，新增独立“跳转对象”列。
- [x] 3.2 Banner 列仅渲染主图/缩略图和 fallback，不再展示标题、内部识别或其他文字。
- [x] 3.3 保留展示位置、展示端、跳转类型、状态、有效期、排序、更新时间和操作列。
- [x] 3.4 跳转对象长文本单行截断，外部链接不得撑宽表格，操作列保持可见可点击。
- [x] 3.5 搜索 placeholder 与可见字段保持一致；如纳入跳转对象搜索，后端和测试同步覆盖。

## 4. 横切一致性与 UI 证据

- [x] 4.1 保持分页 DOM：`page-summary`、`page-right`、`page-buttons`、`page-size-wrap`。
- [x] 4.2 保持指标卡 DOM：`.metric-label`、`.metric-value`、`.metric-desc`。
- [x] 4.3 保持 fixed toast 与 DS confirm modal；不得使用文档流 notice 或 `window.confirm`。
- [x] 4.4 记录 1440px 桌面视口截图或等价视觉证据，确认新增列后表格密度、截断和操作列不回归。

## 5. 测试与校验

- [x] 5.1 补充后端 pytest：品牌、SKU、专题、外链、无跳转、对象缺失兜底。
- [x] 5.2 补充 Web Vitest：Banner 列只显示图片、跳转对象列、既有列保留、分页/confirm/toast 不回退。
- [x] 5.3 运行相关后端测试、Web 测试、OpenAPI/Orval 生成校验。
- [x] 5.4 运行 `python scripts/validate-openspec-language.py` 与 OpenSpec 校验。

## 验收返修记录

- [x] 2026-08-11 22:56:03 返修 Banner 管理列表换行规则：除有效期列保留起止时间换行外，所有表头字段和其他列表字段均单行展示；补充 Web Vitest CSS/DOM 契约。
