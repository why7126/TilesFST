## 1. 文档与规范

- [x] 1.1 新增 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`，沉淀 BUG-0125、BUG-0126 案例、四联证据链和可复制验收片段。
- [x] 1.2 更新 `docs/knowledge-base/README.md` 最佳实践索引。
- [x] 1.3 更新 `rules/media.md` 和媒体标准文档，补充小程序媒体四联最佳实践引用、Network evidence 和 helper 边界。
- [x] 1.4 更新 `rules/object-storage.md`，补充历史对象 dry-run 审计、fallback 风险、apply 回填门禁和脱敏输出要求。
- [x] 1.5 更新 `docs/standards/miniapp-device-evidence-template.md`，补充媒体资源 Network evidence 字段和状态边界。

## 2. Helper 实现

- [x] 2.1 新增或复用测试 helper，覆盖图片展示 URL、preview URL、视频 URL、poster / cover、fallback、lazy-load 和受控 `/media` URL 断言。
- [x] 2.2 新增或复用审计 helper，默认 dry-run，输出历史媒体对象 object、缩略图收益、fallback 风险和脱敏统计摘要。
- [x] 2.3 确认审计 helper 不默认写 DB 或对象存储；如提供 apply，必须要求显式参数、备份确认、幂等验证和失败重试。

## 3. 验证

- [x] 3.1 增加 focused tests，覆盖测试 helper 的图片、视频、fallback、lazy-load 和 URL 安全断言。
- [x] 3.2 增加 focused tests 或脚本 smoke，覆盖审计 helper 的 dry-run、脱敏输出、分类统计和不写入行为。
- [x] 3.3 运行 OpenSpec 校验、语言校验、目录结构校验和相关 pytest / 静态测试。
- [x] 3.4 在 Change trace 或 acceptance 中记录不涉及 API、DB、Orval、Docker Compose 运行时变更的判断；若实现阶段发现涉及，先更新设计和验证范围。
