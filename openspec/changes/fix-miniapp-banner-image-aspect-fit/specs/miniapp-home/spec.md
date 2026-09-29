---
created_at: '2026-09-08 18:36:57'
updated_at: '2026-09-08 18:36:57'
---

## MODIFIED Requirements

### Requirement: Banner 与快捷入口

小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。首页 Banner SHALL 只读取小程序首页轮播位置；品牌入口 SHALL 进入品牌列表页，品牌列表页轮播 SHALL 使用独立位置。Banner 图片 SHALL 使用后端授权、公开安全且符合性能策略的轻量展示图 URL；小程序 Banner 轮播图属于首屏大图展示位，目标规格 SHALL 为 `display`；首页 Banner 响应 SHALL 暴露 `display_url`、`thumbnail_url` 或等价轻量字段，端侧普通展示 SHALL 优先消费 `display_url`，缺失或不可读时降级到 `thumbnail_url`，再降级到安全视图占位。首页 Banner SHALL NOT 仅依赖语义不明的 `image_url`，也 SHALL NOT 在普通展示冷加载中退到 `original_url`、`preview_url` 或旧 `url`。首页存在有效 Banner 图片时，页面 SHALL NOT 渲染 Banner `title` 作为前台主标题；页面 SHALL NOT 在首页 Banner 图片上叠加从左深到右浅的渐变遮罩，且 SHALL NOT 通过透明度降低 Banner 图片本身不透明度；与标题绑定的副标题、按钮或空文案容器 SHALL NOT 造成空白占位、遮挡、错位、高度异常或内容重叠。无 Banner 数据时，首页原有品牌兜底 Hero 文案 MAY 继续展示。首页 Banner 点击、搜索兜底、分享和埋点展示链路 SHALL 对内部标题做防御，MUST NOT 让 `internal-*` 标识进入用户可见文案；`jump_type=none` 的首页 Banner 点击 SHALL 保持静默，不显示“内容建设中”或其他占位提示。


首页Banner SHALL 在既有稳定容器内等比完整适配并居中，允许上下或左右留白，SHALL NOT 裁切、拉伸或位移隐藏图片内容。展示图和缩略图回退 SHALL 使用相同适配规则；图片URL与变体消费、权限、加载和错误回退契约 SHALL 保持。

#### Scenario: 首页 Banner 轻量图字段优先

- **WHEN** 小程序首页渲染 Banner 图片
- **THEN** 页面 SHALL 优先请求 `display_url`，缺失或不可读时降级请求 `thumbnail_url` 或等价轻量展示 URL
- **AND** 轻量字段缺失、为空或加载失败时 SHALL 展示安全占位或首页品牌兜底 Hero
- **AND** 安全占位 SHALL NOT 请求不存在的本地静态资源或触发 `__pageframe__/assets/*` 500
- **AND** 普通展示 SHALL NOT 请求 `original_url`、`preview_url`、旧 `url` 或语义不明 `image_url` 指向的原图
- **AND** 小程序 Network/render evidence SHALL 记录 Banner URL 类型、HTTP 状态、资源大小、耗时和渲染结果。

#### Scenario: 首页Banner不同比例完整显示

- **WHEN** 图片比例与容器不同，或展示图失败后切换到可用缩略图
- **THEN** 页面 SHALL 完整显示当前图片画面且保持等比与居中
- **AND** 页面 SHALL 保持容器高度，不因切换、加载或回退产生布局跳动
- **AND** 320、375、430pt等价逻辑宽度下 SHALL 无横向溢出或图片边缘裁切

#### Scenario: 首页Banner空态与既有交互兼容

- **WHEN** 图片为空、全部加载失败或用户触发现有点击与切换
- **THEN** 页面 SHALL 沿用既有占位、跳转、预览和轮播契约
- **AND** 页面 SHALL NOT 因完整适配新增原图冷加载或改变非Banner图片展示
