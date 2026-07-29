## Root Cause

`CertificateImageGrid` 在 `images.length > 0` 时渲染 `certificate-image-list-meta` 区块，并逐个输出 `images[].file_name`。因此编辑已有证书或新增弹窗上传图片后，上传说明下方会显示图片文件名。

根本原因是证书多图控件保留了补充文件名展示设计，但现有交互已经通过图片卡片、主图标记、设为主图、删除和继续添加入口承载图片编辑任务。文件名文本列表没有进入验收约束，也没有实际用户价值。

## Fix Strategy

1. 从品牌证书图片上传组件中移除文件名文本列表渲染。
2. 移除对应无用样式，避免保留不可达 CSS。
3. 保持图片列表卡片、主图标记、设为主图、删除、继续添加、上传中进度条和失败 alert 的 DOM 行为不变。
4. 更新组件测试：有图片时仍能操作图片，但 `cover.webp`、`page-2.webp` 等文件名不会作为上传说明下方文本出现。

## Scope Boundaries

- 不修改上传 API。
- 不修改 `BrandCertificateImage.file_name` 数据模型或后端响应。
- 不修改图片保存、排序、主图兜底、删除、预览或对象存储策略。
- 不修改小程序证书展示。
- 不修改品牌证书列表证书摘要中已有的文件名 fallback 语义。

## Tests

- 前端 Vitest / Testing Library：
  - 有图片时渲染图片列表、主图标记、删除和设为主图。
  - 有图片时不展示图片文件名文本列表。
  - 上传中 progressbar、失败 alert 保持可访问。
- OpenSpec 校验：`openspec validate fix-admin-certificate-image-filename-noise`。

## Risks

| 风险 | 缓解 |
|---|---|
| 测试误把缩略图 `alt/title` 与可见文本混淆 | 测试应断言文件名不作为可见文本列表出现，同时不破坏缩略图可访问信息 |
| 移除样式误伤图片网格布局 | 仅移除 `.certificate-image-list-meta` 相关样式，不改图片网格和卡片样式 |
| 修复扩大到后端字段删除 | 明确保留 `file_name` 数据，用于元数据、调试和其他展示场景 |
