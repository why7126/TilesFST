## 1. Backend / Storage

- [x] 1.1 梳理品牌图片、证书图片和 SKU 图片当前上传/读取链路，确认可复用的缩略图生成函数、目标尺寸、质量、格式和同目录 `.thumb` 命名策略。
- [x] 1.2 为新上传品牌图片生成真实缩略图，覆盖 JPG、PNG、WebP、小图、横图、竖图、透明图和异常图片输入。
- [x] 1.3 为新上传图片类品牌证书生成真实缩略图；PDF 或非图片证书继续使用文件类型占位或既有策略。
- [x] 1.4 实现缩略图读取回退：缩略图 → 原图 → 占位，并记录脱敏失败原因。
- [x] 1.5 提供存量品牌图片和证书图片 dry-run / apply 补齐或重生成方案，输出成功、失败、跳过、重试和风险统计摘要。

## 2. API / Schema / Docs

- [x] 2.1 决定是否新增显式 `thumbnail_url` / `thumbnail_object_key` / `original_url` 字段；若新增，更新 Pydantic Schema、OpenAPI、Orval、API 文档和测试。
- [x] 2.2 N/A：本次新增显式缩略图字段，已在 2.1 同步 Pydantic Schema、OpenAPI、Orval、API 文档和测试。
- [x] 2.3 N/A：未新增图片处理依赖或 Docker 镜像层变化，复用既有 Pillow 缩略图能力并记录验证摘要。
- [x] 2.4 N/A：未持久化新增缩略图字段，缩略图 URL 由现有对象 key 同目录 `.thumb` 规则派生，已记录不需要 DB 变更的原因。

## 3. Web Admin / Store-owner Web

- [x] 3.1 更新管理端品牌列表 Logo 与品牌编辑弹窗小预览，优先使用缩略图，预览使用原图，失败稳定回退。
- [x] 3.2 更新品牌证书列表、证书卡片、证书弹窗文件/图片卡片，优先使用主图缩略图，PDF 继续占位，失败不显示破图。
- [x] 3.3 保持上传控件 `idle -> uploading -> done/failed` 状态机、同会话即时回显、字段级错误和 fixed toast 不回归。
- [x] 3.4 店主 Web 品牌与证书小图展示优先使用缩略图；原图预览或证书预览继续使用原图/原文件。
- [x] 3.5 验证管理端列表分页 DOM、DS confirm、弹窗 computed width、矮视口滚动和 semantic token 约束。

## 4. Miniapp

- [x] 4.1 更新小程序品牌列表、品牌主页信息区、品牌卡片组件或数据映射，品牌 Logo/图片小图优先使用缩略图。
- [x] 4.2 更新小程序证书列表、品牌主页证书 Tab、证书详情/预览入口，证书卡片优先使用缩略图，预览使用原图或原文件。
- [x] 4.3 补充小程序静态测试或 DevTools evidence；真机/体验版 evidence 如无法补齐，写入 release-prepare 检查清单。

## 5. Validation

- [x] 5.1 后端 pytest 覆盖品牌图片和证书图片缩略图真实生成、失败回退、透明图/小图/WebP 边界和存量 dry-run/apply 幂等。
- [x] 5.2 Web Vitest/Testing Library 覆盖品牌 Logo、证书图片卡片、上传状态机、失败态和 fixed toast 无布局位移。
- [x] 5.3 小程序静态测试覆盖品牌/证书缩略图字段映射、占位回退和预览入口。
- [x] 5.4 Docker Web `http://localhost:3000` 验证小文件上传成功、超限文件返回业务错误而非 Nginx 413。
- [x] 5.5 媒体五联验收记录 key、object、URL、thumbnail benefit、render evidence。
- [x] 5.6 运行 `openspec validate add-brand-certificate-image-thumbnails --strict`。
