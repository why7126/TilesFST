---
change_id: fix-miniapp-lightweight-image-variant-consumption
type: fix
source_bug: BUG-0137-miniapp-lightweight-image-variant-consumption
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
sprint: sprint-025
status: applied
lifecycle_stage: change
created_at: 2026-08-24 18:09:18
updated_at: 2026-08-25 09:03:03
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-miniapp-lightweight-image-variant-consumption
type: fix
source_bug: BUG-0137-miniapp-lightweight-image-variant-consumption
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
sprint: sprint-025
status: applied
change_type: fix
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - media-multi-variant-images
    - miniapp-home
    - miniapp-brand-list-page
    - miniapp-brand-detail-home-page
    - miniapp-brand-card-component
    - miniapp-sku-detail-page
    - miniapp-certificate-list-page
readiness: ready
tasks_total: 33
tasks_completed: 33
```

## BUG Readiness Report

| 项 | 结论 |
|---|---|
| 评审状态 | pass：BUG 状态为 `in_sprint`，已完成 `/bug-review` 并纳入 `sprint-025`。 |
| 根因状态 | pass：`root_cause_status: confirmed`，证据链覆盖代码定位、DevTools Network/render 和 AppData 样本。 |
| 文档齐备 | pass：`bug.md`、`root-cause.md`、`workaround.md`、`acceptance.md`、`review.md`、`trace.md` 齐备。 |
| Sprint Inclusion | pass：BUG 已在 `iterations/archive/sprint-025/sprint.yaml` 正式范围内。 |

## 影响分析

```yaml
impact:
  backend: true
  miniapp: true
  storage: true
  api: true
  database: false
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 09:03:03 | evidence-update | 用户补充品牌主页顶部 Hero DevTools Network/render evidence：`.webp` 过滤下可见品牌 Logo/Hero `*.display.webp` 200 请求，content-length 约 13.1 kB，同屏商品卡继续使用 `*.thumb.webp`，品牌主页 Hero 和商品列表渲染正常；Change 任务更新为 33/33，BUG acceptance 更新为 accepted。 |
| 2026-08-25 08:53:42 | `/opsx-modify` | 验收策略升级：品牌主页顶部品牌图位定义为独立 Hero 大图展示位；品牌详情响应新增 `brand_hero_display_url` / `brand_hero_thumbnail_url`，小程序顶部 Hero 改为 display 优先、thumbnail 兜底，小 Logo/品牌卡仍保持 thumbnail 目标规格；聚焦测试、OpenAPI/Orval、OpenSpec、API 标准和 root-cause evidence 校验通过，BUG acceptance 回到 pending，待补品牌主页 Hero DevTools Network/render evidence。 |
| 2026-08-25 08:40:18 | evidence-update | 用户补充首页与品牌列表 Banner display 优先策略 DevTools Network/render evidence；`.webp` 过滤下可见 `*.display.webp` 200 请求，商品卡片和品牌 Logo 继续使用 `*.thumb.webp`，页面渲染正常，未见原图或不存在静态占位图请求。Change 任务更新为 26/26，BUG acceptance 更新为 accepted。 |
| 2026-08-25 08:29:38 | `/opsx-modify` | 验收策略升级：小程序 Banner 轮播图明确为首屏大图展示位，目标规格调整为 `display`；首页和品牌列表 Banner 普通展示改为 `display_url -> thumbnail_url -> 安全视图占位`，兼容 `image_url` 优先承载 display 轻量 URL，不回退原图、preview、旧 url 或不存在静态占位图。 |
| 2026-08-25 08:17:05 | workflow-sync-dry-run | `sync-workflow-status.py --event opsx.modify --dry-run` 通过且 Errors=0，但该事件仍会将 BUG acceptance 计算为 pending；为保留用户已补齐首页返修回归证据后的 accepted 结论，未执行写入同步。 |
| 2026-08-25 08:17:05 | evidence-update | 用户补充首页返修后 DevTools Network/render evidence：Network 过滤 `place` 未出现 `tile-placeholder.png` 请求，首页 Banner 以视图占位渲染可见，商品卡片正常展示；Change 任务更新为 25/25，BUG acceptance 更新为 accepted。 |
| 2026-08-25 08:07:55 | `/opsx-modify` | 验收返修：用户补充首页 Network 证据显示 `tile-placeholder.png` 307 后 500；已移除小程序 `/assets/tile-placeholder.png` fallback，首页和品牌 Banner 缺图改为视图占位，列表类图片错误改为空字段并由现有空态渲染；聚焦测试 80 passed，待首页 DevTools Network/render 回归证据。 |
| 2026-08-24 20:59:27 | workflow-sync-dry-run | `sync-workflow-status.py --event opsx.apply --dry-run` 通过且 Errors=0，但该事件会将 BUG acceptance 计算为 pending；为保留用户已补齐的修复后小程序 Network/render evidence accepted 结论，未执行写入同步。 |
| 2026-08-24 20:54:30 | evidence-update | 用户补充修复后小程序 DevTools Network/render evidence；首页、品牌列表、商品详情、证书详情均渲染可见，Network 未见 `.jpg` 原图冷加载行，BUG acceptance 更新为 accepted。 |
| 2026-08-24 18:42:54 | `/opsx-apply` | Change 实现已 applied：已完成后端 schema/service、小程序消费、API 文档、OpenAPI/Orval 与自动化测试；4.x 小程序 DevTools Network/render 修复后证据仍待人工补齐，BUG 验收保持 pending。 |
| 2026-08-24 18:09:18 | `/bug-opsx` | 基于 BUG-0137 创建 OpenSpec Change，生成 proposal、design、delta specs、tasks 与 trace。 |
