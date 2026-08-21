---
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
review_status: approved
created_at: 2026-08-21 08:39:53
updated_at: 2026-08-21 08:39:53
reviewed_at: 2026-08-21 08:39:53
reviewer: user
decision: approve
---

# 缺陷评审

## 评审结论

批准修复。

## 评审清单

- [x] 可复现或根因充分：用户截图可证明首页轮播画面实际出现内部标题；代码证据显示内部标题生成并进入公开 Banner 数据链路。当前根因状态为 `probable`，足以进入修复设计，实施阶段需补齐接口响应、素材或小程序包证据闭环。
- [x] 严重等级合理：维持 `medium`。问题发生在首页首屏公开展示，影响体验并暴露内部实现标识；当前未证明阻断核心浏览或交易链路。
- [x] 回归验收明确：`acceptance.md` 已覆盖首页轮播、公开接口净化、点击/兜底链路、品牌列表页回归、后台管理能力，以及媒体 key/object/URL/render 四联验收。
- [x] hotfix 路径判断：暂不按 hotfix 处理。若确认线上所有用户稳定可见或无法通过下线/替换素材规避，可升级为高优先级修复。

## 评审说明

该问题属于已上线公开体验缺陷，且包含内部命名暴露风险。建议尽快纳入 Sprint，优先修复公开端 Banner DTO 的内部标题净化，并补充小程序首页与品牌列表页轮播回归。

## 后续建议

1. 先通过 `/sprint-propose` 纳入迭代。
2. 再通过 `/bug-opsx` 创建修复 Change。
3. 实施阶段补充生产/体验版接口响应、图片素材或小程序包证据，确认根因是否可从 `probable` 更新为 `confirmed`。
