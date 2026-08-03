## 背景与原因

`BUG-0108-admin-certificate-edit-file-ready-text-and-image-info` 已确认需要修复。管理后台证书编辑弹窗在打开已有证书时，PDF/兼容文件区域显示冗余的 `证书文件已就绪` 文案，同时图片信息无法正常显示，影响运营人员判断已有文件、图片列表和主图状态。

该问题与 `BUG-0089-admin-certificate-edit-image-filename-noise` 同属品牌证书弹窗展示模型偏差：编辑回显态、上传完成态和运营可读展示态没有被清晰区分。需要通过 OpenSpec Change 约束修复范围，确保文件提示、图片回显、主图状态和既有文件名噪音约束一起回归。

## 变更内容

- 修复品牌证书编辑弹窗的 PDF/兼容文件展示逻辑，已有文件回显时不显示 `证书文件已就绪`。
- 修复已有证书图片数组、主图状态、缩略图 URL / 原图 URL 的编辑弹窗回显映射。
- 保留上传失败、文件缺失、格式不兼容等必要错误提示。
- 保证新增、替换、删除图片和设置主图后，保存并再次打开弹窗仍正确回显。
- 补充品牌证书弹窗回归测试，覆盖文件提示、图片卡片、主图状态和文件名噪音不回归。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `brand-certificate-management`: 管理端品牌证书编辑弹窗必须区分已有文件回显态与上传就绪态，正常回显图片列表与唯一主图，并避免对象 key、原始文件名或无意义文件名噪音。

## 影响范围

- 影响范围：管理后台 `/admin/brand-certificates` 页面、品牌证书新增/编辑弹窗、品牌证书通用文件/图片展示组件。
- 预计影响文件：`src/web/src/features/admin/components/BrandCertificateComponents.tsx`、`src/web/src/pages/admin/BrandCertificateManagementPage.tsx`、相关前端测试。
- API：优先不变更；若修复阶段确认详情 API 缺少必要图片字段，必须同步 OpenAPI / Orval / docs / tests。
- 数据库：预计不变更。
- 对象存储：不改变上传链路和 MinIO 单桶策略。
- 小程序：不影响。
- Docker Compose：不需要。

## 回滚方案

- 若修复导致证书编辑弹窗保存、上传或预览流程回归，可回退本 Change 的前端展示映射与组件调整。
- 回退后保留现有 API、数据库和对象存储数据，不需要数据迁移。
- 若修复阶段引入 API 字段补齐，应在回退时同步回退 OpenAPI / Orval 生成物与对应测试。
