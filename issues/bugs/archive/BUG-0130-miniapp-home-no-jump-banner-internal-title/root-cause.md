---
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
created_at: 2026-08-21 08:37:23
updated_at: 2026-08-21 08:39:12
root_cause_status: probable
category: code
---

# 根因分析

## 根因状态

`probable`

现有证据能说明后台 Banner 内部标题会进入公开 Banner 数据链路，但还缺少生产小程序包、接口响应样本或对象素材的闭环证据来确认标题最终被叠加到画面的具体位置。因此当前不得写为 `confirmed`。

## 直接原因

小程序首页无跳转 Banner 使用了 `internal-MINIAPP_HOME_NO_JUMP-...` 一类内部标题，并在公开首页轮播画面中暴露。该内部标题原本只应作为后台唯一识别或兼容字段使用，不应进入用户可见展示层。

## 根本原因

后台 Banner 表单为了满足保存链路与唯一键需求，会自动生成 `internal-*` 标题并保存到 `title` 字段；后端小程序公开 Banner item 又将数据库中的 `title` 原样作为公开字段返回。公开端缺少“内部标题净化/隔离”边界，导致内部识别字段具备进入小程序展示、搜索、分享、埋点或素材生成链路的可能。

## 触发条件

- Banner 展示端为小程序首页。
- Banner 位置为首页轮播。
- 跳转类型为无跳转。
- 后台生成或保留了 `internal-*` 内部标题。
- 小程序首页展示该 Banner，且当前发布包、缓存包、图片素材或未覆盖展示路径使用该内部标题参与画面渲染。

## 证据链

| 证据入口 | 类型 | 摘要 |
|---|---|---|
| 用户截图 | 截图 | 首页轮播图画面上出现 `internal-MINIAPP_HOME_NO_JUMP-1786622496149` 大号文字覆盖。 |
| `src/web/src/features/admin/components/BannerFormModal.tsx` | 代码定位 | `buildInternalBannerTitle()` 会生成 `internal-${position}-${jumpType}-${Date.now()}` 并作为保存 payload 的 `title`。 |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | `_to_banner_item()` 将 `record.title` 原样写入 `MiniappBannerItem.title`。 |
| `src/miniapp/pages/index/index.wxml` | 代码定位 | 当前仓库首页轮播块只渲染 `item.image_url` 与遮罩，不直接渲染 `item.title`。 |
| `tests/test_miniapp_static.py` | 测试约束 | 静态测试要求首页轮播块不包含 `{{item.title` 和 `hero-copy`。 |
| `src/miniapp/README.md` | 文档约束 | 明确要求有图 Banner 不渲染后台内部标题遮罩。 |

## 待补证

- 采集线上或测试环境 `GET /api/v1/miniapp/home` 响应中对应 Banner 的脱敏字段摘要，确认 `title`、`image_url`、`jump_type`、`image_object_key` 的实际值。
- 获取当前小程序体验版或线上包版本，确认是否与仓库当前 WXML 一致，排除旧包仍渲染标题的可能。
- 对对应 `image_url` 的图片对象做脱敏截图或 OCR 检查，确认内部标题是否已经写入图片像素本身。
- 若修复进入实现阶段，补充回归测试证明公开接口和页面渲染均不再暴露 `internal-*`。

## 验证方式

- 修复前：配置无跳转首页 Banner，确认公开接口或页面可复现内部标题暴露；若标题已写入图片素材，记录对象检查摘要。
- 修复后：同一 Banner 在小程序首页只显示公开图片内容，接口公开字段不返回内部标题，点击无跳转 Banner 不出现内部标题；品牌列表页轮播同步回归。
