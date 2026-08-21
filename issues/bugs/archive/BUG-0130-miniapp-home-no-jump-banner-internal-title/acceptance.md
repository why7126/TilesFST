---
bug_id: BUG-0130-miniapp-home-no-jump-banner-internal-title
acceptance_status: passed
created_at: 2026-08-21 08:37:23
updated_at: 2026-08-21 14:44:50
---

# 验收标准

## 回归 AC

| AC | 验收项 | 通过标准 |
|---|---|---|
| AC-001 | 首页无跳转 Banner 不显示内部标题 | 配置无跳转首页轮播 Banner 后，小程序首页画面不出现 `internal-*`、`MINIAPP_HOME`、`NO_JUMP` 或时间戳等内部标识。 |
| AC-002 | 公开接口净化内部标题 | `GET /api/v1/miniapp/home` 返回的公开 Banner 数据不暴露后台内部标题；如保留 `title` 字段，应为空、安全展示名或仅用于公开搜索语义。 |
| AC-003 | 点击/兜底链路不暴露内部标题 | 点击首页无跳转 Banner 后保持静默，不显示“内容建设中”；搜索兜底、分享文案和埋点展示摘要不包含内部标题。 |
| AC-004 | 品牌列表页轮播回归 | 品牌列表页 Banner 轮播不显示后台内部标题，且不存在首页轮播兜底误用。 |
| AC-005 | 后台管理能力不回退 | 后台 Banner 创建、编辑、列表、唯一识别、排序和上下线仍可正常工作。 |
| AC-006 | 首页 Banner 图片无遮挡且不透明化 | 首页首屏存在有效 Banner 图片时，不叠加从左深到右浅的渐变遮罩，且不通过 opacity 降低 Banner 图片本身不透明度。 |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0130-miniapp-home-no-jump-banner-internal-title |
| 标题 | 小程序首页无跳转轮播图显示内部标题 |
| 严重等级 | medium |
| 影响范围 | 小程序首页 / 后端公开 Banner 接口 / 后台 Banner 管理 / 媒体 URL 渲染 |
| 复现入口 | 管理后台创建无跳转首页 Banner 后打开小程序首页 |
| 受影响端 | miniapp / backend / admin |
| 环境 | miniapp-devtools / miniapp-device / prod 待补证 |
| 媒体类型 | image |
| 业务资源 | 脱敏：首页轮播 Banner 图片 |
| 修复前实际结果 | 首页轮播图画面显示 `internal-MINIAPP_HOME_NO_JUMP-...` 内部标题。 |
| 修复后期望结果 | 首页轮播图只显示公开图片内容，不显示内部标题或枚举/时间戳。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass_by_contract | 回归测试使用 `banners/internal-home.webp`、`banners/internal-brand.webp`、`banners/internal-search.webp`，公开接口只返回受控 `image_url`，不返回 raw object key。 | 生产存量对象 key 需在上线验收时按实际 Banner 记录补充。 |
| object | pass_by_user_render_evidence | 用户补充首页截图显示 Banner 图片本身不包含 `internal-*`、`MINIAPP_HOME` 或 `NO_JUMP` 文案，画面为公开 Logo 图片。 | 若后续更换生产 Banner 素材，仍需按同一标准复核图片像素。 |
| URL | pass_by_test | `test_miniapp_public_banners_hide_internal_no_jump_titles` 覆盖首页/品牌页公开 DTO：内部标题被清空，`search_keyword` 不使用内部标题。 | 若生产 URL 指向的图片像素含内部标题，按 object 项替换。 |
| render | pass_by_user_screenshot | 静态测试确认首页/品牌页 WXML 不渲染 `item.title`，点击搜索不再使用原始标题兜底；验收返修补充确认首页轮播不再包含 `hero-shade` 渐变遮罩，Banner 图片不透明化，且首页无跳转 Banner 点击静默。用户补充首页运行截图显示首屏 Banner 无内部标题、无遮挡、不透明化。 | 后续发布包若重新引入旧小程序代码，需重新截图复核。 |

### 媒体上传横切检查项

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本次修复仅净化公开 DTO 与小程序点击兜底，不新增上传动作。 |
| 同会话即时回显 | n/a | 本次修复不改后台保存或回显链路，后台内部标题兼容保留。 |
| Docker Web 边界 | n/a | 当前 BUG 不涉及上传大小、Nginx 或 Docker Web 边界。 |
| 媒体代理一致性 | pass_by_contract | 后端仍通过 `_card_media_url(..., prefer_thumbnail=True)` 派生公开缩略图 URL，未绕过媒体代理。 |
| 历史对象与审计 | pass_by_user_render_evidence | 当前用户补充截图未显示内部标题写入 Banner 图片像素；本次代码不迁移历史对象。 |
| 小程序 evidence | pass_by_user_screenshot | 用户补充首页运行截图作为 render evidence：首屏 Banner 无内部标题、无遮挡、不透明化。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-21 14:44:50
accepted_by: workflow-sync
source_change: fix-miniapp-home-no-jump-banner-internal-title
source_sprint: sprint-024
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

