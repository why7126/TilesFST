---
requirement_id: REQ-0099-global-thumbnail-size-limit
status: pending_review
created_at: 2026-08-05 09:44:12
updated_at: 2026-08-05 09:44:12
prototype_type: web-admin
---

# 原型说明

## 目标

该原型用于说明“系统设置 - 媒体与存储”中新增全局缩略图体积目标上限配置的位置、文案和交互边界，不代表最终视觉稿。

## 页面入口

```text
管理后台 -> 系统设置 -> 媒体与存储
```

## 关键元素

- 在“上传限制”区域新增“缩略图体积上限 (KB)”字段。
- 字段值 `0` 表示不限制。
- 字段帮助文案明确“仅对新生成缩略图生效；历史需维护任务重生成”。
- 继续沿用设置页底部唯一保存 CTA。
- 恢复默认和 dirty Tab 切换沿用 DS confirm modal。

## 非目标

- 不新增独立历史重生成后台页面。
- 不展示缩略图压缩算法细节。
- 不改变对象存储策略只读区域。

## 待导出

- PNG Golden Reference：待后续 OpenSpec Change 或 UI 实现阶段根据真实页面导出。

