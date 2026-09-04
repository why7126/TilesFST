---
purpose: 小程序 DevTools/真机验收 evidence 模板
content: 微信小程序 DevTools 预览、真机验收、自动化证据、N/A、blocked 与 follow-up 记录规范
source: REQ-0052-miniapp-device-evidence-template / add-miniapp-device-evidence-template
update_method: 小程序设备验收字段、证据边界或 Sprint 验收口径变化时同步更新
created_at: 2026-07-19 18:41:32
updated_at: 2026-08-31 10:23:00
---

# 小程序 DevTools/真机验收 evidence 模板

## 1. 适用范围

本文档用于微信小程序相关 REQ、BUG、OpenSpec Change、Sprint 验收报告和 release note 统一记录设备验收事实。适用对象包括首页、自定义导航栏、分类列表、商品列表、搜索、SKU 详情、品牌页、收藏页、证书页以及后续新增的小程序页面或组件。

本模板不替代自动化测试，也不要求所有 Change 覆盖完整设备矩阵。它用于明确哪些证据已经完成，哪些不适用，哪些被阻塞，哪些需要 follow-up。没有 DevTools 或真机记录时，不得把静态检查或脚本测试写成“设备验收已完成”。

本模板只定义证据结构和记录口径，不新增自动化截图、真机云测、小程序运行时代码、API、数据库、Orval、Docker Compose 或 MinIO 能力。

## 2. 术语与证据边界

| 证据来源 | 可证明 | 不可替代 |
|---|---|---|
| 静态测试 | 文件存在、模板非空、配置合理、规则约束、运行入口同步策略 | 不证明 DevTools 实际渲染通过 |
| 脚本/单元测试 | 数据转换、组件逻辑、页面配置、参数校验或回归条件 | 不证明真机安全区、微信原生能力和真实触控表现 |
| DevTools 预览 | 微信开发者工具中的页面加载、模拟器布局和基础交互 | 不等同于真实设备触控、系统安全区和微信版本差异均通过 |
| DevTools Network | 微信开发者工具 Network 面板中的请求域名、HTTP 状态、业务响应和资源加载 | 不等同于体验版或真机网络链路验收 |
| 真机验收 | 指定设备上的真实运行表现、安全区、状态栏、胶囊避让和触控反馈 | 不覆盖所有设备、系统、微信版本和网络组合 |
| 体验版 Network | 体验版或等价手机体验入口下的生产域名请求、关键页面接口和媒体资源加载 | 不覆盖所有设备、网络运营商和微信版本组合 |
| N/A | 当前 Change 不影响小程序运行态或设备验收对象 | 不可省略原因 |
| follow-up | 可发布但仍需后续人工确认的设备风险 | 不可写成通过 |

## 3. 状态与必填字段

每条 `evidence_items` 记录必须使用以下状态之一：

| 状态 | 含义 | 必填补充 |
|---|---|---|
| `required` | 已识别为必须补齐，尚未执行或尚未记录 | 责任人、目标页面、场景和截止或承接方式 |
| `passed` | 已验收通过，并有可复核证据 | 截图、录屏、命令摘要、人工记录或 artifact 引用 |
| `failed` | 已验收失败 | 失败表现、影响页面、影响范围和后续处理建议 |
| `blocked` | 设备、账号、环境、网络、版本或外部依赖阻塞 | 阻塞原因、责任人和下一步 |
| `not_applicable` | 当前 Change 不需要该类设备验收 | N/A reason，不得留空 |
| `follow_up` | 可发布但保留后续人工确认 | 剩余风险、责任人和承接方式 |

### 3.1 证据来源字段

每条涉及环境、设备或网络的 evidence SHOULD 记录以下字段。历史表格可使用等价列名。

| 字段 | 要求 |
|---|---|
| `evidence_source` | 证据来源，例如 `network_devtools`、`network_trial`、`real_device`、静态校验或人工验收摘要 |
| `verification_boundary` | 当前证据能够证明的范围，以及不能证明的范围 |
| `evidence_ref` | 脱敏命令摘要、截图、报告、artifact 或人工摘要 |

