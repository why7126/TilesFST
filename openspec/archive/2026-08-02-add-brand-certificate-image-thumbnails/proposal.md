## Why

SKU 商品图片已经具备真实同目录 `.thumb` 缩略图生成能力，但品牌图片和证书图片仍缺少同等治理。管理端列表/弹窗、小程序品牌与证书展示、店主 Web 品牌与证书展示继续加载原图，会增加首屏、滚动、移动端流量和对象存储读取成本，也让媒体能力验收停留在 SKU 场景。

## What Changes

- 将真实缩略图生成与优先读取能力扩展到品牌图片和图片类品牌证书。
- 保持原图/原文件用于预览、下载和大图查看；小图、列表、卡片和默认主图优先使用缩略图。
- 明确缩略图失败回退、透明图/小图/WebP/异常图边界、后端受控 `/media/{object_key}` 读取和前端不得直连对象存储。
- 为存量品牌图片和证书图片提供 dry-run / apply 形式的补齐或重生成方案，输出可审计、可重入、脱敏的统计摘要。
- 将媒体五联验收纳入实现门禁：对象 key、对象存在、URL 可访问、真实缩略收益、端上渲染 evidence。
- 不新增视频缩略图、PDF 首页渲染、OCR、品牌/证书业务字段、权限模型或业务审批流。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `object-storage`: 媒体受控读取与真实缩略图生成从商品列表扩展到品牌图片和图片类品牌证书，并补充存量补齐治理。
- `brand-management`: 品牌 Logo 上传、列表、编辑回显和预览需要支持真实缩略图生成、优先读取和失败回退。
- `brand-certificate-management`: 品牌证书图片上传、列表主图、组件展示和横切 UI 验收需要支持真实缩略图生成与优先读取。
- `miniapp-brand-list-page`: 小程序品牌列表品牌 Logo / 品牌图片小图展示需要优先使用后端受控缩略图。
- `miniapp-brand-detail-home-page`: 小程序品牌主页信息区和证书 Tab 需要优先使用品牌/证书缩略图，并保留原图预览。
- `miniapp-certificate-list-page`: 小程序公开证书列表 API 与证书卡片展示需要区分缩略图、原文件和 PDF 占位。
- `web-client`: 管理端品牌 Logo 展示、上传回显和小图预览需要使用受控缩略图且不造成布局回归。

## Impact

- Backend: media/storage、uploads、品牌与证书服务层、媒体读取回退和存量补齐脚本。
- Web/Admin: 品牌列表/编辑弹窗、品牌证书列表/卡片/弹窗、上传状态机、fixed toast、DS confirm 和弹窗宽度回归验收。
- Miniapp: 品牌列表、品牌主页、证书列表、证书详情或预览入口的小图加载和占位回退。
- Store-owner Web: 品牌与证书列表/卡片使用轻量资源，预览仍使用原图或原文件。
- Storage: MinIO 单桶标准前缀、同目录 `.thumb` 或等价可追溯命名、历史对象 dry-run/apply。
- API: 若实现新增或显式化 `thumbnail_url`、`thumbnail_object_key` 或等价字段，必须同步 OpenAPI、Orval、API 文档和测试；若复用现有媒体字段，design/tasks 必须说明不需要 Orval 的原因。
- Database: 默认不新增表；若实现选择持久化缩略图字段，必须同步 SQLite/MySQL schema、迁移、Pydantic Schema 和数据库文档。
- Deployment: 若新增图片处理依赖或 Docker 镜像层变化，必须同步部署/镜像文档并保留容器内验证摘要。
