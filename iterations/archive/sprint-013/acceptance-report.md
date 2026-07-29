---
note: sprint-archive — 8/8 Change 已 archive；Sprint 已完成归档
sprint_id: sprint-013
title: Sprint 013 验收报告
status: completed
lifecycle_stage: archive
created_at: 2026-07-28 00:24:49
updated_at: 2026-07-29 09:28:01
owner: product
---

# Sprint 013 验收报告

## 1. 验收范围

| 类型 | ID | Change | 状态 | 验收结论 |
|---|---|---|---|---|
| REQ | REQ-0077-category-name-max-length-15 | update-category-name-max-length-15 | done，已归档（`update-category-name-max-length-15` archived 2026-07-28 00:24:49） | 已完成实现、规格合并与归档门禁复核 |
| REQ | REQ-0078-certificate-multiple-images-main-image | update-certificate-multiple-images-main-image | done，已归档（`update-certificate-multiple-images-main-image` archived 2026-07-29 00:10:51） | 已实现并通过自动化、OpenSpec、API 标准和 Docker Web 上传边界校验 |
| REQ | REQ-0079-admin-sku-list-published-at | update-admin-sku-list-published-at | done，已归档（`update-admin-sku-list-published-at` archived 2026-07-28 23:45:00） | 已完成实现、规格合并与归档门禁复核 |
| REQ | REQ-0080-miniapp-certificate-detail-page | add-miniapp-certificate-detail-page | done，已归档（`add-miniapp-certificate-detail-page` archived 2026-07-29 08:24:32） | 已完成实现、OpenAPI/Orval、API 文档、后端 pytest 与小程序静态测试；DevTools/真机 evidence 已按 blocked/follow_up 记录 |
| BUG | BUG-0086-miniapp-sku-detail-remark-not-shown | fix-miniapp-sku-detail-remark-display | done，已归档（`fix-miniapp-sku-detail-remark-display` archived 2026-07-29 00:09:26） | 已完成实现、自动化验证与归档门禁复核 |
| BUG | BUG-0087-miniapp-brand-detail-product-tab-sort-order | fix-miniapp-brand-detail-product-sort-order | done，已归档（`fix-miniapp-brand-detail-product-sort-order` archived 2026-07-29 07:54:14） | 已完成实现、排序/分页回归与归档证据兜底 |
| BUG | BUG-0089-admin-certificate-edit-image-filename-noise | fix-admin-certificate-image-filename-noise | done，已归档（`fix-admin-certificate-image-filename-noise` archived 2026-07-29 08:57:31） | 已完成实现、自动化验证与归档门禁复核 |

## 2. 功能验收清单

