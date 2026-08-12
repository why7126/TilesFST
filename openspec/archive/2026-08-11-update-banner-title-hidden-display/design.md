## 上下文

`REQ-0106-admin-banner-title-hidden` 已评审通过并纳入 `sprint-022`。现有正式规格中，`banner-management` 仍把 `title` 作为 `banners` 表字段和唯一键的一部分，`web-client` 的 Banner 弹窗仍要求展示 Banner 标题，`miniapp-home` 与 `miniapp-brand-list-page` 的轮播规格仍允许或要求展示标题。

本 Change 的目标是先解决运营和前台体验，不扩大为 `title` 字段删除或历史数据迁移。当前系统已有上线、下线、图片上传、跳转类型、展示位置、缩略图和小程序分流能力，本次只调整标题的用户可见语义。

## 目标 / 非目标

**目标：**

- 后台运营新增/编辑 Banner 时不再看到或填写标题。
- 保存链路不因标题隐藏而失败。
- 小程序首页和品牌列表页 Banner 有图时不再显示标题遮罩。
- Banner 列表仍可被运营识别和维护。
- 保持现有 API、DB、上传、跳转、状态和排序能力稳定。

**非目标：**

- 不删除 `banners.title` 数据库列。
- 不批量迁移历史 Banner 标题。
- 不重做 Banner 轮播视觉、尺寸、动效或点击统计。
- 不改变 Banner 图片上传边界、Nginx、MinIO 前缀或对象存储策略。

## 决策

### D1. 标题兼容策略

采用“系统生成内部标题”的兼容方案。优先在管理端提交 payload 前生成稳定内部标题，以避免 API schema 变更；如实现中发现后端更适合统一兜底，可在后端补充兼容生成，但必须同步 OpenAPI/Orval。

理由：

- 风险低，不需要 DB migration。
- 可保持现有唯一键 `(display_client, position, title)` 和历史数据兼容。
- 直接解决运营无效录入问题。

备选方案“删除或放宽 title 字段”会扩大到 DB、Pydantic、OpenAPI、Orval、测试夹具和历史数据，超出 REQ-0106 MVP。

### D2. 管理端列表识别

Banner 列表第一列继续以缩略图为核心；标题若保留展示，文案必须表达为内部识别信息，列表识别还应依赖展示位置、跳转类型、跳转目标、排序和更新时间。关键词 placeholder 不再强调“标题”。

理由：

- 隐藏标题后，列表仍要支持运营编辑和上下线判断。
- 与 `admin-list-page-consistency` 和 sprint-020 的列表缩略图经验一致。

### D3. 小程序前台渲染

首页和品牌列表页有有效 Banner 图片时，不渲染 `item.title` 作为主标题。与标题绑定的副标题、按钮或纯文字容器应一并检查，避免残留空容器、遮挡和点击区域异常。无 Banner 兜底 Hero 保留品牌默认文案。

理由：

- 运营图本身已经包含文案和视觉重点。
- 去掉标题遮罩能减少图文冲突。
- 无 Banner 兜底不属于本次“有图 Banner 去标题”范围。

## 冲突处理

优先级：prototype context > acceptance > `rules/ui-design.md` > `openspec/specs`。

- `openspec/specs/web-client` 当前要求 Banner 弹窗展示 Banner 标题，本 Change 修改为不得展示标题输入。
- `openspec/specs/web-client` 当前要求列表第一列展示缩略图与 Banner 标题，本 Change 修改为标题降级为内部识别信息，列表必须用投放上下文识别。
- `openspec/specs/miniapp-brand-list-page` 当前要求轮播展示标题、副标题和指示点，本 Change 修改为有图 Banner 不展示 `title` 主标题，保留图片、指示点和点击跳转。
- `openspec/specs/banner-management` 当前保留 `title` 字段和标题重复错误码，本 Change 不移除字段，只修改用户可见语义和自动补齐策略。

## 风险 / 权衡

- 标题自动生成冲突 → 生成逻辑必须包含展示位置、跳转类型和时间戳或 ID，并在冲突时兜底重试。
- API 是否变更不确定 → 实现阶段优先不变更；若变更请求体，必须同步 OpenAPI、Orval、文档和测试。
- 前台去遮罩可能影响指示点可读性 → 遮罩仅在服务轮播指示器或图片可读性时保留，不能保留标题文案容器。
- 列表标题降级后识别不足 → 列表必须呈现缩略图、展示位置、跳转类型或目标信息，避免只剩内部标题。

## 知识库引用

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-020-retrospective.md`

## 验证策略

- Web 管理端 Vitest 覆盖 Banner 弹窗无标题字段、保存 payload 自动补齐内部标题、列表识别和搜索文案。
- 小程序静态测试或结构断言覆盖首页/品牌列表页有 Banner 图时不渲染标题文本。
- 若 API 不变，明确不运行 Orval 的依据；若 API 变更，运行 OpenAPI/Orval 并更新后端集成测试。
- 保留 Banner 图片上传状态机、即时回显、fixed toast、DS confirm 和弹窗宽度回归测试。
