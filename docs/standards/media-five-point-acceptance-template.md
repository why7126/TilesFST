---
purpose: 媒体五联验收模板
content: key、object、URL、thumbnail benefit、miniapp render 五联验收记录、状态、证据与失败转 BUG 规范
source: REQ-0090-media-five-point-acceptance-template / add-media-five-point-acceptance-template
update_method: 媒体链路、对象存储、小程序渲染或发布验收口径变化时同步更新
created_at: 2026-08-01 10:40:28
updated_at: 2026-08-12 14:54:20
---

# 媒体五联验收模板

## 1. 适用范围

本文档用于媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收报告和发布前检查，统一记录 `key`、`object`、`URL`、`thumbnail benefit`、`miniapp render` 五个维度的验收事实。

适用对象包括图片、视频、Logo、品牌证书图片、SKU 主图、SKU 视频、缩略图、封面图、小程序媒体卡片，以及后续新增的媒体展示或上传链路。

本模板只定义验收证据结构和记录口径，不新增上传接口、缩略图生成流水线、视频转码能力、对象存储架构、API、数据库、Orval、Web 管理端运行时、小程序运行时或 Docker Compose 行为。

小程序媒体相关 REQ、BUG、Change 或发布检查应同时引用 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`。该最佳实践用于细化 DevTools/真机/体验版 Network evidence、测试 helper 和历史对象审计 helper 边界；不替代本模板的 `thumbnail benefit` 维度。

## 2. 状态与必填规则

每个媒体样例的每个五联维度必须使用以下状态之一：

| 状态 | 含义 | 必填补充 |
|---|---|---|
| `pass` | 已验收通过，有可复核证据 | 证据摘要、入口或命令摘要 |
| `fail` | 已验收失败 | 失败现象、影响范围、复现入口、期望结果、实际结果和排查线索 |
| `n/a` | 当前 Change 或场景不涉及该维度 | N/A 理由，不得留空 |
| `blocked` | 环境、账号、网络、依赖、数据或设备阻塞 | 阻塞原因、责任环境、重试条件和当前影响判断 |

`blocked` 不得被视为通过。阻塞项补齐环境或资源后，必须重新记录该维度结果。

媒体样例的整体结论也必须使用 `pass`、`fail`、`n/a`、`blocked` 之一。任一维度为 `fail` 时，整体结论不得为 `pass`；任一必验维度为 `blocked` 时，整体结论不得为 `pass`。

## 3. 五联检查目标

| 维度 | 检查目标 | 通过标准 | 证据字段 | 失败记录要求 |
|---|---|---|---|---|
| `key` | 媒体对象标识与业务资源关系 | `object_key` 或等价脱敏标识符合 MinIO 单桶 + 前缀策略，不使用用户原始文件名 | 媒体类型、业务资源、脱敏 key、前缀、关联记录 | 旧 key / 新 key、命名偏差、业务记录不一致、影响资源 |
| `object` | 对象存储事实 | object 存在，MIME、大小、扩展名、安全校验和权限边界符合预期 | 对象存在性、MIME、size、权限结论、对象来源 | object 缺失、0 字节、类型不符、权限错误、排查入口 |
| `URL` | 受控访问结果 | 相对 URL、公开 URL、签名 URL、代理 URL 或等价受控方式可访问，前端和小程序不直连未授权对象存储 | URL 类型、HTTP 状态、错误码、入口页面或接口、用户可见表现 | 403、404、签名过期、域名错误、代理错误、端上表现 |
| `thumbnail benefit` | 缩略图、封面图或轻量媒体的真实收益 | 说明列表首屏、卡片渲染、弱网体验、带宽节省、后台预览或视频封面识别收益；无缩略图时记录 `n/a` 原因 | 原图与缩略图关系、尺寸或体积摘要、收益说明、适用页面 | 仅生成无收益、体积未降、尺寸异常、封面不匹配 |
| `miniapp render` | 微信小程序端渲染 | 真机或等价预览环境可加载、预览、播放或展示失败态；不涉及小程序时记录 `n/a` 原因 | 页面路径、组件、环境、加载/播放/占位/失败态结论 | 域名限制、组件限制、加载失败、播放失败、占位缺失 |

## 4. 媒体上传横切 Gate

涉及真实上传、上传后回显或媒体表单的 Change 必须保留以下检查；不涉及时标记 `n/a` 并说明原因，不得删除整节。

| Gate | 要求 | N/A 示例 |
|---|---|---|
| 上传状态机 | 检查上传流程覆盖 `idle -> uploading -> done/failed`，成功和失败状态都可见 | `n/a - 仅新增验收模板，不修改上传 UI` |
| 同会话即时回显 | 上传成功后同一会话即时回显缩略图、文件卡片或媒体 URL | `n/a - 无端上上传回显入口` |
| Docker Web 边界 | 经 Docker Web `http://localhost:3000` 或等价用户入口执行边界文件验收，不只调用后端 `:8000` | `n/a - 未执行真实上传链路` |
| 失败信息位置 | 失败信息出现在上传控件、字段组或媒体样例记录中，不只依赖全局 toast | `n/a - 失败记录写入模板样例而非 UI 控件` |