开发阶段 DevTools 预览、DevTools Network、静态校验和开发 API smoke 可支撑开发验收，但不得写作体验版、真机或线上通过。体验版入口、线上域名、线上接口或真机设备暂不可验证时，应记录当前证据来源、不可验证原因、后续承接方式或明确 N/A 理由。`production_only_pending` 仅作为历史兼容字段，不推荐新记录继续使用。

通用字段：

| 字段 | 要求 |
|---|---|
| `template_ref` | 固定记录本模板路径：`docs/standards/miniapp-device-evidence-template.md` |
| `target` | REQ、BUG 或 OpenSpec Change ID |
| `pages` | 页面路径、页面标题、关键 query 参数和验收场景 |
| `evidence_items` | 按自动化、DevTools、真机、N/A、blocked 或 follow-up 分组的证据项 |
| `summary` | 最终结论、阻塞项、剩余风险和后续承接方式 |

## 4. DevTools evidence 字段

DevTools evidence 用于记录微信开发者工具预览结果。仅确认页面可打开时，结论必须说明“不等同于真机验收”。

| 字段 | 要求 |
|---|---|
| `source` | 固定为 `devtools` |
| `status` | 使用 §3 状态 |
| `wechat_devtools_version` | 微信开发者工具版本或可识别版本摘要 |
| `base_library_version` | 小程序基础库版本 |
| `simulator` | 模拟器设备、系统或 viewport 宽度，例如 320、375、430 pt |
| `page_path` | 页面路径和关键 query 参数 |
| `scenario` | 验收场景，例如首页首屏、自定义导航栏、分类列表、SKU 详情页 |
| `evidence_ref` | 截图、录屏、报告的仓库相对路径，或无法保存文件时的人工摘要 |
| `result` | 验收结论、失败表现、阻塞项或剩余风险 |
| `device_equivalence_note` | 是否等同真机验收；通常写“不等同于真机验收” |

## 5. 真机 evidence 字段

涉及自定义导航栏、fixed header、触控区域、分享、返回、关闭、图片预览或页面滚动的 Change，应至少保留一条真机 evidence。无法执行时必须标记 `blocked` 或 `follow_up`，不得写作“真机通过”。

| 字段 | 要求 |
|---|---|
| `source` | 固定为 `real_device` |
| `status` | 使用 §3 状态 |
| `device_model` | 设备型号 |
| `os_version` | 系统类型与版本，例如 iOS 17 或 Android 14 |
| `wechat_version` | 微信版本 |
| `base_library_version` | 小程序基础库版本 |
| `page_path` | 页面路径、关键 query 参数和用户状态 |
| `viewport` | 视口宽度或可识别显示尺寸 |
| `safe_area_result` | 安全区、状态栏和微信原生胶囊避让结论 |
| `touch_result` | 触控区域、滚动、返回、分享或关闭等交互结论 |
| `executor` | 执行人或角色 |
| `executed_at` | 执行时间，使用 `YYYY-MM-DD HH:mm:ss` |
| `evidence_ref` | 截图、录屏或报告的仓库相对路径或稳定 artifact 引用 |
| `remaining_risk` | 剩余风险；无风险写“无” |

## 6. Network evidence 字段

Network evidence 用于记录小程序发布前的真实请求链路。静态测试、生产接口 smoke 和 `urlCheck=true` 只能作为自动门禁结果，不得自动替代 `network_devtools` 或 `network_trial` 人工结论。

