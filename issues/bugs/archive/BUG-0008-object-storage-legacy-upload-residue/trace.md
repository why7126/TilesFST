---
created_at: 2026-06-27 08:42:28
title: 缺陷追踪
purpose: BUG-0008 对象存储修复后本地 uploads 双目录残留与历史数据清理缺失
content: 记录 BUG-0006 修复后 data/uploads 孤儿文件、UPLOAD_DIR 挂载与文档澄清未收敛的问题
owner: product
status: done
lifecycle_stage: archive
note: 已完成 fix-object-storage-legacy-upload-residue archive
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 22:33:15
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0008-object-storage-legacy-upload-residue
bug_name: object-storage-legacy-upload-residue
severity: medium
status: done
iteration: sprint-002
related_requirement: null
related_bug: BUG-0006-object-storage-upload-not-minio
related_change: fix-object-storage-legacy-upload-residue
target_clients:
  web_admin: 否
  backend: 是
  docker: 是
environment: local|docker
lifecycle:
  captured: 2026-06-26 23:49:23
  generated: 2026-06-26 23:54:20
  completed: 2026-06-26 23:55:19
  reviewed: 2026-06-26 23:56:09
  approved: 2026-06-26 23:56:09
  in_sprint: 2026-06-26 23:56:57
  opsx_created: 2026-06-27 00:00:20
  applied: 2026-06-27 00:04:00
  archived: 2026-06-27 08:14:56
openspec_changes:
  - change_id: fix-object-storage-legacy-upload-residue
    type: fix
    status: archived```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（技术债 / 运维清理） |
| 根因类型 | legacy-local-upload / post-migration-cleanup |
| 修复面 | 历史文件清理脚本、data 文档、Docker 挂载收敛、UPLOAD_DIR 配置退役 |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| review | `review.md` |
| 归档 Change | `openspec/changes/archive/2026-06-26-fix-object-storage-legacy-upload-residue/` |
| 正式 spec | `openspec/specs/object-storage/spec.md` |

## 5. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 23:49:23 | `/bug-capture` | 记录双目录残留与历史数据清理策略缺失 |
| 2026-06-26 23:54:20 | `/bug-generate` | 生成正式 `bug.md`，状态更新为 draft |
| 2026-06-26 23:55:19 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态更新为 pending_review |
| 2026-06-26 23:56:09 | `/bug-review --approve` | 评审通过，状态更新为 approved |
| 2026-06-26 23:56:57 | `sprint-scope-update` | 纳入 `sprint-002`，状态更新为 in_sprint |
| 2026-06-27 00:00:20 | `/bug-opsx` | 创建 `fix-object-storage-legacy-upload-residue` |
| 2026-06-27 00:04:00 | `/opsx-apply` | 完成 legacy uploads 清理脚本、UPLOAD_DIR 收敛、文档与测试 |
| 2026-06-27 00:11:29 | `/opsx-archive` | 同步 `object-storage` spec 并归档，状态更新为 done |

## 6. 后续动作

无；BUG-0008 已完成修复、验收与归档。
