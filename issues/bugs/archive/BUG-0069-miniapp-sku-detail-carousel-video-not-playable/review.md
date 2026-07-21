---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
status: done
created_at: 2026-07-20 08:11:37
updated_at: 2026-07-20 22:47:36
reviewed_at: 2026-07-20 08:11:37
review_result: approved
reviewer: AI
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change: fix-miniapp-sku-detail-video-url
---

# Review - BUG-0069 SKU 商品详情页轮播图视频不能显示和播放

## 评审结论

通过，确认进入修复流程。

该缺陷属于已交付 SKU 详情页能力偏差。`REQ-0044-miniapp-sku-detail-page` 已明确要求图片与视频混合轮播、视频播放控制、单项媒体失败兜底和安全媒体 URL；当前证据显示视频 URL 组装链路可能使用 `tile_videos.file_name` 作为播放 URL，和数据库文档及管理端展示逻辑中的 `object_key` 语义不一致，具备明确修复价值。

## 评审清单

| 项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 构造 `object_key` 为媒体对象 key、`file_name` 为原始文件名的视频记录后，可验证小程序详情接口返回的视频 URL 是否错误 |
| 严重等级合理 | 通过 | `high` 合理；不阻断详情页整体访问，但会使已交付视频展示能力不可用 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖接口 URL、混合轮播、视频播放、失败提示、图片回归和测试要求 |
| 是否需 hotfix 路径 | 不需要 | 当前问题影响 SKU 视频展示，建议常规 fix；若线上核心 SKU 视频展示集中失效，可在 Sprint 规划时提高优先级 |

## 门禁结论

- 状态：`approved`
- 可进入：`/bug-opsx BUG-0069-miniapp-sku-detail-carousel-video-not-playable`
- 可纳入 Sprint：是，需通过 `/sprint-propose`
- 修复前不得直接修改 `src/`，应先创建 OpenSpec `fix-*` Change。

## 建议修复方向

1. 小程序 SKU 详情接口视频媒体应优先使用 `tile_videos.object_key` 生成安全媒体 URL。
2. 后端测试应覆盖 `object_key` 与 `file_name` 语义不同的真实保存场景。
3. 小程序端回归 `<video>` 展示、播放、暂停、失败提示和相关埋点。
4. 若 API 契约不变，仅修正响应字段来源，应在修复输出中说明不需要 Orval；若契约变化，则同步 OpenAPI / Orval / docs / tests。