| 字段 | 要求 |
|---|---|
| `source` | 固定为 `network_devtools` 或 `network_trial` |
| `status` | 使用 §3 状态；缺少体验版 Network evidence 时不得写作 `passed` |
| `wechat_devtools_version` | `network_devtools` 必填：微信开发者工具版本或可识别版本摘要 |
| `base_library_version` | 小程序基础库版本 |
| `runtime_strategy` | 运行策略，例如 `prod`、`auto` 或人工确认摘要 |
| `url_check` | `urlCheck` 状态；发布准备应记录为 `true` 或阻塞原因 |
| `trial_entry` | `network_trial` 必填：体验版来源、最新版本确认方式、重新扫码或等价入口确认 |
| `page_path` | 页面路径、关键 query 和验证场景 |
| `request_domain` | 关键请求域名，发布前应确认生产 API 域名 |
| `http_status` | 关键 API HTTP 状态摘要 |
| `business_status` | 业务响应状态摘要，例如 `code=0` 或失败原因 |
| `resource_result` | 图片、视频、证书图片、受控媒体 URL 或静态资源加载结论 |
| `failure_or_blocker` | `failed` / `blocked` / `follow_up` 时必填：失败表现、阻塞原因、剩余风险和下一步 |
| `network_equivalence_note` | `network_devtools` 必须说明“不等同于体验版或真机网络验收” |

`network_devtools` 在开发阶段可作为开发验收证据；若线上 API、线上域名、体验版入口或真机 Network 暂不可验证，应记录当前证据来源、不可验证原因、后续承接方式或明确 N/A 理由。缺少体验版或线上 Network evidence 时仍不得写作体验版或线上通过。

