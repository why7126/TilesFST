## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0002-brand-ui-inconsistency` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 对比 `BrandManagementPage.tsx` 与 `UserManagementPage.tsx` 的分页 DOM
- [x] 1.3 对比 `BrandFormModal.tsx` 与 `UserFormModal.tsx` 的文件选择控件
- [x] 1.4 确认不涉及 API、数据库、Orval、MinIO 策略变更

## 2. 分页 UI 修复

- [x] 2.1 将品牌列表分页结构对齐用户管理页的 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- [x] 2.2 统一分页高度、内边距、边框、圆角、按钮尺寸、激活态和文字层级
- [x] 2.3 处理跳页能力：移除或作为统一分页布局的可选扩展，不破坏主视觉结构
- [x] 2.4 保持上一页、下一页、当前页、每页显示切换功能不回退

## 3. Logo 选择文件控件修复

- [x] 3.1 将品牌 Logo 上传区域调整为与用户头像上传一致的紧凑表单控件
- [x] 3.2 保留 Logo 空态、预览态、帮助文案、选择/更换入口
- [x] 3.3 隐藏原生 file input，不展示浏览器默认文件控件皮相
- [x] 3.4 保持 `uploadBrandLogo`、`logo_object_key` 写入和保存品牌功能不回退

## 4. 测试

- [x] 4.1 更新或新增品牌管理页测试，覆盖分页一致性关键 DOM
- [x] 4.2 更新或新增品牌弹窗测试，覆盖 Logo 文件选择入口与上传回调
- [x] 4.3 运行 `cd src/web && npx vitest run src/pages/admin src/features/admin`
- [x] 4.4 运行 `cd src/web && npm run build`

## 5. 视觉验收与追溯

- [x] 5.1 并排检查 `/admin/brands` 与 `/admin/users` 分页，记录验收结果
- [x] 5.2 并排检查新增品牌弹窗与用户管理弹窗图片上传控件，记录验收结果
- [x] 5.3 更新本 change `trace.md` 的 checklist
- [x] 5.4 更新 `BUG-0002-brand-ui-inconsistency/trace.md` 中 change 状态
- [x] 5.5 若修复过程发现可复用事故知识，再评估是否更新 `docs/knowledge-base/incidents/`
