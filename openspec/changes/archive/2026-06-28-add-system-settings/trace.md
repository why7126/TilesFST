---
change_id: add-system-settings
requirement_id: REQ-0017-system-settings
created_at: 2026-06-28 11:27:21
updated_at: 2026-06-28 17:10:00
---

# Change Trace — add-system-settings

## 关联

| 项 | 值 |
|---|---|
| REQ | REQ-0017-system-settings |
| Change | add-system-settings |
| OpenSpec | `openspec/changes/add-system-settings/` |

## 原型 PNG 并排 checklist（opsx-apply 填写「实现」列）

| 分组 | HTML | PNG | 实现 |
|---|---|---|---|
| 基础信息 | ✓ | 待导出 | ✓ CSS Port + BasicTab |
| 安全策略 | ✓ | 待导出 | ✓ SecurityTab |
| 媒体与存储 | ✓ | 待导出 | ✓ MediaTab + 只读 bucket/Key |
| 通知设置 | ✓ | 待导出 | ✓ NotificationTab + 模板 modal |
| 审计配置 | ✓ | 待导出 | ✓ AuditTab + recent 列表 |
| Shell + settings-nav | ✓ | 待导出 | ✓ page-hero + summary-grid + settings-nav |
| dirty + 双保存 + 底部操作条 | ✓ | 待导出 | ✓ dirty badge + hero/footer save |

> PNG Golden 仍待人工导出至 `prototype/web/system-settings-*.png`；开发验收以 HTML + 实现 checklist 为准。

## Phase 交付记录

| Phase | 范围 | 完成日期 | 备注 |
|---|---|---|---|
| P0 | basic + media + nav | 2026-06-28 | effective upload 已接线 |
| P1 | security | 2026-06-28 | JWT expire + password policy |
| P2 | audit | 2026-06-28 | audit_logs + PATCH/reset 写入 |
| P3 | notification | 2026-06-28 | 无 SMTP 发信路径 |

## 测试

| 套件 | 命令 | 结果 |
|---|---|---|
| Backend | `pytest -k system_settings` | 8 passed |
| Frontend | `vitest run SystemSettings` | 3 passed |
| Build | `pnpm build` | OK |
| Docker smoke | `./scripts/smoke-system-settings-docker.sh` | ✓ 2026-06-28（pytest 8、API 200/403、SPA 200） |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 11:27:21 | `/req-opsx` | 创建 change add-system-settings |
| 2026-06-28 17:10:00 | `/opsx-apply` | P0–P3 全量实现 |