媒体资源 Network evidence 还应补充以下字段，详见 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`：

| 字段 | 要求 |
|---|---|
| `media_kind` | `image`、`video`、`poster`、`cover`、`thumbnail`、`certificate_image` 或 `static_asset` |
| `media_url_type` | `controlled_media_url`、`static_asset`、`signed_url`、`fallback` 或明确 `n/a` |
| `resource_bytes` | Network 面板可见资源大小摘要；不得记录完整 HAR 或敏感 header |
| `duration_ms` | Network 面板可见耗时摘要 |
| `render_result` | 图片展示、preview、视频播放、poster/cover、fallback、lazy-load 或失败态结论 |

## 7. 安全与证据记录规则

允许记录：

- 命令与结果摘要，例如 `python -m pytest tests/test_miniapp_static.py` 通过。
- DevTools 或真机截图、录屏、报告的仓库相对路径。
- 人工验收摘要、失败表现、阻塞原因和剩余风险。
- 页面路径、基础库版本、设备型号、系统版本、微信版本、视口宽度、请求域名、HTTP 状态、业务响应状态和资源加载结论摘要。

禁止记录：

- 本机绝对路径。
- token、Cookie、Authorization header。
- `.env` 内容、真实密钥、数据库 DSN、MinIO 凭据。
- 真实客户数据、未脱敏手机号、地址或个人隐私。
- 大段日志、完整网络日志、HAR 原文、完整构建输出或无法复核的口头描述。

截图、录屏或报告包含敏感信息时，必须先脱敏；无法公开保存时，只记录人工摘要和不可公开原因。

## 8. 可复制 YAML 模板

```yaml
miniapp_device_evidence:
  template_ref: docs/standards/miniapp-device-evidence-template.md
  target:
    type: change
    id: add-miniapp-device-evidence-template
    related_issue: REQ-0052-miniapp-device-evidence-template
  pages:
    - page_path: "pages/index/index"
      title: "首页"
      query: ""
      scenarios:
        - "首页首屏"
        - "自定义导航栏避让"
        - "全部产品瀑布流"
  evidence_items:
    - id: static-001
      source: static_test
      status: passed
      page_path: "pages/index/index"
      scenario: "运行入口与页面结构静态校验"
      command: "python -m pytest tests/test_miniapp_static.py"
      evidence_ref: "测试通过摘要，非完整日志"
      result: "静态测试通过；不证明 DevTools 或真机通过"
      remaining_risk: "仍需 DevTools / 真机确认真实渲染"
    - id: devtools-001
      source: devtools
      status: required
      wechat_devtools_version: "待填写"
      base_library_version: "待填写"
      simulator: "iPhone 12 / 375 pt 或等价"
      page_path: "pages/index/index"
      scenario: "首页首屏不被 fixed header 遮挡"
      evidence_ref: "待填写仓库相对路径或人工摘要"
      result: "待验收"
      device_equivalence_note: "DevTools 不等同于真机验收"
      remaining_risk: "待确认"
    - id: device-001
      source: real_device
      status: follow_up
      device_model: "iPhone 或 Android 真机，待填写"
      os_version: "待填写"
      wechat_version: "待填写"
      base_library_version: "待填写"
      page_path: "pages/index/index"
      viewport: "待填写"
      safe_area_result: "待填写状态栏与胶囊避让结论"
      touch_result: "待填写触控、滚动、返回或分享结论"
      executor: "tester"
      executed_at: "YYYY-MM-DD HH:mm:ss"
      evidence_ref: "待填写仓库相对路径或稳定 artifact 引用"
      remaining_risk: "缺少指定真机验收，发布后保留 follow-up"
    - id: network-devtools-001
      source: network_devtools
      status: required
      wechat_devtools_version: "待填写"
      base_library_version: "待填写"
      runtime_strategy: "prod"
      url_check: true
      page_path: "pages/index/index"
      request_domain: "https://tilesfst.wjoyhappy.site"
      http_status: "待填写"
      business_status: "待填写"
      media_kind: "image/video/poster/cover/thumbnail/static_asset 或 n/a"
      media_url_type: "controlled_media_url/static_asset/signed_url/fallback 或 n/a"
      resource_bytes: "待填写资源大小摘要"
      duration_ms: "待填写耗时摘要"
      render_result: "待填写展示、预览、播放、poster/cover、fallback 或失败态结论"
      resource_result: "首页聚合接口、Banner、推荐商品和静态资源待检查"
      result: "待人工执行 DevTools Network 检查"
      network_equivalence_note: "DevTools Network 不等同于体验版或真机网络验收"
      remaining_risk: "体验版 Network evidence 仍需单独记录"
    - id: network-trial-001
      source: network_trial
      status: required
      trial_entry: "最新体验版二维码；手机删除旧体验版入口后重新扫码"
      base_library_version: "待填写"
      page_path: "pages/index/index；pages/product-list/index；pages/tile-detail/index 或 pages/certificate-detail/index"
      request_domain: "https://tilesfst.wjoyhappy.site"
      http_status: "待填写"
      business_status: "待填写"
      media_kind: "image/video/poster/cover/thumbnail/static_asset 或 n/a"
      media_url_type: "controlled_media_url/static_asset/signed_url/fallback 或 n/a"
      resource_bytes: "待填写资源大小摘要"
      duration_ms: "待填写耗时摘要"
      render_result: "待填写展示、预览、播放、poster/cover、fallback 或失败态结论"
      resource_result: "首页、列表页、详情或媒体资源加载待检查"
      failure_or_blocker: "若无法执行，记录 blocked、follow_up 或明确 not_applicable 原因"
      remaining_risk: "待确认"
    - id: na-001
      source: real_device
      status: not_applicable
      page_path: ""
      scenario: "仅新增模板文档"
      na_reason: "本 Change 不修改小程序运行时代码、页面渲染、触控、安全区或真实运行入口"
      remaining_risk: "无"
  summary:
    status: follow_up
    conclusion: "自动化、DevTools、真机和 N/A 结论已分层记录"
    blockers: []
    remaining_risks:
      - "无真机 evidence 时不得写成真机通过"
    next_owner: "tester"
