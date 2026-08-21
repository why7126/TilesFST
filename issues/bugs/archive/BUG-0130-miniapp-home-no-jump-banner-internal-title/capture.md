---
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
status: done
created_at: 2026-08-21 08:30:25
updated_at: 2026-08-21 14:39:15
severity_hint: medium
environment: miniapp
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

小程序首页无跳转轮播图画面上显示 `internal-MINIAPP_HOME_NO_JUMP-1786622496149` 一类内部标题，内部标识覆盖在轮播图图片上，用户可直接看到后台内部命名。

# 复现步骤

1. 后台配置一张小程序首页轮播 Banner，跳转类型选择无跳转。
2. 将该 Banner 上线并确保位于首页轮播展示范围。
3. 打开微信小程序首页。
4. 观察首页轮播图是否出现 `internal-MINIAPP_HOME_NO_JUMP-...` 内部标题覆盖在图片画面上。

# 期望 vs 实际

- 期望：首页轮播图只展示运营配置的公开图片内容，不应展示后台内部标题、内部枚举名、时间戳或实现细节；无跳转 Banner 点击时也不应暴露内部标题。
- 实际：用户截图显示无跳转轮播图画面上出现 `internal-MINIAPP_HOME_NO_JUMP-1786622496149` 内部标题，影响首页视觉体验并暴露内部命名。

# 影响范围

- 微信小程序首页轮播图公开展示体验。
- 后台 Banner 无跳转配置生成内部标题后的公开展示链路。
- 小程序首页 Banner API、图片素材生成或前端渲染中可能使用 `title` 的路径。
- 品牌列表页等复用 Banner 轮播能力的页面需要回归确认是否存在同类风险。

# 初步线索

- 探索阶段已确认小程序首页 WXML 当前轮播块不直接渲染 `item.title`，但后台 Banner 表单会为无跳转 Banner 生成内部标题并作为 `title` 保存。
- 后端小程序公开 Banner item 仍会返回数据库中的 `title` 字段，后续需要确认该字段是否被图片生成、分享、搜索、埋点或其他展示链路叠加到画面。
- 用户截图可作为现象证据：内部标题以大号白色文字覆盖在首页轮播图上。

# 建议验收或复现要点

- [ ] 首页无跳转轮播图不再显示 `internal-*` 内部标题或任何后台内部枚举/时间戳。
- [ ] 小程序首页 Banner API 不向公开端暴露不必要的内部标题，或对内部标题做公开字段净化。
- [ ] 无跳转 Banner 点击后的提示文案不包含内部标题。
- [ ] 覆盖首页轮播、品牌列表页轮播和不同跳转类型的 Banner 回归。
- [ ] 后台 Banner 列表仍可满足唯一键、排序和管理识别需要，不因公开端净化破坏管理端编辑能力。

# 附件

- 用户截图：`/var/folders/26/jcqks9nx23185wqvs17rzgkw0000gn/T/codex-clipboard-9bd4b171-6dca-4544-bef9-423a8e484233.png`（本地会话临时路径，仅作为本次用户反馈证据入口；不得提交到仓库）。
