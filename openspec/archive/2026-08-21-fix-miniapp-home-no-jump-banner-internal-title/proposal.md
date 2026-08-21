---
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: proposed
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 08:45:32
source_bug: BUG-0130-miniapp-home-no-jump-banner-internal-title
sprint: sprint-024
---

# 修复小程序首页无跳转 Banner 内部标题暴露

## 背景

`BUG-0130-miniapp-home-no-jump-banner-internal-title` 记录了小程序首页无跳转轮播图显示 `internal-MINIAPP_HOME_NO_JUMP-...` 内部标题的问题。用户截图显示内部标识覆盖在首页轮播图画面上，影响首屏体验并暴露后台内部命名。

当前后台 Banner 管理为了兼容 `(display_client, position, title)` 唯一键，会自动生成 `internal-*` 标题；但该标题不应进入小程序公开展示、点击兜底、搜索、分享或埋点展示链路。

## 变更内容

- 净化小程序公开 Banner 数据中的内部标题，避免公开端获得或展示 `internal-*` 标识。
- 保留后台 Banner 管理的内部标题兼容能力，不改变管理端唯一键和保存链路。
- 覆盖首页轮播、品牌列表页轮播、无跳转点击兜底和媒体 key/object/URL/render 四联验收。
- 若确认内部标题已写入存量图片对象，记录素材替换或清理路径。

## 回滚计划

- 若公开 Banner DTO 净化导致兼容问题，可回滚到原字段下发逻辑，但必须临时下线或替换含内部标题的 Banner 图片，避免继续公开暴露。
- 后台 Banner 保存、唯一键和上下线能力保持不变，回滚不涉及数据库结构变更。
- 若小程序端防御逻辑影响跳转，可先保留后端净化并回退端侧 fallback 调整。

## 关联

- BUG：`issues/bugs/archive/BUG-0130-miniapp-home-no-jump-banner-internal-title/`
- Sprint：`iterations/archive/sprint-024/`
- 相关能力：`miniapp-home`、`banner-management`
