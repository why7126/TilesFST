---
change_id: update-object-storage-key-layout
requirement_id: REQ-0012-object-storage-key-layout
status: proposed
created_at: 2026-06-28 10:32:00
updated_at: 2026-06-28 10:32:00
---

# Change Trace — update-object-storage-key-layout

## 关联

| 字段 | 值 |
|---|---|
| REQ | REQ-0012-object-storage-key-layout |
| Sprint | sprint-003 |
| 关联 REQ | REQ-0005-brand-management、REQ-0005-user-management、REQ-0006-tile-sku-management |
| 迁移策略 | 方案 A — `scripts/migrate_object_keys.py`（dry-run + apply） |

## 验收 Checklist（无 UI 原型）

| # | 检查项 | acceptance | 实现 | Pass |
|---|---|---|---|---|
| 1 | Key 形态无 YYYY/MM | AC-001～AC-004 | | |
| 2 | images/videos 前缀 | AC-005～AC-008 | | |
| 3 | 四 API resource_type | AC-009～AC-014 | | |
| 4 | /media 读取与安全 | AC-015～AC-017 | | |
| 5 | 迁移脚本 dry-run/apply | AC-018～AC-022 | | |
| 6 | 文档与 pytest | AC-023～AC-030 | | |
| 7 | Docker 冒烟 | AC-029 | | |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 10:32:00 | `/req-opsx` | 创建 change update-object-storage-key-layout |