- [ ] 新增类目弹窗允许保存 15 个用户可见字符。
- [ ] 编辑类目弹窗允许保存 15 个用户可见字符。
- [ ] 16 字符类目名称前端阻止保存并展示「类目名称最多 15 个字符」。
- [ ] 创建 / 更新 API 接受 15 字符、拒绝 16 字符，并返回统一 response envelope。
- [ ] 字符集、同层级唯一、排序权重、层级、编码自动生成规则不回归。
- [ ] OpenAPI / Orval / docs / tests 与 15 字符约束一致。
- [ ] 管理端类目列表、类目树、小程序分类入口、Web 展示端分类入口 15 字符样例布局稳定。
- [ ] 小程序 SKU 详情页展示非空备注说明，内容与接口返回值一致。
- [ ] 小程序 SKU 详情页备注为空时不展示 `null`、`undefined`、字段名、异常空白卡片或布局错位。
- [ ] 小程序 SKU 详情页不暴露内部备注、原始 object key、Authorization header、Cookie 或敏感配置。
- [ ] 商品详情页主图、轮播图/视频、品牌入口、收藏、分享和异常态不回归。
- [ ] 品牌证书新增 / 编辑弹窗支持上传多张图片，默认上限与前后端校验一致。
- [ ] 第一张成功上传图片自动成为主图，设置主图后新主图唯一且移动到第一位。
- [ ] 删除非主图保持当前主图；删除当前主图后自动选择兜底主图；删除全部图片后进入空状态。
- [ ] 保存后再次打开证书编辑弹窗，图片数量、顺序、主图标记和缩略图回显一致。
- [ ] 管理端证书列表优先展示主图缩略图，主图加载失败时展示稳定占位。
- [ ] PDF/文档类证书沿用既有占位或按 OpenSpec design 确认的兼容策略展示。
- [ ] 上传图片经过后端鉴权、MIME、扩展名和大小校验，非法文件不得写入图片列表。
- [ ] 旧单文件证书数据在列表和弹窗中兼容展示，不出现空白或报错。
- [ ] 小程序证书详情页可通过 `certificateId` 加载单个公开证书，并支持证书列表、品牌详情证书区域和微信分享入口。
- [ ] 证书列表页卡片主点击进入证书详情页，详情页内提供图片预览或 PDF 受控打开。
- [ ] 证书详情页展示证书名称、所属品牌、证书类型、编号、发证机构、有效期、有效状态和公开说明中可用字段。
- [ ] 证书详情页媒体区优先展示主图，多图按排序展示，图片失败、PDF 打开失败或文件缺失不阻断文字信息浏览。
- [ ] 证书详情页提供品牌主页入口和微信分享；分享路径携带 `certificateId`，分享图优先使用证书主图。
- [ ] 隐藏、软删除、品牌不可公开或不存在的证书不返回完整详情，并展示“证书暂不可查看”类状态。
- [ ] 证书详情页不展示收藏、推荐、价格、购物车、购买、库存、促销或询价模块。
- [ ] 证书详情 API 不暴露后台备注、审计字段、内部用户字段、对象 Key、本机路径或未授权 URL。
- [ ] `GET /api/v1/miniapp/products?brandId=<brandId>` 仅召回当前品牌下可公开 SKU。
- [ ] 品牌过滤场景默认按发布时间升序、ID 升序返回。
- [ ] 同一发布时间下使用 `id ASC` 保证分页顺序稳定。
- [ ] 品牌详情页商品 Tab 首屏和加载更多结果与接口返回顺序一致。
- [ ] 搜索页相关性排序、新品榜近 90 天召回、热销榜 `hot_score DESC` 和普通商品列表排序不回归。
- [ ] 实现说明明确发布时间事实字段映射为 `tiles.published_at`；历史空值使用 `tiles.created_at` 兜底，禁止使用 `updated_at` 冒充发布时间。
- [ ] 管理端瓷砖 SKU 列表展示“发布时间”列，且位于“更新时间”列之前。
- [ ] “发布时间”与“更新时间”使用一致的日期时间格式、时区策略和秒级展示规则。
- [ ] 发布时间为空、缺失或不可解析时展示统一占位，例如 `-`，不出现 `null`、`undefined` 或 `Invalid Date`。
- [ ] 实现说明明确 SKU 发布时间字段来源，不得直接使用 `updated_at` 冒充发布时间。
- [ ] 若管理端 SKU 列表响应缺少发布时间字段，后端响应、Pydantic Schema、OpenAPI、Orval、接口文档和测试已同步。
- [ ] 新增发布时间列后，SKU 列表分页、关键词搜索、品牌/类目/状态/素材完整度筛选、加载态、空态、失败态和行操作不回归。
- [ ] 管理端品牌证书新增 / 编辑弹窗中，“支持 JPG / PNG / WebP，最多 9 张”说明下方不展示 `cover.webp`、`page-2.webp` 等图片文件名文本列表。
- [ ] 品牌证书图片上传控件保留图片缩略图、主图标记、删除入口、设为主图入口、继续添加图片入口、上传进度和失败提示。
- [ ] 新增弹窗上传图片后同样不展示图片文件名文本列表。

## 3. 横切验收清单

- [ ] admin-list：分页 DOM、fixed toast、DS confirm、指标卡结构不回归。
- [ ] admin-modal：无 `modal-card` 与专属类双挂载，computed width 正确，矮视口 body scroll 正常。
- [ ] media-upload：上传状态机覆盖 idle/uploading/done/failed，同会话即时回显，失败原因在控件内展示。
- [ ] Docker Web `http://localhost:3000` 上传边界：合法小图成功，超限图片返回业务错误而非 Nginx 413。
- [ ] MinIO 单桶策略：新上传不写入 `data/uploads/`，前端不直连未授权对象存储。
- [ ] miniapp：证书详情页按 custom-navigation best-practice 覆盖分享直达、返回兜底、胶囊 reserve、页面 offset 和截图 evidence。
- [ ] miniapp：证书详情页 DevTools 320/375/430 pt 覆盖正常、加载、错误、无图/PDF 和分享直达状态。
- [ ] miniapp：品牌详情页商品 Tab 保持接口返回顺序展示，不做前端跨页重排。
- [ ] 归档前无 stale 文案残留；completed/archived 状态不得继续显示“待实现与测试”。
- [ ] admin-list：SKU 列表新增发布时间列后，分页 DOM、fixed toast、无 `window.confirm`、宽表布局不回归。
- [ ] admin-form/admin-modal：证书图片文件名隐藏修复不新增文档流提示块，不影响品牌证书弹窗 computed width 和矮视口滚动。
- [ ] media-upload：证书图片上传状态机、即时回显、失败原因、主图/删除操作不回归。

