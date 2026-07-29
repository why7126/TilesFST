## 1. Web 管理端修复

- [x] 1.1 移除 `CertificateImageGrid` 中证书图片上传说明下方的文件名文本列表渲染。
- [x] 1.2 移除或整理不再使用的 `.certificate-image-list-meta` 相关样式。
- [x] 1.3 确认图片卡片、主图标记、删除、设为主图、继续添加、上传进度和失败提示不回归。

## 2. 回归测试

- [x] 2.1 更新 `BrandCertificateComponents.test.tsx`，覆盖有图片时不展示 `cover.webp`、`page-2.webp` 等文件名文本列表。
- [x] 2.2 保留或补充主图、设为主图、删除、上传中 progressbar 和失败 alert 测试。

## 3. 校验与工作流

- [x] 3.1 运行品牌证书组件相关前端测试。
- [x] 3.2 运行 `openspec validate fix-admin-certificate-image-filename-noise`。
- [x] 3.3 完成 apply 后运行 Workflow Sync。
- [x] 3.4 评估是否需要沉淀到 `docs/knowledge-base/incidents/`；本次为低严重度 UI 噪音且无复用事故价值，不需要新增 incident。
