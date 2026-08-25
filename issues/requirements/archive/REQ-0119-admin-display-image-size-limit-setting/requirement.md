---
requirement_id: REQ-0119-admin-display-image-size-limit-setting
title: 管理端媒体与存储新增 display 图体积目标上限配置
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-22 21:16:01
updated_at: 2026-08-25 14:53:29
related_change: add-admin-display-image-size-limit-setting
---

# REQ-0119 管理端媒体与存储新增 display 图体积目标上限配置

## 1. 需求背景

系统已具备图片 `thumbnail`、`display`、`original` 三规格能力。其中 `thumbnail` 用于列表、卡片和轻量预览，`display` 用于详情普通展示和图册浏览，`original` 用于高清预览、下载或需要保真的场景。

当前管理端「系统设置 - 媒体与存储」已提供 `media.thumbnail_max_size_kb`，用于配置缩略图体积目标上限。但 `.display` 图的体积目标仍由后端代码常量固定为 768KB，管理员无法在不同部署环境、网络条件或展示策略下独立调整详情展示图的清晰度与流量平衡。

本需求要求新增 display 图体积目标上限配置，默认值沿用 768KB，并保持其与缩略图体积目标相互独立。该配置只影响后续新生成或维护任务重生成的 `.display` 图，不在保存系统设置时自动扫描或覆盖历史对象。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 后台系统管理员 | 在不改代码、不重新发布的情况下调整详情展示图体积目标。 |
| 后台运营人员 | 在商品详情、图册浏览等场景中获得可控的清晰度与加载体验。 |
| 小程序用户 / 店主 Web 访客 | 间接受益于更适合网络环境的详情展示图，减少过大图片带来的等待和流量消耗。 |
| 运维 / QA | 能明确配置默认值、生效范围、历史对象处理边界和回归验证方式。 |
| 前后端开发 | 有统一字段与契约，避免 display 图继续依赖代码硬编码。 |

## 3. 需求目标

- 在管理端「系统设置 - 媒体与存储」新增 display 图体积目标上限配置。
- 默认 effective 值 MUST 沿用现有 display 图目标体积 `768KB`。
- display 图体积目标 MUST 独立于缩略图体积目标，不能复用 `media.thumbnail_max_size_kb`。
- 新上传、新正式化和维护任务重生成 `.display` 图时读取该 effective 配置。
- 保存设置 MUST NOT 自动批量读取、扫描、覆盖或重建历史 `.display` 对象。
- 字段变化 MUST 同步后端系统设置 API、OpenAPI / Orval、管理端页面、测试和媒体 / 对象存储文档。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 全局配置项 | 新增 display 图体积目标上限配置，建议字段语义为 `media.display_max_size_kb` 或等价命名。 |
| 默认值 | 默认 effective 值为 `768`，对齐现有 display 图硬编码目标。 |
| 管理后台入口 | 在「系统设置 - 媒体与存储」展示和编辑该字段，和缩略图体积目标处于同一媒体策略区域。 |
| 后端有效配置 | 系统设置 GET / PATCH / reset 支持该字段，上传和维护任务生成 display 图时读取同一 effective 值。 |
| 多规格图片生成 | `.display` 图生成继续使用既有最大宽高、质量和同目录 `.display` key 规则，仅将体积目标从常量改为配置。 |
| 历史处理边界 | 保存设置不自动重建历史对象；历史 `.display` 重生成必须通过受控维护任务。 |
| API / 类型同步 | 系统设置字段新增需要同步 OpenAPI、Orval 和前端类型消费。 |
| 测试覆盖 | 覆盖默认值、读写重置、上传生成、维护任务读取配置、与缩略图配置互不影响。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 改变多规格 key 模型 | 不改变同目录 `.thumb`、`.display` 和原图 key 推导规则。 |
| 自动重建历史 display 图 | 保存系统设置时不得自动扫描对象存储或覆盖历史 `.display` 对象。 |
| 单资源差异化配置 | 不为 SKU、品牌 Logo、Banner、证书图片分别设置 display 体积目标。 |
| 新增图片格式转换策略 | 不默认把 display 图从原格式转换为 WebP；格式策略如需变化应另行明确。 |
| 视频多清晰度或封面体积配置 | 本需求仅覆盖图片 `.display` 规格，不覆盖视频转码、视频封面或多清晰度播放。 |
| 独立媒体处理控制台 | 不新增独立运维页面或批处理操作入口。 |
| 前端展示重设计 | 不重做商品详情、图册、列表或上传组件视觉布局。 |

## 5. 功能要求

### FR-001 display 图体积目标配置

系统 MUST 新增 display 图体积目标上限配置。该配置 MUST 使用 KB 作为单位，默认值 MUST 为 `768`。

建议配置语义：

