## Why

BUG-0084 记录了小程序 SKU 详情页视频在内嵌轮播区域已经可以播放，但点击右上角全屏入口后，全屏态重新进入长时间加载的问题。该问题打断客户查看商品视频的连续体验，也使 `REQ-0044-miniapp-sku-detail-page` 中“当前视频进入微信小程序支持的视频全屏播放态”的验收缺少对已播放视频切换全屏耗时的约束。

当前判断的核心风险是：内嵌播放和全屏入口可能使用不同播放路径，导致全屏态不复用已加载的 `<video>` / `VideoContext` 上下文，而是打开独立媒体预览链路重新探测或重新拉流。

## What Changes

- 调整小程序 SKU 详情页视频全屏入口策略：优先复用当前视频组件上下文进入全屏播放态，避免已播放视频切换全屏时重新长时间加载。
- 增加全屏切换加载反馈与失败兜底要求，避免用户误以为页面卡死。
- 补充小程序静态测试和真机验收要求，记录内嵌播放首帧耗时与全屏切换首帧耗时。
- 保持图片轮播、图片预览、内嵌视频主动播放、页面隐藏暂停、媒体安全 URL、收藏分享能力不回归。

## Capabilities

### Modified Capabilities

- `miniapp-sku-detail-page`: 强化视频全屏入口、全屏切换性能、失败兜底和真机证据验收要求。

## Impact

- 影响微信小程序 SKU 详情页：`src/miniapp/pages/tile-detail/`。
- 影响小程序静态测试：`tests/test_miniapp_static.py`。
- 可能影响真机验收记录：`issues/bugs/archive/BUG-0084-miniapp-sku-video-fullscreen-reloads-slow/` 或后续 Change trace / acceptance 材料。
- 默认不新增后端 API、不修改数据库、不影响 Orval、不新增 Docker Compose 服务。
- 若实现阶段发现必须调整媒体接口或响应字段，必须同步 API / OpenAPI / Orval / docs / tests。

## Rollback Plan

1. 保留现有内嵌 `<video>` 播放路径和媒体安全 URL，确保回滚时 SKU 详情页基础视频播放仍可用。
2. 若新全屏入口在真机上出现兼容性问题，恢复到变更前的全屏入口策略，同时保留明确失败提示。
3. 回滚后重新运行小程序静态测试，并用真机确认图片轮播、内嵌视频播放、收藏分享和页面隐藏暂停不回归。
