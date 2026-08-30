---
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:44:12
---

# 验收

## 验收标准

- `release-prepare` 说明中明确 Web shared、小程序 TS、小程序 JS 的 `PRODUCT_VERSION` 必须等于发布版本。
- `release-publish` 说明中明确用户可见版本号不一致时不得发布，`version_change_rationale` 不可放行。
- `validate-release.py` 能阻断 shared 或小程序任一版本源不一致，并提示更新版本源后重跑 `/image-prepare` 与 `/image-build`。
- `release-status` 将产品版本不一致归类为 prepare 阶段证据缺口。
- 治理日志、CHANGELOG、Sprint 范围和 Workflow Sync 完整记录。

## 验收结果

```yaml
acceptance_status: pending_validation
accepted_at:
accepted_by:
evidence:
  - "release validator 已改为阻断 shared / miniapp PRODUCT_VERSION 不一致。"
  - "image build input candidates 已纳入 shared / miniapp 产品版本源。"
  - "聚焦测试：4 passed。"
pending_items:
  - "等待 OpenSpec、目录、上下文预算、文档卫生、Workflow Sync 和 AI Usage hook 验证完成后回填。"
```
