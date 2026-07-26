## 1. 准备与定位

- [x] 1.1 阅读 BUG-0030～0036 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `BannerManagementPage.tsx`、`BannerFormModal.tsx`、`UserManagementPage.tsx`、`BrandFormModal.tsx`
- [x] 1.3 确认 BUG-0035 默认走 SKU 详情 fetch（无 API 变更）；BUG-0036 分钟精度区间

## 2. 前端修复（BUG-0030 — 列表 UI）

- [x] 2.1 删除 `section-head`（「Banner 列表」+「共 N 个 Banner」）
- [x] 2.2 删除 `table-toolbar` / `table-count`；删除规则保留 disabled 按钮 `title`
- [x] 2.3 分页替换为 `pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- [x] 2.4 删除 `banner-pagination` / `banner-page-left` JSX 与 CSS
- [x] 2.5 验证翻页、pageSize 10/20/50、筛选后 total

## 3. 前端修复（BUG-0031/0032 — 图片模块 UI）

- [x] 3.1 移除 `banner-upload-title` 首行文案（0031）
- [x] 3.2 上传按钮：未选图「选择」、有图「更换」、上传中「上传中」+ disabled（0032）
- [x] 3.3 `<input type="file" hidden>` 对齐 `BrandFormModal`；onChange 后 `input.value = ''`
- [x] 3.4 勾选 BUG-0031 AC-001～002、BUG-0032 AC-001～007

## 4. 前端修复（BUG-0033 — 弹窗布局）

- [x] 4.1 `banner-modal-card` flex 列布局；`.modal-body { overflow-y:auto; flex:1 }`
- [x] 4.2 运营备注 `textarea`：`width:100%`、高度 ~72px、`resize:none`、placeholder 12px semantic token
- [x] 4.3 小视口验证 footer「取消/保存 Banner」始终可见可点
- [x] 4.4 勾选 BUG-0033 AC-001～006

## 5. 前端修复（BUG-0034 — 可搜索 Combobox）

- [x] 5.1 实现或引入 `SearchableSelect`（`shared/ui/`）
- [x] 5.2 SKU 详情：单一控件 debounce 搜索 + 选择；编辑态回显
- [x] 5.3 专题页：单一控件 debounce 搜索 + 选择；编辑态回显
- [x] 5.4 删除独立 search input + select 双控件
- [x] 5.5 勾选 BUG-0034 AC-001～008

## 6. 前端修复（BUG-0035 — SKU 主图）

- [x] 6.1 选择 SKU / 「使用 SKU 主图」：调用 `fetchTileSku(id)` 取主图 `object_key`
- [x] 6.2 无主图 inline 错误；编辑模式切换回 SKU 主图可用
- [x] 6.3 保存 SKU 详情 Banner 成功（`image_source=sku_main_image`）
- [x] 6.4 Vitest：mock 列表 `images:[]` + 详情含主图 → 断言 `imageKey` 设置
- [x] 6.5 勾选 BUG-0035 AC-001～008

## 7. 前端修复（BUG-0036 — 有效期 DateTime）

- [x] 7.1 移除双 `datetime-local`；改为单字段「有效期」区间 UI
- [x] 7.2 格式 `YYYY-MM-DD HH:mm 至 YYYY-MM-DD HH:mm`；可选开始/结束
- [x] 7.3 提交 ISO：`valid_from` 秒 00、`valid_to` 秒 59；空值长期有效
- [x] 7.4 编辑回填正确；列表 `formatBannerDateTime` 无回归
- [x] 7.5 勾选 BUG-0036 AC-001～010

## 8. 测试

- [x] 8.1 SHOULD：`BannerManagementPage.test.tsx` — 无 section-head / banner-pagination
- [x] 8.2 SHOULD：`BannerFormModal.test.tsx` — 按钮文案、Combobox 单控件、SKU 主图
- [x] 8.3 运行 `cd src/web && pnpm vitest run Banner && pnpm build`
- [x] 8.4 Docker 冒烟：`./scripts/smoke-banner-docker.sh`（若可用）

## 9. 验收与追溯

- [x] 9.1 并排 BUG-0030：Banner 列表 vs 用户管理分页（1440×1024）
- [x] 9.2 四套 modal jump_type 手工冒烟
- [x] 9.3 勾选 BUG-0030～0036 各 acceptance
- [x] 9.4 填写本 change `trace.md`；更新 BUG trace `openspec_changes`
- [x] 9.5 评估 `docs/knowledge-base/incidents/`（通常不需要）

## 10. 归档准备

- [x] 10.1 全部 `[x]` 后 `/opsx-archive fix-banner-admin-ui`
- [x] 10.2 与 `add-banner-management` archive 顺序协调（可先 archive add-* 或并行）
