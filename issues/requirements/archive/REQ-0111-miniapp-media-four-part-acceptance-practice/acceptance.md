---
requirement_id: REQ-0111-miniapp-media-four-part-acceptance-practice
acceptance_status: passed
created_at: 2026-08-12 14:29:30
updated_at: 2026-08-12 22:03:11
source_change:
source_sprint:
---

# Acceptance

## 功能 AC

- [ ] AC-001 知识库必须新增小程序媒体四联验收最佳实践，覆盖 BUG-0125、BUG-0126 案例，并说明对象存在、`.thumb` URL 存在或接口测试通过均不能单独证明媒体性能验收通过。
- [ ] AC-002 最佳实践必须明确 key -> object -> URL -> render 四联证据链，且说明任一维度不能替代后续维度。
- [ ] AC-003 key 维度必须要求记录业务资源、媒体类型、脱敏 key 摘要、标准前缀、原图 / 缩略图 / 视频 / poster 关系，不得记录真实 object key 全量值。
- [ ] AC-004 object 维度必须要求记录 object 存在性、MIME、大小、扩展名、权限边界、缩略图收益或无收益原因。
- [ ] AC-005 URL 维度必须要求记录 URL 类型、入口接口或页面、HTTP 状态、业务错误码、受控 `/media` 访问、resolved / fallback 结论和缓存相关证据。
- [ ] AC-006 render 维度必须要求记录小程序页面路径、组件、DevTools / 真机 / 体验版 evidence、展示 / 预览 / 播放 / 占位 / 失败态结论。
- [ ] AC-007 每个四联维度必须使用 `pass`、`fail`、`n/a` 或 `blocked`；`blocked` 不得视为通过，`n/a` 必须说明原因。
- [ ] AC-008 Network evidence 规则必须明确 DevTools Network 不等同于体验版或真机网络验收，自动化测试、静态检查、接口 smoke 或 `urlCheck=true` 不得自动替代 Network evidence。
- [ ] AC-009 测试 helper 必须能表达图片展示 URL 优先缩略图、preview URL 保留原图、视频 URL 不被替换、poster / cover 优先轻量图、fallback、lazy-load 和页面模板绑定断言。
- [ ] AC-010 测试 helper 必须能表达受控 `/media/{object_key}` 或等价 URL 语义，不直连未授权对象存储，不暴露 raw object key。
- [ ] AC-011 审计 helper 必须默认 dry-run，支持按资源类型抽样或批量检查 object 存在性、MIME、大小、缩略图是否存在、缩略图是否明显轻量、URL 是否可能 fallback、失败原因枚举和统计摘要。
- [ ] AC-012 审计 helper 输出必须脱敏，使用 key hash、标准前缀、资源类型、计数和失败原因枚举；不得输出真实 object key 全量值、密钥、`.env`、Authorization header、Cookie、本机绝对路径或真实客户数据。
- [ ] AC-013 历史对象审计结果必须分类为已闭环、缺缩略图、缩略图无收益、URL fallback、object 缺失、权限异常或证据不足。
- [ ] AC-014 若需要 apply 回填或重生成，必须要求显式参数、MySQL 与对象存储 bucket / prefix 备份确认、幂等验证、成功 / 失败 / 跳过数量和失败原因。
- [ ] AC-015 最佳实践必须声明只读审计和批处理摘要不能替代小程序受影响页面的 render evidence。
- [ ] AC-016 需求必须明确不新增上传、缩略图生成、视频转码、CDN、缓存、对象存储 provider、生产批量写入默认执行或自动真机云测能力。
- [ ] AC-017 后续 OpenSpec design / tasks 必须引用 `rules/media.md`、`rules/object-storage.md`、`docs/standards/media-bug-four-point-acceptance-template.md`、`docs/standards/media-five-point-acceptance-template.md`、`docs/standards/miniapp-device-evidence-template.md` 中与本需求相关的验收边界。

## 验收记录模板

```yaml
miniapp_media_four_part_acceptance:
  target:
    type: req_or_bug_or_change
    id: ""
  sample:
    media_type: image
    business_resource: "脱敏资源描述"
    page_path: "pages/tile-detail/index"
  checks:
    key:
      status: pass
      evidence: "脱敏 key 摘要、标准前缀、原图/缩略图关系"
    object:
      status: pass
      evidence: "object 存在，MIME/大小/扩展名/权限符合预期，缩略图明显轻量"
    url:
      status: pass
      url_type: media_proxy
      http_status: 200
      fallback: false
      evidence: "受控 /media URL 可访问，未直连未授权对象存储"
    render:
      status: blocked
      evidence: null
      reason: "缺少体验版 Network evidence"
      retry_condition: "体验版上传后补充页面资源加载和用户可见行为记录"
  conclusion: blocked
```

## 横切 AC（knowledge-base）

| 标签 | 来源 | AC 条数 | 结论 |
|---|---|---:|---|
| 无匹配标签 | `docs/knowledge-base/README.md` | 0 | N/A — 本 REQ 不涉及管理端列表页、管理端表单页、管理端弹窗或管理端媒体上传回显。 |

说明：REQ-0111 是小程序媒体治理、文档规范、测试 helper 与审计 helper 需求；未命中 `req-complete` 固定横切标签 `admin-list`、`admin-form`、`admin-modal`、`media-upload`，因此不追加 `AC-XCUT-*`。后续 OpenSpec 仍必须引用本需求列出的媒体与小程序 evidence 规范。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 22:03:11
accepted_by: workflow-sync
source_change: update-miniapp-media-four-part-acceptance-practice
source_sprint: sprint-023
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

