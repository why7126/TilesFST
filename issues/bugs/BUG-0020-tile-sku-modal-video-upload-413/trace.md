---
created_at: 2026-06-27 14:01:38
title: 缺陷追踪
purpose: BUG-0020 SKU 弹窗视频上传 413
content: 记录瓷砖 SKU 弹窗视频上传 Request Entity Too Large
owner: product
status: done
note: 纳入 sprint-002；REV-BUG-0020-001 评审通过
iteration: sprint-002
readiness: ready
updated_at: 2026-06-27 15:52:00
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0020-tile-sku-modal-video-upload-413
bug_name: tile-sku-modal-video-upload-413
severity: high
status: done
iteration: sprint-002
related_requirement: REQ-0006-tile-sku-management
related_bug: BUG-0018-tile-sku-modal-video-upload-display
related_change: fix-tile-sku-modal-video-upload-413
suggested_fix_change: fix-tile-sku-modal-video-upload-413
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 14:01:38
  generated: 2026-06-27 15:20:48
  completed: 2026-06-27 15:23:29
  reviewed: 2026-06-27 15:27:53
  approved: 2026-06-27 15:27:53
  opsx_created: 2026-06-27 15:32:00
  opsx_applied: 2026-06-27 15:45:00
openspec_changes:
  - change_id: fix-tile-sku-modal-video-upload-413
    type: fix
    status: archived
    bug_id: BUG-0020-tile-sku-modal-video-upload-413```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready（已评审 approved）

## 3. 分类结论

| 项 | 结论 |
|---|---|
| 根因类型 | infrastructure + config（Nginx body 限制；上传 env 未统一） |
| 主要修复面 | `nginx.conf`、`config.py`、`uploads.py`、`.env.example` |
| 需求条款 | REQ-0006 AC-035（Docker 路径可上传） |
| 关联 BUG | BUG-0018（同链路、上传成功后的 UI 层） |
| 建议 Change | `fix-tile-sku-modal-video-upload-413` |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-27 14:01:38 | `/bug-capture` | 记录 SKU 弹窗视频上传 413 |
| 2026-06-27 15:20:48 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-27 15:23:29 | `/bug-complete` | 补齐 root-cause、workaround、acceptance |
| 2026-06-27 15:27:53 | `/bug-review --approve` | REV-BUG-0020-001 评审通过 |
| 2026-06-27 15:29:57 | `/sprint-propose` | 纳入 sprint-002 正式规划 |
| 2026-06-27 15:32:00 | `/bug-opsx` | 创建 `fix-tile-sku-modal-video-upload-413` |
| 2026-06-27 15:45:00 | `/opsx-apply` | Nginx 512m + env 上传限制；pytest 23 passed；Web 镜像重建 |

## 5. 后续动作

- `/opsx-archive fix-tile-sku-modal-video-upload-413`
