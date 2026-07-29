---
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
status: done
created_at: 2026-07-29 08:31:34
updated_at: 2026-07-29 09:07:56
---

# 直接原因

管理端品牌证书图片上传组件 `CertificateImageGrid` 在 `images.length > 0` 时，除了渲染图片卡片、主图标记、删除和设为主图操作外，还额外渲染了 `certificate-image-list-meta` 区块。

该区块逐个输出 `images[].file_name`，因此当编辑已有证书且后端返回图片文件名时，“支持 JPG / PNG / WebP，最多 9 张”说明下方会显示 `cover.webp` 等文件名。

# 根本原因

证书多图上传控件沿用了“补充展示图片文件名”的组件设计，但当前编辑弹窗的业务信息架构已经由图片缩略图、主图标记、设为主图、删除和继续添加入口覆盖主要操作上下文。文件名文本列表没有明确用户任务价值，也没有进入验收约束，导致冗余展示被保留下来。

# 触发条件

1. 管理端打开 `/admin/brand-certificates`。
2. 打开新增或编辑品牌证书弹窗。
3. 证书图片列表 `images` 至少包含一项。
4. 图片对象包含 `file_name` 字段。

# 分类

- 类型：UI / design
- 层级：Web 管理端前端组件
- 数据风险：无
- API 风险：无
- 回归风险：低，修复范围应限定在证书图片上传控件的冗余文本渲染与对应样式/测试。
