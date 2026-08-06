---
note: workflow-sync — 4/4 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-020
status: completed
acceptance_status: passed
created_at: 2026-08-05 09:55:00
updated_at: 2026-08-06 08:23:35
---

# Sprint 020 验收报告

## 验收范围

| 类型 | 编号 | 状态 | 验收要点 |
|---|---|---|---|
| REQ | REQ-0098-admin-media-list-thumbnails | done | SKU/Banner 缩略图字段、前端 fallback、品牌/证书复核、OpenAPI/Orval、测试已随 Change 归档闭环 |
| BUG | BUG-0117-miniapp-privacy-clipboard-phone-drift | done | 小程序提交包无电话/剪贴板隐私接口、home 服务动作收敛、证书文件失败兜底不复制 URL、文档测试同步已随 Change 归档闭环 |
| Change | optimize-admin-media-list-thumbnails | archived | 归档路径：`openspec/archive/2026-08-05-optimize-admin-media-list-thumbnails/` |
| Change | fix-miniapp-privacy-interface-drift | archived | 归档路径：`openspec/archive/2026-08-05-fix-miniapp-privacy-interface-drift/` |
| Change | improve-mintlify-docs-site | archived | 归档路径：`openspec/archive/2026-08-06-improve-mintlify-docs-site/` |
| Change | update-global-thumbnail-size-limit | archived | 归档路径：`openspec/archive/2026-08-05-update-global-thumbnail-size-limit/` |

## 横切验收

- [x] 管理端列表分页 DOM 不回归。
- [x] 图片加载失败不造成表格、sticky action column 或分页布局抖动。
- [x] 不新增 `window.confirm`。
- [x] 如出现 toast，必须为 fixed toast。
- [x] 验收证据包含列表缩略图 URL/render 与详情原图可访问记录。
- [x] 小程序静态扫描确认无 `wx.makePhoneCall` / `wx.setClipboardData`。
- [x] 小程序提审隐私声明复核不再检测电话或剪贴板接口。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 08:21:16
accepted_by: AI workflow gate
evidence:
  - python scripts/validate-sprint-archive-readiness.py --sprint sprint-020
  - openspec/archive/2026-08-05-optimize-admin-media-list-thumbnails/trace.md
  - openspec/archive/2026-08-05-fix-miniapp-privacy-interface-drift/trace.md
  - openspec/archive/2026-08-06-improve-mintlify-docs-site/trace.md
  - openspec/archive/2026-08-05-update-global-thumbnail-size-limit/trace.md
failed_items: []
notes:
  - 4/4 Change 已归档且归档证据为 trace.md present；Sprint close stale scan 后续复核。
```