```text
display_max_size_kb = 768   表示生成 display 图时尽量控制在 768KB 以内
```

该配置 MUST 有后端校验。字段最终命名、是否支持 `0` 表示不限制、以及允许范围需要在后续需求完善或 OpenSpec 阶段收敛。若采用 `0` 表示不限制，API、管理端 UI、默认值、reset 和文档 MUST 保持一致语义。

### FR-002 管理后台媒体与存储入口

管理后台「系统设置 - 媒体与存储」MUST 提供 display 图体积目标上限配置入口。该入口 SHOULD 与「缩略图体积目标上限 (KB)」放在同一组媒体生成策略区域，避免被误解为上传原文件大小限制。

UI 文案 MUST 避免承诺绝对必达，推荐使用“目标上限”“尽量不超过”等表达，并明确：

- 默认值为 `768KB`。
- 该配置控制详情展示图或 display 图，不控制列表缩略图。
- 保存后仅对新生成或维护任务重生成的 display 图生效。
- 历史 display 图需要通过维护任务重生成。

### FR-003 与缩略图配置独立

系统 MUST 保持 display 图体积目标与缩略图体积目标独立。

- `.thumb` 继续读取 `media.thumbnail_max_size_kb` 或等价缩略图配置。
- `.display` MUST 读取新增 display 图体积目标配置。
- 管理员修改缩略图体积目标时，MUST NOT 隐式改变 display 图体积目标。
- 管理员修改 display 图体积目标时，MUST NOT 隐式改变缩略图体积目标。

该独立性用于避免列表图压缩策略伤害详情图清晰度，也避免详情图默认目标导致列表图过大。

### FR-004 配置对 display 图生成场景生效

系统 MUST 将该配置应用于所有后端生成 `.display` 图的场景，包括但不限于：

- SKU 图片上传生成 display 图。
- SKU pending 图片正式化时复制或补生成 display 图。
- 品牌 Logo、Banner 图片、品牌证书图片等图片资源的多规格生成或维护任务。
- 存量图片多规格维护任务中 `.display` 图缺失或不合格时的重生成。

若某类图片资源暂不生成 `.display` 图，需求文档、OpenSpec 或实现记录 MUST 明确不适用原因，避免误写为已覆盖。

### FR-005 Key、URL 与格式策略保持稳定

本需求 MUST 保持现有同目录 `.display` key / URL 推导规则稳定。配置变更只影响 display 图对象的内容、编码质量、像素尺寸和最终体积目标，不影响资源寻址。

示例：

```text
images/default/tiles/1/main.webp
  -> images/default/tiles/1/main.display.webp
```

系统设置新增字段不得要求新增业务表 `display_key` 字段，不得改变既有 `display_url`、`original_url` 或受控 `/media/...` 读取语义。若 OpenSpec 实现阶段发现接口字段或 schema 已存在生成物差异，必须同步 OpenAPI / Orval / API 文档和测试。

### FR-006 增量生效与历史处理边界

管理员保存 display 图体积目标后，系统 MUST 默认只对后续新生成的 `.display` 图生效，包括新上传、新正式化和后续维护任务重生成。

系统 MUST NOT 在保存设置时自动批量读取原图、覆盖历史 `.display` 对象或重建历史 display 图。该限制用于避免不可预期的对象存储 I/O、CPU 消耗、缓存变化和线上展示抖动。

历史 `.display` 图如需应用新策略，MUST 通过受控维护任务处理。维护任务 SHOULD 支持 dry-run 预览影响数量、跳过原因、失败原因和预计写入对象数量；apply 执行时 SHOULD 记录成功、失败、跳过与重试候选。

### FR-007 生成策略与未达标处理

当配置了 display 图目标体积上限时，系统 SHOULD 沿用既有图片派生压缩策略，例如：

1. 按 display 图最大宽高和默认质量生成。
2. 若超过目标上限，对 JPEG / WebP 递减质量。
3. 若仍超过目标上限，可按比例降低尺寸后重新生成。
4. 对 PNG、透明图和复杂纹理图片，应优先保证可用性与透明度处理正确，再尽量控制体积。

若最终仍无法达到目标上限，系统 MUST 不阻断原图上传、业务保存或维护任务整体执行。系统 SHOULD 记录 warning、任务链路信息或维护任务失败原因，便于后续排查。

### FR-008 默认行为与向后兼容

新增配置的默认值 MUST 对齐当前 display 图目标体积 `768KB`，避免升级后改变现有 display 图生成效果。

新增字段 MUST 向后兼容：

- 不移除现有媒体设置字段。
- 不改变现有上传接口返回的 `display_key`、`display_url`、`thumbnail_key`、`thumbnail_url`、`original_url` 语义。
- 不改变对象存储 bucket、前缀、key 生成规则或权限读取边界。
- 不要求小程序或店主 Web 因系统设置字段新增而改造页面逻辑。

