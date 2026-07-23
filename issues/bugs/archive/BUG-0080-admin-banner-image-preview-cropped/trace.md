---
bug_id: BUG-0080-admin-banner-image-preview-cropped
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-22 08:41:49
updated_at: 2026-07-22 09:36:24
lifecycle:
  captured: 2026-07-22 08:41:49
  generated: 2026-07-22 08:57:22
  completed: 2026-07-22 09:00:41
  reviewed: 2026-07-22 09:15:12
  approved: 2026-07-22 09:15:12
iteration: sprint-010
related_requirement: REQ-0016-banner-management
related_bug: null
related_change: fix-admin-banner-image-preview-cropped
source_command: /capture
captured_via: capture
classification_rationale: 项目已有管理端 Banner 管理能力，列表与编辑弹窗中的 Banner 图片预览未完整显示属于既有 UI 展示行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-admin-banner-image-preview-cropped
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0080-admin-banner-image-preview-cropped
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-22 08:41:49
updated_at: 2026-07-22 09:27:33
lifecycle:
  captured: 2026-07-22 08:41:49
  generated: 2026-07-22 08:57:22
  completed: 2026-07-22 09:00:41
  reviewed: 2026-07-22 09:15:12
  approved: 2026-07-22 09:15:12
iteration: sprint-010
related_requirement: REQ-0016-banner-management
related_bug: null
related_change: fix-admin-banner-image-preview-cropped
source_command: /capture
captured_via: capture
classification_rationale: 项目已有管理端 Banner 管理能力，列表与编辑弹窗中的 Banner 图片预览未完整显示属于既有 UI 展示行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-admin-banner-image-preview-cropped
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: admin_web
  module: banner_management
  page: /admin/banners
  issue_type: image_preview_cropped
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: bug-opsx
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 管理端 Banner 列表和弹窗中的 Banner 图片均显示不全 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| Banner 列表 | 检查图片缩略图是否被裁切、压缩或遮挡 |
| Banner 弹窗 | 检查新建/编辑弹窗中图片预览区域是否被裁切、压缩或遮挡 |
| 图片来源 | 覆盖自定义上传图、品牌 Logo/SKU 主图等图片来源 |
| 图片比例 | 覆盖横幅图、方图、竖图和超宽图 |
| CSS 策略 | 重点检查 `object-fit`、固定尺寸、overflow、表格行高和弹窗预览容器 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 列表图片完整 | Banner 列表缩略图完整呈现图片主体，不裁掉关键信息 |
| 弹窗图片完整 | Banner 弹窗预览完整呈现当前图片，上传和编辑回显一致 |
| 无变形 | 修复不得引入明显拉伸、压扁或比例失真 |
| 布局无回退 | 列表行、弹窗滚动、上传控件和保存按钮布局保持稳定 |
| 回归场景 | 覆盖新建、编辑、保存后回显和不同图片比例 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:35:54 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-banner-image-preview-cropped） |
| 2026-07-22 09:35:32 | /opsx-archive | Change `fix-admin-banner-image-preview-cropped` 已归档，状态同步完成。 |
| 2026-07-22 09:31:35 | /opsx-apply | Change `fix-admin-banner-image-preview-cropped` apply 完成，待 archive。 |
| 2026-07-22 09:27:33 | /sprint-propose | 纳入 `sprint-010` 正式范围 |
| 2026-07-22 09:20:30 | /bug-opsx BUG-0080 | 创建 OpenSpec Change `fix-admin-banner-image-preview-cropped` |
| 2026-07-22 09:15:56 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-22 09:15:12 | /bug-review --approve | 评审通过，允许 bug-opsx 与纳入 Sprint 规划 |
| 2026-07-22 09:00:41 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-22 08:57:22 | /bug-generate | 生成正式 bug.md，状态推进为 draft |
| 2026-07-22 08:41:49 | /capture | 记录管理端 Banner 列表和弹窗图片显示不全缺陷 |

- 2026-07-22 09:35:32 workflow-sync：状态同步为 done（Change archived）
