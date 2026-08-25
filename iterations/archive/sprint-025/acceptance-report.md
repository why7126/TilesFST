---
note: workflow-sync — 18/18 Change 已 archive；0 applied；待人工 sign-off
title: sprint-025 验收报告
acceptance_status: passed
created_at: 2026-08-21 18:43:30
updated_at: 2026-08-25 14:51:36
---

# sprint-025 验收报告

## 验收范围

| 类型 | 编号 | 标题 | 验收状态 | 说明 |
|---|---|---|---|---|
| REQ | REQ-0114-version-deployment-upgrade-rollback-governance | 版本部署升级与回滚治理能力 | done，已归档（`add-version-deployment-upgrade-rollback-governance` archived 2026-08-22 20:06:55） | 已完成实现、验收与归档 |
| REQ | REQ-0115-media-multi-variant-images | 媒体图片多规格展示图能力 | done，已归档（`add-media-multi-variant-images` archived 2026-08-22 18:22:44） | 已完成 previewImage 二次返修；小程序 original_url DevTools Network 复验证据已补 |
| REQ | REQ-0119-admin-display-image-size-limit-setting | 管理端媒体与存储新增 display 图体积目标上限配置 | done，已归档（`add-admin-display-image-size-limit-setting` archived 2026-08-22 22:18:00） | 已完成 `/opsx-apply`、上传限制布局验收返修与 `/opsx-archive` |
| BUG | BUG-0132-miniapp-sku-detail-large-image-cold-load | 小程序商品详情页冷加载大图资源 | done，已归档（`fix-miniapp-sku-detail-large-image-cold-load` archived 2026-08-22 19:56:51） | 已补后端可用派生图过滤、详情页占位图兜底和小程序 Network 复测证据 |
| BUG | BUG-0134-miniapp-certificate-detail-display-url | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 | done，已归档（`fix-miniapp-certificate-detail-display-url` archived 2026-08-24 14:30:46） | 已补 Tencent COS `NoSuchResource` 缺失对象识别、历史 key 漂移维护摘要、全量 `backfill-image-variants` dry-run/apply/幂等证据、小程序首页商品卡 render evidence，以及证书详情半迁移 key 运行时接口/object 证据 |
| BUG | BUG-0137-miniapp-lightweight-image-variant-consumption | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 | done，已归档（`fix-miniapp-lightweight-image-variant-consumption` archived 2026-08-25 09:03:03） | 首页 fallback `tile-placeholder.png` 307/500 已返修；首页、品牌列表 Banner 和品牌主页 Hero display 优先策略均已补 DevTools Network/render evidence |

## 验收门禁

- REQ-0114 的功能 AC 与非功能 AC 全部有实现或明确 N/A 说明。
- upgrade 计划与校验输出不得泄露真实 env、密钥、连接串或客户数据。
- 跨版本升级支持级别必须证据驱动，缺少演练或事实源时不得标记为 supported。
- 回滚证据必须覆盖旧镜像、旧 env 摘要、DB 备份、对象存储影响和回滚后 smoke。
- Workflow Sync、OpenSpec 校验和相关脚本测试通过。
- REQ-0115 必须完成媒体 key/object/URL/render 四联验收、小程序 Network evidence、存量批量生成 dry-run/apply 证据和对象存储直出安全边界证明。
- BUG-0132 验收需确认接口不返回不存在或不可读的 `.display` / `.thumb` 派生 URL；派生图缺失时详情页使用可用占位图，且普通展示链路不得回退原图冷加载。
- BUG-0134 验收需确认证书详情媒体项具备 `display_url`、小程序展示不回退原图、历史图片 key 漂移已收敛、全量 WebP 派生对象回填覆盖完整，且小程序真实页面 render evidence 已补。
- REQ-0119 验收需确认管理端系统设置可配置 display 图体积目标上限，默认 768KB；该配置与缩略图目标独立，并实际被新上传 display 派生生成链路读取。媒体与存储 Tab 上传限制区域桌面 2 列网格按四行展示：图片最大尺寸 / 视频最大尺寸、文件最大尺寸 / 空位、缩略图体积目标上限 / 详情展示图体积目标上限、支持图片格式 / 支持视频格式。
- BUG-0137 首页 fallback 已返修并复验：不得再请求不存在的 `/assets/tile-placeholder.png`，缺图展示视图占位或现有空态；首页 DevTools Network/render 回归证据确认未出现 `tile-placeholder.png` 307/500。
- BUG-0137 品牌主页顶部品牌图位已升级为 Hero 大图位：品牌详情响应提供 `brand_hero_display_url` / `brand_hero_thumbnail_url`，端侧顶部 Hero display 优先、thumbnail 兜底；DevTools Network/render evidence 已确认 `*.display.webp` 200，商品卡片继续使用 `*.thumb.webp`。
- REQ-0120 Docker Web 上传边界已补证：管理端 SKU 编辑弹窗从 `http://localhost:3000` 触发 `tile-images` 上传，返回 `200 OK` / `code=0`；原图保留 PNG，响应返回 `.thumb.webp` 与 `.display.webp`；SKU 图片即时回显，`display.webp` GET `200`，样本原图约 `1189508` bytes、`display.webp` 传输约 `26.96 kB`。

