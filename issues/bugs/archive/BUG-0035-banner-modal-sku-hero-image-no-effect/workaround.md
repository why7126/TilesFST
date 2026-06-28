---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
status: pending_review
created_at: 2026-06-28 16:17:35
updated_at: 2026-06-28 16:17:35
---

# 临时规避方案

## 1. 运营规避（当前可用手段）

创建 **SKU 详情** 类 Banner 时，若「使用 SKU 主图」无响应：

1. 改用 **「自定义上传」**：从本地选择与 SKU 主图相同的运营图文件上传，保存为 `image_source=custom_upload`。
2. 或先在 **瓷砖 SKU** 管理页确认该 SKU 主图 URL，下载后通过 Banner 弹窗自定义上传。

**限制：** 无法使用 `image_source=sku_main_image` 引用模式；SKU 主图变更后 Banner **不会** 自动跟随（与 REQ-0016 设计意图不符）。

## 2. 验收规避

在正式修复前，验收 REQ-0016 时应：

- 将 **AC-031**（选择 SKU 后默认 SKU 主图）**标注为已知缺陷 BUG-0035**，暂不作为通过项。
- AC-032/033 中「SKU 图库切换」若同样依赖 `object_key`，应一并标注待 BUG-0035 修复后复验。
- 自定义上传路径、其他 `jump_type` 弹窗变体可单独验证。

## 3. 开发规避

未修复分支上验证 Banner SKU 跳转能力：

- DevTools → Network：保存时确认 `POST /api/v1/admin/banners` payload 含合法 `image_object_key`。
- 可手工构造 payload（与 `test_admin_banners.py` 中 `_create_sku` 返回的 `main_key` 一致）通过 API 创建 Banner，绕过前端回填缺陷。

## 4. 风险说明

| 风险 | 说明 |
|---|---|
| 功能阻断 | SKU 详情 Banner 无法按需求使用主图引用，运营需重复上传 |
| 数据不一致 | 自定义上传与 SKU 主图可能不同步，维护成本高 |
| 静默失败 | 用户误以为按钮损坏，可能反复点击或放弃配置 |

**结论：** 无前端零成本完整规避；须通过 `/bug-review` → `fix-*` Change 修复 SKU 主图回填逻辑。