```

## 9. Markdown 表格模板

| ID | 来源 | 状态 | 页面 / 场景 | 环境 | 证据 | 结论 | 剩余风险 / 原因 |
|---|---|---|---|---|---|---|---|
| static-001 | static_test | passed | `pages/index/index` / 运行入口 | pytest | `python -m pytest tests/test_miniapp_static.py` 摘要 | 静态校验通过 | 不证明 DevTools 或真机通过 |
| devtools-001 | devtools | required | `pages/index/index` / 首页首屏 | DevTools 版本、基础库、375 pt | 待填写截图或人工摘要 | 待验收；不等同真机 | 待补 DevTools evidence |
| device-001 | real_device | follow_up | `pages/index/index` / 胶囊避让 | 机型、系统、微信、基础库 | 待填写截图或录屏 | 可发布但需补真机 | 缺 Android 或 iOS 指定设备 |
| network-devtools-001 | network_devtools | required | `pages/index/index` / 首页 Network | DevTools 版本、基础库、prod、urlCheck=true | 待填写人工摘要 | 待验收；不等同体验版或真机网络验收 | 待补体验版 Network |
| network-trial-001 | network_trial | required | 首页、列表页、详情或媒体资源页 | 最新体验版入口、生产 API 域名 | 待填写人工摘要 | 待验收 | 缺失时记录 blocked / follow_up / not_applicable |
| na-001 | real_device | not_applicable | 仅新增模板文档 | N/A | N/A reason | 不涉及小程序运行态 | 无 |

## 10. 后续流程引用方式

| 位置 | 建议写法 |
|---|---|
| REQ `acceptance.md` | 在测试与验证章节引用本模板，并明确 DevTools / 真机 / N/A / follow-up 的 AC |
| OpenSpec `tasks.md` | 将 DevTools 或真机 evidence 作为人工验收任务，任务完成后记录仓库相对证据路径或人工摘要 |
| Change `trace.md` / `acceptance.md` | 汇总每类 evidence 状态、结论、阻塞项和剩余风险 |
| Sprint `acceptance-report.md` | 只汇总设备验收通过、阻塞、N/A 或 follow-up，不复制完整证据 |
| release note | 只记录用户可理解的设备验收结论和剩余风险，不复制完整 evidence |
| `/miniapp-prepare` | 输出自动门禁结果后，将 DevTools Network 与体验版 Network 作为待人工执行 checklist |
| `/miniapp-confirm` | 记录 DevTools Network、体验版 Network、失败项、阻塞项、剩余风险和下一步 |

引用示例：

```markdown
设备验收 evidence 采用 `docs/standards/miniapp-device-evidence-template.md`。本 Change 影响自定义导航栏和 fixed header，因此 DevTools evidence 为 `required`，真机 evidence 至少保留一条；若无法执行真机验收，标记 `blocked` 或 `follow_up` 并写明原因。
```

## 11. 本 Change 的 N/A evidence

`add-miniapp-device-evidence-template` 仅新增本文档和轻量校验，不修改小程序运行时代码、页面渲染、触控、安全区、微信原生能力或真实运行入口。

```yaml
miniapp_device_evidence:
  template_ref: docs/standards/miniapp-device-evidence-template.md
  target:
    type: change
    id: add-miniapp-device-evidence-template
    related_issue: REQ-0052-miniapp-device-evidence-template
  evidence_items:
    - id: devtools-na-001
      source: devtools
      status: not_applicable
      scenario: "仅新增设备验收模板文档"
      na_reason: "不修改小程序页面、组件、样式、服务、配置或真实运行入口"
      remaining_risk: "无"
    - id: real-device-na-001
      source: real_device
      status: not_applicable
      scenario: "仅新增设备验收模板文档"
      na_reason: "不影响真实设备渲染、触控、安全区、状态栏或微信原生胶囊"
      remaining_risk: "无"
  summary:
    status: passed
    conclusion: "模板能力已建立；本 Change 的 DevTools 与真机验收为 N/A"
    blockers: []
    remaining_risks: []
```

## 12. 复盘来源

本模板承接 `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 中“小程序设备验收建立独立 Gate”“设备/视口验收残留”和“自动化覆盖与设备验收拆成不同任务状态”的经验。后续小程序 Sprint 应优先引用本模板，避免 DevTools、真机、自动化和人工 follow-up 结论再次散落。
