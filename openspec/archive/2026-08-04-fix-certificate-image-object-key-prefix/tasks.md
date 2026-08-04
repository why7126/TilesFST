---
change_id: fix-certificate-image-object-key-prefix
type: fix
status: proposed
related_bug: BUG-0112-certificate-image-object-key-prefix
created_at: 2026-08-04 08:28:57
updated_at: 2026-08-04 08:28:57
---

# 任务清单

- [x] 1. 梳理品牌证书上传、证书多图保存、缩略图生成和历史补齐脚本中的证书图片 key 生成路径。
- [x] 2. 修复后端图片类证书 key 分流：JPG、PNG、WebP 进入 `images/default/brand-certificates/` 或等价标准图片前缀。
- [x] 3. 保持 PDF 等文档类证书使用 `files/` 前缀，并补充防止文档附件误入 `images/` 的测试。
- [x] 4. 修复证书图片缩略图生成与回填，使缩略图与原图保持同一图片资源归属。
- [x] 5. 增加或更新历史证书图片 key 审计/迁移脚本，支持 dry-run、apply、幂等复跑和脱敏摘要。
- [x] 6. 更新 `rules/media.md`、`docs/standards/file-upload.md`、对象存储相关文档和必要 Skill，明确证书图片归入 `images/`、证书 PDF/文档归入 `files/`。
- [x] 7. 补充后端、脚本和媒体四联验收测试，覆盖 key、object、URL、render 维度。
- [x] 8. 运行相关测试与校验：后端 pytest、脚本单测、`python scripts/validate-openspec-language.py`、`python scripts/validate-directory-structure.py`。
- [x] 9. 更新 BUG 验收回填证据，记录 dry-run/apply 摘要和跨端展示验证；必要时沉淀 `docs/knowledge-base/incidents/`。