## 5. Markdown 记录模板

| 样例 | 媒体类型 | 业务资源 | key | object | URL | thumbnail benefit | miniapp render | 结论 |
|---|---|---|---|---|---|---|---|---|
| sample-001 | image/video/logo/certificate | 待填写 | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked | pass/fail/n/a/blocked |

每个非 `pass` 单元格必须在下方补充原因：

```markdown
### sample-001 失败 / N/A / blocked 记录

- key：pass；证据：业务记录中的脱敏 object_key 与对象前缀一致。
- object：fail；实际结果：对象存储中未找到对应 object；期望结果：object 存在且 MIME、size 符合上传结果；影响范围：SKU 主图无法展示；复现入口：管理端 SKU 编辑页保存后刷新。
- URL：blocked；原因：测试域名未配置媒体代理；责任环境：测试 Web 网关；重试条件：代理配置完成后重新访问媒体 URL。
- thumbnail benefit：n/a；原因：当前媒体类型为证书 PDF，不生成缩略图。
- miniapp render：n/a；原因：当前 Change 不影响小程序页面或组件。
```

## 6. YAML 记录模板

```yaml
media_five_point_acceptance:
  template_ref: docs/standards/media-five-point-acceptance-template.md
  target:
    type: change
    id: add-media-five-point-acceptance-template
    related_issue: REQ-0090-media-five-point-acceptance-template
  samples:
    - id: sample-001
      media_type: image
      business_resource: "SKU main image / 脱敏资源描述"
      key:
        status: pass
        evidence: "脱敏 object_key 符合 MinIO 单桶 + 前缀策略"
      object:
        status: pass
        evidence: "object 存在，MIME 与 size 符合预期"
      url:
        status: pass
        url_type: proxy_url
        http_status: 200
        evidence: "用户入口可展示媒体，未直连未授权对象存储"
      thumbnail_benefit:
        status: n/a
        reason: "当前场景不使用缩略图或封面图"
      miniapp_render:
        status: blocked
        reason: "缺少可用小程序预览环境"
        retry_condition: "小程序预览环境恢复后重新验证页面渲染"
      conclusion: blocked
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
      status: n/a
      reason: "失败记录写入模板样例"
```

## 7. 失败转 BUG 最小信息

任一五联维度为 `fail` 时，记录必须足以支撑后续 `/bug-capture` 或返修，至少包含：

- 失败现象。
- 影响范围。
- 复现入口。
- 期望结果。
- 实际结果。
- 相关媒体类型、业务资源、脱敏 key 或 URL 摘要。
- 端和环境，例如 Web 管理端、小程序、Docker Web 或发布检查。
- 截图、日志或命令摘要位置；不得粘贴大段日志。

## 8. 后续流程引用方式

| 位置 | 建议写法 |
|---|---|
| REQ `acceptance.md` | 在媒体相关 AC 中引用本模板，并按媒体样例列出五联记录要求 |
| BUG `acceptance.md` | 对媒体类缺陷使用本模板记录失败复现、修复验证和回归证据 |
| OpenSpec `design.md` / `tasks.md` | 在 Cross-cutting Gate 或 Validation 中引用本模板，明确是否涉及真实上传和小程序渲染 |
| Sprint `acceptance-report.md` | 汇总每个媒体 Change 的五联结论、blocked 项和剩余风险 |
| Release 检查 | 对公开媒体、缩略图、封面图和小程序媒体展示引用本模板，记录发布前结论 |

引用示例：

```markdown
媒体链路验收采用 `docs/standards/media-five-point-acceptance-template.md`。本 Change 涉及 SKU 主图和小程序卡片渲染，因此必须按媒体样例记录 key、object、URL、thumbnail benefit、miniapp render；不涉及真实上传的 gate 标记 `n/a` 并说明原因。
```

## 9. 安全与证据边界

允许记录：

- 脱敏后的对象 key、相对 URL、代理 URL 摘要或 HTTP 状态。
- 命令与结果摘要。
- 仓库相对路径形式的截图、录屏、报告或人工验收摘要。
- N/A、blocked、失败现象和剩余风险。

禁止记录：

- 真实客户数据、个人隐私、未脱敏手机号、地址或订单信息。
- 真实密钥、AccessKey、SecretKey、数据库 DSN、MinIO 凭据。
- Authorization header、Cookie、`.env` 内容。
- 本机绝对路径、完整敏感请求体、大段日志或不可公开运维地址。

截图、录屏或报告包含敏感信息时，必须先脱敏；无法公开保存时，只记录人工摘要和不可公开原因。
