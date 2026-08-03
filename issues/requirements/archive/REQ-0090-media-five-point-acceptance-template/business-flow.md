---
requirement_id: REQ-0090-media-five-point-acceptance-template
status: done
created_at: 2026-08-01 09:50:59
updated_at: 2026-08-01 11:38:21
---

# Business Flow

## 1. 主流程

```text
媒体相关 REQ / BUG / Change / Release
        |
        v
判断是否涉及图片 / 视频 / Logo / 证书图片 / SKU 媒体 / 缩略图 / 小程序渲染
        |
        v
套用媒体五联验收模板
        |
        +--> key：确认 object_key 规范、业务资源关联、历史兼容
        |
        +--> object：确认 MinIO object 存在、类型、大小、权限
        |
        +--> URL：确认后端返回或代理 URL 可访问
        |
        +--> thumbnail benefit：确认缩略图或封面图收益，不适用则说明原因
        |
        +--> miniapp render：确认小程序端渲染、失败态和平台限制
        |
        v
记录状态 pass / fail / n/a / blocked 与证据
        |
        +--> 全部通过或合理 N/A：进入需求验收 / 发布检查结论
        |
        +--> fail：按失败记录发起 /bug-capture
        |
        +--> blocked：补环境、测试资源或配置后重试
```

## 2. 与现有流程关系

| 流程节点 | 关系 |
|---|---|
| `/req-complete` | 本需求补齐模板自身的 user stories、business flow、acceptance 和 trace。 |
| `/req-review` | 评审模板是否可作为后续媒体类验收标准。 |
| `/req-opsx` | 评审通过后创建 OpenSpec Change，确定模板最终落点和接入方式。 |
| Sprint 验收 | 若某 Sprint 包含媒体变更，应引用该模板作为横切检查项。 |
| Release 验收 | 若发布涉及媒体链路、对象存储、缩略图或小程序渲染，应引用该模板补证。 |
| BUG capture | 五联任一维度失败时，可将失败记录转化为独立 BUG。 |

## 3. 失败分支

| 分支 | 处理 |
|---|---|
| key 不符合规范 | 记录实际 key、业务资源、期望 key 形态和影响范围，后续进入对象存储或媒体链路修复。 |
| object 不存在或类型不匹配 | 记录对象存储环境、业务资源、MIME、大小、权限状态和上传入口。 |
| URL 不可访问 | 记录 URL 类型、HTTP 状态、错误码、域名/代理/签名策略和用户可见表现。 |
| 缩略图收益不成立 | 记录缩略图是否存在、尺寸/体积关系、展示入口和不满足收益的证据。 |
| 小程序渲染失败 | 记录小程序页面、组件、环境、域名配置、失败态截图或日志线索。 |
| 验收被阻塞 | 记录阻塞原因、责任环境和重试条件，不得直接标记通过。 |

## 4. 与父 REQ 差异

本需求没有父需求。它不是新增媒体上传能力，而是从对象存储、上传链路、小程序渲染和 Sprint 016 媒体缺陷复盘中抽象出的验收治理模板。

## 5. 模板落点策略

```text
req-complete 阶段：在 acceptance.md 固化模板要求
req-opsx design 阶段：确认长期落点
implementation 阶段：按落点沉淀到 rules/docs/templates 或脚本
archive 阶段：确保后续媒体类需求可引用模板
```
