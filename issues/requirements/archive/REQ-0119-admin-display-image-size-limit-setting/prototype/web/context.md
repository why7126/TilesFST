---
requirement_id: REQ-0119-admin-display-image-size-limit-setting
status: pending_review
created_at: 2026-08-22 21:19:48
updated_at: 2026-08-22 21:19:48
---

# Web Prototype Context

## 1. 原型目标

本原型用于说明管理端「系统设置 - 媒体与存储」新增详情展示图体积目标字段的位置、文案和交互边界。它不是最终视觉稿，不替代后续 OpenSpec Change 阶段的 UI Contract、Skeleton、截图和 computed style evidence。

## 2. 页面与入口

- 页面：`/admin/settings/media`
- 所属区域：上传限制 / 媒体生成策略
- 推荐字段名：详情展示图体积目标上限 (KB)
- 推荐字段 key：`display_max_size_kb` 或 `display_image_max_size_kb`，最终以 OpenSpec 设计为准
- 默认值：`768`

## 3. 布局策略

- 复用现有 SystemSettingsPage Shell：page-hero、summary-grid、settings-nav、settings-panel。
- 新字段与「缩略图体积目标上限 (KB)」相邻，避免被误解为上传原图大小限制。
- 字段使用数字输入或既有选择控件，单位为 KB。
- 帮助文案短句表达，不展开算法：
  - 默认 768KB。
  - 仅影响后续新生成详情展示图。
  - 历史 display 图需通过维护任务重生成。
  - 与缩略图体积目标独立。

## 4. 交互状态

| 状态 | 表现 |
|---|---|
| 默认加载 | 字段显示 effective 值 `768` 或 DB override |
| 编辑中 | 页面进入 dirty 态，footer 保存按钮可用 |
| 保存成功 | fixed toast，不改变 settings-layout 垂直位置 |
| 恢复默认 | DS modal 二次确认，确认后 reset 为 `768` |
| 校验失败 | 字段级错误或表单错误，不使用原生 alert |

## 5. 视觉验收提示

- 1440×1024 视口下新增字段不应造成上传限制表单网格挤压、label 换行异常或 footer 遮挡。
- 若使用“display 图”文案，需要确保非技术用户可理解；默认推荐“详情展示图”。
- 禁止新增裸 Hex；后续实现必须使用既有 semantic token 和 `cn()` 合并 className。

## 6. 后续 OpenSpec 阶段待补证

- UI Contract：字段名称、字段 key、默认值、校验范围、帮助文案。
- Skeleton 截图：`/admin/settings/media` 1440×1024。
- 交互证据：保存、恢复默认、dirty 切换确认、fixed toast。
- 媒体证据：配置变更后新上传图片的 `.display` key、object、URL、render 摘要。