## BUG-0134 验收证据补充

| 时间 | 证据 | 结论 |
|---|---|---|
| 2026-08-24 13:08:11 | 全量 `backfill-image-variants`：初始 dry-run `total=684`、`thumbnail_missing=186`、`display_missing=186`、`estimated_writes=372`；apply 成功 370 个派生对象；幂等 dry-run `skipped=682`、`thumbnail_missing=1`、`display_missing=1`、`estimated_writes=3`、`retry_candidates=2` | 前序 `--limit 100/500` 覆盖不足导致首页新品图片未生成派生对象；全量回填后大面积恢复 |
| 2026-08-24 13:08:11 | `/api/v1/miniapp/products?page=1&page_size=12` 同一批商品刷新后返回 `cover_image=/media/...thumb.webp`、`thumbnail_url=/media/...thumb.webp`、`display_url=/media/...display.webp`、`original_url=/media/...原图` | 商品卡可展示字段恢复，未暴露对象存储 endpoint 或密钥 |
| 2026-08-24 13:08:11 | 用户补充截图 `codex-clipboard-77f20599-cb4c-4c6c-b85e-c070c03d10b0.png` | 小程序首页新品推荐与热销推荐商品卡图片正常渲染，空图现象恢复 |
| 2026-08-24 14:30:46 | SQLite 证据显示证书 `media_id=40` 的 `file_key` 已迁移到 `images/default/brand-certificates/...jpg`，但 `file_url` 仍是旧 `/media/files/default/brand-certificates/...jpg`；`migrate-certificate-image-keys` dry-run 为 `image_candidates=0`、`document_skipped=5`、`failed=0` | 图片 key 迁移已完成，剩余 `files/default/brand-certificates` 为文档类；详情占位由接口仍读旧 `file_url` 派生变体导致 |
| 2026-08-24 14:30:46 | `/api/v1/miniapp/certificates/4` 运行时响应显示 `media_id=40` 的 `display_url`、`thumbnail_url`、`original_url` 均为 `/media/images/default/brand-certificates/...`；`.display.webp` 与 `.thumb.webp` HEAD 均 `200 OK`、`content-type=image/webp`、`x-media-fallback=0` | 证书详情轮播可用 display/thumb URL 已恢复，且继续由后端 `/media` 代理读取 |

## REQ-0120 验收证据补充

| 时间 | 证据 | 结论 |
|---|---|---|
| 2026-08-25 12:02:00 | 用户提供微信开发者工具截图：品牌页渲染可见，Network 过滤 `.webp` 后存在多条 `.thumb.webp` / `.display.webp` 请求；选中 `display.webp` 返回 `200 OK`，`content-length=13126` | 小程序 render evidence 已补，四联 render 由 blocked 更新为 pass |
| 2026-08-25 14:18:06 | 用户提供 Docker Web Network 与 SKU 编辑弹窗截图：`POST http://localhost:3000/api/v1/admin/uploads/tile-images` 返回 `200 OK` / `code=0`；原图保留 PNG；响应返回 `.thumb.webp` 与 `.display.webp`；SKU 编辑弹窗即时回显，`GET http://localhost:3000/media/...display.webp` 返回 `200` | Docker Web 上传边界、派生 URL、即时回显和轻量展示图收益证据已补 |

## 验收结果

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 14:45:16
accepted_by: sprint-archive
evidence:
  - python scripts/validate-sprint-archive-readiness.py --sprint sprint-025
  - python scripts/check-sprint-close-stale-scan.py --sprint sprint-025
  - python scripts/promote-issues-for-archive.py --sprint sprint-025
failed_items: []
notes: 18/18 Change 已归档，306/306 tasks 完成；AI usage snapshot 缺失，关闭报告按 estimated_fallback 风险提示记录。
```
