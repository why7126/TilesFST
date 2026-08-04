---
purpose: 媒体类 BUG 四联验收模板
content: 媒体类缺陷修复后的原 BUG 场景、key、object、URL、render 四联验收记录、状态、证据与返修规范
source: REQ-0091-media-bug-four-point-acceptance-template / add-media-bug-four-point-acceptance-template
update_method: 媒体 BUG 验收口径、对象存储策略、小程序证据或上传链路治理变化时同步更新
created_at: 2026-08-01 11:04:15
updated_at: 2026-08-04 09:05:00
---

# 媒体类 BUG 四联验收模板

## 1. 适用范围

本文档用于媒体类 BUG 修复、返修、回归测试、Sprint 验收和发布前检查。凡 BUG 涉及图片、视频、Logo、品牌证书、SKU 主图、SKU 视频、缩略图、封面图、小程序媒体卡片、媒体代理 URL、对象存储 key 或上传回显，均必须使用本模板。

非媒体 BUG 可标记 `n/a`，但必须说明原因。例如：`n/a - 本 BUG 仅涉及文本筛选条件，不读写媒体 key、object、URL 或端侧渲染`。

本模板聚焦 BUG 修复闭环，不新增上传接口、对象存储 provider、Bucket、签名 URL 策略、缩略图生成、视频转码、API、数据库、Orval、Web 管理端运行时、小程序运行时或 Docker Compose 行为。

与 `docs/standards/media-five-point-acceptance-template.md` 的关系：

- 媒体五联模板用于媒体相关 REQ、Change、发布验收和通用能力治理，额外覆盖 `thumbnail benefit`。
- 媒体 BUG 四联模板用于缺陷修复闭环，先还原原 BUG 场景，再验证 `key`、`object`、`URL`、`render` 是否一起恢复。
- 当原 BUG 涉及缩略图、封面图、历史回填或媒体性能收益时，缩略图收益必须写入 `object`、`URL` 或 `render` 证据；如需独立评估体积/尺寸收益，可同时引用五联模板。

## 2. 状态与证据规则

每个维度必须使用以下状态之一，禁止留空：

| 状态 | 含义 | 必填补充 |
|---|---|---|
| `pass` | 已验收通过，有可复核证据 | 证据摘要、入口、命令摘要、截图/录屏位置或人工验收摘要 |
| `fail` | 已验收失败 | 实际结果、期望结果、复现步骤、影响范围和排查线索 |
| `n/a` | 当前 BUG 不涉及该维度、端或 evidence | N/A 原因和影响判断 |
| `blocked` | 环境、账号、域名、MinIO、网络、设备、数据或小程序体验版阻塞 | 阻塞原因、缺失资源、责任环境、重试条件和补证方式 |

`blocked` 不得视为通过。阻塞解除后必须重新记录对应维度结果。

## 3. 原 BUG 场景

每次四联验收必须先记录原 BUG 场景，避免只验证修复后的单点表现。

| 字段 | 内容 |
|---|---|
| BUG | BUG-xxxx |
| 标题 |  |
| 严重等级 | blocker / critical / high / medium / low |
| 影响范围 | Web 管理端 / 店主 Web / 小程序 / 后端接口 / 对象存储 / 发布检查 |
| 复现入口 | 页面、接口、脚本或操作路径 |
| 受影响端 | admin / web / miniapp / backend / storage |
| 环境 | local / docker-web-3000 / test / miniapp-devtools / miniapp-device / miniapp-trial / prod |
| 媒体类型 | image / video / logo / certificate / thumbnail / cover / other |
| 业务资源 | 脱敏资源描述，不记录真实客户数据 |
| 修复前实际结果 |  |
| 修复后期望结果 |  |

## 4. 四联检查目标

| 维度 | 检查目标 | 通过标准 | 证据字段 | 失败记录要求 |
|---|---|---|---|---|
| `key` | 业务记录中的媒体对象标识 | `object_key` 或等价脱敏标识稳定、可追溯，符合单 Bucket 与标准前缀策略 | 媒体类型、业务资源、脱敏 key、前缀、旧 key / 新 key、关联记录 | 用户原始文件名、本机绝对路径、临时路径、未脱敏内部路径、历史 key 兼容失败 |
| `object` | 对象存储事实 | object 真实存在，与业务记录 key 对应，MIME、大小、扩展名、权限边界和可读性符合预期 | object 存在性、MIME、size、扩展名、权限结论、对象来源、缩略图/封面关系 | object 缺失、0 字节、类型不符、权限错误、存储环境不可用、缩略图名义存在但无收益 |
| `URL` | 受控访问结果 | 相对 URL、公开 URL、签名 URL、代理 URL 或等价受控方式可访问，客户端不直连未授权对象存储 | URL 类型、页面或接口入口、HTTP 状态、业务错误码、用户可见表现 | 403、404、签名过期、代理错误、域名错误、后端与对象 key 不一致 |
| `render` | 端侧用户可见行为 | 受影响端可展示、预览、播放、占位或展示失败态，且符合平台限制 | 端、页面/组件、截图/录屏/日志摘要、失败态、小程序 DevTools/真机/体验版 evidence | 管理端预览失败、列表缩略图缺失、店主 Web 不显示、小程序域名/组件限制、依赖 Web 专属 API |

