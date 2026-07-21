## Context

REQ-0055 来源于 `issues/requirements/archive/REQ-0055-brand-certificate-common-component`，当前状态为 `in_sprint`，已纳入 `sprint-009`。父需求 REQ-0038 已定义品牌证书管理页、上传链路、预览、权限和横切 UI 验收，本 change 只把已存在页面中的证书展示与文件状态沉淀为管理端业务组件。

现有 prototype 位于 `prototype/web/brand-certificate-common-component.html`，它是组件状态矩阵，不是完整页面。视觉优先级为 HTML > prototype context > acceptance > `rules/ui-design.md` > 现有 OpenSpec specs。prototype 中的裸 Hex 仅用于原型表达，实现时必须转换为 Design System semantic token。

## Goals / Non-Goals

**Goals:**

- 建立品牌证书缩略图、摘要、有效期、有效状态、展示状态、预览入口和文件卡片的组件契约。
- 保持 `/admin/brand-certificates` 页面既有筛选、分页、权限、保存、删除、显示/隐藏确认和 toast 责任边界。
- 覆盖图片、PDF、文件 fallback、加载失败、长期有效、有效、即将到期、已过期、未设置、展示/隐藏、上传中、上传失败等状态矩阵。
- 复用现有 helper、Design System token、Badge/文本/边框语义和管理端列表/弹窗结构。

**Non-Goals:**

- 不新增品牌证书 API、数据库字段、上传接口、MinIO 策略或 Orval 生成物。
- 不新增店主 Web 品牌详情证书展示。
- 不新增微信小程序证书展示组件。
- 不新增证书审批、OCR、真伪校验、电子签章或批量操作。

## Decisions

### D1. UI Strategy: tailwind-ds

采用管理端业务组件 + Tailwind semantic token 方案。原因是本需求不是登录页 CSS Port，也不是静态视觉复刻；目标是可复用组件契约和状态矩阵。实现应优先落在管理端品牌证书业务组件目录，复用现有 helper 与 DS 组件，必要样式使用 `bg-surface`、`text-primary`、`text-secondary`、`text-muted`、`text-brand-gold`、`border-border-default` 等 semantic token。

备选方案：

- CSS Port：适合高保真页面复刻，但本 prototype 是状态矩阵，直接 port 会把一次性样式带入业务组件。
- 跨端共享组件：当前只有管理端真实复用诉求，字段、交互和视觉尚未稳定到跨端层。

### D2. 组件只处理展示模型和回调

组件 props 面向展示模型，可使用 `BrandCertificateItem` 的窄类型或 `Pick<>`。组件不得接收页面分页、筛选、保存状态或权限对象；状态切换、删除确认、上传 API、保存阻塞、toast 和错误映射继续由页面容器负责。

### D3. 有效状态以服务端返回为事实源

有效期文本可由统一 helper 格式化，但有效状态 Badge 必须复用服务端返回的有效状态，前端不得作为唯一事实源重新计算。未知状态降级展示原始文本，避免新枚举导致页面渲染失败。

### D4. 文件预览只消费受控 URL

图片和 PDF v1 均可通过新窗口打开服务端返回的受控 URL。组件必须在 URL 缺失时阻止预览并返回失败原因，不得拼接未授权对象存储直连地址。

## Conflict Resolution

- HTML prototype 与 UI 规则冲突：prototype 内裸 Hex 和 scoped rgba 仅作为视觉说明，实现必须使用 semantic token 和既有管理端语义。
- HTML prototype 与 acceptance 范围冲突：prototype 展示状态矩阵，acceptance 定义交付边界；实现不需要还原完整 prototype 页面。
- 预览行为冲突：父 spec 允许图片大图预览、PDF 新窗口预览；REQ-0055 v1 统一为图片/PDF 可通过新窗口打开受控 URL，后续如恢复图片大图 modal，不得改变组件的 URL 缺失和失败兜底契约。
- 文件卡片职责冲突：prototype 展示上传中和失败状态，但组件不得直接调用上传 API；上传进度、错误映射和保存阻塞由页面容器传入状态与回调。

## Risks / Trade-offs

- [Risk] 过度抽象导致页面容器和组件边界不清 → Mitigation: tasks 中先梳理现有 helper 与页面状态，再抽取窄 props 契约。
- [Risk] 组件化改动回归品牌证书页分页、指标卡或弹窗宽度 → Mitigation: 保留 REQ-0038 横切验收，并增加 1440x1024 回归检查。
- [Risk] 上传文件卡片与已有上传链路耦合过深 → Mitigation: 文件卡片只展示 `idle/uploading/done/failed` 状态和触发回调，不持有上传副作用。

## Migration Plan

1. 在管理端品牌证书业务组件目录新增或整理组件与 helper 导出。
2. 用通用组件替换 `/admin/brand-certificates` 页面中的证书列、状态列和文件展示区。
3. 补充单元测试、页面回归测试和 Docker Web 入口上传边界验收。
4. 若发现必须新增 API 字段或后端契约，停止实现并创建 follow-up REQ/BUG，不在本 change 内扩大范围。

## Open Questions

- 无阻断问题。PNG Golden Reference 可在后续设计验收时补充，本 change 以 HTML prototype、prototype context 和 acceptance 作为首轮实现依据。
