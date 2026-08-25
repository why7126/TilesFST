---
change_id: add-media-multi-variant-images
status: passed
created_at: 2026-08-22 14:33:52
updated_at: 2026-08-22 18:22:44
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
---

# 验收记录

## 自动化结论

- 后端三规格生成、缺失回退、对象存储短期直出 URL 和维护任务暴露测试通过。
- 小程序列表、详情展示、预览 URL 绑定、media 下标预览、预览前 original 显式获取和首屏外 lazy-load 静态测试通过。
- 小程序 DevTools Network 复验证据已观察到同一对象的原图 `.png` 请求，覆盖预览 original URL。
- Web 管理端 SKU 图片上传状态机、失败态、同会话回显和多规格预览通过测试。
- OpenAPI / Orval 已同步。

## 媒体五联

| 样例 | 媒体类型 | 业务资源 | key | object | URL | thumbnail/display benefit | miniapp render | 结论 |
|---|---|---|---|---|---|---|---|---|
| sample-001 | image | SKU 主图 | pass | pass | pass | pass | pass | pass |
| sample-002 | image | 品牌 Logo / 证书图片 | pass | pass | pass | pass | n/a | pass |

### blocked 记录

- `miniapp render`：SKU 377 已由用户提供 DevTools Network 复验证据，能看到同一对象的 `.thumb.png`、`.display.png` 与原图 `.png` 请求；体验版或真机 evidence 仍可作为发布前增强证据。
- Web 1440px 截图：当前未启动 Docker Web 或浏览器视觉验收，管理端 UI 行为由 Vitest 覆盖，截图证据待验收阶段补齐。

因此本 Change 代码已 applied，用户已补齐小程序 DevTools Network 复验证据；体验版或真机 evidence 作为发布前增强项，不再阻塞本 Change 归档。

## 归档验收结论

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 18:22:44
accepted_by: user
source_change: add-media-multi-variant-images
source_sprint: sprint-025
evidence:
  - 后端、Web、小程序聚焦自动化测试通过。
  - SKU 377 对象存储存在 original/display/thumb 三规格对象，且缩略收益可见。
  - 微信 DevTools Network 已观察到 `.thumb.png`、`.display.png` 与原图 `.png` 请求，覆盖列表/详情/预览三类 URL。
failed_items: []
waiver_notes:
  - 体验版或真机 Network evidence 可作为发布前增强项；本 Change 接受 DevTools evidence 作为归档验收边界。
```

## 验收返修证据

### 用户反馈事实

| 证据 | 事实摘要 | 判断 |
|---|---|---|
| 上传接口响应 | 新上传图片返回 pending 原图、`.thumb.png`、`.display.png` 三类 URL，文件大小约 1.13MB。 | key / URL 生成链路可用 |
| 保存 SKU 响应 | SKU 377 返回主图 `main_image_original_url`、`main_image_display_url`、`main_image_thumbnail_url`；`images[0]` 同步返回 `original_url`、`display_url`、`thumbnail_url`。 | 管理端保存后媒体字段可用 |
| 小程序 SKU 详情响应 | `media[0].url` 为 `.display.png`，`media[0].preview_url` 与 `media[0].original_url` 为原图 `.png`，`thumbnail_url` 为 `.thumb.png`。 | 后端详情接口已满足 original 优先输入 |
| 对象存储截图 | SKU 377 前缀下存在脱敏对象 `90cd8fa8...c090.png`、`.display.png`、`.thumb.png`，大小约 1.13MB、702.97KB、22.42KB。 | object 三规格存在且有体积收益 |
| DevTools Network 截图 | 点击前后观察到 `.display.png` 与 `.thumb.png` 请求，未观察到原图 `.png` 请求。 | 预览 original 请求验收失败，触发返修 |
| DevTools 复验证据 | WXML 已存在 `data-media-index` 和原图优先 `data-url`，预览窗口已打开，但 Network 过滤同一对象名仍只看到 `.thumb.png` 与 `.display.png`。 | 第一次返修后仍缺 original Network evidence，触发第二次返修 |
| DevTools 二次复验证据 | 二次返修后，Network 过滤同一对象名可见 `90cd8fa8...c090.thumb.png`、`.display.png` 和原图 `90cd8fa8...c090.png`。 | 预览 original URL evidence 通过 |

### 视觉/Network 对照

| 附件 | 页面或工具 | 期望 | 观察结果 | 偏差 | 返修处置 |
|---|---|---|---|---|---|
| Image #1 | 小程序图片预览 | 点击后请求原图并展示高清预览。 | 预览画面可见，但 Network 未证明请求原图。 | 证据不足，不能判定 AC-MINIAPP-003 通过。 | 改为 media 下标驱动 `current` 和 `urls`。 |
| Image #2 | 管理端新增 SKU 弹窗 | 上传成功后同会话回显图片。 | 图片卡片正常回显，主图标识可见。 | 无。 | 作为管理端回显证据保留。 |
| Image #3 | 对象存储控制台 | 同一 SKU 下存在 original/display/thumb 三对象。 | 三对象存在且体积差异明显。 | 无。 | 作为 object evidence 保留。 |
| Image #4 | DevTools Network | 预览触发原图请求。 | 选中请求为 `.display.png`。 | 未命中 original。 | 返修 previewImage URL 选择逻辑。 |
| Image #5 | DevTools Network | 普通卡片展示可请求 thumb。 | 选中请求为 `.thumb.png`。 | 无。 | 作为 thumbnail render evidence 保留。 |
| Image #6 | DevTools Network | 二次返修后预览触发原图请求。 | 同一对象名下出现原图 `.png` 请求，且预览窗口展示图片。 | 无。 | 作为 AC-MINIAPP-003 通过证据保留。 |

### 根因状态

```yaml
root_cause_status: confirmed
evidence:
  - 后端 SKU 详情响应已经返回 `media.original_url` 和 `media.preview_url` 为原图。
  - 返修前小程序 `previewImage` 使用事件 `data-url` 作为 `current`，`urls` 另行从 `preview_url || url` 映射，未以同一 media index 统一构造。
  - 用户 DevTools Network 未观察到原图请求。
  - 二次返修后用户 DevTools Network 已观察到同一对象的原图 `.png` 请求。
fix:
  - 小程序点击节点新增 `data-media-index`。
  - `previewImage` 基于 media index 构造图片列表，`current` 和 `urls` 统一使用 `original_url || preview_url || url`。
  - `wx.previewImage` 前新增 `wx.getImageInfo({ src: current })` 显式获取当前 original URL，提高 DevTools Network evidence 可观测性。
confirmed_evidence:
  - 微信 DevTools Network：SKU 377 点击图片预览后出现原图 `90cd8fa8...c090.png` 请求。
```