品牌证书类媒体 BUG 必须在 `key` 维度明确区分图片与 PDF/文档：JPG、PNG、WebP 证书图片 key 和缩略图 key 应使用 `images/default/brand-certificates/` 或等价标准图片前缀；PDF/文档证书 key 应使用 `files/default/brand-certificates/`。涉及历史 `files/` 图片 key 时，`object` 维度必须记录 dry-run/apply/幂等迁移摘要。

## 5. Markdown 记录模板

```markdown
## 媒体类 BUG 四联验收

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-xxxx |
| 标题 |  |
| 严重等级 |  |
| 影响范围 |  |
| 复现入口 |  |
| 受影响端 |  |
| 环境 |  |
| 媒体类型 |  |
| 业务资源 |  |
| 修复前实际结果 |  |
| 修复后期望结果 |  |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass / fail / n/a / blocked | 媒体类型、业务资源、脱敏 object_key、前缀策略 |  |
| object | pass / fail / n/a / blocked | object 存在性、MIME、大小、扩展名、权限、缩略图/封面关系 |  |
| URL | pass / fail / n/a / blocked | URL 类型、入口、HTTP 状态、业务错误码、用户可见表现 |  |
| render | pass / fail / n/a / blocked | 端、页面/组件、截图/录屏/日志摘要、失败态 |  |

### 非 pass 记录

- key：n/a；原因：当前 BUG 不涉及媒体对象 key 读写；影响判断：无需对象存储验证。
- object：fail；实际结果：对象存储中未找到对应 object；期望结果：object 存在且 MIME、size 符合上传结果；影响范围：SKU 主图无法展示；复现入口：管理端 SKU 编辑页保存后刷新。
- URL：blocked；原因：测试域名未配置媒体代理；责任环境：测试 Web 网关；重试条件：代理配置完成后重新访问媒体 URL。
- render：pass；证据：小程序 DevTools 商品卡片显示 fallback，未出现白屏或崩溃。
```

## 6. YAML 记录模板

```yaml
media_bug_four_point_acceptance:
  template_ref: docs/standards/media-bug-four-point-acceptance-template.md
  bug:
    id: BUG-xxxx
    title: ""
    severity: high
    impact_scope:
      - admin
      - miniapp
    entry: ""
    environment: docker-web-3000
    media_type: image
    business_resource: "脱敏资源描述"
    before_actual: ""
    after_expected: ""
  checks:
    key:
      status: pass
      evidence: "脱敏 object_key 符合单桶 + 标准前缀策略"
    object:
      status: pass
      evidence: "object 存在，MIME、size、扩展名和权限符合预期"
    url:
      status: pass
      url_type: proxy_url
      http_status: 200
      business_error_code: null
      evidence: "用户入口通过后端受控 URL 可读取媒体"
    render:
      status: blocked
      evidence: null
      reason: "缺少可用小程序体验版"
      retry_condition: "体验版发布后补充 Network 和页面 evidence"
  conclusion: blocked
```

## 7. 媒体上传横切检查项

涉及上传、编辑、列表回显、历史对象、缩略图、回填或审计脚本的媒体 BUG，必须补充以下检查；不涉及时标记 `n/a` 并说明原因，不得删除整节。

| Gate | 要求 | N/A 示例 |
|---|---|---|
| 上传状态机 | 记录 `idle -> uploading -> done/failed` 或等价状态证据，失败必须能在控件或验收记录中定位 | `n/a - 本 BUG 只修历史 URL 兼容，不涉及上传入口` |
| 同会话即时回显 | Web 管理端上传、编辑或列表刷新必须记录同一会话即时回显 evidence | `n/a - 无管理端上传或编辑入口` |
| Docker Web 边界 | 上传大小、Nginx 或 Docker Web 边界相关 BUG 必须经 `http://localhost:3000` 或等价 Web 入口验证边界文件 | `n/a - 本 BUG 不涉及文件大小、Nginx 或上传入口` |
| 媒体代理一致性 | 验证 `object_key` 与 `/media/{object_key}` 或等价受控 URL 一致，不能只验证对象存储存在 | `n/a - 当前 BUG 不读媒体 URL` |
| 历史对象与审计 | 历史对象、缩略图、回填或审计脚本必须记录 dry-run、apply、幂等性或统计摘要 | `n/a - 当前 BUG 不涉及历史数据或脚本` |
| 小程序 evidence | 小程序媒体 BUG 必须记录 DevTools、真机或体验版 evidence；无法补齐时进入 Release 前检查清单 | `n/a - 当前 BUG 不影响小程序页面或组件` |

## 8. 流程嵌入

| 位置 | 要求 |
|---|---|
| BUG `acceptance.md` | 媒体类 BUG 必须引用本模板，并按原 BUG 场景和四联维度记录修复验收 |
| OpenSpec `design.md` / `tasks.md` | 涉及媒体 BUG 修复时列出四联验收计划、N/A 维度和 blocked 补证方式 |
| Sprint `acceptance-report.md` | 汇总媒体 BUG 四联结论、blocked 项、Release 前补证项和剩余风险 |
| Release 检查 | 对小程序体验版、真实域名、历史对象、公开媒体 URL 等发布前证据补齐结论 |

Workflow Sync 管辖的 Sprint Scope marker 块不得手工编辑。若四联验收结论需要进入 Sprint 报告，只能写入非 marker 的验收摘要、风险或发布前补证清单。

本模板不修改 `.agents/skills/bug-*` 行为，不会自动创建 follow-up Issue。若任一维度为 `fail` 且需要新增缺陷，必须由人工或当前命令显式触发 `/bug-capture`、`/capture` 或返修流程。

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
