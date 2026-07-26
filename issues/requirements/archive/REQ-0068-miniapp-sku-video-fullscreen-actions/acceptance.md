---
requirement_id: REQ-0068-miniapp-sku-video-fullscreen-actions
status: done
created_at: 2026-07-23 23:19:20
updated_at: 2026-07-24 16:01:15
---

# 验收标准

## 功能 AC

- [ ] AC-001 商品详情页存在视频媒体时，视频媒体项展示明确可感知的全屏播放入口。
- [ ] AC-002 无视频媒体、视频 URL 为空或视频加载失败时，不展示误导性的可用全屏入口，或点击后展示明确错误提示。
- [ ] AC-003 用户点击全屏入口后，当前视频进入微信小程序支持的视频全屏播放态。
- [ ] AC-004 视频全屏播放不默认自动触发，必须由用户主动点击播放或全屏入口触发。
- [ ] AC-005 用户退出全屏后，页面回到当前 SKU 详情页和当前媒体上下文，不重置到首图、不丢失商品数据。
- [ ] AC-006 页面隐藏、锁屏、跳转、返回上一页或切换媒体时，视频暂停策略不回归。
- [ ] AC-007 全屏态长按视频可唤起操作菜单或平台允许的等价交互。
- [ ] AC-008 操作菜单包含“转发给朋友”“保存视频”“取消”，或在微信原生能力限制下提供等价入口与验收说明。
- [ ] AC-009 点击“转发给朋友”复用商品详情页分享能力，分享路径保留当前 `skuId` 与 `source=share` 或等价来源参数。
- [ ] AC-010 被分享用户打开分享卡片后进入对应 SKU 商品详情页，视频存在时仍可使用全屏入口。
- [ ] AC-011 点击“保存视频”在权限、下载与平台能力允许时保存当前视频到相册，并展示成功提示。
- [ ] AC-012 保存失败时展示明确提示，覆盖权限拒绝、网络异常、视频暂不可保存、平台不支持等主要失败原因。
- [ ] AC-013 点击“取消”关闭菜单，不触发分享、保存、页面跳转或异常退出。
- [ ] AC-014 图片全屏预览、图片长按交互、图片缩放拖动和左右切换不回归。
- [ ] AC-015 商品详情页底部收藏、分享、推荐跳转、品牌入口和错误态不受视频全屏改造影响。
- [ ] AC-016 视频全屏入口、菜单动作、保存成功 / 失败 SHOULD 有埋点或等价预留；埋点失败不得阻断用户操作。

## 平台与安全 AC

- [ ] AC-017 OpenSpec / 实现阶段明确微信 `video` 组件全屏、长按、自定义菜单、下载和保存到相册的能力边界。
- [ ] AC-018 若微信原生全屏态无法自定义长按菜单，验收材料必须记录降级方案和用户可达路径，不得宣称完全支持自定义长按。
- [ ] AC-019 视频 URL 必须来自详情接口返回的安全可播放 URL，不得使用原始 object key 拼接对象存储地址。
- [ ] AC-020 保存视频不得放宽 MinIO 权限、不得提交密钥、不得暴露 bucket、endpoint 或内部对象路径。
- [ ] AC-021 若后续实现新增签名下载 URL、媒体字段或 API contract，必须同步 OpenAPI / Orval / docs / tests；若未新增，验收记录写明 N/A。

## 小程序验收 AC

- [ ] AC-022 `src/miniapp/pages/tile-detail/index.ts` 与运行时 `index.js` 的视频全屏、菜单、分享和保存逻辑保持同步，避免微信开发者工具加载入口漂移。
- [ ] AC-023 小程序静态测试覆盖 `video` 组件全屏入口属性、页面分享路径、保存视频降级提示或等价关键逻辑。
- [ ] AC-024 DevTools evidence 覆盖 320 / 375 / 430 pt 视口下视频全屏入口不遮挡媒体计数、原生胶囊、返回按钮或底部操作栏。
- [ ] AC-025 至少一台真机 evidence 覆盖全屏入口、全屏播放、长按菜单或降级入口、转发、保存成功或失败提示、退出全屏回到详情页。
- [ ] AC-026 若真机暂不可用，验收状态必须标记 `real_device_follow_up` 或 `blocked`，不得把静态测试或 DevTools 截图写成真机通过。

## 横切 AC（knowledge-base）

本 REQ 不命中 `req-complete` 定义的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切标签，因此不追加 admin 系列 AC-XCUT。

小程序交互验收参考：

- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- `docs/knowledge-base/retrospectives/sprint-008-retrospective.md`
- `docs/knowledge-base/retrospectives/sprint-009-retrospective.md`
- `docs/knowledge-base/retrospectives/sprint-010-retrospective.md`

上述参考已转化到 AC-022 至 AC-026：运行入口同步、DevTools / 真机 evidence、分享路径与埋点不阻断。
