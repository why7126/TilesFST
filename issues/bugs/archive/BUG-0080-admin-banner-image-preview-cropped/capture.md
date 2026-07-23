---
bug_id: BUG-0080-admin-banner-image-preview-cropped
title: 管理端 Banner 列表和弹窗中 Banner 图片显示不全
status: done
created_at: 2026-07-22 08:41:49
updated_at: 2026-07-22 09:35:50
severity_hint: medium
environment: 管理端 Web
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 项目已有管理端 Banner 管理能力，列表与编辑弹窗中的 Banner 图片预览未完整显示属于既有 UI 展示行为偏差，倾向记录为 BUG。
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

管理端 Banner 管理中，Banner 图片在两个位置显示不全：

1. Banner 列表中的 Banner 图片缩略图显示不全。
2. Banner 弹窗中的 Banner 图片预览显示不全。

# 复现步骤

1. 登录 Web 管理端。
2. 进入 Banner 管理页面。
3. 查看列表中已有 Banner 的图片缩略图。
4. 新建或编辑一条 Banner，打开 Banner 弹窗。
5. 查看弹窗中的 Banner 图片预览区域。

# 期望 vs 实际

期望：Banner 列表缩略图与弹窗预览能够完整呈现 Banner 图片主体，不裁掉关键信息；在固定容器中应保持清晰、比例合理，并与管理端 Design System 视觉规范一致。

实际：列表和弹窗中的 Banner 图片均存在显示不全问题，图片主体或边缘内容被裁切，影响运营人员识别和确认 Banner 素材。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 | 运营人员无法准确确认 Banner 素材内容 |
| Banner 列表 | 缩略图无法完整预览，可能误判当前 Banner 图片 |
| Banner 弹窗 | 新建或编辑时无法完整确认上传或已选图片 |
| 展示端数据 | 暂未发现影响 API、数据库或实际投放数据，当前主要为管理端预览展示问题 |

# 建议复现或补充要点

| 要点 | 说明 |
|---|---|
| 图片比例 | 记录横幅图、方图、竖图等不同比例在列表和弹窗中的表现 |
| 容器尺寸 | 确认列表缩略图列宽、高度和弹窗预览区域尺寸 |
| object-fit 策略 | 检查是否因 `object-cover`、固定高度或父容器 overflow 导致裁切 |
| 视口差异 | 覆盖桌面宽屏、较窄管理端视口和弹窗滚动场景 |
| 回归位置 | 同时验证自定义上传图、品牌 Logo/SKU 主图等 Banner 图片来源 |

# 建议验收要点

| 验收点 | 说明 |
|---|---|
| 列表完整预览 | Banner 列表图片缩略图应完整展示图片主体，不裁掉关键信息 |
| 弹窗完整预览 | Banner 弹窗图片预览应完整展示当前图片，便于运营确认 |
| 比例合理 | 不同比例图片应使用一致的适配策略，避免明显拉伸变形 |
| 布局稳定 | 修复后列表行高、弹窗宽高、上传控件和主操作按钮不得出现新的布局溢出 |
| 回归覆盖 | 覆盖已有 Banner、上传新图片、编辑保存后回显等场景 |

# 附件

- 用户原始反馈：`管理端Banner，一方面列表中Banner图片显示不全；第二方面Banner弹窗中Banner图片也显示不全`
- 暂无截图、具体 Banner ID、图片尺寸和浏览器视口信息；后续 `/bug-explore` 阶段需补充。