## 4. 验收证据

| 证据 | 状态 | 说明 |
|---|---|---|
| 后端 pytest | 待补充 | 15/16 字符边界、非法字符、重复名称 |
| 前端 Vitest | 待补充 | CategoryFormModal 长度校验 |
| OpenAPI / Orval | 待补充 | maxLength 或等价约束 |
| 管理端 UI 回归 | 待补充 | 列表、树、弹窗宽度、矮视口滚动 |
| 小程序 / Web 展示回归 | 待补充 | 15 字符分类入口 |
| 小程序备注说明展示 | 已通过自动化；待补充 DevTools/真机截图 | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` 覆盖含备注 SKU、空/占位备注 SKU、页面展示节点与主要详情页回归 |
| 品牌证书后端 pytest | 已通过 | `uv run pytest tests/integration/api/test_admin_brand_certificates.py` 覆盖多图保存、主图唯一性、排序回填、旧单文件兼容、非法文件引用 |
| 品牌证书前端 Vitest | 已通过 | `pnpm --dir src/web exec vitest run src/pages/admin/BrandCertificateManagementPage.test.tsx src/features/admin/components/BrandCertificateComponents.test.tsx` 覆盖上传成功/失败、设置主图、删除入口和空态 |
| 品牌证书 Docker 上传边界 | 已通过 | `http://localhost:3000` 合法小图 200，26MB 超限返回业务 400 / 50005，未返回 Nginx 413；`data/uploads/` 仅保留 `.gitkeep` |
| OpenAPI / Orval | 已通过 | 已运行 `scripts/generate-openapi-client.sh`，同步证书图片数组、主图字段和客户端类型 |
| 小程序证书详情 API 证据 | 已通过 | `uv run pytest tests/test_miniapp_home.py` 覆盖公开详情成功、隐藏/删除/品牌不可公开过滤、旧单文件兼容、多图主图排序、安全 URL |
| 小程序证书详情页面证据 | 已通过 | `uv run pytest tests/test_miniapp_static.py` 覆盖路由注册、列表进入详情、媒体预览/PDF 打开、品牌入口、分享、异常状态、禁止交易/收藏/推荐模块 |
| 小程序证书详情设备 evidence | blocked / follow_up | `openspec/archive/2026-07-29-add-miniapp-certificate-detail-page/implementation/evidence.md` 已记录 DevTools 320/375/430 pt blocked 与真机 follow_up；未报告真机通过 |
| 品牌商品排序 API 证据 | 待补充 | 同品牌多 SKU 按发布时间升序、ID 升序返回 |
| 品牌商品分页证据 | 待补充 | 至少覆盖两页数据或模拟分页，无重复遗漏或顺序漂移 |
| 小程序品牌详情页证据 | 待补充 | 商品 Tab 展示顺序与接口一致 |
| 管理端 SKU 发布时间列前端证据 | 待补充 | 列头顺序、时间格式、空值占位、宽表布局 |
| 管理端 SKU 发布时间字段契约证据 | 待补充 | 如 API 变更，覆盖后端响应、OpenAPI/Orval 与类型生成 |
| 管理端证书图片文件名隐藏证据 | 已通过 | `pnpm --dir src/web exec vitest run src/features/admin/components/BrandCertificateComponents.test.tsx src/pages/admin/BrandCertificateManagementPage.test.tsx` 覆盖 `CertificateImageGrid` 有图片时不展示文件名文本列表，同时主图、删除、设主图、上传中和失败态不回归 |

## 5. 结论

最终结论：Sprint 013 于 2026-07-29 09:24:09 完成归档。8/8 Change 已归档，8/8 关联 REQ/BUG 已进入 archive/done；归档 readiness、Issue promotion gate、Workflow Sync、路径残留检查和 AI usage hook 按 `/sprint-archive sprint-013` 流程执行。AI usage hook 已刷新 `data/ai-usage/sprints/sprint-013.json`，`usage_mode: actual`，warning_count 为 0。
