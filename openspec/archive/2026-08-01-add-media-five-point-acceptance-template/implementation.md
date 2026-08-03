---
change_id: add-media-five-point-acceptance-template
status: applied
created_at: 2026-08-01 10:40:28
updated_at: 2026-08-01 11:13:14
---

# Implementation

## 长期模板落点

媒体五联验收模板已沉淀到 `docs/standards/media-five-point-acceptance-template.md`。

选择 `docs/standards/` 的原因：

- 该目录已经承载上传规范、测试治理、小程序 evidence 模板和 XL 管理端验收模板，符合长期治理文档边界。
- 媒体五联模板面向 REQ、BUG、OpenSpec Change、Sprint 和 Release 复用，不属于单一需求或单一 Change 的临时证据。
- 本 Change 不修改运行时媒体能力，因此不把模板并入 `rules/media.md` 或对象存储运行时规格，避免把验收口径误读为功能实现。

## 后续引用方式

| 流程 | 引用方式 |
|---|---|
| REQ | 在 `acceptance.md` 的媒体相关 AC 中引用 `docs/standards/media-five-point-acceptance-template.md`，并说明五联维度是否必填或 N/A |
| BUG | 在 `acceptance.md` 中用五联模板记录复现、修复验证和回归证据，失败项可直接转 `/bug-capture` |
| OpenSpec Change | 在 `design.md`、`tasks.md` 或 `trace.md` 中引用模板，说明是否涉及真实上传、小程序渲染和 media-upload 横切 gate |
| Sprint | 在 `acceptance-report.md` 汇总媒体 Change 的五联结论、blocked 项和剩余风险 |
| Release | 对公开媒体、缩略图、封面图和小程序媒体展示执行发布前五联记录 |

## 实现边界

本次实现仅新增长期模板文档、docs 索引和 Change 实现记录。未修改：

- 后端 API、Pydantic schema、数据库 schema 或 migration。
- OpenAPI、Orval 或前端 API client。
- Web 管理端、店主端或小程序运行时代码。
- 上传接口、缩略图生成、视频转码、对象存储架构、MinIO bucket 策略或 Docker Compose 行为。

## 本 Change 的 N/A 记录

```yaml
media_five_point_acceptance:
  template_ref: docs/standards/media-five-point-acceptance-template.md
  target:
    type: change
    id: add-media-five-point-acceptance-template
    related_issue: REQ-0090-media-five-point-acceptance-template
  samples:
    - id: template-na-001
      media_type: governance_template
      business_resource: "媒体五联验收模板"
      key:
        status: n/a
        reason: "本 Change 只新增验收模板，不创建或迁移媒体对象 key"
      object:
        status: n/a
        reason: "本 Change 不写入对象存储"
      url:
        status: n/a
        reason: "本 Change 不新增媒体访问 URL"
      thumbnail_benefit:
        status: n/a
        reason: "本 Change 不生成缩略图或封面图"
      miniapp_render:
        status: n/a
        reason: "本 Change 不修改小程序运行时代码或页面"
      conclusion: pass
  upload_cross_cutting_gate:
    upload_state_machine:
      status: n/a
      reason: "仅模板治理，不修改上传 UI"
    same_session_preview:
      status: n/a
      reason: "无端上上传回显入口"
    docker_web_boundary:
      status: n/a
      reason: "未执行真实上传链路"
    failure_message_location:
      status: pass
      evidence: "模板定义了失败记录最小信息和媒体样例失败记录位置"
```

## 验收返修确认

2026-08-01 11:13:14 复核结论：首次 apply 的功能范围完整，无需补充 API、DB、Orval、Web、小程序、管理端运行时或 Docker Compose 实现。

补充完善项：

- 在长期模板中明确媒体样例整体结论也支持 `pass`、`fail`、`n/a`、`blocked` 四态，并补充 fail/blocked 对整体结论的约束。
- 将 Sprint 验收报告中的 REQ-0090 检查项校准为原始五联：key、object、URL、thumbnail benefit、miniapp render。
