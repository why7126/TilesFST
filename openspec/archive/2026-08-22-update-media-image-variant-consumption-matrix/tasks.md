## 1. OpenSpec 规格

- [x] 1.1 更新 `media-multi-variant-images` delta spec，新增统一消费矩阵 requirement 与场景。
- [x] 1.2 明确小程序真实页面、Web 管理端真实媒体位置和店主 Web 预留规范的覆盖边界。
- [x] 1.3 明确非原图目标场景不得 fallback 到 `original`，并写入验收场景。

## 2. 文档与追踪

- [x] 2.1 在 design 中记录矩阵归属、非目标、偏离点只记录不修复和知识库引用。
- [x] 2.2 更新 REQ-0118 trace，关联本 Change，保持 `iteration: sprint-025`。
- [x] 2.3 由 Workflow Sync 将本 Change 回填到 `sprint-025` scope。

## 3. 校验

- [x] 3.1 运行 `python scripts/validate-openspec-language.py`。
- [x] 3.2 运行 `openspec validate update-media-image-variant-consumption-matrix --strict`。
- [x] 3.3 运行 Workflow Sync：`req.opsx`。
- [x] 3.4 运行 `/opsx-apply` dry-run scope 解析校验，确认本 Change 已纳入 `sprint-025`。
