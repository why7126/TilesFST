## Context

REQ-0092 来自 BUG-0101 的重新分类：SKU 商品图片缩略图已经经 BUG-0100 修复为真实轻量 `.thumb`，但品牌图片和证书图片仍缺少同等能力。现有规格已经覆盖 MinIO 单桶、后端受控 `/media/{object_key}` 读取、品牌 Logo 上传、证书文件/多图上传、管理端列表/弹窗横切 UI 和小程序品牌/证书展示，但真实缩略图生成主要落在商品/SKU 场景。

当前需求横跨后端媒体处理、对象存储、管理端、微信小程序和店主 Web 展示端。风险点集中在：把原图 bytes 误当缩略图、只验证 object 存在而未验证尺寸/体积收益、前端直连对象存储、上传状态机/同会话回显回归、存量脚本不幂等或输出泄露敏感信息。

## Goals / Non-Goals

**Goals:**

- 新上传品牌图片和图片类品牌证书生成真实、轻量、可追溯缩略图。
- 小图场景优先使用缩略图，原图预览和 PDF 文件预览保持原有语义。
- 缩略图缺失、生成失败、读取失败时安全回退原图或占位，并记录可定位信息。
- 存量品牌图片和证书图片具备 dry-run / apply 补齐方案，输出脱敏统计摘要。
- 管理端、小程序和店主 Web 不直连未授权对象存储。
- 实现阶段以媒体五联验收覆盖 key、object、URL、thumbnail benefit、render evidence。

**Non-Goals:**

- 不新增视频缩略图、PDF 首页渲染缩略图或 OCR。
- 不改变品牌、证书 CRUD、权限、启停删除规则或审批流程。
- 不要求立即物理清理历史原图或历史无效缩略图。
- 不直接实现代码；实现由 `/opsx-apply` 执行。

## Decisions

### D1. UI 策略：Design System / shared component 优先

采用 DS / shared component 策略，不执行 prototype CSS Port。

理由：`prototype/web/thumbnail-usage.html` 是状态和布局说明，不是最终 Golden Reference；REQ 的核心是媒体链路与展示策略。实现应复用现有 `BrandFormModal`、品牌证书通用组件、AdminListPage/Pagination、上传控件状态机和 semantic token，避免把 prototype 中的裸 Hex 和静态 DOM 引入生产代码。

备选：CSS Port。放弃原因是该 prototype 没有最终视觉细节，也不应覆盖既有管理端页面风格。

### D2. 缩略图命名与追溯策略

默认沿用 SKU 已验证的同目录 `.thumb` 或等价文件名差异化策略，缩略图与原图位于同一对象目录并由后端生成。若品牌 Logo、品牌封面、Banner 或证书图片需要细分目标尺寸，必须在实现 design 或 tasks 中明确资源类型、最大宽高、质量和格式策略。

缩略图不得是原图 bytes 复制品；测试必须比较像素尺寸、文件体积或 hash/bytes 差异。

### D3. API 字段策略

优先复用现有 `logo_url`、`file_url`、主图 URL 或等价受控读取 URL，让后端在小图场景返回缩略图或提供派生 URL；当端侧必须同时持有缩略图与原图时，允许新增显式 `thumbnail_url` / `thumbnail_object_key` / `original_url` 字段。

若新增或显式化字段，必须同步 OpenAPI、Orval、docs、Pydantic Schema 和测试。若不新增字段，必须在实现 trace 中说明“不需要 Orval”的证据。

### D4. 回退与可观测性

缩略图生成失败不得阻断原图上传和业务保存；展示时按“缩略图 → 原图 → 占位”的顺序回退。后端或脚本必须记录脱敏 object key、原因分类和统计摘要，避免静默失败。

### D5. 存量补齐

存量补齐必须先 dry-run，再 apply。dry-run 不写数据库或对象存储；apply 只处理缺失或不合格缩略图，重复执行保持幂等。输出只允许包含脱敏 key、数量、状态和错误分类，不得泄露 `.env`、Authorization header、Cookie、本机绝对路径、真实密钥或真实客户数据。

### D6. Prototype Conflict Resolution

优先级按 `HTML > PNG > context.md > acceptance.md > ui-design.md > openspec/specs` 处理。

- HTML prototype 只作为状态说明：列表小图策略、上传状态机、存量 dry-run 摘要。
- PNG 不存在，后续设计阶段可导出，不阻断本 Change。
- `context.md` 明确 prototype 不定义真实接口字段名、不替代 OpenSpec design。
- `acceptance.md` 对媒体链路、安全、Docker、小程序 evidence 和横切 AC 更具体，优先作为实现验收事实源。
- `rules/ui-design.md` 和既有 specs 约束生产 UI 必须复用 semantic token 与 DS/shared 组件，不复制 prototype 裸 Hex。

## Risks / Trade-offs

- 缩略图策略过度复用 SKU 尺寸，可能不适合 Logo 或证书图比例 → 实现阶段按资源类型记录目标尺寸/质量策略，并用横图/竖图/透明图样例回归。
- 新增 API 字段会触发 Orval 和端侧同步成本 → 先评估是否可复用现有 URL；新增字段时完整同步契约和测试。
- 小图原图比缩略图更小时可能体积反增 → 实现需允许跳过重写、保留原图回退或记录告警。
- 小程序真机 evidence 不一定在实现阶段可得 → DevTools evidence 至少覆盖；真机/体验版缺证必须进入 release-prepare 检查清单。
- Docker/图片处理依赖可能影响镜像构建 → 新依赖必须同步部署/镜像文档，并保留容器内导入或缩略图生成验证摘要。

## Migration Plan

1. 实现后端品牌与证书图片缩略图生成、读取和回退。
2. 更新管理端品牌/证书页面和小程序/店主端小图消费策略。
3. 提供存量 dry-run/apply 脚本或等价运维命令。
4. 补充后端、Web、miniapp 静态/DevTools、脚本和 Docker Web 上传边界验证。
5. 若字段/API/DB/依赖发生变化，同步 OpenAPI、Orval、docs、schema、部署文档和测试。
6. 回滚时保留原图读取路径，禁用缩略图优先读取即可回到原行为；不得删除原图对象。

## Open Questions

- 品牌 Logo、品牌封面和证书图片是否采用完全相同目标最大宽高，还是按资源类型区分。
- 是否需要新增显式 `thumbnail_url` 字段，或由现有 URL 在列表/卡片场景直接返回缩略图。
- 存量补齐是否与本 Change 同步上线，还是拆为实现任务中的可选 apply 步骤。
