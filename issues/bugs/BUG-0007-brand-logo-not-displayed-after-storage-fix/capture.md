---
bug_id: BUG-0007-brand-logo-not-displayed-after-storage-fix
status: captured
recorded_at: 2026-06-26 14:51:17
severity_hint: high
environment: local|docker
related_requirement: REQ-0005-brand-management
---

# 现象

对象存储写入问题修复后，品牌列表页以及品牌编辑页仍没有正常显示品牌 Logo 图片。

当前用户反馈：

- 品牌列表页 Logo 未显示。
- 品牌编辑弹窗 Logo 未显示。
- 之前判断与对象存储问题有关；对象存储问题已经修复后，前端展示仍未恢复。

# 复现步骤

1. 启动本地或 Docker 环境。
2. 确认对象存储上传链路已修复并可写入 MinIO。
3. 进入管理端 `/admin/brands`。
4. 查看品牌列表中的 Logo 展示。
5. 打开品牌编辑弹窗，查看 Logo 回显。

# 期望 vs 实际

| 项目 | 内容 |
|---|---|
| 期望 | 品牌列表页和品牌编辑弹窗都能展示已上传的品牌 Logo 图片。 |
| 实际 | 品牌列表页和品牌编辑弹窗仍未显示 Logo 图片。 |

# 附件

- 暂无截图。

# 初步备注

- 该问题发生在对象存储写入问题修复之后，可能与媒体 URL 生成、后端受控读取、前端 `logo_url` 绑定、缓存或旧数据对象 key 迁移有关。
- 相关缺陷：`BUG-0003-brand-image-display-layout-shift`、`BUG-0006-object-storage-upload-not-minio`。
- 本阶段仅 capture，不修改源码、不创建 OpenSpec Change。
