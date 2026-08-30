---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
created_at: 2026-08-30 10:28:24
updated_at: 2026-08-30 10:28:24
---

# 临时规避

当前没有端侧无代码规避方案。小程序列表页只有在接口返回非空 `thumbnail_url` 时才会展示证书图片；生产接口返回空值时，端侧只能显示“证书”占位。

# 可选人工处理

在正式修复前，可以由运维或管理员在生产侧进行受控数据检查与补救：

1. 核查受影响证书记录是否存在标准图片 key：图片证书应使用 `images/default/brand-certificates/`，PDF / 文档证书应使用 `files/default/brand-certificates/`。
2. 核查 `brand_certificates` 与 `brand_certificate_images` 中主图记录的 `file_url` 是否与 `file_key` 对应为 `/media/{file_key}`。
3. 对历史图片证书先运行媒体 key 迁移和缩略图回填 dry-run，确认候选数量和目标 key。
4. 经生产备份确认后再执行 apply，并再次 dry-run 验证幂等。
5. 若单条证书急需展示，可在管理端重新上传该证书图片，使上传链路生成新的标准 key 和派生缩略图。

# 风险说明

- 不建议临时放宽小程序列表页去加载原图 `file_url`；这会回退到大图冷加载，违背轻量图治理目标。
- 不建议让前端直连对象存储或拼接未授权 URL；媒体访问仍应走后端受控 `/media/` 路径。
- 不建议直接手工修改生产数据库字段，除非已有备份、dry-run 输出和回滚路径。
