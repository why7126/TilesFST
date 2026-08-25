## 1. Runbook 范围与现状盘点

- [x] 1.1 盘点现有图片转换、派生图生成、缩略图重建、对象 key 迁移和生产媒体维护脚本，标注现有可用、需修改、需新增或仅预留。
- [x] 1.2 对照 `media-multi-variant-images`、`object-storage` 和 `prod-media-maintenance-jobs` specs，确认 Runbook 不改变既有运行时契约。
- [x] 1.3 确认首次 Runbook 投影版本，并记录长期事实源与版本快照路径。

## 2. 长期 Runbook 文档

- [x] 2.1 新增或更新 `docs/` 下批量图片处理 Runbook 事实源，覆盖图片转换脚本、`thumb` / `display` 派生生成和缩略图专项重建。
- [x] 2.2 补充对象 key 迁移章节，覆盖候选识别、dry-run、apply、幂等、失败分类、二次审计和快照回滚边界。
- [x] 2.3 补充生产执行章节，覆盖 Docker Compose 一次性容器、环境注入、备份确认、执行窗口、日志脱敏和失败中止条件。
- [x] 2.4 补充安全门禁章节，禁止真实 `.env`、密钥、Authorization header、Cookie、本机绝对路径、真实客户数据和未脱敏 object key 写入长期文档。

## 3. 版本使用文档投影

- [x] 3.1 将 Runbook 投影到目标 `releases/vX.Y.Z/usage-docs/` 快照或对应版本使用文档索引。
- [x] 3.2 在 usage docs manifest 或等价索引中记录 Runbook 源路径、快照路径、更新时间和适用版本。
- [x] 3.3 校验长期 Runbook 与版本快照的关键章节一致，确保双投影不遗漏安全门禁和验收证据模板。

## 4. 验收证据模板

- [x] 4.1 在 Runbook 中提供 dry-run 摘要模板，覆盖待处理数量、预计写入对象、跳过原因、失败分类和风险摘要。
- [x] 4.2 在 Runbook 中提供 apply 与二次审计模板，覆盖 key、object、URL、render、benefit、幂等复跑和失败处理。
- [x] 4.3 提供缩略图专项重建和对象 key 迁移的专项验收模板，覆盖新旧 key、对象存在性、受控 URL、端侧展示和回滚记录。

## 5. 校验与追踪

- [x] 5.1 运行 OpenSpec strict 校验、OpenSpec 语言校验和目录结构校验。
- [x] 5.2 回填 REQ-0122 trace、acceptance 与 Change trace，记录 Runbook 路径、投影路径、验证命令和剩余风险。
- [x] 5.3 如实现新增或修改脚本，补充对应测试；如仅文档化现有脚本，记录不需要 API、DB、Orval 和 Docker Compose 验证的原因。

## 验收返修记录

- [x] 6.1 新增生产媒体维护聚合任务语义化别名 `media-drift-reconcile`，保留 `bug-0116-media-drift` 历史兼容别名。
- [x] 6.2 更新 Runbook、usage-docs 模板、部署文档、对象存储文档和帮助文案，推荐生产命令不再暴露具体 BUG 编号。
- [x] 6.3 补充聚焦测试，覆盖新别名 apply 备份门禁、旧别名兼容和语义化 `task` 输出。
