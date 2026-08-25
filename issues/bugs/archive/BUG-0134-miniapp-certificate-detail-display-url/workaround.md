---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
created_at: 2026-08-22 21:08:06
updated_at: 2026-08-22 21:08:06
---

# Workaround

## 临时规避方案

正式修复前，可先从素材和运营侧降低影响：

1. 优先压缩图片类品牌证书原图，避免详情页回退原图时加载过大的图片。
2. 对高频访问品牌的证书图片优先确认缩略图和 display 派生对象是否存在。
3. 若某证书图片原图明显过大，可临时替换为适合移动端展示的 WebP、JPG 或 PNG 素材。
4. 对 PDF/文档证书保持文件打开或占位展示，不临时伪装为图片展示。

## 不足与风险

- 人工压缩不能保证后续新增或替换的证书图片继续符合多规格展示策略。
- 如果证书详情接口仍不返回 `display_url`，小程序详情页仍无法稳定使用展示图规格。
- 直接压缩原图可能影响证书预览、下载或管理端高清查看场景。
- 临时素材治理无法覆盖历史对象、缩略图缺失、display 图缺失或对象存储漂移。

## 正式修复方向

- 后端证书详情接口补齐图片媒体项的 `display_url`、`thumbnail_url`、`original_url` 或等价语义字段。
- 小程序证书详情页顶部展示优先使用 `display_url`，预览才使用原图或高清 URL。
- 图片证书使用 `images/default/brand-certificates/` 前缀；PDF/文档证书使用 `files/default/brand-certificates/` 前缀。
- 若涉及历史对象或派生图缺失，执行并记录 dry-run、apply 和幂等摘要。
- 增加接口与小程序静态/渲染回归测试，防止详情页再次退回原图展示。