## 6. UI 约束

- 管理后台入口应复用现有「系统设置 - 媒体与存储」页面结构，不新增独立页面。
- 字段建议展示为“详情展示图体积目标上限 (KB)”或“display 图体积目标上限 (KB)”。若面向业务用户，优先使用“详情展示图”。
- 控件应使用现有设置页表单样式、数字输入或既有选择控件，保持暗色旗舰风与 Design System 语义 token。
- 帮助文案应明确“默认 768KB”“仅影响新生成 display 图”“历史需通过维护任务重生成”“与缩略图体积目标独立”。
- 不应在页面内展示过长技术说明、对象 Key 细节或压缩算法流程。
- 保存、重置、校验错误和只读对象存储策略区域应沿用现有系统设置交互。

## 7. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 若系统设置已使用通用 key-value 表存储，则不要求新增业务表；如配置默认值、seed 或迁移脚本有约束，需同步。 |
| Pydantic Schema | `MediaSettingsPatch`、`MediaSettingsData` 或等价系统设置 Schema 需要新增 display 图体积目标字段。 |
| OpenAPI/Orval | 系统设置响应与 PATCH payload 字段变化，需要同步 OpenAPI 与 Orval 生成物。 |
| 管理端 Web | 系统设置媒体页需要新增字段展示、编辑、保存、重置和测试。 |
| 小程序 | 不新增配置入口；通过后续生成的 display 图间接受益。 |
| 店主 Web | 不新增配置入口；通过后续生成的 display 图间接受益。 |
| 媒体上传 / 对象存储 | display 图生成内容会受配置影响；对象 key、URL、鉴权读取链路不变。 |
| 维护任务 | 历史 display 图重生成任务应读取同一配置，并支持 dry-run / apply 边界。 |
| 测试 | 需要补充后端生成、系统设置 API、管理端设置页和维护任务相关测试。 |

## 8. 关联需求与现状参考

| 关联项 | 关系 | 说明 |
|---|---|---|
| `REQ-0115-media-multi-variant-images` | 父能力 | 已定义 `thumbnail`、`display`、`original` 三规格语义。 |
| `REQ-0099-global-thumbnail-size-limit` | 类似配置 | 缩略图体积目标配置为本需求提供字段、UI 文案、生效边界和历史处理参考。 |
| `REQ-0118-unified-web-miniapp-image-variant-consumption-matrix` | 消费矩阵 | 后续可引用矩阵确认哪些页面消费 display 图。 |
| `REQ-0017-system-settings` | 配置入口基础 | 系统设置页面、分组 API、effective settings、审计和权限模型基础。 |
| `REQ-0012-object-storage-key-layout` | 存储边界 | 本需求保持单桶、标准前缀、受控 `/media/...` 读取与同目录派生 key 规则。 |
| `rules/media.md` | 媒体规则 | 后续实现需同步媒体生成、URL 和验收规则。 |
| `rules/object-storage.md` | 对象存储规则 | 后续实现需同步对象 key、维护任务和对象存储安全边界。 |

## 9. 状态块

```yaml
requirement_id: REQ-0119-admin-display-image-size-limit-setting
status: done
priority: P1
readiness: Partially Ready
parent_requirement: REQ-0115-media-multi-variant-images
terminal: multi
target_clients:
  web_admin: included
  web_catalog: indirect
  wechat_miniapp: indirect
api_change_required: true
database_change_required: false
orval_required: true
prototype_required: true
iteration: sprint-025
next_step: /opsx-apply REQ-0119
open_questions:
  - 字段最终命名采用 media.display_max_size_kb、media.display_image_max_size_kb 还是其他名称。
  - 是否允许 0 表示不限制；如允许，UI、默认值和 reset 语义需与默认 768 并存说明。
  - 配置允许范围是否采用 0-2048KB、1-2048KB 或其他边界。
  - 历史 display 图重生成是否只依赖既有维护任务，还是需要新增维护任务统计项。
notes:
  - 已根据 capture 生成 requirement.md。
  - 已补齐 user-stories、business-flow、acceptance 与 prototype 策略。
  - 已确认正式新增配置项，默认值沿用 768KB。
  - Readiness 为 Partially Ready：命中的 knowledge-base best-practices 当前为 draft，且 prototype 为轻量 HTML/context，PNG 待后续 OpenSpec Change 阶段导出。
  - 已评审通过；推荐先纳入 Sprint，再执行 /req-opsx REQ-0119。
  - 已纳入 sprint-025；下一步创建 OpenSpec Change。
  - 已创建 OpenSpec Change add-admin-display-image-size-limit-setting；下一步执行 /opsx-apply REQ-0119。
```
openspec_changes:
  - change_id: add-admin-display-image-size-limit-setting
    type: update
    status: archived
