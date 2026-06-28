---
bug_id: BUG-0042-system-settings-page-title-v2-suffix
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断任何功能，系统设置各 Tab 均可正常读写：

1. **忽略眉标后缀**：`/ V2` 仅为展示文案，不影响保存、恢复默认或 API。
2. **版本信息**：如需确认产品版本，查看侧栏品牌行 `ProductVersionBadge` 即可。

## 2. 操作规避

无配置、脚本或权限变更可规避；无需改后端或数据库。

## 3. 风险说明

规避仅保证功能可用，不能消除页头文案与用户期望不一致。建议 `/bug-review BUG-0042 --approve` 后通过 `fix-system-settings-page-title-v2-suffix` 修复。
