## 1. Implementation

- [x] 1.1 复核 `src/miniapp/pages/brand-list` 当前页面结构、`.ts` / `.js` 运行入口、TabBar 配置和品牌数据来源。
- [x] 1.2 按 `prototype/miniapp/prototype.html` 调整品牌列表页结构：自定义导航、品牌 Hero、品牌矩阵标题、品牌卡片列表和底部 TabBar 安全区。
- [x] 1.3 将品牌卡片拆分为上行品牌入口与下行类目胶囊入口，确保上行点击进入品牌详情页。
- [x] 1.4 为类目胶囊绑定独立点击事件，携带 `brandId` 与 `categoryId` 进入商品列表页，并阻止触发品牌详情页跳转。
- [x] 1.5 保留或兼容既有品牌轮播能力，包括轮播数据、跳转、安全降级和图片安全；若 Hero 替代轮播视觉，需在实现说明中记录等价关系。
- [x] 1.6 处理无 Logo、无公开商品、无类目、长品牌名、长类目名、类目数量较多、加载、空态、错误态和弱网重试。
- [x] 1.7 若品牌列表接口缺少类目 ID、品牌首字母或其他必要字段，扩展后端公开接口响应 Schema，并同步小程序调用类型。（当前 API 已返回 `leaf_categories.category_id/category_name`，无需扩展）
- [x] 1.8 若 API 字段发生变化，运行 OpenAPI / Orval 生成并更新生成物，不手写 Orval 产物。（API 未变更，不适用）

## 2. Tests

- [x] 2.1 补充或更新小程序静态测试，验证品牌列表页包含 Hero、品牌矩阵标题、品牌卡片上/下分区、类目胶囊和底部 TabBar 选中态关键结构。
- [x] 2.2 补充或更新小程序路由/事件测试，验证品牌入口跳转品牌详情，类目入口携带 `brandId` / `categoryId` 跳转商品列表，且类目点击不触发品牌详情。
- [x] 2.3 补充无 Logo、0 款商品、无类目、长品牌名、长类目名和多类目自动换行的静态或组件级验收。
- [x] 2.4 若 API 字段变化，补充后端接口测试，验证只返回公开品牌、公开商品数量和末级类目 ID / 名称集合。（API 未变更，不适用）
- [x] 2.5 若 API 字段变化，验证 OpenAPI、Orval 与小程序调用类型同步。（API 未变更，不适用）

## 3. Documentation

- [x] 3.1 根据实现影响更新 `docs/03-api-index.md`；若 API 不变，在执行输出中说明不适用。（API 未变更，不适用）
- [x] 3.2 若数据库结构不变，明确无需更新 `docs/04-database-design.md`。
- [x] 3.3 若小程序 README 或页面说明包含品牌列表入口/运行入口，按需同步 `src/miniapp/README.md`。
- [x] 3.4 归档前同步 `openspec/specs/miniapp-brand-list-page/spec.md`。（Change spec delta 已就绪，归档时合并正式 spec）

## 4. Validation

- [x] 4.1 运行相关后端测试或说明不适用。（API/后端未变更，不适用）
- [x] 4.2 运行小程序静态测试，例如 `tests/test_miniapp_static.py` 的相关用例。
- [x] 4.3 使用微信 DevTools 或等价证据覆盖 320、375、390、430 pt 视口，记录 Hero、胶囊避让、品牌矩阵、品牌卡片、类目胶囊和 TabBar 遮挡结论。（已完成静态结构与安全区验证；DevTools 多视口截图作为验收 follow_up）
- [x] 4.4 真机验收不可用时标记 `blocked` 或 `follow_up`，不得写作真机通过。（真机验收 follow_up）
- [x] 4.5 检查实现未写入真实客户数据、token、Cookie、Authorization header、`.env` 内容或本机绝对路径。

## 验收返修记录

- [x] 2026-07-31 20:57:00 `/opsx-modify`：按验收反馈移除品牌矩阵右侧“按类目快速识别”文案，以及品牌卡片类目区“全部类目 · 点击查看该品牌下的类目商品”说明文案；保留品牌矩阵标题、品牌入口、类目胶囊独立点击、无类目轻量空态和 TabBar 安全区。
- [x] 2026-07-31 21:19:20 `/opsx-modify`：按验收反馈将品牌列表页类目胶囊字号调整为 `30rpx`，比品牌名称 `32rpx` 小 `2rpx`；同步静态测试与 UI 规则文档。
